from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from blue_line.publication import build_manuscript_bundle

if __name__ == "__main__":
    print(build_manuscript_bundle(Path(__file__).resolve().parents[1]))
