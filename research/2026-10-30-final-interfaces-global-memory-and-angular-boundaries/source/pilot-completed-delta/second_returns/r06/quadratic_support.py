"""Acquire and test an actual quadratic scalar minor-support rule.

The rule lambda(A)=L X(A)+M det(A) is sufficient only when its full global
support polynomial is nonnegative. Numerical testing does not establish that.
"""
from pathlib import Path
import json,math,time
import numpy as np
import sympy as S
from full_pc_search import energy_data,E,D

HERE=Path(__file__).resolve().parent
a,b,c,d,t=S.symbols('a b c d t',real=True);A=(a,b,c,d)
T=sum(x*x for x in A);q=a*d-b*c;X=a*a+c*c-b*b-d*d

def acoustic_support(tau):
    u=S.Rational(tau);B=1-3*u*u;H=1+3*u*u
    beta=B/H;r=4-12*u/H
    m=S.Poly(B*B*(1-t*t)**2-(1-4*u+3*u*u)*H*(1+t*t)**2,t).monic()
    K=[-B*(u*(1-t*t)+H*t*t)*(1+t*t),B*t*(H-u*(1-t*t))*(1+t*t),
       B*B*t*(1-t*t)-u*H*t*(1+t*t)**2,B*B*t*t*(1-t*t)+u*H*(1+t*t)**2]
    K=[S.rem(x,m.as_expr(),t) for x in K]
    F=T*T+4*(r-1)*q*q+4*beta*q*X
    FF=S.hessian(F,A)
    hv=FF*S.Matrix([1,t,0,0])
    lam=S.rem(hv[3].subs(dict(zip(A,K)),simultaneous=True).expand(),m.as_expr(),t)
    qk=S.rem((K[0]*K[3]-K[1]*K[2]).expand(),m.as_expr(),t)
    ratio=S.rem(lam*S.invert(qk,m.as_expr(),t),m.as_expr(),t)
    assert not S.Poly(ratio,t).degree()
    return {'tau':str(u),'beta':str(beta),'r':str(r),'lambda_over_q_at_acoustic_base':str(ratio),
            'X_over_q_at_acoustic_base':str(4*u/B)}

def numerical_support_rule(item,seed=60602):
    beta,r=float(S.Rational(item['beta'])),float(S.Rational(item['r']))
    j,k=float(S.Rational(item['lambda_over_q_at_acoustic_base'])),float(S.Rational(item['X_over_q_at_acoustic_base']))
    rng=np.random.default_rng(seed);vv=rng.normal(size=(12000,4));vv/=np.linalg.norm(vv,axis=1)[:,None]
    # Canonical rank-one-acoustic neighborhoods are deliberately included.
    C=float(-S.Poly((1-S.Rational(item['tau'])**2*3)**2*(1-t*t)**2-(1-4*S.Rational(item['tau'])+3*S.Rational(item['tau'])**2)*(1+3*S.Rational(item['tau'])**2)*(1+t*t)**2,t).monic().nth(2))
    root=math.sqrt((C-math.sqrt(C*C-4))/2)
    near=np.column_stack([np.ones(2000),root+rng.normal(0,.01,2000),np.zeros(2000),rng.normal(0,.01,2000)])
    near/=np.linalg.norm(near,axis=1)[:,None];vv=np.concatenate([vv,near])
    N0=[];N1=[]
    for v in vv:
        f,g,h,qv=energy_data(v,beta,r)
        N0.append(h/2-np.outer(g,g)/(4*f)-qv*j*E/2)
        N1.append(qv*(D-k*E/2))
    N0=np.array(N0);N1=np.array(N1)
    values=[]
    for L in np.linspace(-12,12,241):
        value=float(np.linalg.eigvalsh(N0-L*N1)[:,0].min());values.append((value,L))
    best=max(values)
    return {'best_sampled_minimum':best[0],'L':best[1],'M':j-k*best[1],
            'all_parameters_tested':len(values),'direction_count':len(vv)}

if __name__=='__main__':
    ans=[]
    for tau in ('1/30','1/6','1/5','1/4','3/10'):
        item=acoustic_support(tau);item['quadratic_rule_search']=numerical_support_rule(item);ans.append(item)
        print(json.dumps(item),flush=True)
    (HERE/'quadratic_support_result.json').write_text(json.dumps(ans,indent=2)+'\n')
