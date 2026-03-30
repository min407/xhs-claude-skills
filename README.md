<div align="center">

# RedNote to Obsidian

### Claude Code skills for extracting RedNote posts into actionable Obsidian notes

[![Platform](https://img.shields.io/badge/platform-macOS-black?logo=apple)](https://github.com/chenxiachan/xhs-claude-skills)
[![Claude Code](https://img.shields.io/badge/Claude_Code-skill-blueviolet?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJ3aGl0ZSI+PGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiLz48L3N2Zz4=)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**[中文](README_CN.md)** &nbsp;|&nbsp; English

---

*Extract text, images, and video transcriptions from [RedNote (小红书)](https://www.xiaohongshu.com) — no headless browser needed.*

</div>

<br>

## Features

| Command | What it does |
|:--------|:-------------|
| `/xhs <url>` | Extract a single post — text, images, video transcription |
| `/xhs-batch <urls>` | Batch extract multiple posts |
| `/xhs-analyze [keyword]` | Analyze saved posts — summarize, compare, find patterns |

<br>

## Architecture

```
 RedNote URL
     │
     ▼
 ┌─────────────────────────┐
 │  Chrome cookies auth    │  ← Export once, no login conflict
 └────────────┬────────────┘
              ▼
 ┌─────────────────────────┐
 │  Parse __INITIAL_STATE__ │  ← All data in one HTTP request
 └────┬──────┬──────┬──────┘
      ▼      ▼      ▼
    Text   Images  Video
      │      │      │
      │      │      ├─ curl download
      │      │      ├─ ffmpeg → audio
      │      │      └─ mlx-whisper → transcript
      │      │      │
      ▼      ▼      ▼
 ┌─────────────────────────┐
 │   Obsidian Markdown     │  ← Scan in 5s, decide to dig deeper
 └─────────────────────────┘
```

> **Zero infrastructure** — no MCP server, no Playwright, no headless browser. Just cookies + HTTP + local whisper.

<br>

## Output

```
xhs/
├── 2026-03-22 社区反馈训练AI判断力.md
├── 2026-03-28 AI学习法三问框架.md
├── 2026-03-29 世界模型反坍塌证明.md
├── img/
└── video/
```

Each note is a **decision tool**, not a knowledge dump:

```markdown
# One-line insight                          ← not a description, a judgment

Core argument in 2-3 sentences.

**Relevance:** Why this matters to you.
**Worth digging?** Yes/No + reason.

> [!tip]- Details                            ← collapsed
> Full structured content...

> [!info]- Metadata                          ← collapsed
> Source, date, stats, tags...
```

<br>

## Prerequisites

| Dependency | Install | Required for |
|:-----------|:--------|:-------------|
| macOS (Apple Silicon) | — | Best performance |
| `ffmpeg` | `brew install ffmpeg` | Audio extraction |
| `mlx-whisper` | `pip install mlx-whisper` | Video transcription |
| Chrome cookies | See below | Authentication |

### Cookie Export

Open Chrome DevTools on `xiaohongshu.com` → Console → paste:

```javascript
copy(JSON.stringify(document.cookie.split('; ').map(c => {
  const [name, ...rest] = c.split('=');
  return { name, value: rest.join('='), domain: '.xiaohongshu.com', path: '/',
    expires: Date.now()/1000 + 86400*30, size: name.length + rest.join('=').length,
    httpOnly: false, secure: false, session: false, priority: 'Medium',
    sameParty: false, sourceScheme: 'Secure', sourcePort: 443 };
})))
```

Save clipboard → `~/cookies.json`. Refresh when cookies expire.

<br>

## Install

```bash
cp commands/xhs*.md ~/.claude/commands/
```

Edit paths in each skill if your setup differs:

| Setting | Default |
|:--------|:--------|
| Cookies | `~/cookies.json` |
| Output | `~/Documents/Obsidian Vault/xhs` |

<br>

## Customization

The **"Relevance"** field is personalized to your background. Edit the user description in `commands/xhs.md` (step 4) to match your context — researcher, developer, designer, whatever you are.

<br>

<div align="center">

---

MIT License

</div>
