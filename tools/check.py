#!/usr/bin/env python3
"""Quality gate for Curbwise. Run after build.py; exits non-zero on problems.

Checks:
- every data/<city>.json has its required keys, https sources, unique fee keys,
  valid haul-away entries and a last_checked date that isn't in the future
- every city guide has a Sources section, and no source URL hides an "@" in its host
- every built HTML page has a <title>, a meta description and exactly one <h1>
- every internal link resolves to a built file
"""
import datetime as dt
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"

problems = []


def check_listings():
    """Validate data/<city>.json files: required keys, sources, dates, fee keys."""
    cities = []
    today = dt.date.today()
    for f in sorted((ROOT / "data").glob("*.json")):
        c = json.loads(f.read_text())
        cities.append(c)
        for k in ["slug", "name", "state", "centers", "hours", "rules", "fees", "sources", "last_checked"]:
            if not c.get(k):
                problems.append(f"{f.name}: missing {k}")
        for s in c.get("sources", []):
            if not str(s.get("url", "")).startswith("https://") or not s.get("title"):
                problems.append(f"{f.name}: every source needs a title and an https url")
        for p in c.get("haul_away", []):
            if not (p.get("name") and p.get("blurb") and str(p.get("url", "")).startswith("https://")
                    and isinstance(p.get("affiliate"), bool)):
                problems.append(f"{f.name}: haul_away entries need name, blurb, https url, affiliate true/false")
        keys = [row.get("key") for row in c.get("fees", [])]
        if len(keys) != len(set(keys)):
            problems.append(f"{f.name}: duplicate fee keys")
        try:
            if dt.date.fromisoformat(c.get("last_checked", "")) > today:
                problems.append(f"{f.name}: last_checked is in the future")
        except ValueError:
            problems.append(f"{f.name}: last_checked must be YYYY-MM-DD")
    for f in sorted((ROOT / "content").rglob("*.md")):
        text = f.read_text()
        if "city:" in text.split("---")[1] and "## Sources" not in text:
            problems.append(f"{f.relative_to(ROOT)}: guide has no Sources section")
        for url in re.findall(r"<(https?://[^>]+)>", text):
            if "@" in url.split("/")[2]:
                problems.append(f"{f.relative_to(ROOT)}: suspicious source URL {url}")
    return cities


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.has_title, self.has_desc, self.h1 = [], False, False, 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "link" and a.get("rel") == "stylesheet":
            self.links.append(a.get("href", ""))
        if tag == "script" and a.get("src"):
            self.links.append(a["src"])
        if tag == "title":
            self.has_title = True
        if tag == "meta" and a.get("name") == "description" and a.get("content"):
            self.has_desc = True
        if tag == "h1":
            self.h1 += 1


def check_site():
    if not OUT.exists():
        problems.append("docs/ not built — run python3 build.py first")
        return
    base = json.loads((ROOT / "config.json").read_text()).get("base_path", "").rstrip("/")
    # The build may have been run with --base-path; detect it from the home page stylesheet link.
    home = (OUT / "index.html").read_text()
    m = re.search(r'href="([^"]*)/static/style\.css', home)
    if m:
        base = m.group(1)
    for page in OUT.rglob("*.html"):
        p = PageParser()
        p.feed(page.read_text())
        rel = page.relative_to(OUT)
        if not p.has_title:
            problems.append(f"{rel}: missing <title>")
        if not p.has_desc:
            problems.append(f"{rel}: missing meta description")
        if p.h1 != 1:
            problems.append(f"{rel}: expected exactly one <h1>, found {p.h1}")
        for href in p.links:
            if href.startswith(("http", "mailto:", "tel:", "#")):
                continue
            path = href.split("#")[0].split("?")[0]
            if base and path.startswith(base):
                path = path[len(base):]
            if not path.startswith("/"):
                problems.append(f"{rel}: relative link {href} (use url())")
                continue
            target = OUT / path.lstrip("/")
            if path.endswith("/"):
                target = target / "index.html"
            if not target.exists():
                problems.append(f"{rel}: broken internal link {href}")


if __name__ == "__main__":
    listings = check_listings()
    check_site()
    if problems:
        print("CHECK FAILED:")
        for x in problems:
            print(" -", x)
        sys.exit(1)
    print(f"CHECK OK: {len(listings)} city file(s), site links and pages look good.")
