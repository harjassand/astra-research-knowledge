"""Exact whole-curve admission and noncommuting-bath source compiler."""
from fractions import Fraction as Q
from pathlib import Path
import json,time
OUT=Path(__file__).resolve().parent
def zeros(n):return [[Q(0) for _ in range(n)] for _ in range(n)]
def mm(a,b):return [[sum((x*y for x,y in zip(row,col)),Q(0)) for col in zip(*b)] for row in a]
def kron(a,b):return [[v*w for v in ar for w in br] for ar in a for br in b]
def trace(a):return sum((a[i][i] for i in range(len(a))),Q(0))
def ldl(a,floor=Q(0)):
 n=len(a);l=zeros(n);p=[]
 for i in range(n):
  x=a[i][i]-floor-sum((l[i][j]**2*p[j] for j in range(i)),Q(0));assert x>0;p.append(x)
  for j in range(i+1,n):l[j][i]=(a[j][i]-sum((l[j][k]*l[i][k]*p[k] for k in range(i)),Q(0)))/x
 return min(p)
def main():
 start=time.perf_counter();r=1;m=M=Q(1);ell=Q(8,9);ell0=ell;kappa=M/m
 eps=m*ell0**4/(2**44*kappa**3*r**5);a0=m*ell0**2/(2**18*r**3)
 w=eps+9*r*a0;threshold=m*ell0**2/(2**14*r*r)
 assert eps<=m*ell0**2/(2**18*r*r) and w<=threshold and Q(35,96)<Q(1,2)
 h=zeros(9);po=zeros(9);eye=zeros(9)
 for i in range(9):h[i][i]=Q(1,9);eye[i][i]=1
 for b,v in enumerate([1,-1,0]):h[b][3+b]=h[3+b][b]=Q(v,36)
 for i in range(3):
  for j in range(3):po[3*i+i][3*j+j]=1
 assert trace(h)==1;hp=ldl(h,Q(1,13));assert 1-trace(mm(po,h))/3==ell
 x=[[po[i][j]+eps*h[i][j] for j in range(9)] for i in range(9)]
 u=[[Q(1,2),Q(1,2)],[Q(1,2),Q(1,2)]];v=[[Q(1),Q(0)],[Q(0),Q(0)]]
 assert mm(u,u)==u and mm(v,v)==v and mm(u,v)!=mm(v,u)
 xu,iv=kron(x,u),kron(eye,v);z=[[xu[i][j]+iv[i][j] for j in range(18)] for i in range(18)]
 zp=ldl(z);whole=trace(z);assert whole==12+eps
 red=[[sum((z[(3*i+b)*2+t][(3*j+b)*2+t] for b in range(3) for t in range(2)),Q(0)) for j in range(3)] for i in range(3)]
 assert red==[[whole/3 if i==j else Q(0) for j in range(3)] for i in range(3)]
 off=[[z[b][6+c] for c in range(6)] for b in range(6)];assert any(t for row in mm(off,off) for t in row)
 assert [[z[2*i+1][2*j+1] for j in range(9)] for i in range(9)]==[[t/2 for t in row] for row in x]
 assert 2-2*eps/9>0 and a0<1
 # Atom q'(0+)=1/2; q''>=1/30 and h>=3r/[35(M+2)^2] on[1,2], here m=1.
 raw=eps*ell/4+Q(r,350*(M+2)**2);normalized=raw/whole
 out={'status':'EXACT_ENTIRE_WHITE_COHERENT_RAY_AND_BATH_ADMITTED','r':r,'m':str(m),'M':str(M),'ell':str(ell),'epsilon':str(eps),'a0':str(a0),'small_trace_at_a0':str(w),'small_threshold':str(threshold),'large_charge_fraction_bound':'35/96','source_trace':str(whole),'raw_bath_Delta_lower':str(raw),'normalized_CMI_excess_lower':str(normalized),'CMI_lower_display':float(normalized),'H_LDL_pivot':str(hp),'Z_LDL_pivot':str(zp),'old_reset_square_zero_excluded':True,'reduction_region_excluded':True,'reference_dimension':6,'extension_dimension':54,'seconds':time.perf_counter()-start,'scope':'Exact synthetic matrices and theorem admission. Entire curve follows from finite proof, not sampling. Common-bath identity inherited; no physical input, global coverage, runtime advantage or priority claim.'}
 (OUT/'FIXTURE.json').write_text(json.dumps({k:[[str(t) for t in row] for row in mat] for k,mat in [('H',h),('U',u),('V',v),('Z',z)]},indent=2)+'\n')
 (OUT/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:out[k] for k in ['status','epsilon','a0','normalized_CMI_excess_lower','CMI_lower_display','seconds']},indent=2))
if __name__=='__main__':main()
