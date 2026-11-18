"""``aiintake`` command line: new / assess / export / categories."""

from __future__ import annotations

import argparse
import sys
from importlib import resources
from pathlib import Path

from . import __version__
from .assess import assess
from .policy import EFFECT_AREAS, PRESUMED_CATEGORIES
from .report import export_inventory, to_markdown


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="aiintake", description="Federal AI use case intake and risk screening")
    p.add_argument("--version", action="version", version=f"aiintake {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new", help="write a blank intake form")
    n.add_argument("path")
    a = sub.add_parser("assess", help="validate and assess intake files")
    a.add_argument("files", nargs="+")
    a.add_argument("--out-dir", help="write one Markdown report per intake here")
    e = sub.add_parser("export", help="export intakes as 2025 inventory CSV rows")
    e.add_argument("files", nargs="+")
    e.add_argument("--out", default="inventory.csv")
    sub.add_parser("categories", help="list effect areas and presumed high-impact categories")
    args = p.parse_args(argv)

    if args.cmd == "new":
        path = Path(args.path)
        if path.exists():
            print(f"{path} already exists", file=sys.stderr)
            return 1
        path.write_text(resources.files("aiintake").joinpath("templates/intake.yaml").read_text(encoding="utf-8"),
                        encoding="utf-8")
        print(f"wrote {path}")
    elif args.cmd == "assess":
        status = 0
        for f in args.files:
            a = assess(f)
            md = to_markdown(a)
            if args.out_dir:
                out = Path(args.out_dir)
                out.mkdir(parents=True, exist_ok=True)
                target = out / (Path(f).stem + ".md")
                target.write_text(md, encoding="utf-8")
                print(f"{f}: {a.determination} | {a.compliance} → {target}")
            else:
                print(md, "\n")
            if a.errors:
                status = 2
        return status
    elif args.cmd == "export":
        rows = [assess(f) for f in args.files]
        export_inventory(rows, args.out)
        print(f"wrote {len(rows)} rows → {args.out}")
    elif args.cmd == "categories":
        print("Effect areas (decision_role.effect_areas):")
        for k, v in EFFECT_AREAS.items():
            print(f"  {k:26s} {v}")
        print("\nPresumed high-impact purposes (decision_role.presumed_categories):")
        for k, v in PRESUMED_CATEGORIES.items():
            print(f"  {k:32s} {v['label']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
