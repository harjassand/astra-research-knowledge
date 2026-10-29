import mpmath as mp,json
v=mp.iv;v.dps=45
z=v.mpf(0);one=v.mpf(1);ii=v.mpc(0,1)
def mat(a):return [[v.mpc(x) for x in row] for row in a]
def add(a,b):return [[a[i][j]+b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
def scale(a,c):return [[x*c for x in row] for row in a]
def mul(a,b):return [[sum((a[i][k]*b[k][j] for k in range(len(b))),v.mpc(0)) for j in range(len(b[0]))] for i in range(len(a))]
def dag(a):return [[v.mpc(a[j][i].real,-a[j][i].imag) for j in range(len(a))] for i in range(len(a[0]))]
def tr(a):return sum((a[i][i] for i in range(len(a))),v.mpc(0))
def summ(xs):
 a=mat([[0,0],[0,0]])
 for x in xs:a=add(a,x)
 return a
I=mat([[1,0],[0,1]]);X=mat([[0,1],[1,0]]);Y=[[v.mpc(0),-ii],[ii,v.mpc(0)]];Z=mat([[1,0],[0,-1]]);pauli=[X,Y,Z]
sigma=mat([[.5,.25],[.25,.5]]);K=[[[v.mpc(0),v.sqrt(one/2)],[v.mpc(1),v.mpc(0)]],[[v.mpc(0),v.mpc(0)],[v.mpc(0),v.sqrt(one/2)]]]
def phi(a):return summ(mul(mul(k,a),dag(k)) for k in K)
def phiadj(a):return summ(mul(mul(dag(k),a),k) for k in K)
nu=phi(sigma);s=[one/4,3*one/4];P=[scale(add(I,scale(X,-1)),one/2),scale(add(I,X),one/2)];t=v.sqrt(6)/8;vv=[one/2-t,one/2+t];direction=scale(add(nu,scale(I,-one/2)),1/t);Q=[scale(add(I,scale(direction,-1)),one/2),scale(add(I,direction),one/2)]
ss=summ(scale(P[i],v.sqrt(s[i])) for i in range(2));ni=summ(scale(Q[i],1/v.sqrt(vv[i])) for i in range(2))
def R0(a):return mul(mul(ss,phiadj(mul(mul(ni,a),ni))),ss)
def kap(x,exactzero=False):
 if exactzero:return one
 return x/((v.exp(x)-v.exp(-x))/2)
def rb(a):
 out=mat([[0,0],[0,0]])
 for i in range(2):
  for j in range(2):
   for aa in range(2):
    for b in range(2):
     w=(v.log(s[i])-v.log(s[j])-v.log(vv[aa])+v.log(vv[b]))/2
     c=kap(w,i==j and aa==b)
     out=add(out,scale(mul(mul(P[i],R0(mul(mul(Q[aa],a),Q[b]))),P[j]),c))
 return out
B=[]
for j in range(2):
 ej=mat([[int(a==j and b==j) for b in range(2)] for a in range(2)]);B.append(scale(mul(mul(ss,ej),ss),1/sigma[j][j]))
def eb(a):return add(scale(B[0],a[0][0]),scale(B[1],a[1][1]))
M=[[None]*3 for _ in range(3)];N=[[None]*3 for _ in range(3)]
for j,p in enumerate(pauli):
 dm=add(p,scale(rb(phi(p)),-1));dn=add(p,scale(eb(p),-1))
 for i,q in enumerate(pauli):M[i][j]=(tr(mul(q,dm))/2).real;N[i][j]=(tr(mul(q,dn))/2).real
# Exact algebraic inverse via adjugate, evaluated by outward interval arithmetic.
def det3(a):return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0])
det=det3(M);assert det.a>0
inv=[]
for i in range(3):
 row=[]
 for j in range(3):
  rr=[r for r in range(3) if r!=j];cc=[c for c in range(3) if c!=i];co=M[rr[0]][cc[0]]*M[rr[1]][cc[1]]-M[rr[0]][cc[1]]*M[rr[1]][cc[0]];row.append((-1)**(i+j)*co/det)
 inv.append(row)
T=[[sum(N[i][k]*inv[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
bound=sum(abs(x) for row in T for x in row);assert bound.b<5
out={'prior':'[[1/2,1/4],[1/4,1/2]]','gamma':'1/2','precision_digits':45,'determinant_interval':str(det),'transfer_matrix_intervals':[[str(x) for x in row] for row in T],'entry_l1_interval':str(bound),'certified_integer_diamond_upper_bound':5,'scope':'mpmath interval arithmetic certificate; runtime trusted, not formal proof assistant'}
print(out);open('INTERVAL_CERTIFICATE.json','w').write(json.dumps(out,indent=2)+'\n')
