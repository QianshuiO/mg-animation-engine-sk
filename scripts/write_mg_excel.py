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


COLUMNS = ["\u6587\u6848", "\u5206\u955c", "AI\u63d0\u793a\u8bcd"]


def sanitize_filename(text: str, fallback: str = "MG\u52a8\u753b\u811a\u672c") -> str:
    text = re.sub(r"\s+", "", text or "")
    text = re.sub(r'[\\/:*?"<>|]', "", text).strip(" .")
    return (text or fallback)[:20] or fallback


def unique_path(folder: Path, stem: str) -> Path:
    candidate = folder / f"{stem}.xlsx"
    idx = 2
    while candidate.exists():
        candidate = folder / f"{stem}_{idx}.xlsx"
        idx += 1
    return candidate


def load_rows(path: str) -> list[dict[str, str]]:
    if path == "-":
        data = sys.stdin.read()
    else:
        data = Path(path).read_text(encoding="utf-8-sig")
    rows = json.loads(data)
    if not isinstance(rows, list):
        raise SystemExit("rows-json must contain a JSON array.")
    return [{col: str(item.get(col, "")).strip() for col in COLUMNS} for item in rows]


def default_project_dir() -> Path:
    desktop = Path.home() / "Desktop"
    root = desktop if desktop.exists() else Path.home()
    return root / "MG\u52a8\u753b\u811a\u672c\u8f93\u51fa"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default="")
    parser.add_argument("--title-source", default="")
    parser.add_argument("--rows-json", required=True)
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve() if args.project else default_project_dir().resolve()
    output_dir = project / "\u811a\u672c\u5728\u8fd9\u91cc"
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = load_rows(args.rows_json)
    if not rows:
        raise SystemExit("No rows to write.")

    output_path = unique_path(output_dir, sanitize_filename(args.title_source or rows[0].get(COLUMNS[0], "")))
    wb = Workbook()
    ws = wb.active
    ws.title = "MG\u52a8\u753b\u811a\u672c"
    ws.append(COLUMNS)
    for row in rows:
        ws.append([row.get(col, "") for col in COLUMNS])

    header_fill = PatternFill("solid", fgColor="1F4E79")
    header_font = Font(color="FFFFFF", bold=True)
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    for col, width in {"A": 34, "B": 58, "C": 72}.items():
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
