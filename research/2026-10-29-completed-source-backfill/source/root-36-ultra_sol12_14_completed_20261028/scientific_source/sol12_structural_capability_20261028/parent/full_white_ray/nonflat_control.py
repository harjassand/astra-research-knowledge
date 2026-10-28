"""Exact nonflat theorem-input control; no numeric entropy premise."""
from compile import Q,OUT,zeros,mm,kron,trace,ldl
import json,time
start=time.perf_counter();r=2;n=18;C=[[Q(1),Q(0)],[Q(0),Q(10**6)]];uv=list(range(1,n+1));s=n+sum(v*v for v in uv)
h=[[Q((i==j)+uv[i]*uv[j],s) for j in range(n)] for i in range(n)];po=zeros(9)
for i in range(3):
 for j in range(3):po[3*i+i][3*j+j]=1
p=kron(po,[[Q(1),Q(0)],[Q(0),Q(1)]])
assert trace(h)==1;ldl(h,Q(1,2*s));ell=1-trace(mm(p,h))/3;assert ell==Q(1582,2127)
eps=ell**2/(2**22*r**3);a0=ell**2/(2**18*r**3);assert eps==a0/16
assert eps+9*r*a0<=ell**2/(2**14*r*r)
A=kron(po,C);x=[[A[i][j]+eps*h[i][j] for j in range(n)] for i in range(n)]
ub=[[Q(1,2),Q(1,2)],[Q(1,2),Q(1,2)]];vb=[[Q(1),Q(0)],[Q(0),Q(0)]];eye=[[Q(i==j) for j in range(n)] for i in range(n)]
xu,iv=kron(x,ub),kron(eye,vb);z=[[xu[i][j]+iv[i][j] for j in range(2*n)] for i in range(2*n)];pivot=ldl(z)
whole=trace(z);assert whole==3*trace(C)+eps+9*r
rawmargin=eps*ell/4+Q(r,3150);cmimargin=rawmargin/whole
oldbudget=ell**4/(2**44*Q(10**6)**3*r**5);assert eps>10**20*oldbudget
out={'status':'EXACT_NONFLAT_KAPPA_FREE_INPUT_PASSED','C_eigenvalues':['1','1000000'],'r':r,'ell':str(ell),'epsilon':str(eps),'a0':str(a0),'old_kappa_budget':str(oldbudget),'new_to_old_radius_ratio':str(eps/oldbudget),'source_trace':str(whole),'raw_bath_Delta_lower':str(rawmargin),'normalized_flagged_CMI_lower':str(cmimargin),'reference_before_flag':12,'reference_after_nine_Weyl_flag':108,'extension_dimension':972,'Z_LDL_min_pivot':str(pivot),'seconds':time.perf_counter()-start,'scope':'Exact synthetic PSD and theorem admission. No entropy evaluation or physical preparation. Nine-Weyl flag charged; whole-curve proof is analytic. No runtime advantage.'}
(OUT/'NONFLAT_CONTROL.json').write_text(json.dumps(out,indent=2)+'\n')
(OUT/'NONFLAT_FIXTURE.json').write_text(json.dumps({'H':[[str(t) for t in row] for row in h],'C':[[str(t) for t in row] for row in C],'Z':[[str(t) for t in row] for row in z]},indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','epsilon','new_to_old_radius_ratio','seconds']},indent=2))
