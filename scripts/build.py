#!/usr/bin/env python3
"""Cold-build and link maintained source with the pinned headless profile."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(ROOT/'scripts/verify-target.py')],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/build-reference.py'),'--source-root',str(ROOT)],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/link-reference.py'),'--build-dir',str(ROOT/'build/authored')],check=True)
