#!/usr/bin/env python3
"""Cold-build and link maintained source with the pinned headless profile."""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    # Parse before running any tools: --help must never start a cold build.
    argparse.ArgumentParser(description=__doc__).parse_args()
    subprocess.run([sys.executable, str(ROOT / 'scripts/verify-target.py')], check=True)
    subprocess.run([sys.executable, str(ROOT / 'scripts/build-reference.py'),
                    '--source-root', str(ROOT)], check=True)
    subprocess.run([sys.executable, str(ROOT / 'scripts/link-reference.py'),
                    '--build-dir', str(ROOT / 'build/authored')], check=True)


if __name__ == '__main__':
    main()
