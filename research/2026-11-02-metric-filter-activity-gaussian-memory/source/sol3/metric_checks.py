#!/usr/bin/env python3
"""Finite checks of the new matrix-metric occupation and activity theorem.

Small dense matrices and second-quantization permanents are diagnostics only.
No proof observable Gamma(P) is assumed as a quantum operation by the compiler.
"""
from pathlib import Path
import sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent/'stage2'))
from loss_clock import CoupledBath,annihilators,gamma,expm,norm
import numpy as np
import math,json

sx=np.array([[0,1],[1,0]],complex)
sy=np.array([[0,-1j],[1j,0]],complex)
sz=np.diag([1.,-1.])

def pospow(x,p):
    v,u=np.linalg.eigh((x+x.conj().T)/2)
    assert v.min()>0
    return (u*v**p)@u.conj().T

def minimum(x):return float(np.linalg.eigvalsh((x+x.conj().T)/2).min())

def adjoint(O,G,Ls,eta=1.):
    z=G.conj().T@O+O@G
    for L in Ls:z+=eta*L.conj().T@O@L
    return z

def liouv(G,Ls,eta=1.):
    d=len(G);z=np.kron(np.eye(d),G)+np.kron(G.conj(),np.eye(d))
    for L in Ls:z+=eta*np.kron(L.conj(),L)
    return z

def dg(x,bs):
    return sum(x[i,j]*bs[i].conj().T@bs[j] for i in range(len(bs)) for j in range(len(bs)))

def model(A,E,metric,gap,cc,qq,K=2):
    M=len(A);states,bs=annihilators(M,K);db=len(states);dd=2*db
    G0=dg(A,bs);Hs=.5*sy+.3*sz
    D=np.kron(Hs,np.eye(db))
    for c,Q in zip(cc,qq):
        B=sum(c[i]*bs[i] for i in range(M));D+=np.kron(Q,B+B.conj().T)
    G=np.kron(np.eye(2),G0)-1j*D
    lbs=[sum(E[i,j].conjugate()*bs[i] for i in range(M)) for j in range(E.shape[1])]
    Ls=[np.kron(np.eye(2),L) for L in lbs]
    ap=sum(norm(Q)*np.linalg.norm(c@pospow(metric,.5)) for Q,c in zip(qq,cc))
    ai=sum(norm(Q)*np.linalg.norm(c@pospow(metric,-.5)) for Q,c in zip(qq,cc))
    return dict(A=A,E=E,P=metric,gap=gap,cc=cc,states=states,bs=bs,db=db,G0=G0,G=G,Ls=Ls,lbs=lbs,
                ap=float(ap),ai=float(ai),mu=float(4*ap*ap/gap**2),activity=float(4*ap*ai/gap))

def operator_checks(m):
    pp=m['P'];gap=m['gap'];M=len(pp);bs=m['bs'];db=m['db'];z=2.
    Rz=np.eye(M)+(z-1)*pp;Wb=gamma(Rz,2);W=np.kron(np.eye(2),Wb)
    derivative=np.kron(np.eye(2),Wb@dg(pp@np.linalg.inv(Rz),bs))
    rhs=-(gap/2)*(z-1)*derivative+(2*m['ap']**2/gap)*(z-1)*W
    Wmi=pospow(W,-.5)
    occ=minimum(Wmi@(rhs-adjoint(W,m['G'],m['Ls']))@Wmi)
    theta=.8;eta=math.exp(theta);s=(eta-1)*m['ai']/m['ap']
    Rt=eta*np.eye(M)+s*pp;Wtb=gamma(Rt,2);Wt=np.kron(np.eye(2),Wtb);Wti=pospow(Wt,-.5)
    count=minimum(Wti@(m['activity']*(eta-1)*Wt-adjoint(Wt,m['G'],m['Ls'],eta))@Wti)
    # Free counted observable identity, for a noncommuting matrix R.
    t=.31;F=expm(m['A']*t)
    target=gamma(eta*np.eye(M)+F.conj().T@(Rt-eta*np.eye(M))@F,2)
    G0=m['G0'];ldg=np.kron(np.eye(db),G0.conj().T)+np.kron(G0.T,np.eye(db))
    for L in m['lbs']:ldg+=eta*np.kron(L.T,L.conj().T)
    actual=(expm(ldg*t)@Wtb.reshape(-1,order='F')).reshape(db,db,order='F')
    identity=norm(actual-target)
    assert occ>-3e-6,occ
    assert count>-3e-6,count
    assert identity<3e-6,identity
    return {'occupation_operator_slack_min':occ,'count_operator_slack_min':count,'free_counted_Gamma_identity_error':identity,
            'metric_minus_I_min':minimum(pp-np.eye(M)),
            'Lyapunov_slack_min':minimum(-gap*pp-(m['A'].conj().T@pp+pp@m['A']))}

def process_checks(m):
    db=m['db'];d=2*db;ket=np.array([1.,1j])/math.sqrt(2);rho=np.zeros((db,db),complex);rho[0,0]=1
    rho=np.kron(np.outer(ket,ket.conj()),rho);x=rho.reshape(-1,order='F')
    us=expm(-.47j*sx);u=np.kron(us,np.eye(db));ctrl=np.kron(u.conj(),u)
    vals=[];z=2.;eta=math.e
    occ=gamma(np.eye(len(m['P']))+(z-1)*m['P'],2)
    nt=np.diag([z**sum(n) for n in m['states']]);O=np.kron(np.eye(2),occ);Nw=np.kron(np.eye(2),nt)
    s=(eta-1)*m['ai']/m['ap'];Rt=eta*np.eye(len(m['P']))+s*m['P'];Ct=np.kron(np.eye(2),gamma(Rt,2))
    L0=liouv(m['G'],m['Ls']);Lt=liouv(m['G'],m['Ls'],eta)
    for T in [.1,1.,10.]:
        e=expm(L0*T/2);y=(e@ctrl@e@x).reshape(d,d,order='F')
        e=expm(Lt*T/2);yt=(e@ctrl@e@x).reshape(d,d,order='F')
        a=float(np.trace(O@y).real);b=float(np.trace(Nw@y).real)
        c=float(np.trace(yt).real);cw=float(np.trace(Ct@yt).real)
        ob=math.exp(m['mu']*(z-1));cb=math.exp(m['activity']*(eta-1)*T)
        assert b<=a+3e-6
        assert a<=ob+3e-6
        assert c<=cw+3e-6
        assert cw<=cb+3e-6*cb
        vals.append({'T':T,'occupation_Gamma_metric_MGF':a,'ordinary_number_MGF':b,'uniform_occupation_upper':ob,
                     'actual_count_MGF':c,'count_plus_metric_MGF':cw,'proved_count_upper':cb,
                     'density_trace':float(np.trace(y).real)})
    return vals

if __name__=='__main__':
    (P/'results').mkdir(exist_ok=True)
    rows=[]
    for R in [4.,40.,4000.,400000.]:
        b=CoupledBath(R);pp=3*np.array([[1,1/(2*math.sqrt(R))],[1/(2*math.sqrt(R)),.5]],complex)
        m=model(b.A,b.E,pp,.5,[b.c],[sx]);v=operator_checks(m)
        row={'R':R,'mu':m['mu'],'activity_rate_upper':m['activity'],**v,'process':process_checks(m)}
        rows.append(row);print(json.dumps({k:v for k,v in row.items() if k!='process'}),flush=True)
    rng=np.random.default_rng(1512);generic=[]
    for trial in range(6):
        M=2+trial%2;r=1+trial%M
        X=rng.normal(size=(M,M))+1j*rng.normal(size=(M,M));H=(X+X.conj().T)/2
        E=(rng.normal(size=(M,r))+1j*rng.normal(size=(M,r)))/2
        A=-1j*H-E@E.conj().T/2
        # Acquired dense one-particle Lyapunov solve, not a favorable norm promise.
        op=np.kron(np.eye(M),A.conj().T)+np.kron(A.T,np.eye(M))
        pp=np.linalg.solve(op,-np.eye(M).reshape(-1,order='F')).reshape(M,M,order='F');pp=(pp+pp.conj().T)/2
        ev=np.linalg.eigvalsh(pp);assert ev.min()>0
        gap=.9/ev.max();pp*=1.1/ev.min()
        cc=[.04*(rng.normal(size=M)+1j*rng.normal(size=M)) for _ in range(2)]
        m=model(A,E,pp,gap,cc,[sx,sz]);row={'trial':trial,'M':M,'ports':r,'gap':gap,'mu':m['mu'],'activity':m['activity'],**operator_checks(m)}
        generic.append(row);print(json.dumps(row),flush=True)
    out={'scope':'Finite operator inequalities, counted free Gaussian identity, and actual noncommuting controlled-process MGFs. Not independent proof review or scalable circuit execution.',
         'rank_one_stiffness_family':rows,'separate_complex_multiport_networks':generic}
    (P/'results/metric_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS: metric occupation and activity inequalities; exact count tilt is handled without normalized-state assumptions.',flush=True)
