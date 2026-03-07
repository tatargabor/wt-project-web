"""CLI command for scaffolding web project knowledge files."""

import argparse
import shutil
import sys
from pathlib import Path
from typing import Optional

from wt_project_web.project_type import WebProjectType


def init_project(target_dir: Path, template_id: str, force: bool = False) -> None:
    """Scaffold project knowledge files from a template into the target directory."""
    project_type = WebProjectType()
    template_dir = project_type.get_template_dir(template_id)

    if template_dir is None:
        available = [t.id for t in project_type.get_templates()]
        print(f"Error: Unknown template '{template_id}'. Available: {', '.join(available)}")
        sys.exit(1)

    if not template_dir.exists():
        print(f"Error: Template directory not found: {template_dir}")
        sys.exit(1)

    copied = 0
    skipped = 0

    for src_file in sorted(template_dir.rglob("*")):
        if src_file.is_dir():
            continue

        rel_path = src_file.relative_to(template_dir)
        dest_file = target_dir / rel_path

        if dest_file.exists() and not force:
            print(f"  skip: {rel_path} (already exists, use --force to overwrite)")
            skipped += 1
            continue

        dest_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, dest_file)
        print(f"  create: {rel_path}")
        copied += 1

    print(f"\nDone: {copied} files created, {skipped} skipped")


def main() -> None:
    """Entry point for wt-project init command."""
    parser = argparse.ArgumentParser(
        prog="wt-project-web",
        description="Scaffold web project knowledge files",
    )
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Initialize project knowledge files")
    init_parser.add_argument(
        "--type",
        required=True,
        dest="template_type",
        help="Template type (e.g., nextjs, spa)",
    )
    init_parser.add_argument(
        "--target",
        default=".",
        help="Target project directory (default: current directory)",
    )
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files",
    )

    list_parser = subparsers.add_parser("list", help="List available templates")

    args = parser.parse_args()

    if args.command == "init":
        target = Path(args.target).resolve()
        print(f"Initializing web project knowledge ({args.template_type}) in {target}")
        init_project(target, args.template_type, args.force)
    elif args.command == "list":
        project_type = WebProjectType()
        print("Available templates:")
        for tmpl in project_type.get_templates():
            print(f"  {tmpl.id:12s} — {tmpl.description}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
