"""Exact finite-head leading Cramer certificate, birth-SUPPRESSED exterior upper-return surrogate."""
import sympy as S, json
from test_holey_head_return_matrix import fall,g,fast,absorption
def eta(a,c): return -1 if (a,c)==(0,2) else 1 if (a,c)==(2,1) else 0
z,t=S.symbols('z t');H=5;ORDER=4
st=[(a,n-a) for n in range(H+1) for a in range(n+1)];ix={x:i for i,x in enumerate(st)}
Ps={n:absorption(n) for n in (H+1,H+2)}
dead=[i for i,(a,c) in enumerate(st) if not any(fall(a,y)*fall(c,3-y) for y,_ in fast)]
act=[i for i in range(len(st)) if i not in dead]
M=S.zeros(len(st));rhs=S.zeros(len(st),1)
for i,(a,c) in enumerate(st):
 n=a+c;scale=z**(4 if i in act else 1 if a else 0);rhs[i]=scale*(z**-2 if i in act else 1)
 def add(aa,cc,db,rate):
  if not rate:return
  nn=aa+cc;delta=db-g(nn)+g(n);v=S.expand(scale*rate)
  M[i,i]+=v
  if nn<=H:
   dd=delta+eta(aa,cc)-eta(a,c);M[i,ix[aa,cc]]-=v*t**dd*(2 if dd else 1)
  else:
   P=Ps[nn]
   for k in range(nn-2):
    dd=delta+eta(k,nn-3-k)-eta(a,c)
    M[i,ix[k,nn-3-k]]-=v*t**dd*(2 if dd else 1)*P[aa,k]
 b=1/z+g(n)-eta(a,c);b4=S.prod(b-j for j in range(4))
 add(a+1,c,1,1);add(a+2,c,3,a*b)
 if a>=3:add(a-3,c,-4,fall(a,3)*b4)
 for y,w in fast:
  q=fall(a,y)*fall(c,3-y)
  if q:add(a+w-y,c+y-w,0,q*b4)
M=M.applyfunc(S.expand)
def coeffs(mat):return [mat.applyfunc(lambda e:S.expand(e).coeff(z,k)) for k in range(ORDER+1)]
F=coeffs(M.extract(act,act));B=coeffs(M.extract(dead,act));C=coeffs(M.extract(act,dead));D=coeffs(M.extract(dead,dead))
Fi=[F[0].inv()]
for k in range(1,ORDER+1):Fi.append((-Fi[0]*sum((F[j]*Fi[k-j] for j in range(1,k+1)),S.zeros(len(act)))).applyfunc(S.expand))
Sch=[]
for k in range(ORDER+1):
 v=D[k]
 for i in range(k+1):
  for j in range(k-i+1):v-=B[i]*Fi[j]*C[k-i-j]
 Sch.append(v.applyfunc(S.expand))
rd=coeffs(rhs.extract(dead,[0]));rf=coeffs(rhs.extract(act,[0]));R=[]
for k in range(ORDER+1):
 v=rd[k]
 for i in range(k+1):
  for j in range(k-i+1):v-=B[i]*Fi[j]*rf[k-i-j]
 R.append(v.applyfunc(S.expand))

def polynomial(seq,i,j):
 out={}
 for k,mat in enumerate(seq):
  for term in S.Add.make_args(S.expand(mat[i,j])):
   c,p=term.as_coeff_exponent(t)
   if c:out[k,int(p)]=out.get((k,int(p)),0)+c
 return {k:v for k,v in out.items() if v}
def mul(a,b):
 out={}
 for (i,j),x in a.items():
  for (k,l),y in b.items():
   if i+k<=ORDER:out[i+k,j+l]=out.get((i+k,j+l),0)+x*y
 return {k:v for k,v in out.items() if v}
def det(mat):
 n=len(mat);dp={0:{(0,0):S.Integer(1)}}
 for row in range(n):
  nd={}
  for mask,p in dp.items():
   for col in range(n):
    if mask>>col&1:continue
    sign=(-1)**sum((mask>>q)&1 for q in range(col+1,n))
    d=nd.setdefault(mask|1<<col,{})
    for key,v in mul(p,mat[row][col]).items():d[key]=d.get(key,0)+sign*v
  dp={m:{k:v for k,v in p.items() if v} for m,p in nd.items()}
 return dp[(1<<n)-1]
def leading(p):
 if not p:return None
 k=min(i for i,j in p);q={j:v for (i,j),v in p.items() if i==k};j=max(q)
 return {'z_degree':k,'leading_t_degree':j,'leading_coefficient':str(q[j]),'coefficient_at_leading_z':str(sum(v*t**j for j,v in q.items()))}
P=[[polynomial(Sch,i,j) for j in range(len(dead))] for i in range(len(dead))];rr=[polynomial(R,i,0) for i in range(len(dead))]
out={'H':H,'fast_forcing':'s^2','shift_slack':2,'eta':{'0,2':-1,'2,1':1},'order':ORDER,'dead':[st[i] for i in dead],'det':leading(det(P)),'numerators':[]}
for j in range(len(dead)):
 Q=[[rr[i] if k==j else P[i][k] for k in range(len(dead))] for i in range(len(dead))]
 out['numerators'].append(leading(det(Q)))
print(json.dumps(out,indent=2))
