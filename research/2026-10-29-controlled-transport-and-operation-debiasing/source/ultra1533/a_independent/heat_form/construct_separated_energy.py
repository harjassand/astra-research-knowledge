"""Construct a quartic with an output-skew proof and a scalar-flow separator.

The same SDP is given actual minors-Jensen cuts as a non-PC constraint.
All results remain floating proposals pending exact qualification.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
import sympy as sp
import cvxpy as cp
from compile_sos import acquire

HERE=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--positive',action='store_true');args=ap.parse_args()
    start=time.perf_counter()
    _,gram,J,_,_,base=acquire('hopf')
    aa=sp.symbols('a b c d');hh=sp.symbols('h0:6');a,b,c,d=aa
    u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
    polys=[u*u,v*v,u*v,w*w,u*w,v*w,q*u,q*v,q*w]
    B1=sp.Matrix([hh[0],hh[1],hh[3],hh[4]])
    B2=sp.Matrix([hh[1],hh[2],hh[4],hh[5]])
    JJ=sp.Matrix([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]])
    maps=[]
    for f in polys:
        H=sp.hessian(f,aa)
        expr=[(B1.T*H*B1)[0],(B1.T*H*B2)[0],(B2.T*H*B2)[0],
              (B1.T*H*JJ*B2)[0]+(B2.T*H*JJ*B1)[0]]
        maps.append([[float(sp.Poly(sp.expand(e),aa+hh).coeff_monomial(m)) for m in base['monomials']] for e in expr])
    E11,E12,E22,Cross=np.array(maps).transpose(1,2,0)
    l=np.array(json.loads((HERE/'param_a12_b3.975_CLARABEL_proposal.json').read_text())['equality_dual'])
    # Exact old three-atom minors-Jensen witness, with A fixed nonzero.
    A=sp.Matrix([36,0,0,35])
    Xs=[sp.Matrix([-sp.Rational(264,28745),-sp.Rational(63481,114980),sp.Rational(5771,143725),sp.Rational(528,28745)]),
        sp.Matrix([0,sp.Rational(11,20),-sp.Rational(1,25),0]),sp.Matrix([sp.Rational(12,5),0,0,-sp.Rational(24,5)])]
    ws=[sp.Rational(5749,11542),sp.Rational(1,2),sp.Rational(11,5771)]
    witness=np.array([float(sum(weight*f.subs(dict(zip(aa,A+X))) for weight,X in zip(ws,Xs))-f.subs(dict(zip(aa,A)))) for f in polys])
    fstar_witness=np.array([49,49,49,0,0,0,1176/25,1176/25,0.])
    P=cp.Variable(9);Q=cp.Variable((24,24),symmetric=True);t=cp.Variable(80);margin=cp.Variable()
    nu=-.1
    eq=gram@cp.vec(Q,order='C')==((E11+E22)+nu*Cross)@P+J@t
    Lam=cp.bmat([[cp.reshape(l@E11@P,(1,1),order='C'),cp.reshape(l@E12@P,(1,1),order='C')],
                 [cp.reshape(l@E12@P,(1,1),order='C'),cp.reshape(l@E22@P,(1,1),order='C')]])
    constraints=[eq,Q-margin*np.eye(24)>>0,-Lam-margin*np.eye(2)>>0,P[0]+P[1]==2,
                 P<=100,P>=-100]
    # Require a non-PC violation. Positive energies need the nonzero-background
    # witness; energies without the positivity requirement may use either one.
    cut=witness if args.positive else fstar_witness
    cut=cut/np.linalg.norm(cut)
    constraints.append(cut@P<=-margin)
    G=None
    if args.positive:
        z2=[sp.prod(aa[k]**e[k] for k in range(4)) for e in __import__('compile_sos').degree(2,4)]
        m4=list(__import__('compile_sos').degree(4,4));G=cp.Variable((10,10),symmetric=True)
        L=np.zeros((35,100));Fcoef=np.zeros((35,9))
        for i,mon in enumerate(m4):
            for j,f in enumerate(polys):Fcoef[i,j]=float(sp.Poly(f,aa).coeff_monomial(mon))
            for j,x in enumerate(z2):
                for k,y in enumerate(z2):L[i,10*j+k]=float(sp.Poly(x*y,aa).coeff_monomial(mon))
        constraints += [L@cp.vec(G,order='C')==Fcoef@P,G-margin*np.eye(10)>>0]
    problem=cp.Problem(cp.Maximize(margin),constraints)
    acq=time.perf_counter()-start;t0=time.perf_counter()
    problem.solve(solver='CLARABEL',max_iter=250,tol_gap_abs=1e-9,tol_feas=1e-9,tol_gap_rel=1e-9)
    result=dict(positive=args.positive,status=problem.status,value=problem.value,nu=nu,
                acquisition_seconds=acq,solver_seconds=time.perf_counter()-t0,
                p=None if P.value is None else P.value.tolist(),Q=None if Q.value is None else Q.value.tolist(),
                alpha=None if t.value is None else t.value.tolist(),
                Fgram=None if G is None or G.value is None else G.value.tolist(),
                lambda_proposal=l.tolist(),witness=cut.tolist())
    (HERE/f'{"positive_" if args.positive else ""}SEPARATED_ENERGY_PROPOSAL.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['Q','alpha','Fgram','lambda_proposal','witness']},indent=2))

if __name__=='__main__':main()
