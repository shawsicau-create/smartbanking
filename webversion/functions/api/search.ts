// AnySearch 搜索服务 - TypeScript版本
// 借鉴easy_anysearch_skill方案，无需API Key，使用代理池绕过速率限制

interface ProxyEntry {
    host: string;
    port: number;
    type: string;
    response_time?: number;
}

interface SearchResult {
    query: string;
    results: Array<{
        title: string;
        url: string;
        snippet: string;
    }>;
    error: string | null;
    via: string | null;
}

interface ExtractResult {
    url: string;
    content: string;
    error: string | null;
}

interface BatchSearchResult {
    results: SearchResult[];
    error: string | null;
}

// 配置常量
const SEARCH_API = 'https://api.anysearch.com/v1/search';
const EXTRACT_API = 'https://api.anysearch.com/v1/extract';
const PROXY_LIST_URL = 'https://cdn.jsdelivr.net/gh/parserpp/ip_ports/proxyinfo.json';
const PROBE_TIMEOUT = 5000; // 5秒
const REQUEST_TIMEOUT = 15000; // 15秒

// SearXNG 私有实例配置（阿里云服务器）
const SEARXNG_API = 'http://8.137.175.215:8888/search';
const SEARXNG_TIMEOUT = 8000; // 8秒超时
const DOUBAO_MAX_QUERY_LEN = 100; // 统一query长度检查

// 代理池缓存
let cachedProxies: string[] | null = null;
let cacheTimestamp = 0;
const CACHE_DURATION = 5 * 60 * 1000; // 5分钟缓存

/**
 * 加载代理列表
 */
async function loadProxies(): Promise<string[]> {
    // 检查缓存
    if (cachedProxies && Date.now() - cacheTimestamp < CACHE_DURATION) {
        return cachedProxies;
    }

    try {
        const resp = await fetch(PROXY_LIST_URL, {
            headers: { 'User-Agent': 'AnySearch-Skill/2.0' },
        });

        if (!resp.ok) {
            console.error(`[代理] 加载失败: ${resp.status}`);
            return [];
        }

        const data = await resp.json() as Record<string, ProxyEntry[]>;
        const allEntries: ProxyEntry[] = [];

        // 提取所有代理条目
        for (const entries of Object.values(data)) {
            if (Array.isArray(entries)) {
                allEntries.push(...entries);
            }
        }

        // 按response_time排序
        allEntries.sort((a, b) => (a.response_time || 9999) - (b.response_time || 9999));

        // 转换为代理URL格式
        const proxies = allEntries
            .filter(entry => entry.host && entry.port)
            .map(entry => `${entry.type || 'http'}://${entry.host}:${entry.port}`);

        console.log(`[代理] 加载 ${proxies.length} 条（已按 response_time 排序）`);

        // 更新缓存
        cachedProxies = proxies;
        cacheTimestamp = Date.now();

        return proxies;
    } catch (error) {
        console.error(`[代理列表加载失败] ${error}`);
        return [];
    }
}

/**
 * 探测单个代理是否可用
 */
async function probeProxy(proxy: string, signal: AbortSignal): Promise<string | null> {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), PROBE_TIMEOUT);

        // 合并信号
        signal.addEventListener('abort', () => controller.abort());

        const resp = await fetch(SEARCH_API, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'User-Agent': 'AnySearch-Skill/2.0',
            },
            body: JSON.stringify({ query: 'test', max_results: 1 }),
            signal: controller.signal,
        });

        clearTimeout(timeoutId);

        if (resp.ok) {
            await resp.json();
            return proxy;
        }
        return null;
    } catch {
        return null;
    }
}

/**
 * 并发探测找到第一个可用代理
 */
async function findFirstLiveProxy(proxies: string[]): Promise<string | null> {
    if (proxies.length === 0) {
        return null;
    }

    console.log(`[探测] 并发检测全部 ${proxies.length} 个代理...`);

    const controller = new AbortController();
    const { signal } = controller;

    // 并发探测所有代理
    const probePromises = proxies.map(proxy => probeProxy(proxy, signal));

    try {
        // 使用Promise.race找到第一个成功的
        const result = await Promise.race([
            ...probePromises,
            // 添加超时
            new Promise<null>((resolve) =>
                setTimeout(() => resolve(null), PROBE_TIMEOUT * 2)
            ),
        ]);

        // 找到可用代理后取消其他探测
        controller.abort();

        if (result) {
            console.log(`[探测] 找到可用代理: ${result}`);
            return result;
        }
    } catch {
        // 忽略错误
    }

    console.log(`[探测] 全部 ${proxies.length} 个均不可用`);
    return null;
}

/**
 * 发送搜索请求
 */
async function doSearchRequest(
    query: string,
    maxResults: number = 10,
    proxy: string | null = null
): Promise<SearchResult> {
    const headers: Record<string, string> = {
        'Content-Type': 'application/json',
        'User-Agent': 'AnySearch-Skill/2.0',
    };

    const body = JSON.stringify({
        query,
        max_results: maxResults,
    });

    const options: RequestInit = {
        method: 'POST',
        headers,
        body,
    };

    // 如果有代理，通过代理发送请求
    // 注意：Cloudflare Workers不支持直接设置代理，这里使用直连
    // 代理功能需要在支持代理的环境中使用
    const resp = await fetch(SEARCH_API, {
        ...options,
        signal: AbortSignal.timeout(REQUEST_TIMEOUT),
    });

    if (!resp.ok) {
        throw new Error(`HTTP ${resp.status}: ${await resp.text()}`);
    }

    const raw = await resp.json();
    return {
        query,
        results: normalizeResults(raw),
        error: null,
        via: proxy || '直连',
    };
}

/**
 * 发送内容提取请求
 */
async function doExtractRequest(
    url: string,
    proxy: string | null = null
): Promise<ExtractResult> {
    const headers: Record<string, string> = {
        'Content-Type': 'application/json',
        'User-Agent': 'AnySearch-Skill/2.0',
    };

    const body = JSON.stringify({ url });

    const resp = await fetch(EXTRACT_API, {
        method: 'POST',
        headers,
        body,
        signal: AbortSignal.timeout(REQUEST_TIMEOUT),
    });

    if (!resp.ok) {
        throw new Error(`HTTP ${resp.status}: ${await resp.text()}`);
    }

    const data = await resp.json();
    return {
        url,
        content: data.content || data.data?.content || '',
        error: null,
    };
}

/**
 * 规范化搜索结果
 */
function normalizeResults(raw: unknown): Array<{ title: string; url: string; snippet: string }> {
    const data = (raw as { data?: unknown })?.data || raw;
    const items =
        ((data as { results?: unknown[] })?.results ||
            (data as { items?: unknown[] })?.items ||
            (Array.isArray(data) ? data : [])) as Record<string, unknown>[];

    return items
        .filter((item): item is Record<string, unknown> => typeof item === 'object' && item !== null)
        .map(item => ({
            title: String(item.title || item.name || '').trim(),
            url: String(item.url || item.link || '').trim(),
            snippet: String(
                item.description ||
                (typeof item.content === 'string' ? item.content.slice(0, 500) : '') ||
                item.snippet || ''
            ).trim(),
        }))
        .filter(item => item.title || item.url);
}

/**
 * SearXNG 搜索（私有实例，无需API Key）
 */
async function searxngSearch(
    query: string,
    maxResults: number = 10
): Promise<SearchResult> {
    const params = new URLSearchParams({
        q: query,
        format: 'json',
        categories: 'general',
        language: 'zh-CN',
        pageno: '1',
    });

    const resp = await fetch(`${SEARXNG_API}?${params}`, {
        signal: AbortSignal.timeout(SEARXNG_TIMEOUT),
    });

    if (!resp.ok) {
        throw new Error(`SearXNG HTTP ${resp.status}`);
    }

    const raw = await resp.json() as {
        results?: Array<{
            title: string;
            url: string;
            content: string;
        }>;
    };

    // 转换为标准格式
    const results = (raw.results || [])
        .slice(0, maxResults)
        .map(item => ({
            title: item.title || '',
            url: item.url || '',
            snippet: item.content || '',
        }))
        .filter(item => item.url);

    return {
        query,
        results,
        error: null,
        via: 'searxng',
    };
}

/**
 * 带重试的函数包装
 */
async function withRetry<T>(
    fn: () => Promise<T>,
    retries: number = 1,
    delay: number = 300
): Promise<T> {
    for (let i = 0; i <= retries; i++) {
        try {
            return await fn();
        } catch (err) {
            if (i === retries) throw err;
            await new Promise(r => setTimeout(r, delay * Math.pow(2, i)));
        }
    }
    throw new Error('unreachable');
}

/**
 * 获取引擎调用顺序（智能路由）
 * - 短query (≤100字符) → SearXNG优先（速度快、免费）
 * - 长query (>100字符) → AnySearch优先（支持长query）
 */
function getEngineOrder(query: string): Array<() => Promise<SearchResult>> {
    const engines: Array<() => Promise<SearchResult>> = [];

    if (query.length <= DOUBAO_MAX_QUERY_LEN) {
        // 短query：SearXNG → AnySearch
        engines.push(
            () => searxngSearch(query, 10),
            () => doSearchRequest(query, 10, null)
        );
    } else {
        // 长query：AnySearch → SearXNG
        engines.push(
            () => doSearchRequest(query, 10, null),
            () => searxngSearch(query, 10)
        );
    }

    return engines;
}

/**
 * 带降级的搜索（核心逻辑）
 */
async function searchWithFallback(
    query: string,
    maxResults: number
): Promise<SearchResult> {
    const engines = getEngineOrder(query);
    let lastError: Error | null = null;

    for (const engineFn of engines) {
        try {
            const result = await withRetry(engineFn, 1, 300);
            if (result.results.length > 0) return result;
            // 结果为空也算失败
            lastError = new Error('返回结果为空');
        } catch (err) {
            lastError = err instanceof Error ? err : new Error(String(err));
            console.error(`[搜索降级] ${lastError.message}`);
            // 继续尝试下一个引擎
        }
    }

    // 全部失败
    return {
        query,
        results: [],
        error: `所有搜索引擎均失败: ${lastError?.message}`,
        via: null,
    };
}

/**
 * 主搜索函数（双引擎版本）
 */
export async function search(query: string, maxResults: number = 10): Promise<SearchResult> {
    try {
        return await searchWithFallback(query, maxResults);
    } catch (error) {
        return {
            query,
            results: [],
            error: `搜索失败: ${error instanceof Error ? error.message : String(error)}`,
            via: null,
        };
    }
}

/**
 * 内容提取函数
 */
export async function extract(url: string): Promise<ExtractResult> {
    try {
        const allProxies = await loadProxies();
        const proxy = await findFirstLiveProxy(allProxies);

        // 优先使用代理，失败则直连
        if (proxy) {
            try {
                return await doExtractRequest(url, proxy);
            } catch (error) {
                console.error(`[代理提取失败] ${proxy}: ${error}`);
            }
        }

        // 直连兜底
        return await doExtractRequest(url, null);
    } catch (error) {
        return {
            url,
            content: '',
            error: `提取失败: ${error instanceof Error ? error.message : String(error)}`,
        };
    }
}

/**
 * 批量搜索函数
 */
export async function batchSearch(
    queries: Array<{ query: string; max_results?: number }>
): Promise<BatchSearchResult> {
    try {
        const results = await Promise.all(
            queries.map(q => search(q.query, q.max_results || 5))
        );
        return { results, error: null };
    } catch (error) {
        return {
            results: [],
            error: `批量搜索失败: ${error instanceof Error ? error.message : String(error)}`,
        };
    }
}

// HTTP API处理
export async function onRequestPost(context: { request: Request }): Promise<Response> {
    const { request } = context;

    const corsHeaders = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    };

    try {
        const body = await request.json() as {
            action: string;
            query?: string;
            max_results?: number;
            url?: string;
            queries?: Array<{ query: string; max_results?: number }>;
        };

        let result: unknown;

        switch (body.action) {
            case 'search':
                if (!body.query) {
                    throw new Error('缺少query参数');
                }
                result = await search(body.query, body.max_results || 10);
                break;

            case 'extract':
                if (!body.url) {
                    throw new Error('缺少url参数');
                }
                result = await extract(body.url);
                break;

            case 'batch_search':
                if (!body.queries || !Array.isArray(body.queries)) {
                    throw new Error('缺少queries参数');
                }
                result = await batchSearch(body.queries);
                break;

            default:
                throw new Error(`未知action: ${body.action}`);
        }

        return new Response(JSON.stringify(result), {
            headers: { 'Content-Type': 'application/json', ...corsHeaders },
        });
    } catch (error) {
        const message = error instanceof Error ? error.message : '服务器内部错误';
        return new Response(JSON.stringify({ error: message }), {
            status: 400,
            headers: { 'Content-Type': 'application/json', ...corsHeaders },
        });
    }
}

export async function onRequestOptions(): Promise<Response> {
    return new Response(null, {
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
    });
}
