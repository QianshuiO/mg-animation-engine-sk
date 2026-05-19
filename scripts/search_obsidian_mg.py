#!/usr/bin/env python3
"""Search the bundled encrypted MG animation RAG library."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from cryptography.fernet import Fernet
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: cryptography. Install it before searching encrypted db.") from exc


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_VAULT = SKILL_DIR / "db"
DEFAULT_KEY = SKILL_DIR / "key.auth"
SKIP_DIRS = {".obsidian", "_图片附件", "_参考图素材库"}
TEXT_SUFFIXES = {".md", ".txt"}
ENCRYPTED_SUFFIX = ".mgenc"


def load_cipher(key_file: Path) -> Fernet:
    if not key_file.exists():
        raise SystemExit(f"Key file not found: {key_file}")
    key = key_file.read_text(encoding="utf-8").strip()
    return Fernet(key.encode("utf-8"))


def tokenize(text: str) -> list[str]:
    raw = re.split(r"[\s,，。；;：:/\\()\[\]{}<>《》\"'`]+", text)
    tokens: list[str] = []
    for item in raw:
        item = item.strip().lower()
        if not item:
            continue
        tokens.append(item)
        if re.search(r"[\u4e00-\u9fff]", item) and len(item) >= 4:
            for i in range(0, len(item) - 1):
                tokens.append(item[i : i + 2])
    return list(dict.fromkeys(tokens))


def iter_notes(vault: Path):
    for path in vault.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name.endswith(ENCRYPTED_SUFFIX):
            yield path


def read_plain_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="ignore")


def read_note(path: Path, cipher: Fernet | None) -> str:
    if path.name.endswith(ENCRYPTED_SUFFIX):
        if cipher is None:
            raise SystemExit("Encrypted note found, but no cipher was loaded.")
        data = cipher.decrypt(path.read_bytes())
        return data.decode("utf-8", errors="replace")
    return read_plain_text(path)


def display_name(path: Path) -> str:
    name = path.name
    if name.endswith(ENCRYPTED_SUFFIX):
        name = name[: -len(ENCRYPTED_SUFFIX)]
    return name


def first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return Path(fallback).stem


def snippet(text: str, tokens: list[str], size: int = 220) -> str:
    low = text.lower()
    positions = [low.find(t) for t in tokens if low.find(t) >= 0]
    if not positions:
        clean = re.sub(r"\s+", " ", text).strip()
        return clean[:size]
    start = max(min(positions) - 40, 0)
    clean = re.sub(r"\s+", " ", text[start : start + size]).strip()
    return clean


def score_note(path: Path, text: str, tokens: list[str], required: list[str]) -> int:
    haystack = f"{display_name(path)}\n{path.parent.name}\n{text}".lower()
    score = 0
    for token in tokens:
        count = haystack.count(token)
        if count:
            score += min(count, 6)
            if token in display_name(path).lower():
                score += 8
            if token in path.parent.name.lower():
                score += 5
    for token in required:
        if token.lower() not in haystack:
            return 0
        score += 10
    priority_dirs = ("07-风格规范", "03-结构讲解", "02-场景演绎", "04-数据图表", "05-转场过渡", "06-标题结尾", "01-开场钩子")
    if path.parent.name in priority_dirs:
        score += 3
    return score


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=False, default="", help="Chinese keywords or narration fragment.")
    parser.add_argument("--vault", default=str(DEFAULT_VAULT), help="RAG db path. Defaults to ../db.")
    parser.add_argument("--key", default=str(DEFAULT_KEY), help="Authorization key path. Defaults to ../key.auth.")
    parser.add_argument("--top", type=int, default=10, help="Number of results.")
    parser.add_argument("--required", default="", help="Space/comma separated terms that must appear.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    parser.add_argument("--show", default="", help="Print one decrypted note by relative path or filename.")
    args = parser.parse_args()

    vault = Path(args.vault).resolve()
    if not vault.exists():
        raise SystemExit(f"Vault not found: {vault}")

    cipher = load_cipher(Path(args.key).resolve())

    if args.show:
        wanted = args.show.replace("\\", "/")
        for path in iter_notes(vault):
            rel = path.relative_to(vault).as_posix()
            if wanted in (rel, display_name(path), rel.removesuffix(ENCRYPTED_SUFFIX)):
                print(read_note(path, cipher))
                return 0
        raise SystemExit(f"Note not found: {args.show}")

    if not args.query:
        raise SystemExit("--query is required unless --show is used.")

    tokens = tokenize(args.query)
    required = tokenize(args.required)
    results = []
    for path in iter_notes(vault):
        text = read_note(path, cipher)
        score = score_note(path, text, tokens, required)
        if score <= 0:
            continue
        rel = path.relative_to(vault)
        results.append(
            {
                "score": score,
                "title": first_heading(text, display_name(path)),
                "path": str(path),
                "relative_path": str(rel),
                "category": rel.parts[0] if rel.parts else "",
                "snippet": snippet(text, tokens),
            }
        )

    results.sort(key=lambda item: (-item["score"], item["relative_path"]))
    results = results[: args.top]

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0

    for idx, item in enumerate(results, 1):
        print(f"{idx}. [{item['score']}] {item['title']}")
        print(f"   path: {item['path']}")
        print(f"   relative_path: {item['relative_path']}")
        print(f"   category: {item['category']}")
        print(f"   snippet: {item['snippet']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
