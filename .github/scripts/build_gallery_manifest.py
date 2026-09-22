"""Scans assets/galerie for photos and assets/videos/videos.json for
manually-dated video entries, merging both into a single
dist/assets/galerie/manifest.json sorted newest first."""
import datetime
import json
import pathlib
import subprocess

GALERIE_DIR = pathlib.Path("assets/galerie")
VIDEOS_DIR = pathlib.Path("assets/videos")
VIDEOS_FILE = VIDEOS_DIR / "videos.json"
OUT_FILE = pathlib.Path("dist/assets/galerie/manifest.json")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def added_date(path):
    log = subprocess.run(
        ["git", "log", "--follow", "--format=%aI", "--", str(path)],
        capture_output=True, text=True,
    ).stdout.strip().splitlines()
    return log[-1] if log else ""


def load_photos():
    items = []
    if GALERIE_DIR.exists():
        for f in sorted(GALERIE_DIR.glob("*")):
            if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS:
                items.append({"type": "photo", "file": f.name, "date": added_date(f)})
    return items


def load_videos():
    if not VIDEOS_FILE.exists():
        return []
    entries = json.loads(VIDEOS_FILE.read_text())
    # Basic validation so a malformed entry fails loudly instead of
    # silently breaking the sort or the frontend render.
    for entry in entries:
        entry["type"] = "video"
        for required in ("image", "date", "url", "title"):
            if not entry.get(required):
                raise ValueError(f"video entry missing '{required}': {entry}")
        image_path = VIDEOS_DIR / entry["image"]
        if not image_path.is_file():
            raise FileNotFoundError(
                f"videos.json references '{entry['image']}', "
                f"but no such file exists in {VIDEOS_DIR}/"
            )
    return entries


def sort_key(item):
    # Compare as real, timezone-aware datetimes instead of raw strings —
    # string comparison breaks as soon as two dates use different UTC
    # offsets (e.g. a git commit at "+00:00" vs. a manual video date at
    # "+02:00"), even though one is chronologically clearly the other.
    date_str = item["date"]
    if not date_str:
        return datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)
    return datetime.datetime.fromisoformat(date_str)


def main():
    items = load_photos() + load_videos()
    items.sort(key=sort_key, reverse=True)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(items, indent=2))

    photo_count = sum(1 for i in items if i["type"] == "photo")
    video_count = sum(1 for i in items if i["type"] == "video")
    print(f"gallery manifest: {photo_count} photo(s), {video_count} video(s)")


if __name__ == "__main__":
    main()
