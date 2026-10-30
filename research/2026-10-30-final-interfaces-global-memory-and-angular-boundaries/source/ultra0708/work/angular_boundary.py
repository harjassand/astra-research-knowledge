"""Local closed-form acquisition on a curved ROC boundary. No numerical proof."""
from pathlib import Path
import json, time, os
import numpy as np
import sympy as S
import cvxpy as cp

HERE = Path(os.environ.get('ASTRA_ANGULAR_CASE',Path(__file__).parent))

def degrees(total,n):
    if n==1:
        yield (total,)
    else:
        for j in range(total+1):
            for p in degrees(total-j,n-1):
                yield (j,)+p

def build():
    start=time.perf_counter()
    A=S.symbols('a b c d',real=True)
    powers=list(degrees(5,4)); swap=(1,0,3,2); signs=(1,-1,-1,1)
    keys=[(i,p) for i in range(4) for p in powers
          if signs[i]*S.prod(signs[j]**p[j] for j in range(4))==-1]
    seen=set(); basis=[]
    for key in keys:
        if key in seen: continue
        i,p=key; other=(swap[i],tuple(p[swap[j]] for j in range(4)))
        seen.update((key,other)); v=S.zeros(4,1)
        v[i]+=S.prod(A[j]**p[j] for j in range(4))
        k,q=other; v[k]-=S.prod(A[j]**q[j] for j in range(4)); basis.append(v)
    z=S.symbols('z:'+str(len(basis)))
    P=sum((v*c for v,c in zip(basis,z)),S.zeros(4,1))
    J=S.Matrix([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]])
    lie=P.jacobian(A)*J*S.Matrix(A)+J.T*P
    eq=[v for ex in lie for v in S.Poly(S.expand(ex),A).coeffs()]
    M,_=S.linear_eq_to_matrix(eq,z); N=S.Matrix.hstack(*M.nullspace())
    v=S.symbols('v:'+str(N.cols)); P=S.expand(P.subs(dict(zip(z,N*S.Matrix(v)))))
    T=sum(a*a for a in A); jac=P.jacobian(A); W=S.zeros(4)
    for i in range(4):
        for j in range(i+1,4):
            W[i,j]=S.expand(T*(jac[j,i]-jac[i,j])-2*(A[i]*P[j]-A[j]*P[i]))
            W[j,i]=-W[i,j]
    rows=[]
    for i in range(4):
        for j in range(i+1,4):
            for val in S.Poly(W[i,j],A).coeffs(): rows.append([S.diff(val,x) for x in v])
    piv=S.Matrix(rows).rref()[1]; gauge={v[j]:0 for j in range(len(v)) if j not in piv}
    P=P.subs(gauge); W=W.subs(gauge); v=[x for x in v if x not in gauge]
    beta,r=S.symbols('beta r',real=True); q=A[0]*A[3]-A[1]*A[2]
    X=A[0]**2+A[2]**2-A[1]**2-A[3]**2
    F=T*T+4*(r-1)*q*q+4*beta*q*X; H=S.hessian(F,A)
    h=S.symbols('h0:6'); B1=S.Matrix([h[0],h[1],h[3],h[4]])
    B2=S.Matrix([h[1],h[2],h[4],h[5]])
    C=S.hessian(S.expand(T*T*(B1.T*H*B1+B2.T*H*B2)[0]+(B1.T*W*B2)[0]),h)/2
    out={'variables':[str(x) for x in v], 'P':[str(x) for x in P],
         'W':[[str(x) for x in row] for row in W.tolist()],
         'C':[[str(S.expand(x)) for x in row] for row in C.tolist()],
         'seconds':time.perf_counter()-start}
    (HERE/'angular_family.json').write_text(json.dumps(out))
    print('built',len(v),'effective parameters',out['seconds'],flush=True)

def acquire(beta_value=S.Rational(11,13),r_value=S.Rational(28,13),exact_jets=False):
    start=time.perf_counter(); data=json.loads((HERE/'angular_family.json').read_text())
    config=json.loads((HERE/'case_config.json').read_text()) if (HERE/'case_config.json').exists() else {'k':'4/11','z2':'65/81'}
    beta_value=S.Rational(config.get('beta',beta_value));r_value=S.Rational(config.get('r',r_value))
    a,b,c,d,beta,r=S.symbols('a b c d beta r',real=True)
    v=[S.Symbol(n,real=True) for n in data['variables']]
    loc={str(x):x for x in (a,b,c,d,beta,r,*v)}
    C=S.Matrix([[S.sympify(x,locals=loc) for x in row] for row in data['C']])
    C=C.subs({a:1,c:0,beta:beta_value,r:r_value})
    if exact_jets:
        jj=json.loads((HERE/'boundary_jets.json').read_text())
        C=C.subs(dict(zip(v,[S.sympify(x,locals=loc) for x in jj['solution']])),simultaneous=True)
        C=C.applyfunc(S.expand); v=[loc[n] for n in jj['free']]
    zero=dict.fromkeys(v,0)
    pieces=[C.subs(zero)]+[C.diff(p) for p in v]
    funcs=[S.lambdify((b,d),p,'numpy',cse=True) for p in pieces]
    points=[]
    N=14
    for i in range(N+1):
        for j in range(-N,N+1):
            if i*i+j*j<=N*N: points.append((i/N,j/N))
    # Interior canonical-disk representatives of acoustic zero gradients.
    av=S.Matrix([a,b,c,d]); T=(av.T*av)[0]; q=a*d-b*c; X=a*a+c*c-b*b-d*d
    F=T*T+4*(r_value-1)*q*q+4*beta_value*q*X
    hf=S.lambdify((a,b,c,d),S.hessian(F,av),'numpy',cse=True)
    bv=float(beta_value); rv=float(r_value)
    if bv>0.5 and bv<1:
        ss=(1-2/np.sqrt(3)*np.sqrt(1-bv*bv))/(bv*bv)
        th=np.arccos(np.sqrt(ss))
        for theta in [th,-th,np.pi-th,np.pi+th]:
            RR=np.array([np.cos(theta/2),np.sin(theta/2),0,0])
            vals,vec=np.linalg.eigh(hf(*RR)); AA=vec[:,0].reshape(2,2)
            if np.linalg.norm(AA[:,0])<np.linalg.norm(AA[:,1]): AA=AA[:,::-1]
            col=AA[:,0]; scale=np.linalg.norm(col)
            rot=np.array([[col[0],col[1]],[-col[1],col[0]]])/scale
            AA=rot@AA/scale
            points.append((abs(float(AA[0,1])),float(AA[1,1])))
    y=cp.Variable(len(v)); margin=cp.Variable(); constraints=[]
    for point_index,(bb,dd) in enumerate(points):
        TT=1+bb*bb+dd*dd
        mats=[np.array(f(bb,dd),dtype=float)/TT**3 for f in funcs]
        target=cp.Constant(mats[0])
        for i in range(len(v)): target+=y[i]*mats[i+1]
        if exact_jets:
            xx=(1-bb*bb-dd*dd)/TT; zz=2*dd/TT
            weight=(xx-float(S.Rational(config['k']))*zz)**2+(zz*zz-float(S.Rational(config['z2'])))**2
            if point_index>=len(points)-4:
                gram=sum(mm.T@mm for mm in mats)
                vals,vecs=np.linalg.eigh(gram)
                Q=vecs[:,vals>1e-7]
                print('zero-face dimension',Q.shape[1],flush=True)
                constraints.append(Q.T@target@Q >> 0)
                continue
        else: weight=1
        constraints.append(target-margin*weight*np.eye(6)>>0)
    model=cp.Problem(cp.Maximize(margin),constraints)
    err=None
    try: model.solve(solver='CLARABEL',tol_gap_abs=1e-9,tol_gap_rel=1e-9,tol_feas=1e-9,max_iter=180)
    except Exception as e: err=repr(e)
    out={'beta':str(beta_value),'r':str(r_value),'points':len(points),
         'status':model.status,'error':err,
         'margin':None if margin.value is None else float(margin.value),
         'parameters':None if y.value is None else dict(zip(map(str,v),y.value.tolist())),
         'seconds':time.perf_counter()-start,
         'scope':'Finite proposal only; not a certificate or global infeasibility theorem.'}
    (HERE/('boundary_jet_proposal.json' if exact_jets else 'boundary_proposal.json')).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2),flush=True)

if __name__=='__main__':
    import sys
    if '--build' in sys.argv: build()
    if '--acquire' in sys.argv: acquire()
    if '--jets' in sys.argv: acquire(exact_jets=True)
