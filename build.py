#!/usr/bin/env python3
"""Build Curbwise into docs/ for GitHub Pages.

Layout:
  config.json                 site settings (haul-away providers live in each data/<city>.json)
  data/<city>.json            official city rules (centers, hours, fees, sources)
  content/<city>/<item>.md    item guides for that city (front matter + Markdown)
  content/<page>.md           site pages (about, disclosures, suggest)

Front matter keys: title, description, path, kind (guide|page), city, item_label,
summary, eyebrow, lede, updated, order.
Jinja helpers inside Markdown: url(path), fee(key) -> dict, fee_text(key),
centers(*keys) -> HTML list, haul_away() -> HTML box, hub_url().
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup, escape

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "docs"


def human_date(value):
    if not value:
        return ""
    if isinstance(value, str):
        value = dt.date.fromisoformat(value[:10])
    return value.strftime("%b %-d, %Y")


def parse_front_matter(text):
    if not text.startswith("---"):
        return {}, text
    _, fm, body = text.split("---", 2)
    meta = {}
    for line in fm.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, body.lstrip("\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-path", default=None)
    ap.add_argument("--site-url", default=None)
    ap.add_argument("--relative", action="store_true")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    global OUT
    if args.out:
        OUT = Path(args.out).resolve()

    site = json.loads((ROOT / "config.json").read_text())
    if args.base_path is not None:
        site["base_path"] = args.base_path
    if args.site_url is not None:
        site["site_url"] = args.site_url
    base = site.get("base_path", "").rstrip("/")

    cities = {}
    for f in sorted((ROOT / "data").glob("*.json")):
        c = json.loads(f.read_text())
        cities[c["slug"]] = c

    current = {"page": "/", "city": None}

    def url(path):
        if not args.relative:
            return f"{base}{path}"
        target, _, frag = path.partition("#")
        if target.endswith("/"):
            target += "index.html"
        page_dir = current["page"] if current["page"].endswith("/") else str(Path(current["page"]).parent) + "/"
        rel = os.path.relpath(target, page_dir)
        return rel + (("#" + frag) if frag else "")

    def canonical(path):
        return f"{site['site_url'].rstrip('/')}{base}{path}"

    env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=select_autoescape(["html"]))
    env.filters["human_date"] = human_date
    build_id = hashlib.sha1(dt.datetime.now().isoformat().encode()).hexdigest()[:8]

    # ---------- Markdown helpers ----------
    def city():
        return cities[current["city"]]

    def fee(key):
        for row in city()["fees"]:
            if row["key"] == key:
                return row
        raise KeyError(f"fee {key} not in {current['city']}")

    def fee_text(key):
        r = fee(key)
        return Markup(f"<strong>{escape(r['fee'])}</strong> at {escape(r['where'])} ({escape(r['limits'])})")

    def centers(*keys):
        rows = [c for c in city()["centers"] if not keys or c["key"] in keys]
        # Inline spans (shown as blocks by CSS) so the list can sit inside a
        # Markdown bullet or paragraph without breaking it.
        spans = "".join(f'<span class="ctr"><strong>{escape(c["name"])}</strong> — {escape(c["address"])}</span>' for c in rows)
        return Markup(f'<span class="ctrs">{spans}</span>')

    def hub_url():
        return url(f"/{current['city']}/")

    def haul_away():
        items = []
        any_aff = False
        providers = city().get("haul_away", [])
        if not providers:
            return Markup("")
        for p in providers:
            rel = "sponsored nofollow noopener" if p.get("affiliate") else "nofollow noopener"
            any_aff = any_aff or p.get("affiliate")
            href = p["url"].replace("{page}", current["page"].strip("/").replace("/", "-") or "home")
            items.append(f'<li><a href="{escape(href)}" rel="{rel}"><strong>{escape(p["name"])}</strong></a> — {escape(p["blurb"])}</li>')
        note = ('<p class="affiliate-note">Some of these are affiliate links: if you book through one, Curbwise may earn a commission '
                f'at no extra cost to you. <a href="{url("/disclosures/")}">Disclosures</a>.</p>') if any_aff else ""
        return Markup('<aside class="haul"><h3>Rather not lift a thing?</h3>'
                      '<p>Paid junk-removal services pick up from inside your home or the curb, and many donate usable items. '
                      'It costs more than dropping it off yourself, but it\'s the fastest option.</p>'
                      f'<ul>{"".join(items)}</ul>{note}</aside>')

    md_globals = dict(site=site, url=url, fee=fee, fee_text=fee_text, centers=centers, haul_away=haul_away, hub_url=hub_url)

    common = dict(site=site, url=url, canonical=canonical, build_id=build_id, cities=cities)

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(ROOT / "static", OUT / "static")
    (OUT / ".nojekyll").write_text("")
    sitemap = []

    def write(path, html):
        target = OUT / path.lstrip("/") / "index.html" if path.endswith("/") else OUT / path.lstrip("/")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html)

    md = markdown.Markdown(extensions=["extra", "sane_lists", "smarty"])

    # ---------- collect item guides per city ----------
    guides = {slug: [] for slug in cities}
    pages = []
    for f in sorted((ROOT / "content").rglob("*.md")):
        meta, body = parse_front_matter(f.read_text())
        meta["_body"] = body
        if meta.get("city"):
            guides[meta["city"]].append(meta)
        else:
            pages.append(meta)
    for slug in guides:
        guides[slug].sort(key=lambda m: int(m.get("order", 99)))

    updated_all = max([c["last_checked"] for c in cities.values()] + [m.get("updated", "2000-01-01") for g in guides.values() for m in g])
    common["updated_human"] = human_date(updated_all)

    # ---------- render guides ----------
    for slug, items in guides.items():
        for meta in items:
            current.update(page=meta["path"], city=slug)
            html_body = md.reset().convert(env.from_string(meta["_body"]).render(**md_globals))
            article = {"@context": "https://schema.org", "@type": "HowTo", "name": meta["title"],
                       "description": meta.get("description", ""), "dateModified": meta.get("updated", updated_all)}
            write(meta["path"], env.get_template("page.html").render(page=meta, body=html_body, city=cities[slug],
                                                                       jsonld=json.dumps(article), **common))
            sitemap.append((meta["path"], meta.get("updated", updated_all)))

    # ---------- city hubs ----------
    for slug, c in cities.items():
        current.update(page=f"/{slug}/", city=slug)
        page = dict(path=f"/{slug}/", title=f"How to get rid of anything in {c['name']}, {c['state']}",
                    description=f"{c['name']} Convenience Centers: locations, hours, fees and rules for mattresses, furniture, appliances, electronics, paint and tires — from official {c['authority']} pages.")
        write(page["path"], env.get_template("city.html").render(page=page, city=c, guides=guides[slug], **common))
        sitemap.append((page["path"], c["last_checked"]))

    # ---------- site pages ----------
    for meta in pages:
        current.update(page=meta["path"], city=next(iter(cities)))
        html_body = md.reset().convert(env.from_string(meta["_body"]).render(**md_globals))
        write(meta["path"], env.get_template("page.html").render(page=meta, body=html_body, city=None, jsonld="", **common))
        sitemap.append((meta["path"], meta.get("updated", updated_all)))

    # ---------- home + 404 ----------
    current.update(page="/", city=next(iter(cities)))
    page = dict(path="/", title=site["site_name"], description=site["description"])
    write("/", env.get_template("home.html").render(page=page, guides=guides, **common))
    sitemap.insert(0, ("/", updated_all))
    page = dict(path="/404.html", title="Page not found", description="This page could not be found.")
    (OUT / "404.html").write_text(env.get_template("404.html").render(page=page, **common))

    urls = "".join(f"<url><loc>{canonical(p)}</loc><lastmod>{d}</lastmod></url>" for p, d in sitemap)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    if site.get("adsense_client"):
        pub = site["adsense_client"].replace("ca-", "")
        (OUT / "ads.txt").write_text(f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {canonical('/sitemap.xml')}\n")
    print(f"Built {len(sitemap)} pages for {len(cities)} city/cities -> {OUT}")


if __name__ == "__main__":
    main()
