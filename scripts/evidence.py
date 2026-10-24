"""Fail-closed provenance checks for locally reproduced matching artifacts."""
import hashlib,json,tomllib
from pathlib import Path

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def check_build(root,unit,linked=False):
    root=Path(root)
    if 'build_receipt' not in unit:return  # Synthetic/legacy diagnostic units.
    receipt=json.loads((root/unit['build_receipt']).read_text())
    lock=tomllib.loads((root/'config/tools.lock.toml').read_text())
    if receipt['compiler_sha256']!=lock['msvc70']['compiler_sha256']:raise ValueError('compiler receipt is not pinned VC7.0')
    recorded={r['path']:r['sha256'] for r in receipt['source_tree']}
    current={str(p.relative_to(root)):digest(p) for p in sorted((root/'src').rglob('*')) if p.is_file()}
    if current!=recorded:raise ValueError('maintained source tree differs from compiler receipt')
    command=next((r for r in receipt['commands'] if r['object']==unit['object']),None)
    if command is None or digest(root/unit['object'])!=command['object_sha256']:raise ValueError('unit object differs from compiler receipt')
    compiler=Path(command['command'][0])
    if digest(compiler)!=receipt['compiler_sha256'] or digest(compiler.parent/'c1xx.dll')!=receipt['frontend_sha256']:raise ValueError('compiler/frontend changed after build')
    if linked:
        link=json.loads((root/unit['link_receipt']).read_text())
        if digest(root/unit['image'])!=link['output_sha256']:raise ValueError('linked image differs from receipt')
        if digest(root/unit['map'])!=link['map_sha256']:raise ValueError('linker map differs from receipt')
        if link['linker_sha256']!=lock['msvc70']['linker_sha256'] or digest(Path(link['command'][0]))!=link['linker_sha256']:raise ValueError('linker is not the pinned executable')
        built={r['object']:r['object_sha256'] for r in receipt['commands']}
        for item in link['objects']:
            if item['object_sha256']!=built.get(item['object']) or digest(root/item['object'])!=item['object_sha256']:raise ValueError('linked object graph changed after link')
    return receipt
