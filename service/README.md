# Local Service

This folder contains a lightweight local HTTP service for one-click Xiaohongshu clipping.

## What it is for

- Turn the current Xiaohongshu post page into a local Markdown note
- Save images locally
- Power a bookmarklet, Raycast script, Alfred workflow, or any other local automation

If you want batch extraction, AI analysis, or cover generation, use the Claude Code skills in `../skills/`.

## Before you start

1. Log in to Xiaohongshu in Chrome.
2. Export cookies into `~/cookies.json`.
3. Make sure Python 3 is available.

## Start the service

```bash
cd service
python3 server.py
```

Default address:

- `http://127.0.0.1:7895/health`
- `http://127.0.0.1:7895/clip`

## Optional environment variables

```bash
export XHS_COOKIES_FILE=~/cookies.json
export XHS_OUTPUT_DIR=~/Documents/Obsidian\ Vault/xhs
export XHS_HOST=127.0.0.1
export XHS_PORT=7895
```

## Test it

```bash
curl "http://127.0.0.1:7895/clip?url=https://www.xiaohongshu.com/explore/xxxxxxxxxxxxxxxxxxxxxxxx"
```

## Bookmarklet example

Save the snippet below as a browser bookmark URL. Open a Xiaohongshu post and click it.

```javascript
javascript:(function(){fetch('http://127.0.0.1:7895/clip',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url:location.href})}).then(r=>r.json()).then(data=>alert(data.success?'已保存：'+data.file:'失败：'+(data.error||'未知错误'))).catch(err=>alert('请求失败：'+err));})();
```

## Privacy

- `cookies.json` stays on your own machine
- this repo ignores cookies, logs, caches, and local outputs by default
- do not commit your own exported notes or vault contents
