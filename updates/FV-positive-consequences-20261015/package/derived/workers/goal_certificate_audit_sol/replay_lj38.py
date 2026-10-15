#!/usr/bin/env python3
"""Replay the saved witness after reloading source-decimal coefficient bands.

This audits ingress and reproducibility of the proof-backed verifier. It is not
an independent full rational solve of the 71,887-state network or an external
validation of the model. Only this worker's replay receipt is written.
"""
import hashlib
import json
from pathlib import Path
import sys
import time
sys.dont_write_bytecode=True
import repair_checks as repair

BASE=Path(__file__).resolve().parent
R=BASE.parents[1]
AUTHOR=R/'workers/directional_lifetime_genesis_sol'
DATA=R/'workers/lj38_acquisition_luna/full-network'
mod=repair.mod
np=mod.np

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    begun=time.perf_counter()
    witness_path=AUTHOR/'lj38_T02_1_to_7_witness.npz'
    published_path=AUTHOR/'lj38_T02_1_to_7_repaired_certified.json'
    published=json.loads(published_path.read_text())
    g,receipt=mod.load_lj38(DATA,'0.2',True,80,1,7)
    with np.load(witness_path) as witness:
        assert int(witness['n'])==g.n
        assert int(witness['source'])==g.s and int(witness['target'])==g.t
        for name in ['u','v','c','w']:
            assert np.array_equal(witness[name],getattr(g,name)),name
        cert=mod.interval_certificate(g,witness['x'],witness['y'],witness['tree'],80)
    target=published['adaptive']['certificate']
    compared=[key for key in cert if key not in ['certificate_seconds']]
    for key in compared: assert cert[key]==target[key],(key,cert[key],target[key])
    htst=mod.htst_time_interval(cert,80)
    assert htst==published['adaptive']['htst_time_interval']
    result={'status':'REPRODUCED_SOURCE_DECIMAL_BANDS_AND_SAVED_WITNESS',
            'verifier_sha256':sha(BASE/'snapshots/repaired_terminal_mass_certificate.py'),
            'witness_sha256':sha(witness_path),'published_result_sha256':sha(published_path),
            'input':receipt,'replayed_certificate':cert,'htst_time_interval':htst,
            'matched_numerical_fields':compared,'wall_seconds':time.perf_counter()-begun,
            'scope':'Source-decimal input bands and arbitrary-potential verifier replay; not independent full rational solve or physical rate uncertainty certification'}
    (BASE/'lj38_replay.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'states':g.n,'edges':len(g.c),
                      'lower':cert['lower'],'upper':cert['upper'],
                      'relative_width':cert['relative_width'],'wall_seconds':result['wall_seconds']},indent=2))

if __name__=='__main__': main()
