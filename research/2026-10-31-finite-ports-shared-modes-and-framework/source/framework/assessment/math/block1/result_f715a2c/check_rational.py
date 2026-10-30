from pathlib import Path
path=Path(__file__).with_name('rational_heat.py');code=path.read_text().split('pts=')[0];exec(compile(code,str(path),'exec'))
result=np.load(Path(__file__).with_name('search_result.npz'));theta=result['theta'];rng=np.random.default_rng(9163)
pts=[]
for scale in [.01,.03,.1,.3,1,3,10,30,100]:
 pts.extend(tuple([*rng.normal(size=3)*scale,0]) for _ in range(2000))
for tau in np.linspace(-10,10,201):
 zz=-.25+1j*tau;ww=-tau/2-.25j;zz*=np.exp(-2j*np.angle(ww));ww=abs(ww)
 pt=np.array([zz.real,zz.imag,ww])
 for eps in [0,.0001,.001,.01,.1]:
  pts.extend(tuple([*(pt+rng.normal(size=3)*eps),0]) for _ in range(3))
worst=(0,None,None)
for pt in pts:
 mm=np.array([ff(*pt) for ff in funcs],float);mat0=mm[0]+np.einsum('p,pij->ij',theta,mm[1:]);scale=max(np.linalg.norm(mm[0]),1);ev,U=np.linalg.eigh(mat0/scale)
 if ev[0]<worst[0]:worst=(ev[0],pt,U[:,0])
print('Out of sample worst normalized eigenvalue:',worst,flush=True)
# Save a positive loss as a defect, never a QC violation.
Path(__file__).with_name('out_of_sample.txt').write_text(repr(worst))
