---
title: 零成本给博客添加AI语音播报功能，5分钟搞定
date: 2026-04-19
tags: 博客, TTS, 技术
---

<audio controls style="width: 100%; margin: 20px 0;">
  <source src="https://static.yyfollower.com/voice/blog_intro.mp3" type="audio/mpeg">
  你的浏览器不支持音频播放，请点击 <a href="https://static.yyfollower.com/voice/blog_intro.mp3">这里</a> 下载收听。
</audio>

最近折腾了下免费的AI语音合成服务，给博客加了个语音播报功能，访客打开文章就能点播放听全文，完全不用花一分钱，全程5分钟就能搞定，给大家分享下怎么弄：

## 用到的工具：微软Edge-TTS
完全免费无限制，不需要申请API密钥，不需要注册任何账号，直接pip安装就能用，内置几十种中英文音色（温柔女声、御姐音、少女音、萝莉音、各种方言都有），生成速度1秒/段，音质比很多收费的TTS服务还好。

## 部署步骤：
1. **安装依赖**：服务器上直接跑 `pip install edge-tts` 就行，没有额外依赖
2. **生成语音**：一行命令搞定，比如生成文章导语：
   ```bash
   edge-tts --voice zh-CN-XiaoxiaoNeural --text "你要转的文本内容" --write-media 输出文件名.mp3
   ```
3. **上传静态资源**：把生成的mp3扔到你的静态资源站就行，我直接用的自己的 `static.yyfollower.com`
4. **嵌入博客**：在文章里加个原生的HTML audio标签，把src指向你的mp3地址，所有浏览器都支持，访客打开就能直接点播放

## 成本：0元
微软这个服务完全免费无调用次数限制，我用了快俩月了啥问题都没有，生成的语音也很自然，没有很多免费服务那种生硬的机械音。

## 进阶玩法
如果不想每次手动生成，写个10行的小脚本，发布文章的时候自动把全文转成语音上传，连手动操作的步骤都省了，全自动生成播报语音。
