---
title: "又一个Vibe Coding产物：Image Overlay Compare — 在线图片对比工具"
date: 2026-05-13
tags: ["前端工具", "开源项目", "图片处理"]
---

# 又一个Vibe Coding产物：Image Overlay Compare — 在线图片对比工具

![工具界面截图](https://static.yyfollower.com/overlay-compare-screenshot.png)

做前端开发的都懂一个痛点：设计师给了你一张设计稿，你撸完了代码，然后要逐像素对比还原度。打开Photoshop叠图层？太重了。用截图工具左右分屏？眼睛看瞎。

所以我写了个纯前端的小工具——**Image Overlay Compare**，在线、免费、无需上传服务器、100%浏览器本地处理。

🔗 在线体验：[https://overlay-image.yyfollower.com/](https://overlay-image.yyfollower.com/)
🔗 GitHub：[https://github.com/andy7076/overlay_image](https://github.com/andy7076/overlay_image)

## ✨ 核心功能

### 🎚 图片叠加对比
上传两张图片，第二张默认半透明叠加在第一张上，通过**不透明度滑块**从0%到100%调节透明度，差异一目了然。

![界面概念图](https://static.yyfollower.com/overlay-compare-interface.png)

### 🎨 Blend混合模式
内置了8种CSS混合模式，最有用的就是 **Difference（差值）**——两张图一模一样的地方变全黑，不一样的地方发光发亮，像素级差异瞬间现原形。

其他模式：Multiply、Screen、Overlay、Darken、Lighten、Exclusion，不同场景各有妙用。

### ✋ 拖拽、缩放、拉伸
- **拖拽**：图片2可以随意拖动位置，对齐两张图的细节
- **8个手柄**：拖拽四角/四边的手柄自由缩放或单轴拉伸
- **Shift+拖拽角**：保持原始宽高比缩放
- **滚轮缩放**：以鼠标位置为中心缩放，精准定位

### ⚡ 快捷操作
- **Fit**：自适应画布大小
- **1:1 Actual**：查看原始像素尺寸
- **Match base**：让图片2自动匹配图片1的尺寸
- **Swap**：一键交换两张图的位置
- **👁 显示/隐藏**：快速切换图片2的可见性，确认原图状态

![差异对比概念图](https://static.yyfollower.com/overlay-compare-diff.png)

### 🌍 中英文双语
界面原生支持英语和简体中文，一键切换，中英文SEO也同时做了。

## 🔒 隐私第一
所有图片处理都在浏览器本地完成，**你的图片永远不会上传到任何服务器**。没有后端、没有数据库、没有API调用，纯HTML5 + CSS + JavaScript搞定。放心传敏感的设计稿和截图。

## 🛠️ 技术栈
纯静态站点，零构建步骤、零依赖：

- **index.html** — 语义化HTML5，内嵌JSON-LD结构化数据（WebApplication + FAQPage）
- **styles.css** — 纯白极简风格，响应式布局
- **script.js** — 纯原生JavaScript，无框架，所有交互 + 国际化逻辑手写

SEO方面下了点功夫：完整的 Open Graph / Twitter Card 标签、`hreflang` 多语言标注、规范URL、robots.txt + sitemap.xml、PWA Web Manifest，搜索引擎友好度拉满。

## 💡 使用场景
- **前端开发**：对比设计稿和实际渲染的还原度
- **UI/UX设计**：对比不同版本的界面方案
- **摄影后期**：对比原片和修图后的效果
- **QA测试**：视觉回归测试，快速定位UI差异
- **图片盗用检测**：对比两张图是否一致

## 写在最后
又是Vibe Coding的产物，一个下午从想法到上线。不需要复杂的框架，不需要后端，一个HTML文件+一个CSS+一个JS，就能做一个实实在在有用的小工具。GitHub仓库已经开源，欢迎star和提issue。

项目地址：[https://github.com/andy7076/overlay_image](https://github.com/andy7076/overlay_image)
在线体验：[https://overlay-image.yyfollower.com/](https://overlay-image.yyfollower.com/)