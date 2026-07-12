---
title: '课件中心'
description: '36张SVG幻灯片 + 8章语音导览 — 全课程可视化课件浏览'
---

<div id="slides-app">
  <div style="background:linear-gradient(135deg,#1E293B,#334155);border-radius:16px;padding:24px;margin-bottom:24px;color:#F1F5F9">
    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px">
      <div>
        <h2 style="margin:0;font-size:1.5rem;background:linear-gradient(90deg,#3B82F6,#10B981);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">智慧银行实验教程 · 课件中心</h2>
        <p style="margin:4px 0 0;color:#94A3B8;font-size:0.9rem">36张SVG幻灯片 + 8章语音导览</p>
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <button onclick="slidesPrev()" style="background:rgba(59,130,246,0.2);border:1px solid rgba(59,130,246,0.5);color:#3B82F6;padding:8px 16px;border-radius:8px;cursor:pointer;font-size:14px">← 上一张</button>
        <button onclick="slidesNext()" style="background:rgba(59,130,246,0.2);border:1px solid rgba(59,130,246,0.5);color:#3B82F6;padding:8px 16px;border-radius:8px;cursor:pointer;font-size:14px">下一张 →</button>
      </div>
    </div>
  </div>

  <div id="slide-tabs" style="display:flex;gap:4px;flex-wrap:wrap;margin-bottom:16px">
    <button class="slide-tab active" data-ch="all" onclick="filterSlides('all')" style="padding:6px 14px;border:1px solid #e2e8f0;border-radius:20px;background:#3B82F6;color:white;cursor:pointer;font-size:13px">全部</button>
  </div>

  <div id="slide-viewer" style="background:#1E293B;border-radius:12px;padding:20px;margin-bottom:24px;text-align:center">
    <img id="current-slide" src="/slides/ch01_title.svg" alt="幻灯片" style="max-width:100%;border-radius:8px;box-shadow:0 4px 20px rgba(0,0,0,0.3)" />
    <div style="margin-top:12px;color:#94A3B8;font-size:0.85rem">
      <span id="slide-counter">1 / 36</span> — <span id="slide-title">第1章 标题页</span>
    </div>
  </div>

  <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:16px;margin-bottom:24px">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">
      <span style="font-weight:600;font-size:14px;color:#0f172a">🔊 当前章节语音</span>
    </div>
    <audio id="slides-audio" controls preload="none" style="width:100%">
      <source src="/audio/ch01_narration.mp3" type="audio/mpeg">
    </audio>
  </div>

  <h3>全部幻灯片缩略图</h3>
  <div id="slide-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px">
  </div>
</div>

<script is:inline>
  var allSlides = [
    { ch: 'ch01', file: 'ch01_title', title: '第1章 标题页' },
    { ch: 'ch01', file: 'ch01_agenda', title: '第1章 议程' },
    { ch: 'ch01', file: 'ch01_fintech_stages', title: '金融科技发展阶段' },
    { ch: 'ch01', file: 'ch01_summary', title: '第1章 总结' },
    { ch: 'ch02', file: 'ch02_title', title: '第2章 标题页' },
    { ch: 'ch02', file: 'ch02_agenda', title: '第2章 议程' },
    { ch: 'ch02', file: 'ch02_ide_comparison', title: 'AI IDE对比' },
    { ch: 'ch02', file: 'ch02_python_setup', title: 'Python环境配置' },
    { ch: 'ch02', file: 'ch02_ai_collaboration_modes', title: 'AI协作四模式' },
    { ch: 'ch02', file: 'ch02_summary', title: '第2章 总结' },
    { ch: 'ch03', file: 'ch03_title', title: '第3章 标题页' },
    { ch: 'ch03', file: 'ch03_agenda', title: '第3章 议程' },
    { ch: 'ch03', file: 'ch03_architecture', title: 'MCP架构详解' },
    { ch: 'ch03', file: 'ch03_mcp_concepts', title: 'MCP核心概念' },
    { ch: 'ch03', file: 'ch03_server_development', title: 'MCP Server开发' },
    { ch: 'ch03', file: 'ch03_summary', title: '第3章 总结' },
    { ch: 'ch04', file: 'ch04_title', title: '第4章 标题页' },
    { ch: 'ch04', file: 'ch04_agenda', title: '第4章 议程' },
    { ch: 'ch04', file: 'ch04_skill_overview', title: 'Skill体系设计原理' },
    { ch: 'ch04', file: 'ch04_summary', title: '第4章 总结' },
    { ch: 'ch05', file: 'ch05_title', title: '第5章 标题页' },
    { ch: 'ch05', file: 'ch05_agenda', title: '第5章 议程' },
    { ch: 'ch05', file: 'ch05_cli_ecosystem', title: 'CLI工具生态' },
    { ch: 'ch05', file: 'ch05_summary', title: '第5章 总结' },
    { ch: 'ch06', file: 'ch06_title', title: '第6章 标题页' },
    { ch: 'ch06', file: 'ch06_agenda', title: '第6章 议程' },
    { ch: 'ch06', file: 'ch06_data_features', title: '金融数据特征与处理' },
    { ch: 'ch06', file: 'ch06_summary', title: '第6章 总结' },
    { ch: 'ch07', file: 'ch07_title', title: '第7章 标题页' },
    { ch: 'ch07', file: 'ch07_agenda', title: '第7章 议程' },
    { ch: 'ch07', file: 'ch07_bmad_stages', title: 'BMAD五阶段方法论' },
    { ch: 'ch07', file: 'ch07_summary', title: '第7章 总结' },
    { ch: 'ch08', file: 'ch08_title', title: '第8章 标题页' },
    { ch: 'ch08', file: 'ch08_agenda', title: '第8章 议程' },
    { ch: 'ch08', file: 'ch08_project_topics', title: '项目选题指南' },
    { ch: 'ch08', file: 'ch08_summary', title: '课程总结' },
  ];

  var chapterAudio = {
    ch01: '/audio/ch01_narration.mp3',
    ch02: '/audio/ch02_narration.mp3',
    ch03: '/audio/ch03_narration.mp3',
    ch04: '/audio/ch04_narration.mp3',
    ch05: '/audio/ch05_narration.mp3',
    ch06: '/audio/ch06_narration.mp3',
    ch07: '/audio/ch07_narration.mp3',
    ch08: '/audio/ch08_narration.mp3',
  };

  var chapterNames = {
    ch01: '第1章', ch02: '第2章', ch03: '第3章', ch04: '第4章',
    ch05: '第5章', ch06: '第6章', ch07: '第7章', ch08: '第8章',
  };

  var currentIdx = 0;
  var currentFilter = 'all';
  var filteredSlides = allSlides;

  window.renderGrid = function() {
    var grid = document.getElementById('slide-grid');
    if (!grid) return;
    grid.innerHTML = '';
    filteredSlides = currentFilter === 'all' ? allSlides : allSlides.filter(function(s) { return s.ch === currentFilter; });
    filteredSlides.forEach(function(slide, idx) {
      var card = document.createElement('div');
      card.style.cssText = 'cursor:pointer;border:2px solid #e2e8f0;border-radius:8px;overflow:hidden;transition:border-color 0.2s;background:#1E293B';
      card.onclick = function() { window.showSlide(slide, idx); };
      card.innerHTML = '<img src="/slides/' + slide.file + '.svg" alt="' + slide.title + '" style="width:100%;display:block" />' +
        '<div style="padding:8px 12px;color:#F1F5F9;font-size:12px"><span style="display:inline-block;padding:2px 8px;border-radius:4px;background:rgba(59,130,246,0.3);color:#93C5FD;margin-right:6px">' + chapterNames[slide.ch] + '</span>' + slide.title + '</div>';
      grid.appendChild(card);
    });
  };

  window.showSlide = function(slide, idx) {
    var realIdx = allSlides.indexOf(slide);
    if (realIdx >= 0) currentIdx = realIdx;
    var img = document.getElementById('current-slide');
    var counter = document.getElementById('slide-counter');
    var title = document.getElementById('slide-title');
    if (img) img.src = '/slides/' + slide.file + '.svg';
    if (counter) counter.textContent = (currentIdx + 1) + ' / ' + allSlides.length;
    if (title) title.textContent = slide.title;
    var audio = document.getElementById('slides-audio');
    if (audio) {
      audio.src = chapterAudio[slide.ch] || '';
    }
  };

  window.slidesNext = function() {
    currentIdx = (currentIdx + 1) % allSlides.length;
    window.showSlide(allSlides[currentIdx], currentIdx);
  };

  window.slidesPrev = function() {
    currentIdx = (currentIdx - 1 + allSlides.length) % allSlides.length;
    window.showSlide(allSlides[currentIdx], currentIdx);
  };

  window.filterSlides = function(ch) {
    currentFilter = ch;
    document.querySelectorAll('.slide-tab').forEach(function(t) {
      t.style.background = t.dataset.ch === ch ? '#3B82F6' : '#f1f5f9';
      t.style.color = t.dataset.ch === ch ? 'white' : '#475569';
    });
    window.renderGrid();
  };

  document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowLeft') window.slidesPrev();
    if (e.key === 'ArrowRight') window.slidesNext();
  });

  document.addEventListener('DOMContentLoaded', function() {
    var tabs = document.getElementById('slide-tabs');
    if (tabs) {
      var chapters = ['ch01','ch02','ch03','ch04','ch05','ch06','ch07','ch08'];
      chapters.forEach(function(ch) {
        var btn = document.createElement('button');
        btn.className = 'slide-tab';
        btn.dataset.ch = ch;
        btn.textContent = chapterNames[ch];
        btn.style.cssText = 'padding:6px 14px;border:1px solid #e2e8f0;border-radius:20px;background:#f1f5f9;color:#475569;cursor:pointer;font-size:13px';
        btn.onclick = function() { window.filterSlides(ch); };
        tabs.appendChild(btn);
      });
    }
    window.renderGrid();
  });
</script>

:::tip[使用说明]
- 点击下方缩略图查看大图，或使用 **← →** 方向键切换幻灯片
- 点击章节标签筛选对应章节的幻灯片
- 每张幻灯片切换时自动加载对应章节的语音导览
- 所有幻灯片为 SVG 矢量格式，支持无限缩放不失真
:::
