#!/usr/bin/env python3
"""Portable replay of new calculations only; original owner ZIPs stay untouched."""
import argparse
from decimal import Decimal,localcontext
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from datetime import datetime,timezone
from verify_manifest import verify

ROOT=Path(__file__).resolve().parent


def execute(argv):
    start=time.perf_counter()
    r=subprocess.run([sys.executable,*map(str,argv)],capture_output=True,text=True,check=True)
    return {'arguments':[str(x) for x in argv],'wall_seconds':time.perf_counter()-start,
            'exit_code':r.returncode,'stdout':r.stdout}


def run(receipt):
    started=datetime.now(timezone.utc).isoformat();tick=time.perf_counter()
    integrity=verify(ROOT)
    with tempfile.TemporaryDirectory(prefix='astra_pro3_cycle3_replay_') as tmp:
        t=Path(tmp)
        commands=[]
        commands.append(execute([ROOT/'code/uniform_certificate.py','--dps','80','--output',t/'upper.json']))
        commands.append(execute([ROOT/'code/compare_certificates.py',ROOT/'results/uniform_certificate_80.json',
                                 t/'upper.json','--output',t/'upper_compare.json']))
        commands.append(execute([ROOT/'reviews/vanishing_lower_checks.py','--base-precision','90',
                                 '--output',t/'lower.json','--resources',t/'lower_resources.json']))
        old=json.loads((ROOT/'reviews/vanishing_lower_checks.json').read_text())
        new=json.loads((t/'lower.json').read_text())
        assert len(old['finite_chains'])==len(new['finite_chains'])==16
        with localcontext() as ctx:
            ctx.prec=500
            diffs=[abs(Decimal(a['tv'])-Decimal(b['tv']))
                   for a,b in zip(old['finite_chains'],new['finite_chains'])]
            assert max(diffs)<Decimal('1e-75')
        result={'status':'passed','started_utc':started,
                'finished_utc':datetime.now(timezone.utc).isoformat(),
                'wall_seconds':time.perf_counter()-tick,'integrity':integrity,
                'upper_comparison':json.loads((t/'upper_compare.json').read_text()),
                'lower_full_chain_laws':16,'max_lower_TV_difference':str(max(diffs)),
                'lower_resources':json.loads((t/'lower_resources.json').read_text()),
                'commands':commands,
                'scope':'New finite numerical evidence only; no old scientific replay or proof-by-testing claim.'}
    receipt.parent.mkdir(parents=True,exist_ok=True)
    receipt.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('commands','lower_resources')},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--receipt',type=Path,required=True)
    run(p.parse_args().receipt)
