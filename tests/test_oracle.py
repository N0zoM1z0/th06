"""Negative controls for the acceptance boundary, using synthetic owned bytes only."""
import hashlib
import importlib.util
import struct
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
spec=importlib.util.spec_from_file_location('comparison',ROOT/'scripts/compare-coff-function.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def coff(code,relocs):
    # One code section and one function with an authoritative auxiliary extent.
    ptr=60+len(code)+10*len(relocs)
    header=struct.pack('<HHIIIHH',0x14c,1,0,ptr,3,0,0)
    section=struct.pack('<8sIIIIIIHHI',b'.text',0,0,len(code),60,60+len(code),0,len(relocs),0,0x60000020)
    syms=struct.pack('<8sIhHBB',b'func',0,1,0x20,2,1)
    aux=bytearray(18);struct.pack_into('<I',aux,4,len(code))
    syms+=aux+struct.pack('<8sIhHBB',b'dest',0,0,0,2,0)
    return header+section+code+b''.join(struct.pack('<IIH',o,2,t) for o,t in relocs)+syms+struct.pack('<I',4)

def pe(code):
    d=bytearray(0x400+len(code));d[:2]=b'MZ';struct.pack_into('<I',d,60,0x80);d[0x80:0x84]=b'PE\0\0'
    struct.pack_into('<HH',d,0x84,0x14c,1);struct.pack_into('<H',d,0x94,224)
    struct.pack_into('<H',d,0x98,0x10b);struct.pack_into('<I',d,0x98+28,0x400000)
    struct.pack_into('<8sIIII',d,0x98+224,b'.text',len(code),0x1000,len(code),0x400)
    d[0x400:]=code;return bytes(d)

class OracleTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.saved=m.ROOT,m.TARGET,m.TARGET_MANIFEST,m.UNITS_MANIFEST
        m.ROOT=self.root;m.TARGET=self.root/'target';m.TARGET_MANIFEST=self.root/'target.toml';m.UNITS_MANIFEST=self.root/'units.toml'
        self.code=b'\xb8'+struct.pack('<I',0x401234)+b'\xc3'
        self.target=pe(self.code);m.TARGET.write_bytes(self.target)
        m.TARGET_MANIFEST.write_text(f'[target]\nsize={len(self.target)}\nsha256="{hashlib.sha256(self.target).hexdigest()}"\n')
        (self.root/'unit.obj').write_bytes(coff(b'\xb8\0\0\0\0\xc3',[(1,6)]))
        self.manifest='[units.unit]\nobject="unit.obj"\nsymbol="func"\ntarget_address=0x401000\nsize=6\nrelocations=[{offset=1,type="DIR32",symbol="dest",target=0x401234}]\n'
        m.UNITS_MANIFEST.write_text(self.manifest)
    def tearDown(self):
        m.ROOT,m.TARGET,m.TARGET_MANIFEST,m.UNITS_MANIFEST=self.saved;self.temp.cleanup()
    def test_complete_relocation_replay(self):self.assertEqual(m.compare_unit('unit')['result'],'exact')
    def test_wrong_relocation_destination_fails(self):
        m.UNITS_MANIFEST.write_text(self.manifest.replace('target=0x401234','target=0x401235'))
        self.assertEqual(m.compare_unit('unit')['result'],'mismatch')
    def test_missing_relocation_inventory_fails(self):
        m.UNITS_MANIFEST.write_text(self.manifest.split('relocations=')[0])
        with self.assertRaises(ValueError):m.compare_unit('unit')
    def test_wrong_symbol_identity_fails(self):
        m.UNITS_MANIFEST.write_text(self.manifest.replace('symbol="dest"','symbol="other"'))
        with self.assertRaises(ValueError):m.compare_unit('unit')
    def test_nonrelocation_byte_change_fails(self):
        (self.root/'unit.obj').write_bytes(coff(b'\xb9\0\0\0\0\xc3',[(1,6)]))
        self.assertEqual(m.compare_unit('unit')['result'],'mismatch')
    def test_target_tampering_fails(self):
        m.TARGET.write_bytes(self.target[:-1]+b'\x90')
        with self.assertRaises(ValueError):m.compare_unit('unit')
    def test_truncated_extent_fails(self):
        m.UNITS_MANIFEST.write_text(self.manifest.replace('size=6','size=5'))
        with self.assertRaises(ValueError):m.compare_unit('unit')
    def test_diagnostic_structural_is_separate(self):
        self.assertEqual(m.compare(self.root/'unit.obj','func',0x401000,6)['result'],'structural-exact')
    def test_overlap_deduplication(self):
        spec=importlib.util.spec_from_file_location('baseline',ROOT/'scripts/reference-baseline.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
        self.assertEqual(b.union_size([(10,20),(15,25),(25,30)]),20)

if __name__=='__main__':unittest.main()
