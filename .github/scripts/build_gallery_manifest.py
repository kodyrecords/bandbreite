"""Scans assets/galerie for photos and writes dist/assets/galerie/manifest.json,
sorted newest first by each file's earliest git commit date."""
import json
import pathlib
import subprocess

GALERIE_DIR = pathlib.Path("assets/galerie")
OUT_FILE = pathlib.Path("dist/assets/galerie/manifest.json")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def added_date(path):
    log = subprocess.run(
        ["git", "log", "--follow", "--format=%aI", "--", str(path)],
        capture_output=True, text=True,
    ).stdout.strip().splitlines()
    return log[-1] if log else ""


def main():
    items = []
    if GALERIE_DIR.exists():
        for f in sorted(GALERIE_DIR.glob("*")):
            if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS:
                items.append({"file": f.name, "date": added_date(f)})

    items.sort(key=lambda item: item["date"], reverse=True)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(items, indent=2))
    print(f"gallery manifest: {len(items)} photo(s)")


if __name__ == "__main__":
    main()
