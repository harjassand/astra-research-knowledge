#!/usr/bin/env python3
"""Exact source-disabled statistical checks. No random generator or source queries."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction
import itertools, json
import sympy as S
Q=S.Rational; I=S.I
p=[S.eye(2),S.Matrix([[0,1],[1,0]]),S.Matrix([[0,-I],[I,0]]),S.diag(1,-1)]
def kron(a,b): return S.kronecker_product(a,b)
def simp(a): return a.applyfunc(S.simplify)
def eq(a,b): return simp(a-b)==S.zeros(*a.shape)
def channel(ks,a): return simp(sum((k*a*k.H for k in ks),S.zeros(ks[0].rows)))
def choi(ks):
    d=ks[0].cols; ans=S.zeros(2*d)
    for a in range(d):
        for b in range(d):
            e=S.zeros(d);e[a,b]=1
            ans+=kron(channel(ks,e),e)/d
    return simp(ans)
def tp(ks): return eq(sum((k.H*k for k in ks),S.zeros(ks[0].cols)),S.eye(ks[0].cols))
def pout(a,d): return a[:d,:d]+a[d:,d:]
def paulis(w):
    for labels in itertools.product(range(4),repeat=w):
        z=S.ones(1)
        for j in labels: z=kron(z,p[j])
        yield z
A0=S.diag(1,Q(4,5)); A1=S.Matrix([[0,Q(3,5)],[0,0]])
U=Q(3,5)*p[0]+Q(4,5)*I*p[1]
Cg=S.zeros(4)
for l,g in itertools.product(range(2),repeat=2): Cg[2*(l^g)+g,2*l+g]=1
U4=kron(U,S.diag(1,I))*Cg
append=[kron(S.eye(2),Q(3,5)*S.Matrix([1,0])),kron(S.eye(2),Q(4,5)*S.Matrix([0,1]))]
traceg=[kron(S.eye(2),S.Matrix([[1,0]])),kron(S.eye(2),S.Matrix([[0,1]]))]
sources=[('identity',[S.eye(2)]),('nonunital_amplitude',[A0,A1]),('complex_nonunital',[U*A0,U*A1]),('mixed_gauge_complex',[U4*a*k for a in append for k in [A0,A1]])]
results=[]; normcases=0; events=0; badtranspose=0
for name,ks in sources:
    assert tp(ks)
    d=ks[0].rows;w=d.bit_length()-1; ws=list(paulis(w)); H=S.zeros(2*d); Hbad=S.zeros(2*d)
    for j in range(1,4):
        for s in [-1,1]:
            rho=channel(ks,(p[0]+s*p[j])/2)
            for W in ws:
                z=S.simplify(S.trace(W*rho)); assert z.is_real
                for b in [-1,1]:
                    pr=S.simplify((1+b*z)/(12*d*d)); assert pr>=0
                    grad=-Q(d*d,2)*s*b*kron(p[j],W.T)
                    H+=pr*grad; Hbad+=pr*(-Q(d*d,2)*s*b*kron(p[j],W))
                    assert S.simplify(S.trace(grad.H*grad))==Q(d**5,2)
                    assert eq(grad*grad,Q(d**4,4)*S.eye(2*d))
                    events+=1;normcases+=1
    target=-Q(d,12)*sum((kron(p[j],channel(ks,p[j]).T) for j in range(1,4)),S.zeros(2*d))
    assert eq(H,target)
    if not eq(Hbad,target): badtranspose+=1
    decoders=([('id',[S.eye(2)]),('rotate',[U.H]),('nonunital',[A0,A1])] if d==2 else [('unencode',[v*U4.H for v in traceg]),('trace',traceg),('nonunital_trace',[a*v for a in [A0,A1] for v in traceg])])
    for dn,ds in decoders:
        assert tp(ds); J=choi(ds); assert eq(pout(J,d),S.eye(d)/d)
        risk=S.Integer(0)
        for j in range(1,4):
            for s in [-1,1]:
                rr=channel(ds,channel(ks,(p[0]+s*p[j])/2))
                risk+=(1-s*S.trace(p[j]*rr))/12
        risk=S.simplify(risk)
        linear=S.simplify(Q(1,2)+S.trace(H*J))
        fe=S.simplify(sum((S.trace(a*k)*S.conjugate(S.trace(a*k)) for a in ds for k in ks),S.Integer(0))/4)
        assert risk==linear==S.simplify(Q(2,3)*(1-fe))
        results.append({'source':name,'decoder':dn,'dimension':d,'six_state_error':str(risk),'Bell_loss':str(1-fe)})
assert badtranspose==len(sources)
# Explicit rational Choi repair and uniform grid/objective arithmetic.
repairs=[]
for d in [2,4]:
    ds=[S.eye(2)] if d==2 else traceg
    K=d*choi(ds)
    for den in [1024,16384]:
        delta=Q(1,den); Ktilde=K-delta*kron(p[3],S.eye(d))
        Khat=Ktilde+kron(p[0]/2,S.eye(d)-pout(Ktilde,d))
        Kphys=(Khat+2*delta*S.eye(2*d))/(1+4*delta)
        assert eq(pout(Kphys,d),S.eye(d))
        assert all(x>0 for x in Kphys.eigenvals())
        dif=Kphys/d-Ktilde/d
        assert S.simplify(S.trace(dif.H*dif))<=81*delta**2
        repairs.append({'d':d,'delta':str(delta),'strict_PSD':True,'exact_TP':True})
params=[]
for w in range(1,7):
    d=2**w; G=d*d*2**((w+1)//2)
    for ep in [Fraction(1),Fraction(1,2),Fraction(1,16),Fraction(1,100)]:
        N=1
        while N<(6*G/ep)**2:N*=4
        root=1
        while root*root<N:root*=2
        eta=Fraction(1,G*root);xi=Fraction(1,16*N*N);delta=xi/1024;u=xi/(65536*d)
        assert u<=min(delta/(64*d),xi/(1024*d))
        assert delta<=xi/1000 and delta<=Fraction(1,100)
        assert 4*d*u<=delta/16 and 8*d*u<=delta/8
        # 4u bounds normalized grid displacement; 28u is a safe objective debit.
        assert xi/8+xi/4+100*delta+28*u<xi
        regret=Fraction(1,2)/eta+eta*N*G*G/2+Fraction(3,1)*N*Fraction(1,4*N)/(2*eta)
        assert regret==Fraction(11,8)*G*root
        assert Fraction(3*G,root)<=ep/2
        assert N<144*G*G/(ep*ep)<=288*d**5/(ep*ep)
        nu=Fraction(1,100);R=0
        while 2**R<Fraction(2*N,1)/nu:R+=1
        assert Fraction(N,4**R)<=nu
        params.append({'w':w,'epsilon':str(ep),'N':N,'R':R,'random_bit_cap':N*(2*w+1+2*R)+(N.bit_length()-1)})
# Approx-projection squared-distance constant is 2sqrt(2)<3.
assert 8<9
root=Path(__file__).resolve().parent
src=root/'ordinary_prequential_terminal_memory_recovery_20261028.md'
expected='20e59391aeab608e0fb76dbaee3fee6825d434991892a2c63fe5e57634316079'
assert sha256(src.read_bytes()).hexdigest()==expected
out={'status':'PASS','source_sha256':expected,'source_calls':0,'random_draws':0,'source_acquisition_simulations':0,'actual_Born_event_terms':events,'deterministic_gradient_norm_cases':normcases,'conditional_channel_gradient_cases':len(sources),'wrong_transpose_detected_cases':badtranspose,'six_state_Choi_Bell_cases':results,'exact_rational_repair_cases':repairs,'finite_budget_cases':params,'scope':'Finite exact identities only; no simulated count learner or high-probability terminal claim.'}
path=root/'prequential_terminal_memory_statistics_check_20261028.json'
path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['six_state_Choi_Bell_cases','exact_rational_repair_cases','finite_budget_cases']},indent=2))
print('six_state_cases',len(results),'repair_cases',len(repairs),'budget_cases',len(params))
