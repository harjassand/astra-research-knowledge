"""Independent exact replay of the acquired nontranslation QC heat certificates.
No optimizer, sampled positivity, or prior null-column assertion is trusted.
"""
from pathlib import Path
import ast
import sympy as S
x,y,u,v=S.symbols('x y u v',real=True);Z=S.Matrix([x,y,u,v]);h=S.Matrix(S.symbols('h0:6',real=True));r=x*x+y*y;t=u*u+v*v
symbols={str(z):z for z in [*Z,*h]}
Jx=S.Matrix([h[0]+h[4],h[3]-h[1],h[0]-h[4],h[3]+h[1]]).jacobian(h);Jy=S.Matrix([h[1]+h[5],h[4]-h[2],h[1]-h[5],h[4]+h[2]]).jacobian(h)
def readexpr(a):return S.sympify(a,locals=symbols)
def verify(filename,sign):
    data=ast.literal_eval(Path(__file__).with_name(filename).read_text());lam=S.Rational(data['lambda']);P=t*t+2*r*t+x*(u*u-v*v)+sign*2*y*u*v+lam*(r+t)
    alpha=S.Matrix([readexpr(a) for a in data['primitive']]);W=alpha.jacobian(Z).T-alpha.jacobian(Z);HF=S.hessian(P,Z);temp=Jx.T*W*Jy;B=Jx.T*HF*Jx+Jy.T*HF*Jy+(temp+temp.T)/2
    L=S.Matrix([readexpr(a) for a in data['features']]);G=S.Matrix([[S.Rational(a) for a in row] for row in data['Gram']]);assert G==G.T
    identity=S.Poly(S.expand((h.T*B*h)[0]-(L.T*G*L)[0]),[*Z,*h]);assert identity.is_zero
    # Exact rational LDL elimination; every pivot is strictly positive.
    n=G.rows;T=G.copy();pivs=[]
    for i in range(n):
        p=T[i,i];assert p>0;pivs.append(p)
        for j in range(i+1,n):
            for k in range(j,n):T[j,k]=T[k,j]=T[j,k]-T[j,i]*T[k,i]/p
    print(filename,': full polynomial identity and',n,'positive rational pivots PASSED; lambda=',lam)
    return lam
if __name__=='__main__':
    verify('sos_certificate_99_500.txt',+1)
    verify('sos_minus_certificate_27_100.txt',-1)
    print('These certify global QC by actual compatible ordinary heat flow and Stokes.')
    print('Sharp ROC boundary P0 at lambda=3/16 remains unresolved.')
