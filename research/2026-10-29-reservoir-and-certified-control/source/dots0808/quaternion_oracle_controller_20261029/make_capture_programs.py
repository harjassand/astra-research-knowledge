from pathlib import Path
root=Path(__file__).parent
sources=[('one_axis','producer-workspace/check_gap_free_one_axis.py'),('drift','producer-workspace/check_drifting_memory.py')]
for label,src in sources:
 s=Path(src).read_text();s=s.replace('start=time.time()','bank0=np.zeros((3,3,3),dtype=np.int64);bank2=np.zeros((3,3,3,3,3),dtype=np.int64)\nstart=time.time()')
 s=s.replace('for i in range(1,n):\n   ca=Cs', 'for i in range(1,n):\n   bank0[i-1,a[i],a[0]]+=int(yy[i]*yy[0])\n   bank2[i-1,a[i],a[0],c[i],c[0]]+=int(yy[i]*yy[0]*sign[i]*sign[0])\n   ca=Cs')
 s+=f"\nfrom pathlib import Path\nbank_result=dict(source_fixture={label!r},T=T,probe_calls=nprobe,B=bank0.tolist(),C=bank2.tolist(),scope='Exact integer sufficient coefficient bank from actual sampled product-Pauli probes along the executed retained-memory trajectory.')\nPath(__file__).with_name('bank_{label}.json').write_text(json.dumps(bank_result,indent=2)+'\\n')\n"
 (root/f'capture_{label}.py').write_text(s)
