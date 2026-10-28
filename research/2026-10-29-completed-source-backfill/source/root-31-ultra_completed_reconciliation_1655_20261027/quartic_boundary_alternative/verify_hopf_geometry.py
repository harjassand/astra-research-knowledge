#!/usr/bin/env python3
"""Exact general-coefficient algebra checks, independent of numerical searches."""
from pathlib import Path
import json,time
import sympy as S

def main():
 started=time.perf_counter()
 k,l,m,n,p,r,a,b,c,d,g,e,f,z=S.symbols('k l m n p r a b c d g e f z',real=True)
 v=S.Matrix([a,b,c,d])
 h=S.Matrix([a*a+c*c-b*b-d*d,2*(a*b+c*d),2*(a*d-b*c)])
 T=a*a+b*b+c*c+d*d
 assert S.expand(T*T-(h.T*h)[0])==0
 K=S.Matrix([[k,l,m],[l,n,p],[m,p,r]])
 F=(h.T*K*h)[0]
 order=[0,2,1,3]
 Q=(S.hessian(F,v)/2).subs({a:1,b:0,c:0,d:0}).extract(order,order)
 B=S.Matrix([[6*k,0,6*l,6*m],[0,2*k,-2*m,2*l],
             [6*l,-2*m,4*n-2*k,4*p],[6*m,2*l,4*p,4*r-2*k]])
 assert S.simplify(Q-B)==S.zeros(4)
 grad=S.Matrix([S.diff(F,x) for x in v]).subs({a:1,b:0,c:0,d:0}).extract(order,[0])
 Tf=B-grad*grad.T/(4*k)
 C=S.Matrix([[g,0,e,f],[0,g,-f,e],[e,-f,-g,0],[f,e,0,-g]])
 W=(Tf-z*C/2)/2
 alpha=k-z*g/4
 Schur=W[2:4,2:4]-W[2:4,:2]*W[:2,2:4]/alpha
 St=S.Matrix([[n,p],[p,r]])-S.Matrix([l,m])*S.Matrix([[l,m]])/k
 norm=alpha**2+(l-z*e/4)**2+(m-z*f/4)**2
 assert S.simplify(Schur-2*St+norm/alpha*S.eye(2))==S.zeros(2)
 assert S.simplify(St.det()-K.det()/k)==0

 coeff=S.symbols('p0:9')
 u=a*a+c*c;vv=b*b+d*d;w=a*b+c*d;q=a*d-b*c
 literal=sum(x*y for x,y in zip(coeff,(u*u,vv*vv,u*vv,w*w,u*w,vv*w,q*u,q*vv,q*w)))
 pp=coeff;al=(pp[0]+pp[1]+pp[2])/4
 KH=S.Matrix([[(pp[0]+pp[1])/2,(pp[4]-pp[5])/8,(pp[6]-pp[7])/8],
              [(pp[4]-pp[5])/8,al+pp[3]/4,pp[8]/8],
              [(pp[6]-pp[7])/8,pp[8]/8,al]])
 ell=S.Matrix([(pp[0]-pp[1])/2,(pp[4]+pp[5])/4,(pp[6]+pp[7])/4])
 assert S.expand(literal-(h.T*KH*h)[0]-T*(ell.T*h)[0])==0

 tau,lam=S.symbols('tau lam',real=True)
 family=u*u+vv*vv+3*w*w+(tau-lam)*q*q+4*q*(u-vv)
 restricted=(S.hessian(family,v)/2).subs({a:1,b:0,c:0,d:1}).extract([0,3],[0,3])
 sigma=tau-lam
 assert restricted==S.Matrix([[sigma+18,2*sigma],[2*sigma,sigma-6]])
 assert S.expand(restricted.det()+3*((sigma-2)**2+32))==0
 result={'status':'PASS','literal_nine_coefficient_conversion':True,
         'general_Hopf_acoustic_Hessian':True,'support_Schur_reduction':True,
         'tangent_Schur_determinant_identity':True,
         'all_tau_polynomial_lift_Hessian_extension':True,
         'elapsed_seconds':time.perf_counter()-started}
 (Path(__file__).resolve().parent/'GEOMETRY_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))

if __name__=='__main__':main()
