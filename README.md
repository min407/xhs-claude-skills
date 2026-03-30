<div align="center">

# 📕 小红书转 Obsidian

### 把小红书帖子变成可操作的 Obsidian 笔记 — 支持视频语音转录

[![Platform](https://img.shields.io/badge/macOS-black?logo=apple&logoColor=white)](https://github.com/chenxiachan/xhs-claude-skills)
[![Claude Code](https://img.shields.io/badge/Claude_Code-插件-7C3AED)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

中文 &nbsp;|&nbsp; **[English](README_EN.md)**

</div>

---

## ✨ 功能

| 命令 | 说明 |
|:-----|:-----|
| 📄 `/xhs <链接>` | 提取单个帖子 — 文字、图片、视频转录 |
| 📦 `/xhs-batch <链接列表>` | 批量提取多个帖子 |
| 🔍 `/xhs-analyze [关键词]` | 分析已保存的帖子 — 总结、对比、发现模式 |

## 🏗 工作原理

```
 📕 小红书链接
     │
     ▼
 ┌─────────────────────────┐
 │  🍪 Cookie 认证          │  ← 首次运行：自动引导，30秒搞定
 └────────────┬────────────┘
              ▼
 ┌─────────────────────────┐
 │  📦 解析页面数据         │  ← 一次 HTTP 请求，无需浏览器
 └────┬──────┬──────┬──────┘
      ▼      ▼      ▼
    📝       🖼     🎬
   文字     图片    视频
                     │
                ┌────┴────┐
                │ ffmpeg  │
                │ whisper │
                └────┬────┘
                     ▼
              🗒 Obsidian 笔记
           扫一眼 → 深挖 or 跳过
```

> 🚫 不需要 MCP 服务 &nbsp; 🚫 不需要 Playwright &nbsp; 🚫 不需要无头浏览器
>
> ✅ 只用 cookies + HTTP + 本地 whisper

## 📂 输出格式

```
xhs/
├── 📄 2026-03-15 XX的核心发现.md
├── 📄 2026-03-22 YY方法论解析.md
├── 📄 2026-03-29 ZZ技术突破.md
├── 🖼 img/
└── 🎬 video/
```

### 🗒 笔记结构

```markdown
# 一句话洞察                          ← 判断，不是描述

核心论点，2-3 句话。

**与我的关联：** 为什么跟我有关。
**值得深挖吗：** 是/否 + 理由。

> [!tip]- 详情                         ← 📌 默认折叠
> 结构化内容...

> [!info]- 笔记属性                     ← 📌 默认折叠
> 来源 · 日期 · 互动 · 标签
```

## 📋 前置要求

| | 说明 | 安装 |
|:--|:-----|:-----|
| 🤖 **Claude Code** | 本插件运行环境 | [安装指南](https://docs.anthropic.com/en/docs/claude-code) |
| 📓 **Obsidian** | 笔记保存目标（只需 vault 文件夹存在，不需要 CLI） | [下载](https://obsidian.md) |
| 🍎 **macOS** | Apple Silicon 推荐 | — |

> 💡 Obsidian 不需要安装 CLI。插件只是把 `.md` 文件写入你的 vault 文件夹，Obsidian 会自动识别。

### 视频转录（可选）

文字/图片帖子零额外依赖。视频帖子的语音转录需要：

| | 安装 | 用途 |
|:--|:-----|:-----|
| 🎵 ffmpeg | `brew install ffmpeg` | 提取音频 |
| 🗣 mlx-whisper | `pip install mlx-whisper` | 语音转文字（本地运行） |

## 🚀 快速开始

### 1. 安装插件

```bash
claude /plugin install chenxiachan/xhs-claude-skills
```

### 2. 首次运行

```
/xhs https://www.xiaohongshu.com/explore/...
```

首次运行时，skill 会检测到没有 cookies 并**自动引导你完成 30 秒设置**：

1. 🌐 打开 Chrome → xiaohongshu.com（确保已登录）
2. 🔧 打开 DevTools Console（F12）
3. 📋 粘贴 skill 给出的代码 → cookies 自动复制到剪贴板
4. 💾 保存到 `~/cookies.json`
5. ✅ 搞定 — 之后每次运行自动使用

> 🔄 Cookies 过期时 skill 会自动检测并重新引导，无需手动检查。

## ⚙️ 配置

如果路径不同，编辑 `skills/xhs/SKILL.md` 中的常量：

| 配置项 | 默认值 |
|:------|:------|
| 🍪 Cookies | `~/cookies.json` |
| 📁 输出目录 | `~/Documents/Obsidian Vault/xhs` |

## 🎨 个性化

每条笔记包含"**与我的关联**"——根据你的背景自动生成。Skill 会读取 Claude Code 的 memory 系统（`~/.claude/projects/*/memory/`）了解你是谁。无需手动配置——正常使用 Claude Code，它会逐步学习你的上下文。

## 📁 插件结构

```
rednote-to-obsidian/
├── 📋 .claude-plugin/
│   └── plugin.json
├── 📂 skills/
│   ├── xhs/SKILL.md
│   ├── xhs-batch/SKILL.md
│   └── xhs-analyze/SKILL.md
├── 📄 README.md
└── 📄 README_CN.md
```

<div align="center">

---

MIT License

</div>
