<div align="center">

# 小红书转 Obsidian

### 用 Claude Code 技能包把小红书帖子变成可操作的 Obsidian 笔记

[![Platform](https://img.shields.io/badge/platform-macOS-black?logo=apple)](https://github.com/chenxiachan/xhs-claude-skills)
[![Claude Code](https://img.shields.io/badge/Claude_Code-技能包-blueviolet?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJ3aGl0ZSI+PGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiLz48L3N2Zz4=)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

中文 &nbsp;|&nbsp; **[English](README.md)**

---

*从[小红书](https://www.xiaohongshu.com)提取文字、图片和视频转录 — 无需无头浏览器。*

</div>

<br>

## 功能

| 命令 | 说明 |
|:-----|:-----|
| `/xhs <链接>` | 提取单个帖子 — 文字、图片、视频转录 |
| `/xhs-batch <链接列表>` | 批量提取多个帖子 |
| `/xhs-analyze [关键词]` | 分析已保存的帖子 — 总结、对比、发现模式 |

<br>

## 工作原理

```
 小红书链接
     │
     ▼
 ┌─────────────────────────┐
 │  Chrome cookies 认证     │  ← 导出一次，不影响浏览器登录
 └────────────┬────────────┘
              ▼
 ┌─────────────────────────┐
 │  解析 __INITIAL_STATE__  │  ← 一次 HTTP 请求拿到全部数据
 └────┬──────┬──────┬──────┘
      ▼      ▼      ▼
    文字    图片    视频
      │      │      │
      │      │      ├─ curl 下载
      │      │      ├─ ffmpeg → 音频
      │      │      └─ mlx-whisper → 转录
      │      │      │
      ▼      ▼      ▼
 ┌─────────────────────────┐
 │   Obsidian Markdown     │  ← 扫一眼决定要不要深挖
 └─────────────────────────┘
```

> **零基础设施** — 不需要 MCP 服务、Playwright 或无头浏览器。只用 cookies + HTTP + 本地 whisper。

<br>

## 输出格式

```
xhs/
├── 2026-03-22 社区反馈训练AI判断力.md
├── 2026-03-28 AI学习法三问框架.md
├── 2026-03-29 世界模型反坍塌证明.md
├── img/
└── video/
```

每条笔记是**决策工具**，不是信息搬运：

```markdown
# 一句话洞察                               ← 不是描述，是判断

核心论点，2-3 句话。直接，有态度。

**与我的关联：** 为什么跟我有关。
**值得深挖吗：** 是/否 + 理由。

> [!tip]- 详情                              ← 默认折叠
> 完整结构化内容...

> [!info]- 笔记属性                          ← 默认折叠
> 来源、日期、互动数据、标签...
```

<br>

## 依赖

| 依赖 | 安装 | 用途 |
|:-----|:-----|:-----|
| macOS (Apple Silicon) | — | 最佳性能 |
| `ffmpeg` | `brew install ffmpeg` | 提取音频 |
| `mlx-whisper` | `pip install mlx-whisper` | 视频转录 |
| Chrome cookies | 见下方 | 认证 |

### 导出 Cookies

Chrome 打开 `xiaohongshu.com` → DevTools → Console 粘贴：

```javascript
copy(JSON.stringify(document.cookie.split('; ').map(c => {
  const [name, ...rest] = c.split('=');
  return { name, value: rest.join('='), domain: '.xiaohongshu.com', path: '/',
    expires: Date.now()/1000 + 86400*30, size: name.length + rest.join('=').length,
    httpOnly: false, secure: false, session: false, priority: 'Medium',
    sameParty: false, sourceScheme: 'Secure', sourcePort: 443 };
})))
```

粘贴保存 → `~/cookies.json`。过期后重新导出。

<br>

## 安装

```bash
cp commands/xhs*.md ~/.claude/commands/
```

如果路径不同，修改每个 skill 文件里的配置：

| 配置项 | 默认值 |
|:------|:------|
| Cookies | `~/cookies.json` |
| 输出目录 | `~/Documents/Obsidian Vault/xhs` |

<br>

## 个性化

笔记中的"与我的关联"会根据你的背景生成。编辑 `commands/xhs.md` 步骤 4 中的用户描述，改成你自己的身份和方向即可 — 研究者、开发者、设计师，任何角色都行。

<br>

<div align="center">

---

MIT License

</div>
