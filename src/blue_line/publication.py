"""Local publication checks and artifact packaging; no DOI reservation."""

from __future__ import annotations

import json
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from .version import __version__


def publication_checks(repo: Path) -> tuple[tuple[str, bool, str], ...]:
    results: list[tuple[str, bool, str]] = []
    for filename, pattern in (
        ("pyproject.toml", r'^version = "([^"]+)"$'),
        ("CITATION.cff", r"^version: (\S+)$"),
        ("docs/manuscript/config.yaml", r'^  version: "([^"]+)"$'),
        ("docs/manuscript/references.bib", r"note = \{Version ([^; }]+)"),
    ):
        text = (repo / filename).read_text(encoding="utf-8")
        match = re.search(pattern, text, re.MULTILINE)
        results.append((filename, match is not None and match[1] == __version__, "version consistency"))
    zenodo = json.loads((repo / ".zenodo.json").read_text(encoding="utf-8"))
    results.append((".zenodo.json", zenodo.get("version") == __version__, "version consistency"))
    cff = (repo / "CITATION.cff").read_text(encoding="utf-8")
    config = (repo / "docs/manuscript/config.yaml").read_text(encoding="utf-8")
    doi_pattern = r"10\.\d{4,9}/[A-Za-z0-9.]+"
    cff_doi = re.findall(doi_pattern, cff)
    config_doi = re.findall(doi_pattern, config)
    notes_doi = re.findall(doi_pattern, zenodo.get("notes", ""))
    results.append(("retained_doi", len(cff_doi) == 1 and cff_doi == config_doi == notes_doi,
                    "retained previous-version identifier agrees; not a live DOI verification"))
    return tuple(results)


def check_publication_main(repo: Path) -> int:
    results = publication_checks(repo)
    for name, passed, detail in results:
        print(f"{'PASS' if passed else 'FAIL'}  {name}: {detail}")
    return 0 if all(passed for _, passed, _ in results) else 1


def build_manuscript_bundle(repo: Path) -> Path:
    """Bundle the rendered web tree with its local assets, figures and PDF."""
    pdf = repo / "output/pdf/blue_line_combined.pdf"
    web = repo / "output/web"
    for required in (pdf, web / "index.html"):
        if not required.is_file():
            raise FileNotFoundError(required)
    paths = [pdf] + sorted(p for p in web.rglob("*") if p.is_file())
    paths += sorted(p for p in (repo / "output/figures").glob("*") if p.is_file())
    target = repo / "output" / f"blue_line-v{__version__}-manuscript.zip"
    with ZipFile(target, "w") as archive:
        for path in sorted(paths):
            info = ZipInfo(str(path.relative_to(repo)))
            info.compress_type = ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())
    return target
