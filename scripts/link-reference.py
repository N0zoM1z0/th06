#!/usr/bin/env python3
"""Link the privately compiled reference without using original target bytes."""
import argparse,json,sys,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import importlib.util
spec=importlib.util.spec_from_file_location('build_reference',Path(__file__).with_name('build-reference.py'))
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
ROOT=b.ROOT
parser=argparse.ArgumentParser();parser.add_argument('--build-dir',type=Path,default=ROOT/'build/upstream');args=parser.parse_args()
out=args.build_dir.resolve();receipt=json.loads((out/'build-receipt.json').read_text())
objs=[ROOT/r['object'] for r in receipt['commands']]
libs='dinput8.lib dsound.lib d3d8.lib d3dx8.lib winmm.lib dxguid.lib kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib odbc32.lib odbccp32.lib'.split()
args=[ROOT/'.tools/msvc700/Vc7/bin/link.exe','/nologo','/subsystem:windows','/machine:X86','/opt:win98','/incremental:no','/opt:ref','/opt:icf','/map:'+b.win(out/'th06.map'),'/mapinfo:exports','/mapinfo:lines','/out:'+b.win(out/'th06.exe'),*map(b.win,objs),*libs]
b.run(args,ROOT,out/'link.log',b.environment())
(out/'link-receipt.json').write_text(json.dumps({'command':list(map(str,args)),'objects':[{k:r[k] for k in ['object','object_sha256']} for r in receipt['commands']],'output_sha256':hashlib.sha256((out/'th06.exe').read_bytes()).hexdigest(),'map_sha256':hashlib.sha256((out/'th06.map').read_bytes()).hexdigest(),'linker_sha256':hashlib.sha256(Path(args[0]).read_bytes()).hexdigest()},indent=2)+'\n')
print(out/'th06.exe')
