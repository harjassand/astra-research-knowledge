"""Export a fully explicit exact certificate for the sharp anisotropic slice."""
import sympy as s,numpy as np,pickle,itertools,os,json,time
BASE=os.path.dirname(__file__);cert=pickle.load(open(BASE+'/sharp_endpoint_certificate.pkl','rb'));z=pickle.load(open(BASE+'/c4_spin2.pkl','rb'));L=cert['L'];mp=cert['mp']
def red(expr):return s.rem(s.Poly(s.expand(expr),L,domain=s.QQ),s.Poly(mp,L,domain=s.QQ)).as_expr()
R=cert['R'];T=cert['T'];uu=cert['uu'];vv=cert['vv']
SS=(R*T*R.T).applyfunc(red);UU=(4*uu*uu.T).applyfunc(red);VV=(s.Rational(2,3)*vv*vv.T).applyfunc(red)
ij6=list(itertools.combinations_with_replacement(range(6),2));ij3=list(itertools.combinations_with_replacement(range(3),2))
sv=s.Matrix([SS[i,j] for i,j in ij6]+[UU[i,j] for i,j in ij3]+[VV[i,j] for i,j in ij3])
p=s.Matrix([1,s.Rational(7,2),s.Rational(1,2),L]);rhs=(z['T']*sv-z['EA']*p).applyfunc(red)
assert all(red(e)==0 for e in z['P']*rhs)
print('ALL 165 projected equations verified exactly',flush=True)
zz=np.load(BASE+'/heat_matrices.npz');assert np.all(zz['N']==np.round(zz['N']));N=s.Matrix(zz['N'].astype(int));cols=N.rref()[1];rows=N[:,cols].T.rref()[1]
Nsub=N[list(rows),list(cols)];invrhs=Nsub.inv()*rhs[list(rows),:];cc=s.zeros(80,1)
for i,idx in enumerate(cols):cc[idx]=invrhs[i]
assert all(red(e)==0 for e in N*cc-rhs)
print('ALL 210 exterior derivative polynomial coefficients verified exactly',flush=True)
# Acoustic zero uses k^2=j at the selected critical angle.
j=s.symbols('j');v=L**2;jp=(248-21*v)*(1+j)**2-(64*v-160)*j
GB=s.groebner([mp,jp],j,L,order='lex',domain=s.QQ)
def redj(expr):return GB.reduce(s.expand(expr))[1]
M=s.Matrix([[12+8*j,16*j,-2*j],[16,8+12*j,-(1+3*j)],[-2*v,-v*(1+3*j),4+7*j]])
b=s.Matrix([-3-j,-2,-1]);ac=M.adjugate()*b;D=M.det();aa,bb,c=ac
last=v*(3+j)*aa+2*v*j*bb+j*c+(7+4*j)*D
assert redj(last)==0
print('Exact critical acoustic null identity verified',flush=True)
# Serialization: every algebraic coefficient is a polynomial in L of degree <=5.
def poly(expr):
 p=s.Poly(red(expr),L);return [str(p.nth(i)) for i in range(6)]
def matrix(M):return [[poly(M[i,j]) for j in range(M.cols)] for i in range(M.rows)]
primitive=[]
for co,inds in zip(cc,zz['alphas']):
 if co!=0:primitive.append({'coefficient':poly(co),'monomial_indices':[int(i) for i in inds[:3]],'differential_index':int(inds[3])})
data={'description':'Exact compatible-heat certificate for F_L at the sharp endpoint. All polynomial coefficient lists are ascending powers 1,L,...,L^5.',
'minimal_polynomial_ascending':['-97344','0','29712','0','-2545','0','48'],
'root_interval':[str(cert['left']),str(cert['right'])],
'R':matrix(R),'T':matrix(T),'u':matrix(uu),'v':matrix(vv),'alpha_weight':'4','beta_weight':'2/3','primitive':primitive,
'T_leading_principal_minors':[poly(v) for v in cert['minors']],
'T_minor_interval_bounds':[[str(a),str(b)] for a,b in cert['intervals']]}
path=BASE+'/sharp_certificate.json';open(path,'w').write(json.dumps(data,indent=2))
print('EXACT SHARP CERTIFICATE EXPORTED',path,'bytes',os.path.getsize(path),flush=True)
