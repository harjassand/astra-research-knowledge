import numpy as np,json,random,time,resource,hashlib,statistics
from pathlib import Path
from fast_rs import CSSDecoder,Compiler,decode_syndrome
p=Path(__file__).parent;rng=random.Random(202610290454);rows=[];saved={}
# Independent small reference: actual old totalBW on newbasis syndrome matrices.
small=[]
for h,mod,t in [(3,11,1),(4,19,3),(5,37,5)]:
 d=CSSDecoder(h,mod,t);ref=Compiler(h,mod);code=ref.code(t)
 for repeat in range(20):
  e=np.zeros(1<<h,np.uint16)
  for i in rng.sample(range(1<<h),rng.randrange(t+1)):e[i]=rng.randrange(1,1<<h)
  SX=d.f.moments(e,2*t);eh,ok,detail=d.f.decode(SX,t);syn=[ref.g.dot(row,list(map(int,e))) for row in code['H']];bw,bok=decode_syndrome(ref.g,code,syn)
  assert ok and bok and np.array_equal(e,eh) and np.array_equal(e,np.array(bw))
  assert np.array_equal(d.mono_from_novel(syn),SX)
 small.append({'h':h,'t':t,'exact_BW_crosschecks':20})
for t in [99,147]:
 start=time.perf_counter();d=CSSDecoder(11,2053,t);setup=time.perf_counter()-start;q=d.q
 types=['zero_only','nonzero_only','contiguous_with_zero','contiguous_without_zero','equal_amplitudes','subspace','random_with_zero','random_without_zero']
 cases=[]
 for kind in types:
  for rep in range(3):
   e=np.zeros(q,np.uint16);f=e.copy()
   if kind=='zero_only':loc=[0]
   elif kind=='nonzero_only':loc=[rng.randrange(1,q)]
   elif kind=='contiguous_with_zero':loc=list(range(t))
   elif kind=='contiguous_without_zero':loc=list(range(q-t,q))
   elif kind=='subspace':loc=list(range(1<<(t.bit_length()-1)))
   elif kind=='random_with_zero':loc=[0]+rng.sample(range(1,q),t-1)
   elif kind=='random_without_zero':loc=rng.sample(range(1,q),t)
   else:loc=rng.sample(range(q),t)
   for i in loc:e[i]=1 if kind in ['equal_amplitudes','subspace'] else rng.randrange(1,q);f[i]=1 if kind in ['equal_amplitudes','subspace'] else rng.randrange(1,q)
   begin=time.perf_counter();read=d.actual_readout(e,f);readsecs=time.perf_counter()-begin
   # Check power-syndrome acquisition conversion independently using explicit moments.
   v=np.zeros(q,np.uint16);v[-2*t:]=read[0];Y=d.transpose_fft(d.c.apply(v))[:2*t];assert np.array_equal(d.mono_from_novel(Y),d.f.moments(e,2*t));assert np.array_equal(d.mono_from_novel(d.f.phase_decode[read[1]]),d.f.moments(f,2*t))
   begin=time.perf_counter();eh,fh,ok,detail=d.decode_readout(*read);xbits,zbits=d.logical_correction_bits(eh,fh);elapsed=time.perf_counter()-begin
   assert ok and np.array_equal(e,eh) and np.array_equal(f,fh)
   actualx,actualz=d.logical_correction_bits(e,f);assert np.array_equal(actualx,xbits) and np.array_equal(actualz,zbits)
   key=f't{t}_{kind}_{rep}';saved[key+'_X']=e;saved[key+'_Z']=f;saved[key+'_readout_Xlast']=read[0];saved[key+'_readout_phasebits']=read[1]
   cases.append({'case':kind,'repeat':rep,'support':len(loc),'contains_zero':0 in loc,'simulated_quantum_readout_generation_seconds':readsecs,'complete_classical_decode_and_logical_correction_seconds':elapsed,'X_case':detail['X']['case'],'Z_case':detail['Z']['case']})
 # Unstructured syndrome tests assert total output + verification, not detectalluncorrectableerrors.
 fallback=0;representatives=0
 for rep in range(10):
  S=np.array([rng.randrange(q) for _ in range(2*t)],np.uint16);ee,ok,detail=d.f.decode(S,t)
  if ok:assert np.count_nonzero(ee)<=t and np.array_equal(d.f.moments(ee,2*t),S);representatives+=1
  else:assert len(ee)==q;fallback+=1
 times=[x['complete_classical_decode_and_logical_correction_seconds'] for x in cases]
 rows.append({'h':11,'B':q,'t':t,'payload_qubits':11*(q-4*t),'field_generator':d.f.generator,'setup_seconds':setup,'classical_decode_seconds_min':min(times),'classical_decode_seconds_median':statistics.median(times),'classical_decode_seconds_max':max(times),'field_lookup_bytes':sum(a.nbytes for a in [d.f.exp,d.f.log,d.f.elements,d.f.inverses,d.f.phase_codes,d.f.phase_decode]),'degree_basis_matrix_bytes':d.L.nbytes,'field_addition_gate_records':len(d.c.field),'unstructured_syndrome_fallbacks':fallback,'unstructured_syndrome_valid_representatives':representatives,'cases':cases})
np.savez_compressed(p/'benchmark_cases.npz',**saved)
out={'seed':202610290454,'status':'exact large classical decoder completed, pending independent review','small_BW_checks':small,'large_cases':rows,'peak_process_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'Classical walltimes on this executionhost, not hardware timings or guaranteed latency. Input is actual simulated FFT/CSS readout; no direct hiddenerror labels supplied to decoder. Errors/syndromes saved forreproduction. Outputcorrectionbits computed, no physicalapplication claimed. Above-radius errors maysharecorrectable syndrome; fallbackdoesnot detectall uncorrectableevents.'};(p/'benchmark_decoder.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
