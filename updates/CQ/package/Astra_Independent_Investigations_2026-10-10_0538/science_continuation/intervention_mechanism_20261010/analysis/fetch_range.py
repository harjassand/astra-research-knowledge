import json,pathlib,subprocess,struct,zlib,hashlib,time,concurrent.futures
ROOT=pathlib.Path(__file__).resolve().parents[1]
FS=json.loads((ROOT/'raw/archive_index.json').read_text())
URL='https://ndownloader.figshare.com/files/27453833'
def fetch(f):
 dest=ROOT/'raw/extracted'/f['name']; dest.parent.mkdir(parents=True,exist_ok=True)
 if dest.exists() and dest.stat().st_size==f['size'] and zlib.crc32(dest.read_bytes())==f['crc']: return str(dest)
 cache=ROOT/'raw/ranges'/f"{f['offset']}_{f['compressed']}.bin"; cache.parent.mkdir(exist_ok=True)
 for attempt in range(4):
  r=subprocess.run(['curl','-sS','-L','--max-time','75','-r',f"{f['offset']}-{f['offset']+f['compressed']+1024}",URL+f'?range_start={f["offset"]}&attempt={attempt}','-o',str(cache)],capture_output=True)
  try:
   data=cache.read_bytes(); head=struct.unpack('<IHHHHHIIIHH',data[:30]); assert head[0]==0x04034b50, data[:100]
   raw=data[30+head[-2]+head[-1]:30+head[-2]+head[-1]+f['compressed']]
   out=zlib.decompress(raw,-15) if f['method']==8 else raw
   assert len(out)==f['size']; assert zlib.crc32(out)==f['crc']
   dest.write_bytes(out)
   info={**f,'download_url':URL,'accessed_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'sha256':hashlib.sha256(out).hexdigest()}
   (cache.with_suffix('.json')).write_text(json.dumps(info,indent=2))
   print('OK',f['name'],len(out),flush=True);return str(dest)
  except Exception as e: print('retry',attempt,f['name'],str(e)[:180],r.stderr.decode()[:100],flush=True)
 raise RuntimeError(f['name'])
if __name__=='__main__':
 import sys
 if sys.argv[1]=='metadata': fs=[f for f in FS if f['name'].endswith('.xlsx')]
 else: fs=[f for f in FS if f['name'] in json.loads(pathlib.Path(sys.argv[1]).read_text())]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(fetch,fs))
