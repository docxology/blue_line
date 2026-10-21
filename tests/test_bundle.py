from zipfile import ZipFile

import pytest

from blue_line.publication import build_manuscript_bundle


def test_bundle_retains_referenced_local_assets_and_bytes(tmp_path):
    members = {
        "output/web/index.html": b'<script src="assets/source-web-fonts.js"></script><link href="favicon.ico">',
        "output/web/assets/source-web-fonts.js": b'font loader',
        "output/web/favicon.ico": b'icon bytes',
        "output/figures/figure.png": b'figure bytes',
        "output/pdf/blue_line_combined.pdf": b'PDF bytes',
    }
    for name, data in members.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    archive = build_manuscript_bundle(tmp_path)
    with ZipFile(archive) as bundle:
        assert bundle.testzip() is None
        assert set(bundle.namelist()) == set(members)
        assert all(bundle.read(name) == value for name, value in members.items())


def test_bundle_rejects_incomplete_render(tmp_path):
    with pytest.raises(FileNotFoundError):
        build_manuscript_bundle(tmp_path)
