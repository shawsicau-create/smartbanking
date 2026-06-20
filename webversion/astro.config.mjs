// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: '智慧银行实验教程',
			description: 'AI驱动的金融科技实践',
			logo: {
				src: './src/assets/logo.svg',
				replacesTitle: false,
			},
			defaultLocale: 'zh-CN',
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/xiaosicau/smartbanking' },
			],
			customCss: ['./src/styles/custom.css'],
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
						{ label: 'BMAD-CRM实验手册', slug: 'labs/bmad-crm' },
						{ label: '本地大模型部署', slug: 'labs/local-llm-deploy' },
						{ label: 'BMAD代码云端部署', slug: 'labs/bmad-deploy' },
						{ label: 'BMAD方法论实战', slug: 'labs/bmad-practice' },
						{ label: 'CNB同步项目库', slug: 'labs/cnb-sync' },
					],
				},
			],
		}),
	],
});
