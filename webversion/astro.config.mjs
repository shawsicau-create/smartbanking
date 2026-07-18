// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';
import react from '@astrojs/react';
import mermaid from '@pasqal-io/starlight-client-mermaid';

import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// https://astro.build/config
//
// 部署平台：Cloudflare Pages
// 站点地址：https://smartbanking.pages.dev
const siteUrl = 'https://smartbanking.pages.dev';
const basePath = '/';

export default defineConfig({
	site: siteUrl,
	base: basePath,
	output: 'static',
	markdown: {
		remarkPlugins: [remarkMath],
		rehypePlugins: [rehypeKatex],
	},
	integrations: [
		react(),
		// @astrojs/sitemap 自动读取 site 字段，生成 /sitemap-index.xml
		// 配合 robots.txt 中的 Sitemap 声明，主动提交给 Google / 百度
		sitemap(),
		starlight({
			title: 'SmartBank Agent',
			description: '基于MCP+Skill+BMAD三位一体的金融科技实验教学智能体',
			plugins: [mermaid()],
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
							url: 'https://smartbanking.pages.dev',
						},
						inLanguage: 'zh-CN',
						isAccessibleForFree: true,
					}),
				},
				{
					tag: 'script',
					attrs: { src: 'https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js' },
				},
				{
					tag: 'script',
					attrs: { type: 'text/javascript' },
					content: `document.addEventListener('DOMContentLoaded', function() {
  mermaid.initialize({ startOnLoad: true, theme: 'default' });
  mermaid.init(undefined, '.mermaid');
});`,
				},
				{
					tag: 'script',
					attrs: { type: 'text/javascript' },
					content: `function toggleChapterAudio(ch){var a=document.getElementById(ch+'-audio');var b=document.getElementById(ch+'-play-btn');if(!a)return;if(a.paused){document.querySelectorAll('audio').forEach(function(e){if(e!==a&&e.paused===false){e.pause();var eb=document.getElementById(e.id.replace('-audio','-play-btn'));if(eb){eb.textContent='▶';eb.style.background='linear-gradient(135deg,#3B82F6,#2563EB)';}}});a.play();b.textContent='⏸';b.style.background='linear-gradient(135deg,#10B981,#059669)';}else{a.pause();b.textContent='▶';b.style.background='linear-gradient(135deg,#3B82F6,#2563EB)';}}`,
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
					label: '🏠 返回智能体主页',
					link: '/',
				},
				{
					label: '🤖 使用智能体',
					link: '/chat/',
				},
				{
					label: '🔌 MCP工具 & Skill能力',
					link: '/tools/',
				},
				{
					label: '🎬 课件中心',
					link: '/slides/',
				},
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
