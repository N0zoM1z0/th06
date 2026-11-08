#!/usr/bin/env python3
"""Public validation never requires proprietary targets or downloaded compilers."""
from pathlib import Path
import subprocess,sys,tomllib
ROOT=Path(__file__).resolve().parents[1]
for path in (ROOT/'config').glob('*.toml'):
    with path.open('rb') as f:tomllib.load(f)
for path in (ROOT/'scripts').glob('*.py'):
    compile(path.read_text(),str(path),'exec')
tracked=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
for name in tracked:
    p=Path(name)
    if p.parts[0] in {'.private','.analysis','.tools','_reference','build','ghidra-project'} or p.suffix.lower() in {'.exe','.dll','.obj','.pch','.pdb','.rar','.zip','.7z','.dat','.i64','.idb','.gpr','.lib'}:
        raise SystemExit(f'private/generated artifact tracked: {name}')
subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=ROOT,check=True)
for script,args in [('validate-tracking.py',[]),('progress.py',['--check'])]:
    subprocess.run([sys.executable,str(ROOT/'scripts'/script),*args],cwd=ROOT,check=True)
print('Public source/manifest/artifact checks passed.')
