from pathlib import Path
import concurrent.futures, hashlib, json, time, urllib.request,tarfile
P=Path(__file__).resolve().parent
E=json.loads((P/'sources/event.json').read_text())['events']['GW170817-v3']
items=[(P/'data'/f"{x['detector']}_GW170817_32s.hdf5",x['url']) for x in E['strain'] if x['duration']==32 and x['format']=='hdf5' and x['sampling_rate']==4096]
items += [(P/'sources'/'GWTC1_GW170817_CalEnv.tar.gz','https://dcc.ligo.org/public/0158/P1900040/001/GWTC1_GW170817_CalEnv.tar.gz'),(P/'sources'/'calibration_README.txt','https://dcc.ligo.org/public/0158/P1900040/001/README.txt'),(P/'sources'/'LALDetectors.h','https://raw.githubusercontent.com/lscsoft/lalsuite/master/lal/lib/tools/LALDetectors.h'),(P/'sources'/'nullpol_README.md','https://raw.githubusercontent.com/isaac-cf-wong/nullpol/main/README.md'),(P/'sources'/'Pang2020.html','https://arxiv.org/html/2003.07375'),(P/'sources'/'Cheung2025.html','https://arxiv.org/html/2507.02335v1'),(P/'sources'/'Wong2025.html','https://arxiv.org/html/2510.06327v1')]
def get(item):
    path,url=item;t=time.perf_counter()
    try:
        with urllib.request.urlopen(url,timeout=40) as r: b=r.read();status=r.status;final=r.url
        path.write_bytes(b)
        return dict(file=str(path.relative_to(P)),url=url,final_url=final,status=status,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),wall_s=time.perf_counter()-t)
    except Exception as e: return dict(file=str(path.relative_to(P)),url=url,error=repr(e),wall_s=time.perf_counter()-t)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex: records=list(ex.map(get,items))
(P/'ACQUISITION_RECEIPT_v2.json').write_text(json.dumps(records,indent=2))
print(json.dumps(records,indent=2))
tar=P/'sources/GWTC1_GW170817_CalEnv.tar.gz'
if tar.exists():
    with tarfile.open(tar) as t: t.extractall(P/'data/calibration',filter='data')
