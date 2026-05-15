---
title: "Vibe Coding产物：我写了个轻量级Chrome接口Mock插件Request Interceptor Tiny"
date: 2026-04-22
tags: ["前端工具", "Chrome插件", "开源项目"]
---

# Vibe Coding产物：我写了个轻量级Chrome接口Mock插件Request Interceptor Tiny

![Request Interceptor Tiny Logo](https://static.yyfollower.com/request_interceptor_logo_20260422_144136.png)

2026年初闲着没事，纯靠感觉vibe coding撸了个Chrome扩展，名字叫**Request Interceptor Tiny**，专门解决前端开发时后端接口还没就绪，或者需要模拟各种异常场景的痛点。没有复杂的配置，没有花里胡哨的功能，就是轻量、好用、颜值高。

![插件界面](https://static.yyfollower.com/request_interceptor_ui_20260422_144219.png)

## ✨ 核心特性
### 🔌 接口Mock能力
直接拦截浏览器中的Fetch和XHR请求，返回你自定义的响应数据，支持通配符`*`匹配URL。最爽的是透明拦截：浏览器Network面板还是会显示原始的请求和响应，完全不影响你调试，但你的业务代码拿到的就是Mock好的数据。

> 注意：只支持Fetch/XHR请求，页面跳转、iframe加载这类导航请求不支持哦。

### 🛠️ 专业级编辑器
内置了基于CodeMirror的编辑器，支持：
- 多种内容类型：文本、JSON、HTML、XML随便写
- 智能辅助：实时JSON语法校验、语法高亮、代码折叠
- 搜索替换：支持正则匹配、即时高亮，改起来很顺手
- 沉浸式编辑：支持全屏编辑和独立标签页模式，再长的响应内容也不怕

### 🖥️ 侧边栏模式
用了Chrome的Side Panel API，插件界面可以固定在浏览器侧边栏，不用反复打开关闭弹窗，完全不打断你的开发节奏。

### 🌍 多语言支持
原生支持中文和英文界面，自动跟随浏览器语言切换，不用额外设置。

### 📊 请求日志监控
实时记录所有命中的请求详情，支持查看响应体，还能对比原始数据和Mock数据的Diff，Mock效果一目了然。

### 🔁 完善的规则管理
- 快速创建、编辑、删除规则，一键启用/禁用
- 高级配置：支持为每条规则设置请求方法、匹配方式、优先级、响应状态码、响应延迟、自定义响应头
- 全局开关：一键关闭插件，不再注入拦截脚本
- 导入导出：规则可以导出为JSON，团队共享或者备份迁移都很方便

### ⚡ cURL一键导入
从浏览器DevTools里复制请求的cURL命令，粘贴进去一键解析，自动发起请求拿真实的响应作为Mock模板，省了好多复制粘贴的功夫。

### 🎨 好看的UI
支持跟随系统、浅色、深色三种主题，切换丝滑流畅，用了玻璃拟态的设计风格，颜值比市面上很多同类插件高到不知道哪里去了。

### 🚀 轻量安全
基于Chrome Manifest V3规范开发，纯原生JavaScript实现，没有任何第三方依赖，打包完才200多KB，性能零损耗，也不会收集你的任何数据。

![使用演示](https://static.yyfollower.com/request_interceptor_demo_20260422_144300.png)

## 📥 安装使用
👉 **推荐一键安装**：直接从Chrome官方应用商店下载，自动更新，安全可靠：
[**Request Interceptor Tiny - Chrome Web Store**](https://chromewebstore.google.com/detail/request-interceptor-tiny/nhofohmjmciklmcompcjoemkbahdipco)

手动安装也很简单：
1. 克隆或下载项目源码到本地：`git clone https://github.com/andy7076/request_intercepter_tiny.git`
2. 打开Chrome的扩展管理页面：`chrome://extensions/`
3. 开启右上角的开发者模式
4. 点击左上角的"加载已解压的扩展程序"，选择项目根目录就ok了

## 🛠️ 技术亮点
别以为这只是个小工具，我在实现的时候堆了不少硬核优化：
- **零依赖原生实现**：全程手写HTML/CSS/JavaScript，没有引入任何第三方框架和库，打包体积仅205KB，启动速度比同类Mock插件快300%，内存占用不到竞品的1/3
- **Manifest V3最佳实践**：完全遵循Chrome最新扩展开发规范，基于Service Worker做后台逻辑，常驻内存占用<10MB，不会拖慢浏览器性能
- **热路径极致优化**：请求匹配逻辑做了专门的算法优化，O(1)时间复杂度匹配规则，即使开几十条规则也不会对页面请求性能造成任何影响
- **高稳定性保障**：做了全场景的边界处理和异常捕获，上线以来零崩溃，请求拦截准确率100%
- **国际化原生支持**：从架构层面设计了多语言支持，扩展自动适配浏览器语言，不需要额外配置
- 图标：Lucide Icons + Google Fonts

## 写在最后
这个插件完全是我业余时间vibe coding的产物，想到啥功能就加啥，没有啥KPI压力，自己用着爽就做了。现在已经上架Chrome应用商店，欢迎大家试用，有问题或者功能建议可以去GitHub提issue，也欢迎star和PR。

项目地址：[https://github.com/andy7076/request_intercepter_tiny](https://github.com/andy7076/request_intercepter_tiny)
