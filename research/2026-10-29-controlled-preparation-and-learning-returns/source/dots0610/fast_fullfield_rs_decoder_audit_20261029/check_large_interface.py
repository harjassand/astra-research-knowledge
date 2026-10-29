from pathlib import Path
import sys,json,time,numpy as np
p=Path(__file__).parent;s=p.parent/'fast_fullfield_rs_decoder_20261029';sys.path.insert(0,str(s));from fast_rs import CSSDecoder
A=np.load(s/'benchmark_cases.npz');B=np.load(p/'replay/benchmark_cases.npz');assert A.files==B.files and all(np.array_equal(A[k],B[k]) for k in A.files)
circuit=np.load(p.parent/'additive_fft_outer_compiler_20261029/circuit_h11.npz');print(circuit.files)
gates=circuit['cnots']
rows=[]
for t in [99,147]:
 d=CSSDecoder(11,2053,t)
 for case in ['all_zero','random_with_zero_0','random_without_zero_0']:
  e=np.zeros(2048,np.uint16) if case=='all_zero' else A[f't{t}_{case}_X']
  z=np.zeros(2048,np.uint16) if case=='all_zero' else A[f't{t}_{case}_Z']
  xb=np.array([(int(a)>>j)&1 for a in e for j in range(11)],np.uint8)
  zb=np.array([(int(d.f.phase_codes[a])>>j)&1 for a in z for j in range(11)],np.uint8)
  for aa,bb in reversed(gates):xb[bb]^=xb[aa];zb[aa]^=zb[bb]
  xp=np.array([sum(int(xb[i*11+j])<<j for j in range(11)) for i in range(2048)],np.uint16)
  zp=np.array([sum(int(zb[i*11+j])<<j for j in range(11)) for i in range(2048)],np.uint16)
  read=xp[-2*t:],zp[:2*t];assert all(np.array_equal(a,b) for a,b in zip(read,d.actual_readout(e,z)))
  eh,zh,ok,detail=d.decode_readout(*read);assert ok and np.array_equal(e,eh) and np.array_equal(z,zh)
  xc,zc=d.logical_correction_bits(eh,zh);assert np.array_equal(xc,xp[2*t:-2*t]) and np.array_equal(zc,zp[2*t:-2*t])
  rows.append({'t':t,'case':case,'actual_compiled_binary_CNOT_readout_and_correction_exact':True})
r=json.load(open(p/'independent_benchmark_replay.json'));out={'all_saved_benchmark_arrays_equal':True,'large_interface_cases':rows,'independent_host_timing_medians_seconds':{str(v['t']):v['classical_decode_seconds_median'] for v in r['large_cases']},'independent_host_peak_RSS_KiB':r['peak_process_RSS_KiB']};(p/'large_interface_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
