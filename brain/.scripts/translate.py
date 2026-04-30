#!/usr/bin/env python3
"""
AI translate wiki/ markdown files to Thai for wiki_th/
Usage: translate.sh <source_file> <dest_file>

Requires MINIMAX_API_KEY and MINIMAX_API_BASE environment variables.
"""

import sys
import os
import re

def load_env():
    """Load .env file, properly handling inline comments."""
    env_path = "/Users/chinnawat/.hermes/.env"
    if not os.path.exists(env_path):
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                v = v.split("#")[0].strip()
                os.environ[k] = v

def translate_file(src_path: str, dst_path: str) -> bool:
    """Read source markdown, translate to Thai, write to dest."""

    load_env()
    api_key = os.environ.get("MINIMAX_API_KEY")
    api_base = os.environ.get("MINIMAX_BASE_URL", "https://api.minimax.io/v1")

    if not api_key:
        print("    ✗ MINIMAX_API_KEY not set — copying source as-is (no translation)")
        # Fallback: copy source file if dest doesn't exist
        if not os.path.exists(dst_path):
            with open(src_path) as src:
                content = src.read()
            # Remove frontmatter for wiki_th version
            content = strip_frontmatter(content)
            with open(dst_path, "w") as dst:
                dst.write(content)
            return True
        return False

    with open(src_path) as f:
        content = f.read()

    # Strip frontmatter for translation (preserve it separately)
    frontmatter, body = extract_frontmatter(content)

    if not body.strip():
        return True

    # Translate body to Thai
    translated_body = call_minimax_translate(body, api_key, api_base)

    # Reconstruct with frontmatter (no frontmatter for wiki_th pages)
    result = translated_body

    with open(dst_path, "w") as f:
        f.write(result)

    return True


def extract_frontmatter(content: str) -> tuple:
    """Split YAML frontmatter from body. Returns (frontmatter_str, body_str)."""
    if content.startswith("---"):
        parts = content[3:].split("---", 1)
        if len(parts) == 2:
            return parts[0].strip(), parts[1].strip()
    return "", content


def strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter block from markdown."""
    frontmatter, body = extract_frontmatter(content)
    return body


def call_minimax_translate(text: str, api_key: str, api_base: str) -> str:
    """Call MiniMax LLM API to translate English markdown to Thai."""
    import urllib.request
    import urllib.error
    import json

    system_prompt = """You are an expert translator. Translate English technical markdown to Thai.
Rules:
- Keep ALL markdown syntax intact (headers, lists, code blocks, links, tables, bold, italic)
- Keep technical terms in English when no good Thai equivalent exists (e.g. stop-loss, take-profit, backtesting, paper trade)
- Use natural Thai prose for explanatory text
- Preserve frontmatter tags but do NOT include frontmatter in output for wiki_th files
- Keep code blocks, file paths, class names exactly as-is
- Preserve [[WikiLink]] syntax
- Output ONLY the translated content, no commentary"""

    payload = {
        "model": "MiniMax-M2.5",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Translate this English markdown to Thai:\n\n{text}"}
        ],
        "temperature": 0.3,
        "max_tokens": 8192
    }

    url = f"{api_base.rstrip('/')}/chat/completions"

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            raw = result["choices"][0]["message"]["content"]
            # Strip thinking/reflection blocks if present
            import re
            return re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
    except urllib.error.HTTPError as e:
        print(f"    ✗ API error {e.code}: {e.read().decode()}")
        return text
    except Exception as e:
        print(f"    ✗ Request failed: {e}")
        return text


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: translate.sh <source_file> <dest_file>")
        sys.exit(1)

    src, dst = sys.argv[1], sys.argv[2]
    success = translate_file(src, dst)
    sys.exit(0 if success else 1)
