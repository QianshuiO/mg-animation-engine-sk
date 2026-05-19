#!/usr/bin/env python3
"""Write a three-column MG animation storyboard Excel file."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


COLUMNS = ["文案", "分镜", "AI提示词"]


def sanitize_filename(text: str, fallback: str = "MG动画脚本") -> str:
    text = re.sub(r"\s+", "", text or "")
    text = re.sub(r'[\\/:*?"<>|]', "", text)
    text = text.strip(" .")
    if not text:
        text = fallback
    return text[:20] or fallback


def unique_path(folder: Path, stem: str) -> Path:
    candidate = folder / f"{stem}.xlsx"
    if not candidate.exists():
        return candidate
    idx = 2
    while True:
        candidate = folder / f"{stem}_{idx}.xlsx"
        if not candidate.exists():
            return candidate
        idx += 1


def load_rows(path: str) -> list[dict[str, str]]:
    if path == "-":
        data = sys.stdin.read()
    else:
        data = Path(path).read_text(encoding="utf-8")
    rows = json.loads(data)
    if not isinstance(rows, list):
        raise SystemExit("rows-json must contain a JSON array.")
    cleaned: list[dict[str, str]] = []
    for item in rows:
        if not isinstance(item, dict):
            raise SystemExit("Each row must be an object.")
        cleaned.append({col: str(item.get(col, "")).strip() for col in COLUMNS})
    return cleaned


def default_project_dir() -> Path:
    desktop = Path.home() / "Desktop"
    if desktop.exists():
        return desktop / "MG动画脚本输出"
    return Path.home() / "MG动画脚本输出"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default="", help="User project folder path. Defaults to Desktop/MG动画脚本输出.")
    parser.add_argument("--title-source", default="", help="Copy opening or topic used to name the Excel file.")
    parser.add_argument("--rows-json", required=True, help="Path to rows JSON, or - for stdin.")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve() if args.project else default_project_dir().resolve()
    output_dir = project / "脚本在这里"
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = load_rows(args.rows_json)
    if not rows:
        raise SystemExit("No rows to write.")

    title_source = args.title_source or rows[0].get("文案", "")
    output_path = unique_path(output_dir, sanitize_filename(title_source))

    wb = Workbook()
    ws = wb.active
    ws.title = "MG动画脚本"
    ws.append(COLUMNS)
    for row in rows:
        ws.append([row.get(col, "") for col in COLUMNS])

    header_fill = PatternFill("solid", fgColor="1F4E79")
    header_font = Font(color="FFFFFF", bold=True)
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    widths = {"A": 34, "B": 58, "C": 72}
    for col, width in widths.items():
        ws.column_dimensions[col].width = width
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)
    for idx in range(2, ws.max_row + 1):
        ws.row_dimensions[idx].height = 84
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(ws.max_column)}{ws.max_row}"

    wb.save(output_path)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
