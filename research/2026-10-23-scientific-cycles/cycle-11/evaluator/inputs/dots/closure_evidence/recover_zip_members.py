"""Bounded range recovery of already published small evidence files; no models/fits."""
import urllib.request,json,pathlib,struct,zlib,hashlib,sys
p=pathlib.Path(__file__).resolve().parent
members=json.loads((p/'monroe_zip_member_list.json').read_text())
url='https://zenodo.org/api/records/12537668/files/HONO_Zenodo.zip/content'
sel=[f for f in members if ('read' in pathlib.Path(f['name']).name.lower() and f['size']<20000) or ('NO2_O2_blanks' in f['name'] and pathlib.Path(f['name']).name.lower() in ['runparameters.csv','intensityinfo.csv','kineticsarray.csv','rate constants.csv'])]
log=[]
for f in sel:
 start=f['header_offset'];end=start+30+f['compressed_size']+2048
 row=dict(member=f['name'],url=url,requested_range=f'bytes={start}-{end}',expected_size=f['size'],expected_crc=f['crc'])
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'Range':row['requested_range']}),timeout=20) as r:
   row.update(status=r.status,content_range=r.headers.get('Content-Range'))
   if r.status!=206 or not r.headers.get('Content-Range','').startswith(f'bytes {start}-'):raise ValueError('Range mismatch; no full archive read')
   b=r.read(end-start+2)
  assert b[:4]==b'PK\x03\x04'
  fields=struct.unpack_from('<4s5H3L2H',b,0);n,ex=fields[-2:];fn=b[30:30+n].decode('utf8');assert fn==f['name'];compressed=b[30+n+ex:30+n+ex+f['compressed_size']]
  raw=zlib.decompress(compressed,-15) if f['compression']==8 else compressed
  assert len(raw)==f['size'];assert zlib.crc32(raw)==f['crc']
  target=p/'monroe_selected'/pathlib.Path(f['name']);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
  row.update(file=str(target.relative_to(p)),sha256=hashlib.sha256(raw).hexdigest(),crc_verified=True)
  print(f['name'],len(raw),flush=True)
 except Exception as e:row['error']=str(e);print('ERROR',f['name'],e,flush=True)
 log.append(row);(p/'monroe_selected_recovery_log.json').write_text(json.dumps(log,indent=2))
