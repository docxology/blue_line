from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from blue_line.publication import check_publication_main

if __name__ == "__main__":
    raise SystemExit(check_publication_main(Path(__file__).resolve().parents[1]))
