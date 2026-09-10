#!/usr/bin/env python3
"""Generate the root sitemap index for docs.saltproject.io.

Globs the expected child sitemap.xml files under a docs-saltproject-io/
tree, skips any that are missing (they self-heal once the corresponding
release exists), and writes a <sitemapindex> whose <lastmod> per child is
the max <lastmod> found inside that child.

/en/3008/sitemap.xml is deliberately excluded: it is a duplicate of
/en/latest/, which is disallowed in robots.txt in favor of the durable
/en/latest/ URL, so it is kept out of the sitemap index too.
"""
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
BASE_URL = "https://docs.saltproject.io"

CHILDREN = [
    "salt/user-guide/en/latest/sitemap.xml",
    "salt/install-guide/en/latest/sitemap.xml",
    "en/latest/sitemap.xml",
    "en/3006/sitemap.xml",
    "en/master/sitemap.xml",
]


def max_lastmod(sitemap_path):
    tree = ET.parse(sitemap_path)
    lastmods = [
        el.text
        for el in tree.getroot().iter(f"{{{SITEMAP_NS}}}lastmod")
        if el.text
    ]
    return max(lastmods) if lastmods else None


def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <docs-saltproject-io-dir>", file=sys.stderr)
        return 1

    root_dir = Path(sys.argv[1])
    ET.register_namespace("", SITEMAP_NS)
    sitemapindex = ET.Element(f"{{{SITEMAP_NS}}}sitemapindex")

    for rel_path in CHILDREN:
        sitemap_path = root_dir / rel_path
        if not sitemap_path.is_file():
            print(f"NOTICE: skipping missing sitemap {rel_path}")
            continue

        lastmod = max_lastmod(sitemap_path)
        sitemap_el = ET.SubElement(sitemapindex, f"{{{SITEMAP_NS}}}sitemap")
        loc_el = ET.SubElement(sitemap_el, f"{{{SITEMAP_NS}}}loc")
        loc_el.text = f"{BASE_URL}/{rel_path}"
        if lastmod:
            lastmod_el = ET.SubElement(sitemap_el, f"{{{SITEMAP_NS}}}lastmod")
            lastmod_el.text = lastmod

    out_path = root_dir / "sitemap.xml"
    ET.ElementTree(sitemapindex).write(
        out_path, encoding="UTF-8", xml_declaration=True
    )
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
