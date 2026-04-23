#!/usr/bin/env python3
"""
XHS local clipper.

Fetch a Xiaohongshu post with local cookies and save it as Markdown in a local
folder. This version is designed for sharing publicly, so all personal paths
are configurable via environment variables.
"""
from __future__ import annotations

import json
import os
import re
import ssl
import subprocess
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

DEFAULT_COOKIES_FILE = Path.home() / "cookies.json"
DEFAULT_OUTPUT_DIR = Path.home() / "Documents" / "Obsidian Vault" / "xhs"

COOKIES_FILE = Path(
    os.getenv("XHS_COOKIES_FILE", str(DEFAULT_COOKIES_FILE))
).expanduser()
OUTPUT_DIR = Path(
    os.getenv("XHS_OUTPUT_DIR", str(DEFAULT_OUTPUT_DIR))
).expanduser()
IMG_SUBDIR = OUTPUT_DIR / "img"

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)


def log(message: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}", flush=True)


def safe_filename(text: str, maxlen: int = 40) -> str:
    text = re.sub(r'[\\/:*?"<>|\n\r\t]', "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:maxlen] if text else "untitled"


def load_cookies() -> str:
    if not COOKIES_FILE.exists():
        raise RuntimeError(
            f"Cookies file not found: {COOKIES_FILE}. "
            "Export cookies from a logged-in Xiaohongshu session first."
        )
    with COOKIES_FILE.open(encoding="utf-8") as fh:
        cookies = json.load(fh)
    if not isinstance(cookies, list):
        raise RuntimeError("cookies.json must be a JSON array.")
    return "; ".join(f"{item['name']}={item['value']}" for item in cookies)


def fetch_page(url: str) -> str:
    cookie_str = load_cookies()
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(url)
    req.add_header("Cookie", cookie_str)
    req.add_header("User-Agent", UA)
    req.add_header(
        "Accept",
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
        "image/webp,*/*;q=0.8",
    )
    req.add_header("Accept-Language", "zh-CN,zh;q=0.9")

    with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def parse_note(html: str) -> dict:
    match = re.search(
        r"window\.__INITIAL_STATE__\s*=\s*(\{.+?\})\s*</script>",
        html,
        re.DOTALL,
    )
    if not match:
        raise RuntimeError(
            "Could not find __INITIAL_STATE__. Your cookies may have expired, "
            "or the URL is not a valid Xiaohongshu post page."
        )

    payload = json.loads(match.group(1).replace("undefined", "null"))
    note_map = payload.get("note", {}).get("noteDetailMap", {})
    if not note_map:
        raise RuntimeError("noteDetailMap is empty. The post may be unavailable.")

    key = next(iter(note_map))
    note = note_map[key].get("note", {})
    note["_key"] = key
    return note


def download_image(url: str, out_path: Path) -> None:
    url = url.replace("http://", "https://")
    subprocess.run(
        [
            "curl",
            "-sS",
            "-L",
            "--max-time",
            "30",
            "-H",
            "Referer: https://www.xiaohongshu.com/",
            "-H",
            f"User-Agent: {UA}",
            "-o",
            str(out_path),
            url,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if not out_path.exists() or out_path.stat().st_size == 0:
        raise RuntimeError(f"Failed to download image: {url[:120]}")


def build_markdown(note: dict, post_id: str, url: str, img_files: list[Path]) -> tuple[str, str]:
    title = note.get("title") or note.get("desc", "")[:30] or "Untitled"
    desc = note.get("desc", "")
    user = note.get("user", {}).get("nickname", "Unknown")
    location = note.get("ipLocation", "")
    interact = note.get("interactInfo", {})
    tags = [tag.get("name", "") for tag in note.get("tagList", []) if tag.get("name")]
    ts = note.get("time", 0) / 1000
    pub_date = datetime.fromtimestamp(ts).strftime("%Y-%m-%d") if ts else ""

    clean_desc = re.sub(r"#[^#\[]+\[话题\]#\s*", "", desc).strip()
    img_md = "\n".join(
        f"> ![Image {idx + 1}](img/{file.name})" for idx, file in enumerate(img_files)
    )
    if not img_md:
        img_md = "> No images extracted."

    markdown = f"""# {title}

> [!tip]- Details
> **Original text:**
>
> {clean_desc.replace(chr(10), chr(10) + '> ')}
>
> **Images:**
>
{img_md}

> [!info]- Metadata
> - **Source**: Xiaohongshu · {user}
> - **Post ID**: {post_id}
> - **URL**: {url}
> - **Publish date**: {pub_date}
> - **Saved date**: {datetime.now().strftime("%Y-%m-%d")}
> - **Type**: {note.get("type", "normal")}
> - **Engagement**: {interact.get('likedCount', 0)} likes / {interact.get('collectedCount', 0)} saves / {interact.get('commentCount', 0)} comments / {interact.get('shareCount', 0)} shares
> - **Location**: {location}
> - **Tags**: {', '.join(tags) if tags else 'None'}
"""
    return markdown, pub_date


def clip(url: str) -> dict:
    try:
        log(f"Start clipping: {url[:100]}")
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        IMG_SUBDIR.mkdir(parents=True, exist_ok=True)

        html = fetch_page(url)
        note = parse_note(html)
        post_id = note["_key"]
        log(f"Parsed note: {note.get('title', '')[:30]} | type={note.get('type')}")

        img_files: list[Path] = []
        for index, image in enumerate(note.get("imageList", []), start=1):
            img_url = image.get("urlDefault", "")
            if not img_url:
                continue
            out_path = IMG_SUBDIR / f"{post_id[:8]}-{index}.jpg"
            try:
                download_image(img_url, out_path)
                img_files.append(out_path)
            except Exception as exc:
                log(f"Image {index} failed: {exc}")

        markdown, pub_date = build_markdown(note, post_id, url, img_files)
        date_prefix = pub_date or datetime.now().strftime("%Y-%m-%d")
        title = note.get("title") or note.get("desc", "")[:30] or "Untitled"
        filename = f"{date_prefix} {safe_filename(title)}.md"
        file_path = OUTPUT_DIR / filename
        file_path.write_text(markdown, encoding="utf-8")
        log(f"Saved: {file_path}")

        return {
            "success": True,
            "title": title,
            "file": filename,
            "path": str(file_path),
            "images": len(img_files),
        }
    except Exception as exc:
        log(f"Error: {exc}")
        return {"success": False, "error": str(exc)}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 clipper.py <xiaohongshu-url>")
        sys.exit(1)
    result = clip(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
