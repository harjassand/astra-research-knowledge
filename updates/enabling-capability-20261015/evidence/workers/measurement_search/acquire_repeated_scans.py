from pathlib import Path
import json,urllib.request,hashlib,time,datetime,concurrent.futures
ROOT=Path(__file__).resolve().parent
meta=json.loads((ROOT/'sources'/'zenodo_14783448_metadata.json').read_text())
files=[f for f in meta['files'] if f['key'].startswith('transient_LiF_nirlinpol_run6_') and not (ROOT/'data'/f['key']).exists()]
def acquire(f):
 start=time.perf_counter();url=f['links']['self']
 with urllib.request.urlopen(url,timeout=90) as response:b=response.read()
 md5=hashlib.md5(b).hexdigest();assert f['checksum']=='md5:'+md5
 (ROOT/'data'/f['key']).write_bytes(b)
 return {'key':f['key'],'url':url,'bytes':len(b),'expected_checksum':f['checksum'],'md5':md5,'sha256':hashlib.sha256(b).hexdigest(),'checksum_matches':True,'elapsed_seconds_measured':time.perf_counter()-start}
s=time.perf_counter();receipts=[];errors=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for future in concurrent.futures.as_completed({pool.submit(acquire,f):f for f in files}):
  try:
   receipt=future.result();receipts.append(receipt);print(json.dumps(receipt),flush=True)
  except Exception as error:
   errors.append({'error_type':type(error).__name__,'message':str(error)});print(json.dumps(errors[-1]),flush=True)
report={'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':'https://zenodo.org/records/14783448','purpose':'Same-session repeated scans for calibration-training versus held-out-scan sensitivity; not new specimens.','files':receipts,'errors':errors,'total_new_bytes':sum(r['bytes'] for r in receipts),'parallel_download_slots':3,'elapsed_wall_seconds_measured':time.perf_counter()-s,'cost_telemetry':'Only observed data bytes and wall time; model/instrument/energy costs unavailable.'}
(ROOT/'REPEATED_SCAN_ACQUISITION_RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n')
