"""Exact binary noncommuting matrix-weight source and entropy receiver."""
from pathlib import Path
from fractions import Fraction as Q
import json,time,sys
sys.set_int_max_str_digits(0);START=time.perf_counter()
import sympy as s
OUT=Path(__file__).resolve().parent/'outputs';OUT.mkdir(exist_ok=True)
def rat(v):return Q(int(v.p),int(v.q))
def enc(v):return str(v.numerator)+'/'+str(v.denominator)
def add(*ivs):return sum(v[0] for v in ivs),sum(v[1] for v in ivs)
def scale(c,v):return min(c*v[0],c*v[1]),max(c*v[0],c*v[1])
def mul(v,w):
 vals=[x*y for x in v for y in w];return min(vals),max(vals)
def alog(y):
 z=(y-1)/(y+1);assert 0<=z<=Q(1,3);n=24
 lo=2*sum((z**(2*j+1)/Q(2*j+1) for j in range(n)),Q(0))
 return lo,lo+2*z**(2*n+1)/(Q(2*n+1)*(1-z*z))
LN2=alog(Q(2))
def logq(v):
 assert v>0;y=v;k=0
 while y<1:y*=2;k-=1
 while y>2:y/=2;k+=1
 return add(alog(y),scale(k,LN2))
def flog(iv):
 lo,hi=iv
 if hi==0:return Q(0),Q(0)
 assert lo>0
 return mul(iv,(logq(lo)[0],logq(hi)[1]))
def matrix_f(mat):
 z=s.symbols('z');poly=s.Poly(mat.charpoly(z).as_expr(),z,domain=s.QQ)
 intervals=poly.intervals(eps=s.Rational(1,2**60));total=(Q(0),Q(0));root_record=[]
 assert sum(m for ii,m in intervals)==mat.rows
 for ii,m in intervals:
  iv=tuple(map(rat,ii));assert iv[0]>=0
  total=add(total,scale(m,flog(iv)));root_record.append({'interval':[enc(x) for x in iv],'multiplicity':m})
 return total,{'characteristic_coefficients':list(map(str,poly.all_coeffs())),'root_intervals':root_record,'f_interval':[enc(x) for x in total]}
def bell(a):
 v=s.zeros(9,1)
 for i in range(3):v[3*i+(i+a)%3]=1
 return v*v.T/3
def run():
 A=s.Matrix([[4,1],[1,1]])/10;B=s.diag(1,4)/10;C=A+B
 assert A.det()>0 and B.det()>0 and A[0,0]>0 and B[0,0]>0
 assert s.trace(C)==1 and A*B!=B*A
 v=s.Matrix([0,1,-1]);w=s.Matrix([-1,0,1]);S=v*v.T/2;T=w*w.T/2
 P=s.eye(3)-s.ones(3)/3;Es=2*(P-T)/3;Et=2*(P-S)/3;Ef=s.eye(3)-Es-Et
 for E in [Es,Et,Ef]:
  for m in [1,2,3]:
   from itertools import combinations
   for j in combinations(range(3),m):assert E.extract(j,j).det()>=0
 assert s.trace(S*Es)==s.trace(T*Et)==s.Rational(1,2)
 assert s.trace(S*Et)==s.trace(T*Es)==0
 assert s.trace(S*Ef)==s.trace(T*Ef)==s.Rational(1,2)
 sigma_out=s.Rational(91,200)*(S+T)+s.Rational(3,100)*s.eye(3)
 K=S-T;score=s.Rational(200,97)*K
 assert (sigma_out*score+score*sigma_out)/2==K
 metric_in=s.Rational(400,93);metric_out=s.trace(K*score)
 assert metric_out==s.Rational(300,97) and metric_out/metric_in==s.Rational(279,388)
 M=s.kronecker_product(S,A)+s.kronecker_product(T,B)
 X=s.kronecker_product(bell(0),A)+s.kronecker_product(bell(1),B)
 physical=s.Matrix(3,3,lambda i,j:sum(X[6*i+k,6*j+k] for k in range(6)))
 assert physical==s.eye(3)/3 and s.trace(X)==1 and X.rank()==4
 marginal=sum((X[6*i:6*i+6,6*i:6*i+6] for i in range(3)),s.zeros(6))
 pt=s.Matrix(18,18,lambda i,j:X[(j//6)*6+i%6,(i//6)*6+j%6])
 NX=(s.kronecker_product(s.eye(3),marginal)-pt)/2
 perm=s.zeros(9)
 for u in range(3):
  for d in range(3):perm[3*((u+d)%3)+(u+2*d)%3,3*u+d]=1
 pp=s.kronecker_product(perm,s.eye(2))
 assert pp.T*NX*pp==s.kronecker_product(s.eye(3)/3,M)
 off=X[:6,6:12];assert off*off!=s.zeros(6)
 fvals=[];spectra={}
 for name,mat in [('A',A),('B',B),('C',C),('M',M)]:
  val,rec=matrix_f(mat);fvals.append(val);spectra[name]=rec
 deficit=add(*fvals[:3],scale(-2,fvals[3]));assert deficit[0]>Q(1,4)
 maxbits=max(max(v.numerator.bit_length(),v.denominator.bit_length()) for v in deficit)
 inputs={name:[[str(v) for v in row] for row in mat.tolist()] for name,mat in [('A',A),('B',B),('C',C),('S',S),('T',T),('E_s',Es),('E_t',Et),('E_erasure',Ef),('M',M),('X',X)]}
 (OUT/'BINARY_INPUT.json').write_text(json.dumps(inputs,indent=2)+'\n')
 result={'status':'EXACT_STRONG_BINARY_NONCOMMUTING_SOURCE','labels':[[0,0],[1,0]],'memory_dimension':2,'reference_dimension':6,'input_dimension':18,'extension_dimension':54,'input_rank':4,'A_B_commutator':[[str(v) for v in row] for row in (A*B-B*A).tolist()],'uniform_USD_success':'1/2','failed_USD_branch_retained':True,'physical_marginal':'I3/3','literal_Bell_SIC_components':324,'CMI_excess_lower':'1/4','actual_entropy_interval':[enc(x) for x in deficit],'lower_display':float(deficit[0]),'max_entropy_endpoint_bits':maxbits,'filtered_Bell_fidelity':'4/5','filter_probability':'1/2','old_square_zero_package_excluded':True,'faithful_N966_premise_counter_ratio':'279/388','spectra':spectra,'seconds_including_sympy_import':time.perf_counter()-START}
 (OUT/'BINARY_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['spectra','actual_entropy_interval']},indent=2))
if __name__=='__main__':run()
