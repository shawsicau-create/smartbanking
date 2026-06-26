// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// https://astro.build/config
//
// 多平台部署支持：同一份代码可同时产出 EdgeOne / Vercel / GitHub Pages 三套产物。
// 区分依据是构建时环境变量：
//   GITHUB_PAGES === 'true'   → 走 GitHub Pages（项目页：base='/仓库名/'）
//   否则                       → 走 EdgeOne / Vercel（根路径部署）
//
// 在 GitHub Actions 中：
//   - GITHUB_PAGES 由 workflow 显式设置
//   - GITHUB_REPOSITORY 由 runner 自动提供（格式：owner/repo）
//   - GITHUB_REPOSITORY_OWNER 由 runner 自动提供
const isGitHubPages = process.env.GITHUB_PAGES === 'true';
const ghOwner = process.env.GITHUB_REPOSITORY_OWNER || 'xiaosicau';
const ghRepoName = (process.env.GITHUB_REPOSITORY || `${ghOwner}/smartbanking`).split('/')[1];
const siteUrl = isGitHubPages
	? `https://${ghOwner}.github.io`
	: 'https://smartbanking.edgeone.app';
const basePath = isGitHubPages ? `/${ghRepoName}/` : '/';

export default defineConfig({
	site: siteUrl,
	base: basePath,
	markdown: {
		remarkPlugins: [remarkMath],
		rehypePlugins: [rehypeKatex],
	},
	integrations: [
		// @astrojs/sitemap 自动读取 site 字段，生成 /sitemap-index.xml
		// 配合 robots.txt 中的 Sitemap 声明，主动提交给 Google / 百度
		sitemap(),
		starlight({
			title: '智慧银行实验教程',
			description: 'AI驱动的金融科技实践',
			head: [
				{
					tag: 'script',
					attrs: { type: 'application/ld+json' },
					content: JSON.stringify({
						'@context': 'https://schema.org',
						'@type': 'Course',
						name: '智慧银行实验教程',
						description: 'AI驱动的金融科技实践',
						provider: {
							'@type': 'Organization',
							name: '智能银行实验室',
							url: 'https://smartbanking.edgeone.app',
						},
						inLanguage: 'zh-CN',
						isAccessibleForFree: true,
					}),
				},
			],
			logo: {
				src: './src/assets/logo.svg',
				replacesTitle: false,
			},
			defaultLocale: 'zh-CN',
			social: [
				{ icon: 'github', label: 'CNB', href: 'https://cnb.cool/xiaosicau/smartbanking' },
			],
			customCss: [
				'katex/dist/katex.min.css',
				'./src/styles/custom.css',
			],
			sidebar: [
				{
					label: '前言',
					items: [{ slug: 'preface' }],
				},
				{
					label: '基础模块',
					collapsed: false,
					items: [
						{ label: '第1章 绪论', slug: 'ch01' },
						{ label: '第2章 环境搭建', slug: 'ch02' },
						{ label: '第3章 MCP协议', slug: 'ch03' },
						{ label: '第4章 Skill体系', slug: 'ch04' },
						{ label: '第5章 CLI工具实战', slug: 'ch05' },
					],
				},
				{
					label: '进阶模块',
					collapsed: false,
					items: [
						{ label: '第6章 金融数据分析', slug: 'ch06' },
					],
				},
				{
					label: '综合模块',
					collapsed: false,
					items: [
						{ label: '第7章 BMAD与综合项目', slug: 'ch07' },
						{ label: '第8章 综合项目与创新', slug: 'ch08' },
					],
				},
				{
					label: '附录与实验手册',
					collapsed: true,
					items: [
						{ label: '附录', slug: 'appendix' },
						{ label: '参考文献', slug: 'references' },
						{ label: 'BMAD-CRM实验手册', slug: 'labs/bmad-crm' },
						{ label: '本地大模型部署', slug: 'labs/local-llm-deploy' },
						{ label: 'BMAD代码云端部署', slug: 'labs/bmad-deploy' },
						{ label: 'BMAD方法论实战', slug: 'labs/bmad-practice' },
						{ label: 'CNB同步项目库', slug: 'labs/cnb-sync' },
						{ label: 'CNB流水线自动部署', slug: 'labs/edgeone-deploy' },
					],
				},
			],
		}),
	],
});
