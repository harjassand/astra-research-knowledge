"""Bounded replay of the two supplied P2 scripts; path changes only."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys, time

HERE=Path(__file__).resolve().parent
SOURCE=Path('/Users/harjas/Documents/ChatGPT/coordination/.astra-dispatch/sources/P2_return_1624_20261026/originals')
NAMES=[
 'ASTRA_SPATIOTEMPORAL_RADIATION_ECHO_20261027.md',
 'astra_temporal_dark_inband_certified_20261027.py',
 'astra_temporal_dark_inband_certified_20261027.json',
 'astra_temporal_dark_inband_uniform_certificate_20261027.py',
 'astra_temporal_dark_inband_uniform_certificate_20261027.json',
 'astra_temporal_dark_inband_perturbation_20261027.py',
 'astra_temporal_dark_inband_perturbation_20261027.json',
]


def sha(data):return hashlib.sha256(data).hexdigest()


if __name__=='__main__':
    started=time.perf_counter()
    for d in ['source_copy','runnable_copy','replayed','logs']:(HERE/d).mkdir(exist_ok=True)
    manifest=[]
    for name in NAMES:
        raw=(SOURCE/name).read_bytes()
        shutil.copy2(SOURCE/name,HERE/'source_copy'/name)
        row={'filename':name,'original_sha256_before':sha(raw),'bytes':len(raw)}
        if name.endswith('.py'):
            # Only absolute source/output file destinations change. Parameters,
            # algorithms, tolerances, quadrature and mathematical code are intact.
            modified=raw.replace(b'/mnt/data/',str(HERE/'replayed').encode()+b'/')
            # The perturbation helper is read but deliberately not executed.
            if 'perturbation' in name:
                modified=modified.replace(str(HERE/'replayed'/'astra_temporal_dark_inband_certified_20261027.py').encode(),str(HERE/'runnable_copy'/'astra_temporal_dark_inband_certified_20261027.py').encode())
            (HERE/'runnable_copy'/name).write_bytes(modified)
            row['runnable_copy_sha256']=sha(modified)
            row['change_scope']='literal absolute file paths only; no scientific edits'
        manifest.append(row)
    versions=subprocess.run([sys.executable,'-c','import sys,numpy,scipy,json;print(json.dumps({"python":sys.version,"numpy":numpy.__version__,"scipy":scipy.__version__}))'],capture_output=True,text=True,check=True)
    results=[];env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
    for stem in ['astra_temporal_dark_inband_certified_20261027','astra_temporal_dark_inband_uniform_certificate_20261027']:
        before=time.perf_counter()
        process=subprocess.run([sys.executable,str(HERE/'runnable_copy'/f'{stem}.py')],cwd=HERE/'runnable_copy',env=env,capture_output=True,text=True,timeout=180)
        elapsed=time.perf_counter()-before
        (HERE/'logs'/f'{stem}.stdout.txt').write_text(process.stdout)
        (HERE/'logs'/f'{stem}.stderr.txt').write_text(process.stderr)
        row={'script':stem+'.py','exit_code':process.returncode,'wall_seconds_including_startup_imports_and_serialization':elapsed}
        if process.returncode==0:
            result=json.loads((HERE/'replayed'/f'{stem}.json').read_text())
            saved=json.loads((HERE/'source_copy'/f'{stem}.json').read_text())
            row['replayed_result']=result
            def differences(a,b,path=''):
                out=[]
                if isinstance(a,dict):
                    for k in a:out+=differences(a[k],b[k],path+'.'+k)
                elif isinstance(a,list):
                    for i,(x,y) in enumerate(zip(a,b)):out+=differences(x,y,path+f'[{i}]')
                elif isinstance(a,(int,float)) and isinstance(b,(int,float)):
                    if a!=b:out.append({'field':path,'producer':a,'reviewer':b,'absolute_difference':abs(a-b)})
                elif a!=b:out.append({'field':path,'producer':a,'reviewer':b})
                return out
            row['differences_from_saved']=differences(saved,result)
        results.append(row)
        print(json.dumps(row),flush=True)
        if process.returncode:break
    for row in manifest:
        row['original_sha256_after']=sha((SOURCE/row['filename']).read_bytes())
        row['original_unchanged']=row['original_sha256_before']==row['original_sha256_after']
    receipt={'scope':'Supplied main model and uniform script replay only. Perturbation source/data inspected, not rerun. No parameter/tolerance changes and no new experiments.',
             'runtime':json.loads(versions.stdout),'source_manifest':manifest,'runs':results,
             'total_reviewer_script_seconds':time.perf_counter()-started}
    (HERE/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
