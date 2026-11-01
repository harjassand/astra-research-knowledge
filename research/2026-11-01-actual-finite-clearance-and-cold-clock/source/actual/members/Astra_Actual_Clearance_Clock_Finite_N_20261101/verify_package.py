#!/usr/bin/env python3
"""Scoped read-only payload/source checks and ordinary numerical receiver replay."""
from pathlib import Path
import hashlib,json,subprocess,sys,os
ROOT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def bindings(name):
 obj=json.loads((ROOT/name).read_text())
 for row in obj['files']:
  p=ROOT/row['path'];assert p.is_file(),row['path']
  assert sha(p)==row['sha256'],row['path']
  if 'bytes' in row:assert p.stat().st_size==row['bytes'],row['path']
 return len(obj['files'])
n=bindings('PACKAGE_MANIFEST.json');sources=bindings('SOURCE_ALLOWLIST.json')
receipt=ROOT/'boundary_clearance_kernel_root_20261101/audit_two_fixture_numerical_join_20261101/REVIEW_RECEIPT.json'
assert sha(receipt)=='991199e59638196c866cbe93748391642998fe1f5b4951ed9f43457ee2e89ef0'
assert json.loads(receipt.read_text())['status']=='PASS_SOURCE_BOUND_TWO_FIXTURE_ACTUAL_CLEARANCE_INTERVALS'
p=ROOT/'boundary_clearance_kernel_root_20261101/finite_window_consumer'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
run=lambda args:subprocess.run([sys.executable,str(p/'admit.py'),*args],capture_output=True,env=env)
a=run([]);assert a.returncode==0,a.stderr.decode();assert a.stdout==(p/'ADMITTED_WINDOWS.json').read_bytes()
for t in ['10000','100000']:
 r=run(['--T',t]);assert r.returncode==0,r.stderr.decode()
 z=json.loads(r.stdout);assert len(z['fixtures'])==1 and z['fixtures'][0]['T']==t
r=run(['--T','10001']);assert r.returncode==2
print(json.dumps({'status':'PASS_FROZEN_PACKAGE_AND_ORDINARY_RECEIVER','payloads':n,'exact_scientific_sources':sources,'runtime_sources':json.loads(a.stdout)['source_files_verified'],'accepted_cli_replays':3,'unsupported_fixture_refused':True,'fresh_scalar_acquisition':False},indent=2))
