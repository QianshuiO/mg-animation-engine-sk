#!/usr/bin/env python3
"""Encrypt or decrypt MG skill resources using the local key.auth file."""

from __future__ import annotations

import argparse
from pathlib import Path

from cryptography.fernet import Fernet


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_KEY = SKILL_DIR / "key.auth"
ENCRYPTED_SUFFIX = ".mgenc"


def load_cipher(key_file: Path) -> Fernet:
    return Fernet(key_file.read_text(encoding="utf-8").strip().encode("utf-8"))


def encrypt_file(path: Path, cipher: Fernet, remove_source: bool) -> Path:
    target = path.with_name(path.name + ENCRYPTED_SUFFIX)
    target.write_bytes(cipher.encrypt(path.read_bytes()))
    if remove_source:
        path.unlink()
    return target


def decrypt_file(path: Path, cipher: Fernet, remove_source: bool) -> Path:
    if not path.name.endswith(ENCRYPTED_SUFFIX):
        raise ValueError(f"Not encrypted: {path}")
    target = path.with_name(path.name[: -len(ENCRYPTED_SUFFIX)])
    target.write_bytes(cipher.decrypt(path.read_bytes()))
    if remove_source:
        path.unlink()
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["encrypt", "decrypt"])
    parser.add_argument("target")
    parser.add_argument("--key", default=str(DEFAULT_KEY))
    parser.add_argument("--keep-source", action="store_true")
    args = parser.parse_args()

    cipher = load_cipher(Path(args.key))
    target = Path(args.target)
    files = [target] if target.is_file() else [p for p in target.rglob("*") if p.is_file()]
    changed = []
    for path in files:
        if path.name == "key.auth":
            continue
        if args.mode == "encrypt":
            if path.name.endswith(ENCRYPTED_SUFFIX):
                continue
            changed.append(str(encrypt_file(path, cipher, not args.keep_source)))
        else:
            if not path.name.endswith(ENCRYPTED_SUFFIX):
                continue
            changed.append(str(decrypt_file(path, cipher, not args.keep_source)))
    print("\n".join(changed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
