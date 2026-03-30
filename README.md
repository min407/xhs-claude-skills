# xhs-claude-skills

Claude Code slash commands for extracting, transcribing, and summarizing Xiaohongshu (小红书) posts into Obsidian-friendly Markdown notes.

## Skills

| Command | Description |
|---------|-------------|
| `/xhs <url>` | Extract a single post — text, images, video transcription |
| `/xhs-batch <urls>` | Batch extract multiple posts |
| `/xhs-analyze [keyword]` | Analyze saved posts — summarize, compare, find patterns |

## How it works

1. Fetches post HTML using exported Chrome cookies
2. Parses `window.__INITIAL_STATE__` for all post data (no MCP or headless browser needed)
3. For video posts: downloads video → `ffmpeg` extracts audio → `mlx-whisper` transcribes
4. Outputs a concise, opinionated Markdown note (Peter Thiel style — scan in 5 seconds, decide to dig deeper or skip)

## Output format

```
xhs/
├── 2026-03-22 RLCF训练科研品味.md
├── 2026-03-28 AI学习法三问框架.md
├── 2026-03-29 杨立昆JEPA反坍塌.md
├── img/
└── video/
```

Each note:
- **H1**: One-line insight (not a description)
- **2-3 sentences**: Core argument
- **Relevance**: One line on why this matters to you
- **Worth digging?**: Yes/No + reason
- **Collapsible details**: Full structured content (click to expand)
- **Collapsible metadata**: Source, date, stats, tags

## Prerequisites

- **macOS** (Apple Silicon recommended for whisper)
- **`ffmpeg`**: `brew install ffmpeg`
- **`mlx-whisper`**: `pip install mlx-whisper` (video transcription)
- **Chrome cookies**: Export from Chrome DevTools once, refresh when expired

### Cookie export

Open Chrome DevTools on xiaohongshu.com, run in Console:

```javascript
copy(JSON.stringify(document.cookie.split('; ').map(c => {
  const [name, ...rest] = c.split('=');
  return { name, value: rest.join('='), domain: '.xiaohongshu.com', path: '/',
    expires: Date.now()/1000 + 86400*30, size: name.length + rest.join('=').length,
    httpOnly: false, secure: false, session: false, priority: 'Medium',
    sameParty: false, sourceScheme: 'Secure', sourcePort: 443 };
})))
```

Save clipboard to `~/cookies.json`.

## Installation

Copy the `commands/` folder to your Claude Code config:

```bash
cp commands/xhs*.md ~/.claude/commands/
```

Then configure the Obsidian save path and cookies path in each skill file if your setup differs from the defaults.

## Customization

The `"与我的关联"` section in `/xhs` is personalized — edit the user background description in `commands/xhs.md` (step 4) to match your own research/work context.

## License

MIT
