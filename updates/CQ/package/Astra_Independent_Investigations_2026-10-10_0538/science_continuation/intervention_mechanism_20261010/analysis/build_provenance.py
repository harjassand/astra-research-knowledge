import pathlib,json,hashlib,zlib,struct
R=pathlib.Path(__file__).resolve().parents[1];items=[]
for info in sorted((R/'raw/ranges').glob('*.json')):
 f=json.loads(info.read_text());raw=R/'raw/extracted'/f['name'];b=raw.read_bytes();assert len(b)==f['size'];assert zlib.crc32(b)==f['crc'];assert hashlib.sha256(b).hexdigest()==f['sha256']
 compressed=info.with_suffix('.bin');cb=compressed.read_bytes();h=struct.unpack('<IHHHHHIIIHH',cb[:30]);data_offset=30+h[-2]+h[-1]
 items.append({**f,'source_revision':'10.6084/m9.figshare.14371232.v2','requested_range_start':f['offset'],'requested_range_end_inclusive':f['offset']+f['compressed']+1024,'received_range_bytes':len(cb),'range_sha256':hashlib.sha256(cb).hexdigest(),'deflate_stream_start':f['offset']+data_offset,'deflate_stream_end_inclusive':f['offset']+data_offset+f['compressed']-1,'crc32_verified':True,'uncompressed_sha256_verified':True})
manifest={'source_archive_bytes':4085227742,'source_archive_md5_unverified':'d42879e66142ff7190f256f4276db111','complete_archive_downloaded':False,'entries':items}
(R/'raw/provenance_manifest.json').write_text(json.dumps(manifest,indent=2))
paths=[p for p in R.rglob('*') if p.is_file() and 'python_packages' not in p.parts and 'mplcache' not in p.parts and p.name!='SHA256SUMS.txt']
(R/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(R))+'\n' for p in sorted(paths)))
print('Verified entries:',len(items),'traces:',sum(f['name'].endswith('.txt') for f in items),'range bytes:',sum(x['received_range_bytes'] for x in items),'raw bytes:',sum(x['size'] for x in items))
