import sympy as s, json, pathlib,itertools
ROOT=pathlib.Path(__file__).resolve().parent
coeffs=json.loads((ROOT/'extremal_multiaffine_4.json').read_text())['coefficients']
p=101
coeffs=[a%p*pow(coeffs[-1]%p,-1,p)%p for a in coeffs]
m=lambda I:coeffs[15^sum(1<<i for i in I)]
a=[m([i]) for i in range(4)]
r={(i,j):(a[i]*a[j]-m([i,j]))%p for i in range(4) for j in range(i+1,4)}
t=lambda i,j,k:(m([i,j,k])-a[i]*a[j]*a[k]+a[i]*r[j,k]+a[j]*r[i,k]+a[k]*r[i,j])%p
print('prime',p,'diagonal',a,'pair products',r,'triple cycle sums',[t(*I) for I in itertools.combinations(range(4),3)])
u,v,w=s.symbols('u v w')
f=[r[0,2]*u**2-t(0,1,2)*u+r[0,1]*r[1,2], r[0,3]*v**2-t(0,1,3)*v+r[0,1]*r[1,3], r[0,3]*w**2-t(0,2,3)*w+r[0,2]*r[2,3]]
# 3-cycle sum on indices 2,3,4 after multiplying by u*v*w.
g=r[1,3]*u**2*w**2+r[1,2]*r[2,3]*v**2-t(1,2,3)*u*v*w
G=s.groebner(f+[g],u,v,w, modulus=p)
print('Groebner basis',G)
(ROOT/'diagonal_determinant_mod101.txt').write_text(str({'p':p,'diagonal':a,'pair_products':r,'equations':[str(x) for x in f+[g]],'groebner_basis':[str(x) for x in G.polys]}))
# Quotient-algebra norm certificate. The first 3 polynomials have disjoint
# variables and unit leading coefficients, hence the quotient has this basis.
G3=s.groebner(f,u,v,w,modulus=p)
basis=[u**i*v**j*w**k for i,j,k in itertools.product(range(2),repeat=3)]
cols=[]
for b in basis:
 rem=s.Poly(G3.reduce(s.Poly(g*b,u,v,w,modulus=p).as_expr())[1],u,v,w,modulus=p)
 cols.append([int(rem.coeff_monomial(mon))%p for mon in basis])
M=s.Matrix(cols).T
norm=int(M.det())%p
print('basis',basis,'multiplication matrix',M,'norm',norm,sep='\n')
(ROOT/'norm_certificate_mod101.json').write_text(json.dumps({'prime':p,'basis':[str(b) for b in basis], 'equations':[str(s.Poly(h,u,v,w,modulus=p).monic().as_expr()) for h in f], 'g':str(s.Poly(g,u,v,w,modulus=p).as_expr()),'multiplication_matrix':[list(map(int,M[i,:])) for i in range(8)],'norm':norm},indent=2))
a,b,c,d=[t(*I) for I in itertools.combinations(range(4),3)]
p12,p13,p14,p23,p24,p34=[r[I] for I in itertools.combinations(range(4),2)]
N=s.Matrix([[a*p14,b*p13,c*p12,2*d*p12*p13*p14+c*b*a],[b*p23,a*p24,d*p12,2*c*p12*p23*p24+d*b*a],[c*p23,d*p13,a*p34,2*b*p13*p23*p34+d*c*a],[d*p14,c*p24,b*p34,2*a*p14*p24*p34+d*c*b]]).applyfunc(lambda x:int(x)%p)
print('Nanson top4 matrix',N,'det',int(N.det())%p,sep='\n')
(ROOT/'nanson_certificate_mod101.json').write_text(json.dumps({'prime':p,'matrix':[list(map(int,N[i,:])) for i in range(4)],'det':int(N.det())%p},indent=2))
