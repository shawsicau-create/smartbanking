---
name: news-read
description: "Search today's news and read aloud via edge-tts natural voice."
description_zh: 搜索今日新闻并用自然语音播报，支持中英文切换和多种音色。
workflow_stage: communication
compatibility:
  - claude-code
  - cursor
  - codex
  - gemini-cli
author: Qoder Skills Library
version: 2.0.0
tags:
  - news
  - tts
  - voice
  - speech
  - read-aloud
  - edge-tts
---

# News Read — 新闻语音播报

## Purpose

搜索当日新闻并自动以自然语音播报结果。使用 `edge-tts`（微软 Edge 神经网络语音），音质远优于系统自带 TTS，接近真人水平。适合在通勤、休息时"听"新闻。

## When to Use

- 用户说"播报新闻"、"朗读新闻"、"read the news"、"news briefing"时触发
- 需要以语音方式获取今日要闻的场景
- 适合多任务场景：边做其他事情边听新闻

## Instructions

### Step 1: 确定搜索参数

从用户输入 `$ARGUMENTS` 中提取以下信息（若未提供则使用默认值）：

| 参数 | 默认值 | 示例 |
|------|--------|------|
| 主题/关键词 | `today's top news` | 科技、财经、体育 |
| 语言 | 中文 | 中文 / English |
| 地区 | 全球 | 中国、美国、日本 |

### Step 2: 搜索新闻

使用 `WebSearch` 工具搜索新闻：

- 中文新闻：用中文关键词搜索，如"今日新闻摘要"、"中国财经新闻"
- 英文新闻：用英文关键词搜索，如"today's top news"、"tech news today"
- 特定主题：将用户关键词加入搜索，如"AI news today"、"体育新闻"

### Step 3: 整理播报文本

将搜索结果整理为一段流畅的播报文本：

1. **开头**：播报日期 + "为您播报今日新闻摘要"
2. **主体**：每条新闻用 1-2 句话概括，按重要性排序（国际 → 国内 → 财经 → 科技 → 体育）
3. **结尾**："以上是今日新闻摘要，感谢收听"
4. **格式要求**：
   - 去除 Markdown 格式符号
   - 去除 URL 链接
   - 将英文人名/地名转为中文或保留原文（视播报语言而定）
   - 控制总长度在 500 字以内（约 2-3 分钟播报）

### Step 4: 生成语音并播放

使用 `edge-tts` 生成自然语音 MP3，然后用 `afplay` 播放：

```bash
python3 -c "
import asyncio, edge_tts

TEXT = '''<播报文本>'''
VOICE = 'zh-CN-XiaoxiaoNeural'
OUTPUT = '/tmp/news_edge.mp3'

async def main():
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT)
asyncio.run(main())
"

afplay /tmp/news_edge.mp3
```

#### 语音选择

| Voice ID | 性别 | 风格 | 推荐场景 |
|-----------|------|------|----------|
| `zh-CN-XiaoxiaoNeural` | 女 | 温暖、专业 | 📰 **新闻播报（默认）** |
| `zh-CN-YunyangNeural` | 男 | 专业、稳重 | 🎙️ 新闻播音腔 |
| `zh-CN-YunjianNeural` | 男 | 激情 | ⚽ 体育赛事 |
| `zh-CN-YunxiNeural` | 男 | 阳光、活泼 | 🎧 轻松闲聊 |
| `zh-CN-XiaoyiNeural` | 女 | 活泼、可爱 | 📚 有声读物 |
| `en-US-JennyNeural` | 女 | 自然、亲切 | 🇺🇸 英文新闻 |
| `en-US-GuyNeural` | 男 | 成熟、专业 | 🇺🇸 英文播报 |

#### 保存为音频文件

```bash
# 保存到桌面
python3 -c "
import asyncio, edge_tts
async def main():
    communicate = edge_tts.Communicate('<播报文本>', 'zh-CN-XiaoxiaoNeural')
    await communicate.save('~/Desktop/news-\$(date +%Y%m%d).mp3')
asyncio.run(main())
"
```

### Step 5: 屏幕展示

在语音播报的同时，将结构化新闻摘要以 Markdown 格式展示在终端，方便用户阅读：

```markdown
## 📻 今日新闻播报 — YYYY年MM月DD日

### 🌍 国际
- **标题**：一句话摘要

### 🏠 国内
- **标题**：一句话摘要

### 💰 财经
- **标题**：一句话摘要

### 🏀 体育 / 🏥 健康
- **标题**：一句话摘要

---
🎙️ 语音播报中 | 音色：晓晓（女） | 时长约 X 分钟
```

## Example Prompts

- "播报今日新闻"
- "朗读今天的国际新闻"
- "news briefing today"
- "帮我搜索今天的科技新闻然后念给我听"
- "播报财经新闻，保存为音频文件"
- "用英文播报今天的新闻"
- "用男声播报体育新闻"

## Requirements

### Software
- Python 3.8+
- `edge-tts`（`pip install edge-tts`）
- macOS: `afplay`（系统自带）| Linux: `mpv` 或 `vlc` | Windows: `start`

### Installation
```bash
pip install edge-tts
```

## Best Practices

1. **控制播报时长** — 新闻摘要控制在 500 字以内，约 2-3 分钟听完
2. **流畅优先** — 播报文本应口语化，避免书面语和生硬的翻译
3. **先展示后播报** — 先在终端展示文字版，再启动语音播报
4. **音色匹配场景** — 新闻用 XiaoxiaoNeural，体育用 YunjianNeural，轻松话题用 YunxiNeural

## Common Pitfalls

- ❌ 播报文本中包含 URL、Markdown 符号等 TTS 无法正确朗读的内容
- ❌ 未安装 `edge-tts` 导致报错（需 `pip install edge-tts`）
- ❌ 使用 `say` 命令替代（音质差、机器味重，应优先使用 edge-tts）

## Fallback

若 `edge-tts` 不可用（离线环境），可降级到 macOS `say`：

```bash
say -v Tingting "<播报文本>"   # 中文
say -v Samantha "<text>"       # 英文
```

## Changelog

### v2.0.0
- 切换默认 TTS 引擎从 macOS `say` 到 `edge-tts`（自然语音）
- 新增 7 种神经网络语音可选（中英文各多种音色）
- 输出格式改为 MP3（更通用）
- 新增 `gemini-cli` 兼容性

### v1.0.0
- Initial release
