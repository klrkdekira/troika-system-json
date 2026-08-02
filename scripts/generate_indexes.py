#!/usr/bin/env python3
"""Regenerate the index.html pages under objects/ from the files on disk.

Run from anywhere: python3 scripts/generate_indexes.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OBJECTS = ROOT / "objects"
SYSTEMS = ROOT / "systems"


def generate_bundled_data():
    master_file = OBJECTS / "troika-system-data.json"
    with open(master_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    categories = [
        "backgrounds",
        "skills",
        "spells",
        "items",
        "enemies",
        "tables",
        "characters",
    ]
    for cat in categories:
        if cat in data and isinstance(data[cat], list):
            new_items = []
            for item in data[cat]:
                if isinstance(item, dict) and "$ref" in item:
                    ref_str = item["$ref"].removeprefix("./")
                    ref_path = OBJECTS / ref_str
                    with open(ref_path, "r", encoding="utf-8") as rf:
                        new_items.append(json.load(rf))
                else:
                    new_items.append(item)
            data[cat] = new_items

    bundled_file = OBJECTS / "troika-system-data.bundled.json"
    with open(bundled_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("wrote objects/troika-system-data.bundled.json")


STYLE = """\
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
          sans-serif;
        line-height: 1.6;
        color: #333;
        background: #f8f9fa;
        padding: 2rem 1rem;
      }

      .container {
        max-width: 720px;
        margin: 0 auto;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        padding: 2.5rem;
      }

      .breadcrumb {
        margin-bottom: 1rem;
        font-size: 0.9rem;
        color: #6c757d;
      }

      h1 {
        color: #2c3e50;
        margin-bottom: 0.25rem;
        font-size: 1.75rem;
      }

      .subtitle {
        color: #6c757d;
        margin-bottom: 2rem;
      }

      code {
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 0.9em;
      }

      a {
        color: #007bff;
        text-decoration: none;
      }

      a:hover {
        text-decoration: underline;
      }

      a code {
        color: #6f42c1;
      }

      .file-list {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        column-gap: 2rem;
      }

      .file-list a {
        display: block;
        padding: 0.35rem 0.25rem;
        border-bottom: 1px solid #e9ecef;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .file-list a:hover {
        background: #f8f9fa;
        text-decoration: none;
      }

      .table-wrap {
        overflow-x: auto;
      }

      table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.95rem;
      }

      th {
        text-align: left;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #6c757d;
        font-weight: 600;
        padding: 0.5rem 0.75rem;
        border-bottom: 2px solid #dee2e6;
      }

      td {
        padding: 0.6rem 0.75rem;
        border-bottom: 1px solid #e9ecef;
        white-space: nowrap;
      }

      tbody tr:hover {
        background: #f8f9fa;
      }

      td.count,
      th.count {
        text-align: right;
        color: #6c757d;
        font-variant-numeric: tabular-nums;
      }

      .muted {
        color: #adb5bd;
      }

      .subtitle a {
        color: inherit;
        text-decoration: underline;
      }

      footer {
        margin-top: 2.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e9ecef;
        display: flex;
        align-items: center;
        gap: 1.25rem;
      }

      footer img {
        width: 64px;
        height: 64px;
        flex-shrink: 0;
      }

      footer p {
        font-size: 0.85rem;
        color: #6c757d;
      }

      @media (max-width: 480px) {
        .container {
          padding: 1.5rem;
        }

        footer {
          flex-direction: column;
          text-align: center;
        }
      }"""

PAGE = """\
<!DOCTYPE html>
<html lang="en-GB">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="icon" href="{favicon}" type="image/svg+xml" />
    <title>{title}</title>
    <style>
{style}
    </style>
  </head>
  <body>
    <div class="container">
{header}
      <h1>{heading}</h1>
      <p class="subtitle">{subtitle}</p>

{body}{footer}
    </div>
  </body>
</html>
"""

FOOTER = """


      <footer>
        <img src="{fortle}" alt="Fortle Logo" />
        <p>
          Troika! System JSON is an independent production by
          <a href="https://cheeleong.dev">Chee Leong</a> and is not affiliated
          with the Melsonian Arts Council. It is published under the terms of
          the
          <a href="https://troika-srd.netlify.app/"
            >Troika! System Reference Document (SRD)</a
          >
          (source repository:
          <a href="https://github.com/dialectrical/troika-srd"
            >dialectrical/troika-srd</a
          >). "Troika!" is a trademark of the Melsonian Arts Council; please
          support the original creators by buying the official rulebook.
        </p>
      </footer>"""

# heading, subtitle ({n} is the live file count) and schema per data directory
SECTIONS = {
    "backgrounds": (
        "Backgrounds",
        "{n} character backgrounds, rolled on a d66",
        "background.schema.json",
    ),
    "characters": (
        "Characters",
        "{n} sample player characters",
        "character.schema.json",
    ),
    "enemies": ("Enemies", "{n} bestiary entries", "enemy.schema.json"),
    "items": ("Items", "{n} pieces of equipment", "item.schema.json"),
    "skills": ("Skills", "{n} advanced skills", "skill.schema.json"),
    "spells": ("Spells", "{n} spells", "spell.schema.json"),
    "tables": ("Tables", "{n} random tables", "table.schema.json"),
}


def breadcrumb(html):
    return f'      <div class="breadcrumb">{html}</div>'


def data_files(directory):
    return sorted(p.name for p in directory.glob("*.json"))


def listing_page(name, heading, subtitle_tpl):
    files = data_files(OBJECTS / name)
    subtitle = subtitle_tpl.format(n=len(files))
    links = "\n".join(f'        <a href="{f}"><code>{f}</code></a>' for f in files)
    body = f'      <div class="file-list">\n{links}\n      </div>'
    return PAGE.format(
        title=f"Troika! {heading}",
        style=STYLE,
        favicon="../../favicon.svg",
        header=breadcrumb(
            f'<a href="../../">Home</a> / <a href="../">objects</a> / {name}'
        ),
        heading=heading,
        subtitle=subtitle,
        body=body,
        footer="",
    )


def table(header_cells, rows):
    head = "\n".join(f"              {cell}" for cell in header_cells)
    row_html = "\n".join(
        "            <tr>\n"
        + "\n".join(f"              {cell}" for cell in cells)
        + "\n            </tr>"
        for cells in rows
    )
    return f"""\
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
{head}
            </tr>
          </thead>
          <tbody>
{row_html}
          </tbody>
        </table>
      </div>"""


def system_files(directory):
    return sorted(
        p.name for p in directory.glob("*") if p.is_file() and p.name != "index.html"
    )


def systems_page():
    files = system_files(SYSTEMS)
    links = "\n".join(f'        <a href="{f}"><code>{f}</code></a>' for f in files)
    body = f'      <div class="file-list">\n{links}\n      </div>'
    return PAGE.format(
        title="Troika! Schemas & Context",
        style=STYLE,
        favicon="../favicon.svg",
        header=breadcrumb('<a href="../">Home</a> / systems'),
        heading="Schemas & Context",
        subtitle=f"{len(files)} JSON schemas and JSON-LD context file for validation and semantic representation",
        body=body,
        footer="",
    )


def objects_page():
    rows = [
        [
            (
                '<td><a href="troika-system-data.json">'
                "<code>troika-system-data.json</code></a></td>"
            ),
            '<td class="count">1</td>',
        ],
        [
            (
                '<td><a href="troika-system-data.bundled.json">'
                "<code>troika-system-data.bundled.json</code></a></td>"
            ),
            '<td class="count">1</td>',
        ],
    ]
    for name in SECTIONS:
        count = len(data_files(OBJECTS / name))
        rows.append(
            [
                f'<td><a href="{name}/"><code>{name}/</code></a></td>',
                f'<td class="count">{count}</td>',
            ]
        )
    body = table(["<th>Data</th>", '<th class="count">Files</th>'], rows)
    return PAGE.format(
        title="Troika! Data Objects",
        style=STYLE,
        favicon="../favicon.svg",
        header=breadcrumb('<a href="../">Home</a> / objects'),
        heading="Data Objects",
        subtitle="JSON data files for the Troika! tabletop RPG",
        body=body,
        footer="",
    )


def root_page():
    def schema_cell(schema):
        return f'<td><a href="systems/{schema}"><code>{schema}</code></a></td>'

    rows = [
        [
            (
                '<td><a href="objects/troika-system-data.json">'
                "<code>troika-system-data.json</code></a></td>"
            ),
            '<td class="count">1</td>',
            schema_cell("troika-system.schema.json"),
        ],
        [
            (
                '<td><a href="objects/troika-system-data.bundled.json">'
                "<code>troika-system-data.bundled.json</code></a></td>"
            ),
            '<td class="count">1</td>',
            schema_cell("troika-system.schema.json"),
        ],
    ]
    for name, (_, _, schema) in SECTIONS.items():
        count = len(data_files(OBJECTS / name))
        rows.append(
            [
                f'<td><a href="objects/{name}/"><code>{name}/</code></a></td>',
                f'<td class="count">{count}</td>',
                schema_cell(schema),
            ]
        )
    rows.append(
        [
            '<td><a href="systems/"><code>systems/</code></a></td>',
            f'<td class="count">{len(system_files(SYSTEMS))}</td>',
            '<td><a href="systems/context.jsonld"><code>context.jsonld</code></a></td>',
        ]
    )
    body = table(
        ["<th>Data</th>", '<th class="count">Files</th>', "<th>Schema / Spec</th>"],
        rows,
    )
    subtitle = (
        "JSON data for the Troika! tabletop RPG, with schemas to validate\n"
        "        against. Source on\n"
        '        <a href="https://github.com/klrkdekira/troika-system-json"'
        ">GitHub</a>."
    )
    return PAGE.format(
        title="Troika! System JSON",
        style=STYLE,
        favicon="favicon.svg",
        header="",
        heading="Troika! System JSON",
        subtitle=subtitle,
        body=body,
        footer=FOOTER.format(fortle="fortle.svg"),
    )


def sync_root_context():
    context_src = SYSTEMS / "context.jsonld"
    context_dst = ROOT / "context.jsonld"
    if context_src.exists():
        context_dst.write_bytes(context_src.read_bytes())
        print("synced context.jsonld to root")


def main():
    generate_bundled_data()
    sync_root_context()
    (ROOT / "index.html").write_text(root_page())
    print("wrote index.html")
    (OBJECTS / "index.html").write_text(objects_page())
    print("wrote objects/index.html")
    (SYSTEMS / "index.html").write_text(systems_page())
    print("wrote systems/index.html")
    for name, (heading, subtitle_tpl, _) in SECTIONS.items():
        page = listing_page(name, heading, subtitle_tpl)
        (OBJECTS / name / "index.html").write_text(page)
        print(f"wrote objects/{name}/index.html")



if __name__ == "__main__":
    main()
