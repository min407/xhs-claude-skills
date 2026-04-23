# XHS Creator Toolkit

Claude Code skills plus a local clipping service for Xiaohongshu creators.

## What is included

1. `skills/` for Claude Code:
   - `/xhs`
   - `/xhs-batch`
   - `/xhs-analyze`
   - `/xhs-cover`
2. `service/` for one-click local clipping

## Best for

- saving Xiaohongshu posts into a structured local knowledge base
- analyzing saved posts for topic research
- generating cover ideas for creators
- clipping the current browser page with a local service

## Quick start

### Install in Claude Code

```bash
/plugin marketplace add chenxiachan/xhs-claude-skills
/plugin install rednote-to-obsidian@chenxiachan-xhs-claude-skills
```

### Export cookies

Export your logged-in Xiaohongshu cookies to:

```text
~/cookies.json
```

### Run the local service

```bash
cd service
python3 server.py
curl http://127.0.0.1:7895/health
```

See [service/README.md](service/README.md) for details.

## Default output path

```text
~/Documents/Obsidian Vault/xhs
```

You can override it with `XHS_OUTPUT_DIR`.

## Privacy

- cookies stay on your machine
- this repo ignores cookies, logs, caches, and temp media files
- do not commit your own exported notes or local vault contents
