import urllib.request,zipfile,io,json,numpy as np,pickletools,hashlib
entries={3:('0.11165005532450728','20260502_154400','28e4bfef7f4ef876af454a67379203c57334ccbd'),6:('0.11300952488511294','20260502_163859','a65f7fb9c96379dc68b97af90a4521d8ac1076e3'),9:('0.11388174409719082','20260502_174321','4eaa9d682b91ca0294a521dcaf6afa743d279814'),12:('0.11465558579340152','20260502_193350','4ac55abc2336ba34619150ddee8a5921ae1da0dd'),30:('0.11836627486983782','20260504_111304','3ab359af9f284d718e61f304dabcc4be385893bc')}
out=[]
for n,(p,t,sha) in entries.items():
 path=f'Independent X-Z States/n_is_{n}/indep_positive_for_p_at_{p}_at_time_{t}.pt'
 url='https://raw.githubusercontent.com/avantikaag03/Enhanced-quantum-capacity-thresholds-from-symmetry/main/'+urllib.parse.quote(path)
 data=urllib.request.urlopen(url,timeout=30).read()
 calc=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 assert calc==sha
 z=zipfile.ZipFile(io.BytesIO(data));pk=z.read([x for x in z.namelist() if x.endswith('data.pkl')][0]);ops=list(pickletools.genops(pk))
 assert any(op.name=='GLOBAL' and arg=='torch ComplexDoubleStorage' for op,arg,pos in ops)
 raw=z.read([x for x in z.namelist() if x.endswith('data/0')][0]);assert len(raw)==2*(n+1)*16
 # No unpickling/evaluation: decode validated raw tensor storage, row-major shape (2,n+1).
 arr=np.frombuffer(raw,dtype='<c16').reshape(2,n+1)
 rec={'n':n,'url':url,'git_blob_sha':sha,'provenance':'validated git blob; pickle disassembled only, not executed; raw complex128 storage extracted','ensemble_real':arr.real.tolist(),'ensemble_imag':arr.imag.tolist(),'row_norms_squared':np.sum(abs(arr)**2,axis=1).tolist(),'total_norm_squared':float(np.sum(abs(arr)**2)),'gram_real':(arr@arr.conj().T).real.tolist(),'gram_imag':(arr@arr.conj().T).imag.tolist()}
 out.append(rec);print(n,rec['row_norms_squared'],rec['total_norm_squared'],flush=True)
json.dump(out,open('producer-workspace/primary_xz_symmetry_seeds.json','w'),indent=2)
