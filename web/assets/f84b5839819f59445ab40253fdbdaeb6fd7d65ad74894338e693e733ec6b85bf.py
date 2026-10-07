from pathlib import Path
import json
import sympy as s
x,y,z=s.symbols("x y z",real=True)
a=s.symbols("a",positive=True)
nu=s.symbols("nu",positive=True)
coords=[x,y,z]
g=s.diag(s.exp(2*a*z),s.exp(-2*a*z),1)
ginv=g.inv()
n=3
Gamma=[[[s.simplify(sum(ginv[i,l]*(s.diff(g[l,k],coords[j])+s.diff(g[l,j],coords[k])-s.diff(g[j,k],coords[l]))/2 for l in range(n))) for k in range(n)] for j in range(n)] for i in range(n)]
Ric=s.Matrix(n,n,lambda j,k:s.simplify(sum(s.diff(Gamma[i][j][k],coords[i])-s.diff(Gamma[i][j][i],coords[k])+sum(Gamma[i][i][l]*Gamma[l][j][k]-Gamma[i][k][l]*Gamma[l][j][i] for l in range(n)) for i in range(n))))
X=s.Matrix([0,0,1])
nablaX=s.Matrix(n,n,lambda i,j:s.simplify(sum(Gamma[i][j][k]*X[k] for k in range(n))))
SX=s.simplify((g*nablaX+(g*nablaX).T)/2)
normS=s.simplify(s.trace(ginv*SX*ginv*SX))
# Direct stress divergence: (div S)_j = g^{ik} nabla_i S_{kj}.
divS=s.Matrix(n,1,lambda j,_unused:s.simplify(sum(ginv[i,k]*(s.diff(SX[k,j],coords[i])-sum(Gamma[l][i][k]*SX[l,j]+Gamma[l][i][j]*SX[k,l] for l in range(n))) for i in range(n) for k in range(n))))
L=s.simplify(2*ginv*divS)
checks={
 "volume_constant":s.simplify(g.det()-1)==0,
 "Ricci":Ric==s.diag(0,0,-2*a*a),
 "strain_norm":s.simplify(normS-2*a*a)==0,
 "strain_eigenvalues":s.simplify(nablaX-s.diag(a,-a,0))==s.zeros(3),
 "deformation_laplacian":s.simplify(L-s.Matrix([0,0,-4*a*a]))==s.zeros(3,1),
 "harmonic_force_residual":s.simplify(L-2*ginv*Ric*X)==s.zeros(3,1),
 "power_sharp":s.simplify(((-nu*L).T*g*X)[0]-4*nu*a*a)==0,
}
# General trace-free 3D strain in frame e=X/|X|.
q,u,v,b,c=s.symbols("q u v b c",real=True)
S=s.Matrix([[u-q/2,v,b],[v,-u-q/2,c],[b,c,q]])
checks["general_quotient_block_identity"]=s.simplify(s.trace(S*S)-(2*(u*u+v*v)+s.Rational(3,2)*q*q+2*b*b+2*c*c))==0
# The transverse eigenvalues have c0 +/- sqrt(u^2+v^2), c0=-q/2.
checks["transverse_characteristic"]=s.expand(S[:2,:2].charpoly().as_expr()-((s.Symbol("lambda")+q/2)**2-u*u-v*v))==0
# Mapping torus A has positive eigenvalues and preserves its lattice.
A=s.Matrix([[2,1],[1,1]])
lam=(3+s.sqrt(5))/2
checks["cat_determinant"]=A.det()==1
checks["cat_eigenvalues"]=s.simplify(A.charpoly().as_expr().subs(s.Symbol("lambda"),lam))==0
allpass=all(checks.values())
output={"status":"PASS" if allpass else "FAIL","checks":checks,"exact_scope":"Symbolic Sol geometry and 3D strain identity; no entropy theorem or global compiler run."}
Path("work/cycle1/pde_transport_checks.json").write_text(json.dumps(output,indent=2)+"\n")
print(json.dumps(output,indent=2))
if not allpass:raise SystemExit(1)
