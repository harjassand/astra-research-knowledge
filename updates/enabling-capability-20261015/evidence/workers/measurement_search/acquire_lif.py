from pathlib import Path
import json, urllib.request, hashlib, time, datetime
ROOT=Path(__file__).resolve().parent
u='https://zenodo.org/api/records/14783448'
t0=time.perf_counter()
raw=urllib.request.urlopen(u,timeout=30).read()
d=json.loads(raw)
(ROOT/'sources'/'zenodo_14783448_metadata.json').write_bytes(raw)
wanted={'LiF_Polarization_Meas.py','LiF_Stabilized_meas.py','LiF_Static_XUV.py','transient_LiF_nirlinpol_run6_scan_000_2024_05_07_16_29_09.hdf5','LiFChop12_stabilized_adprun0_gas_scan_000_2024_05_16_15_14_23.hdf5','static_LiF_2023_11_07_14_55_18.hdf5','DeltaOD_starkshift.npy','DeltaOD_fullmodel.npy','DeltaOD_lowerdark.npy','DeltaOD_upperdark.npy','w.npy','tau.npy'}
receipt=[]
for f in d['files']:
 if f['key'] not in wanted: continue
 p=ROOT/'data'/f['key']
 s=time.perf_counter()
 b=urllib.request.urlopen(f['links']['self'],timeout=45).read()
 p.write_bytes(b)
 md5=hashlib.md5(b).hexdigest()
 item={'key':f['key'],'source':f['links']['self'],'bytes':len(b),'reported_bytes':f['size'],'md5':md5,'expected_checksum':f['checksum'],'checksum_matches':f['checksum']=='md5:'+md5,'sha256':hashlib.sha256(b).hexdigest(),'elapsed_seconds_measured':time.perf_counter()-s}
 receipt.append(item)
 print(json.dumps(item),flush=True)
 assert item['checksum_matches']
report={'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':u,'files':receipt,'total_downloaded_bytes':sum(x['bytes'] for x in receipt),'acquisition_elapsed_seconds_measured':time.perf_counter()-t0,'model_token_usage':'UNAVAILABLE','model_inference_time':'UNAVAILABLE','hardware_energy':'UNAVAILABLE'}
(ROOT/'DATA_ACQUISITION_RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n')
