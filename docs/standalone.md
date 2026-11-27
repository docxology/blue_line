# Render the Blue Line manuscript

Blue Line runs with zero sibling line projects. Its Python runtime uses the standard library. The PDF and HTML build uses a separate pinned Template checkout. [Template source](https://github.com/docxology/template/tree/87704feae0a4490ef7dad9c931d268e8c30273c2)

Install uv, Pandoc, XeLaTeX and the `rsvg-convert` executable. Use `librsvg2-bin` on Debian or Ubuntu and `librsvg` on macOS. Template lists its LaTeX and optional render tools. [Template run guide](https://github.com/docxology/template/blob/87704feae0a4490ef7dad9c931d268e8c30273c2/docs/RUN_GUIDE.md)

Run from a clean Blue Line checkout in a directory named `blue_line`.

```sh
blue_project="$(pwd -P)"
uv sync --locked
uv run --locked python scripts/gen_formalism_ledger.py
uv run --locked python scripts/build_figures.py

git clone https://github.com/docxology/template.git ../blue-line-template
git -C ../blue-line-template checkout --detach 87704feae0a4490ef7dad9c931d268e8c30273c2
cd ../blue-line-template
blue_template="$(pwd -P)"
uv sync --locked --no-dev
mkdir -p projects/working
ln -s "$blue_project" projects/working/blue_line
uv run --no-sync python "$blue_project/scripts/render_manuscript.py" \
  --template-root "$blue_template" --prepare-only
uv run --no-sync python scripts/pipeline/stage_03_render.py \
  --project working/blue_line --skip-manuscript-hydration
uv run --no-sync python scripts/pipeline/stage_04_validate.py \
  --project working/blue_line
```

The numbered sections, bibliography and publication metadata live in [`docs/manuscript/`](manuscript/README.md). Preparation writes the hydrated copy to `output/manuscript/` beside the generated figures.

Read `output/pdf/blue_line_combined.pdf` and `output/web/index.html` in the Blue Line checkout. Confirm the registry map, verdict paths, freshness diagram and bibliography. The validation and provenance reports are in `output/reports/`. Use the [development guide](development.md) to verify the source and build a distribution bundle.

[Documentation index](README.md)
