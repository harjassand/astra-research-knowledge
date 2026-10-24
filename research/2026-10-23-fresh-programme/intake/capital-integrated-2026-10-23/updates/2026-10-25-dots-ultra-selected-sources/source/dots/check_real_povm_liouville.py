import numpy as np,json,time,resource
from pathlib import Path
start=time.perf_counter();rng=np.random.default_rng(13520);a=r=2
I=np.eye(2);X=np.array([[0,1],[1,0]]);Z=np.diag([1,-1])
E=np.array([.3*I+.1*X,.4*I+.1*Z,.3*I-.1*X-.1*Z])
M=np.array([.25*I+.12*X,.5*I+.08*Z,.25*I-.12*X-.08*Z])
x=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));s=x@x.conj().T+.2*np.eye(4);s/=np.trace(s)
x=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));h=x+x.conj().T
hr=np.trace(h.reshape(a,r,a,r),axis1=0,axis2=2);h-=np.kron(I/2,hr)
g1=np.kron(s,I)
g2=np.kron(s.T,I).reshape(a,r,r,a,r,r).transpose(0,2,1,3,5,4).reshape(a*r*r,a*r*r)
g=(g1+g2)/(2*r)
z=np.empty((a*r*r,a),complex)
for aa in range(a):
 for bb in range(a): z[aa*r*r:(aa+1)*r*r,bb]=h.reshape(a,r,a,r)[aa,:,bb,:].reshape(-1)
def measure(e,x,ref):
 return np.einsum('ba,aibj->ij',e,x.reshape(a,ref,a,ref))
def met(s,h,kind):
 v,u=np.linalg.eigh(s);b=u.conj().T@h@u
 w=np.empty((len(v),len(v)))
 for i,x in enumerate(v):
  for j,y in enumerate(v): w[i,j]=2/(x+y) if kind=='sld' else (1/x if abs(x-y)<1e-12*max(x,y) else (np.log(x)-np.log(y))/(x-y))
 return float(np.sum(abs(b)**2*w).real)
receipts=[]
for label,es in [('E',E),('M',M)]:
 residual=[];sld=0;lift=[]
 for e in es:
  si=measure(e,s,r);hi=measure(e,h,r);gi=measure(e,g,r*r)
  residual.append(float(np.linalg.norm(gi-(np.kron(si,I)+np.kron(I,si.T))/(2*r))))
  zi=np.einsum('ba,aib->i',e,z.reshape(a,r*r,a))
  assert np.linalg.norm(zi-hi.reshape(-1))<1e-12
  sld+=met(si,hi,'sld');lift.append((gi,zi,float(np.trace(e).real/a)))
 rows=[]
 for eps in [1e-5,1e-20,1e-100]:
  val=0
  for gi,zi,qi in lift:
   si=np.zeros((r*r+1,r*r+1),complex);si[:-1,:-1]=(1-eps)*gi;si[-1,-1]=eps*qi
   hi=np.zeros_like(si);hi[:-1,-1]=zi;hi[-1,:-1]=zi.conj();val+=met(si,hi,'bkm')
  rows.append({'epsilon':eps,'bkm':val,'scaled':val/(2*r*np.log(1/eps))})
 receipts.append({'name':label,'output_lift_residual':max(residual),'original_sld':sld,'lift_rows':rows})
assert np.linalg.eigvalsh(g)[0]>0
assert all(x['output_lift_residual']<1e-12 for x in receipts)
refz=np.einsum('aia->i',z.reshape(a,r*r,a))
assert np.linalg.norm(refz)<1e-12
out={'purpose':'Noncommuting faithful input, shared-real-basis POVM Liouville lift diagnostic, not proof','seed':13520,'top_baseline_min_eigenvalue':float(np.linalg.eigvalsh(g)[0]),'top_trace':float(np.trace(g).real),'reference_tangent_residual':float(np.linalg.norm(refz)),'measurements':receipts,'original_M_over_E_sld':receipts[1]['original_sld']/receipts[0]['original_sld'],'last_lift_ratio':receipts[1]['lift_rows'][-1]['bkm']/receipts[0]['lift_rows'][-1]['bkm'],'elapsed_seconds':time.perf_counter()-start,'peak_rss_kib_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
