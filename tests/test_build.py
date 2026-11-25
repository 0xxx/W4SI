#!/usr/bin/env python3
"""Smoke-check the generated Ametrine site after `zola build`."""
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1] / "public"
ROUTES = {
    "/": "index.html",
    "/blog/": "blog/index.html",
    "/tags/": "tags/index.html",
    "/blog/hello-world/": "blog/hello-world/index.html",
    "/tags/site-notes/": "tags/site-notes/index.html",
    "/about/": "about/index.html",
}

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.meta_control = False
        self.metadata_card = False
        self.toc = False
        self.no_metadata = False
        self.in_h1 = False
        self.in_card = False
        self.card_text = []
        self.text = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if tag == "h1": self.h1 += 1
        if attrs.get("id") == "mode-meta": self.meta_control = True
        if "page-metadata" in classes:
            self.metadata_card = True; self.in_card = True
        if "toc" in classes: self.toc = True
        if tag == "h1": self.in_h1 = True
    def handle_endtag(self, tag):
        if tag == "h1": self.in_h1 = False
        if tag == "div" and self.in_card: self.in_card = False
    def handle_data(self, data):
        self.text.append(data)
        if self.in_card: self.card_text.append(data)

for route, relpath in ROUTES.items():
    path = ROOT / relpath
    assert path.is_file(), f"missing route {route}: {path}"
    parser = Page(); parser.feed(path.read_text())
    assert parser.h1 >= 1, f"{route}: no real h1"
    assert parser.meta_control, f"{route}: metadata control missing"
    full_text = " ".join(parser.text).lower()
    assert "no metadata found" not in full_text, f"{route}: empty metadata message remains"
    if parser.metadata_card:
        assert len(" ".join(parser.card_text).strip()) > 15, f"{route}: metadata card has no useful text"
    else:
        assert parser.toc, f"{route}: neither populated metadata card nor TOC present"
    print(f"OK {route}: h1, metadata control, useful panel")

for xml_path in (ROOT / "sitemap.xml", ROOT / "atom.xml", ROOT / "blog/atom.xml", ROOT / "tags/site-notes/atom.xml"):
    assert xml_path.is_file(), f"missing generated XML: {xml_path.relative_to(ROOT)}"
    ElementTree.parse(xml_path)
    print(f"OK {xml_path.relative_to(ROOT)}: valid XML")
