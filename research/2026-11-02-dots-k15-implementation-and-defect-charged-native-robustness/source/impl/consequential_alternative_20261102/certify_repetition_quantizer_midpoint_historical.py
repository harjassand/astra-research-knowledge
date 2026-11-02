"""Actual 64x64 cell partition. 50-digit CDF central evaluation PLUS independent
interval midpoint-error enclosure; no arbitrary-precision-as-proof substitution."""
import json,math,hashlib,sys,time
import numpy as np
import mpmath as mp
mp.mp.dps=60;mp.iv.dps=50
IV=mp.iv
N=64;SUB=8;J=8
ROOT='producer-workspace/consequential_alternative_20261102'

def interval_str(x):return str(x)
def bounds_float(x):return [float(x.a),float(x.b)]
def one_axis(vstr,r,inverse):
 v=mp.mpf(vstr)/(mp.mpf(r)) if inverse else mp.mpf(vstr)*r
 vv=IV.mpf(vstr)/r if inverse else IV.mpf(vstr)*r
 H=mp.sqrt(mp.pi)/2;HH=IV.sqrt(IV.pi)/2;L=mp.sqrt(mp.pi);LL=IV.sqrt(IV.pi)
 cell=H/N;step=HH/(N*SUB)
 f2max=1/(IV.sqrt(2*IV.pi)*vv**IV.mpf('1.5'))
 # Missing image intervals lie outside |xi| >= (J+.5)*sqrt(pi).
 tail=2*IV.exp(-((J+IV.mpf('.5'))*LL)**2/(2*vv))
 centers=[];intervals=[]
 for i in range(N):
  a=i*cell;b=(i+1)*cell;row=[];ivrow=[]
  for parity in [0,1]:
   js=[j for j in range(-J,J+1) if j%2==parity]
   val=mp.mpf(0)
   for j in js:
    aa=(a+j*L)/mp.sqrt(2*v);bb=(b+j*L)/mp.sqrt(2*v)
    val+=mp.erf(bb)-mp.erf(aa) # factor2 positive-half cancels erf CDF1/2
   row.append(val)
   mid=IV.mpf(0)
   for u in range(SUB):
    x=HH*(IV.mpf(i*SUB+u)+IV.mpf('.5'))/(N*SUB)
    for j in js:mid+=IV.exp(-(x+j*LL)**2/(2*vv))/IV.sqrt(2*IV.pi*vv)
   mid*=2*step
   error=2*len(js)*SUB*f2max*step**3/24
   ivrow.append(mid+IV.mpf([-1,1])*error+IV.mpf([0,1])*tail)
  centers.append(row);intervals.append(ivrow)
 return centers,intervals,float(v)

def one(vstr):
 v=float(vstr);r=3
 previous=json.load(open(ROOT+'highnoise_jointflags_results.json'))
 previous=next(x for x in previous if x['v']==v and x['r']==3 and x['K']==3)
 cent=np.array(previous['pauli']);H=math.sqrt(math.pi)/2;s=(np.arange(N)+.5)*H/N;m=np.arange(-12,13)
 probs=[]
 for vv in [v/r,v*r]:
  ff=np.exp(-(s[:,None]+m*math.sqrt(math.pi))**2/(2*vv))/math.sqrt(2*math.pi*vv)
  probs.append(ff[:,m%2!=0].sum(1)/ff.sum(1))
 a,b=np.meshgrid(*probs,indexing='ij');P=np.stack([(1-a)*(1-b),a*(1-b),a*b,(1-a)*b],axis=-1)
 labels=np.argmin(-P@np.log(cent).T,axis=-1).astype(np.uint8)
 Q,Qiv,_=one_axis(vstr,r,True);R,Riv,_=one_axis(vstr,r,False)
 masses=[[mp.mpf(0) for _ in range(4)] for _ in range(3)];mi=[[IV.mpf(0) for _ in range(4)] for _ in range(3)]
 for i in range(N):
  for f in range(3):
   js=np.flatnonzero(labels[i]==f)
   rs=[sum((R[j][b] for j in js),mp.mpf(0)) for b in [0,1]]
   ris=[sum((Riv[j][b] for j in js),IV.mpf(0)) for b in [0,1]]
   for col,(qa,pb) in enumerate([(0,0),(1,0),(1,1),(0,1)]):
    masses[f][col]+=Q[i][qa]*rs[pb];mi[f][col]+=Qiv[i][qa]*ris[pb]
 w=[sum(row) for row in masses];p=[[x/ww for x in row] for row,ww in zip(masses,w)]
 h=lambda t:-(t*mp.log(t,2)+(1-t)*mp.log(1-t,2))
 entropy=-sum(x*mp.log(x/ww,2) for row,ww in zip(masses,w) for x in row)
 certifications=[]
 for ori in [1,2,3]:
  others=[j for j in [1,2,3] if j!=ori];rho=IV.mpf(0);bit=IV.mpf(0)
  rhoc=mp.mpf(0);bitc=mp.mpf(0)
  for f in range(3):
   x=mi[f];r0=x[0]+x[ori];r1=x[others[0]]+x[others[1]];wf=r0+r1
   rho+=(x[0]-x[ori])**2/r0+(x[others[0]]-x[others[1]])**2/r1
   bit+=(-r0*IV.ln(r0/wf)-r1*IV.ln(r1/wf))/IV.ln(2)
   x=masses[f];r0=x[0]+x[ori];r1=x[others[0]]+x[others[1]]
   rhoc+=(x[0]-x[ori])**2/r0+(x[others[0]]-x[others[1]])**2/r1
   bitc+=(r0+r1)*h(r1/(r0+r1))
  gap=bit-rho
  certifications.append({'orientation':ori,'rho_cdf':str(rhoc),'b_cdf':str(bitc),'gap_cdf':str(bitc-rhoc),'rho_interval':str(rho),'b_interval':str(bit),'gap_interval':str(gap),'gap_bounds_float_for_readability':bounds_float(gap),'strict_gap_certified':bool(gap.a>0)})
 rec={'v':v,'r':3,'K':3,'N_grid':N,'normalization':str(sum(w)),'w':[float(x) for x in w],'pauli':[[float(x) for x in row] for row in p],'w_60digits':[str(x) for x in w],'pauli_60digits':[[str(x) for x in row] for row in p],'joint_mass_intervals':[[str(x) for x in row] for row in mi],'Ic1_cdf':str(1-entropy),'Ic1_previous_GL':previous['Ic1'],'loss_vs_continuous_previous_diagnostic':float(entropy-(1-previous['Ic1_continuous'])),'assignment':labels.tolist(),'assignment_sha256':hashlib.sha256(labels.tobytes(order='C')).hexdigest(),'assignment_hash_definition':'row-major 64x64 uint8 labels; q normalized syndrome first index, p second; cells |s| in [i H/64,(i+1)H/64), H=sqrt(pi)/2','certification':certifications,'certificate_method':'mpmath interval arithmetic 50digits; composite midpoint rule 8 subcells per actual 64 cell; Gaussian second derivative bound 1/(sqrt(2pi)*v^(3/2)); image J=8 with tail <=2exp(-((8.5)sqrtpi)^2/(2v)). CDF central calculations at60digits are crosscheck, not certificate.'}
 return rec
out=[]
for vstr in ['0.38','0.4']:
 rec=one(vstr);out.append(rec)
 json.dump(out,open(ROOT+'certified_repetition_quantizers.json','w'),indent=2)
 print(json.dumps({'v':rec['v'],'Ic1':rec['Ic1_cdf'],'hash':rec['assignment_sha256'],'gaps':[x['gap_interval'] for x in rec['certification']],'certified':[x['strict_gap_certified'] for x in rec['certification']]}),flush=True)
