"""Low-support factorization and physical Petz tests for lossy channels.
No recovery SDP is used; optima are analytic for the named benchmark families.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np

HERE=Path(__file__).resolve().parent
rng=np.random.default_rng(206031)
def unitary(n):
    X=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));return np.linalg.qr(X)[0]
def channel(k,d,s):
    assert d*s>=k
    X=rng.normal(size=(d*s,k))+1j*rng.normal(size=(d*s,k));Q=np.linalg.qr(X)[0]
    return [Q[j*d:(j+1)*d] for j in range(s)]
def choi(Ks,k):return sum(np.outer(K.T.reshape(-1),K.T.reshape(-1).conj()) for K in Ks)/k
def fe(Rs,Ks,k):return float(sum(abs(np.trace(R@K))**2 for R in Rs for K in Ks)/k**2)
def norm1(X):return float(sum(abs(np.linalg.eigvalsh((X+X.conj().T)/2))))
def learned_petz(Ks,k,d,a):
    h=k*d;J=choi(Ks,k);C=(J+2*a*np.eye(h))/(1+2*h*a)
    vals,v=np.linalg.eigh(C);Q=(v*np.sqrt(vals))@v.conj().T
    learned=[np.sqrt(k)*Q[:,j].reshape(k,d).T for j in range(h)]
    S=sum(K@K.conj().T for K in learned)/k;sv,w=np.linalg.eigh(S)
    inv=(w*(1/np.sqrt(sv)))@w.conj().T
    Rs=[K.conj().T@inv/np.sqrt(k) for K in learned]
    residual=float(np.linalg.norm(sum(R.conj().T@R for R in Rs)-np.eye(d),2))
    assert residual<1e-10
    return Rs,min(1,k*norm1(C-J)/2),residual

# Exact scalar inequality, including delta>F_opt and F_opt near zero.
scalar=0
for i in range(101):
    for j in range(101):
        opt,delta=F(i,100),F(j,100)
        lower=max(F(0),opt-delta)**2-delta
        assert lower>=opt*opt-3*delta
        assert 1-opt*opt<=2*(1-opt)
        scalar+=1

factorization=[]
for k,d,D in [(2,1,4),(3,2,5),(2,4,6),(3,5,8)]:
    Ks=channel(k,d,max(2,(k+d-1)//d+1));W=unitary(D);V=W[:,:d];P=V@V.conj().T
    NK=[V@K for K in Ks]
    actualS=sum(K@K.conj().T for K in NK)/k
    assert np.linalg.norm((np.eye(D)-P)@actualS)<1e-13
    errors=[]
    for i in range(k):
        for j in range(k):
            E=np.zeros((k,k),complex);E[i,j]=1
            out=sum(K@E@K.conj().T for K in NK)
            small=sum(K@E@K.conj().T for K in Ks)
            errors.append(np.linalg.norm(out-V@small@V.conj().T))
            assert np.linalg.norm((np.eye(D)-P)@out)<1e-13
    # Both directions of physical decoder restriction/extension.
    Rsmall=channel(d,k,max(2,(d+k-1)//k+1))
    Rextended=[R@V.conj().T for R in Rsmall]
    z=np.eye(k)[:,0]
    Rextended += [np.outer(z,W[:,j].conj()) for j in range(d,D)]
    assert np.linalg.norm(sum(R.conj().T@R for R in Rextended)-np.eye(D))<1e-12
    assert abs(fe(Rextended,NK,k)-fe(Rsmall,Ks,k))<1e-12
    Rbig=channel(D,k,max(2,(D+k-1)//k+1));Rrestricted=[R@V for R in Rbig]
    assert np.linalg.norm(sum(R.conj().T@R for R in Rrestricted)-np.eye(d))<1e-12
    assert abs(fe(Rbig,NK,k)-fe(Rrestricted,Ks,k))<1e-12
    Rlearn,delta,tp=learned_petz(Ks,k,d,1e-5)
    witness=fe(Rsmall,Ks,k);actual=fe(Rlearn,Ks,k)
    assert actual>=witness*witness-3*delta-1e-11
    factorization.append({'k':k,'support_bound_d':d,'ambient_D':D,'matrix_units_checked':k*k,
                          'maximum_factorization_residual':float(max(errors)),
                          'restriction_extension_fidelity_agree':True,'learned_TP_residual':tp,
                          'random_decoder_witness_Fe':witness,'learned_actual_Fe':actual,
                          'model_distance_upper':delta,'global_optimum_not_numerically_claimed':True})

# For a qubit Pauli channel, twirling an arbitrary recovery preserves its
# objective, so F_opt=max_i p_i. Its exact Petz fidelity is sum_i p_i^2.
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);P=[I,X,Y,Z]
pauli=[]
for pp in [[F(1,10),F(3,5),F(1,5),F(1,10)], [F(2,5),F(3,10),F(1,5),F(1,10)], [F(97,100),F(1,100),F(1,100),F(1,100)], [F(1,4)]*4]:
    opt=max(pp);petz_exact=sum(p*p for p in pp);U=unitary(2)
    Ks=[np.sqrt(float(p))*U@W for p,W in zip(pp,P)]
    for a in [F(1,100),F(1,10000)]:
        learned,delta,tp=learned_petz(Ks,2,2,float(a));actual=fe(learned,Ks,2)
        expected=(petz_exact+2*a)/(1+8*a)
        assert abs(actual-float(expected))<1e-12
        assert actual>=float(opt*opt)-3*delta-1e-12
        pauli.append({'probabilities':[str(p) for p in pp],'exact_optimal_Fe':str(opt),
                      'ridge_a':str(a),'exact_learned_actual_Fe':str(expected),'matrix_Fe':actual,
                      'model_distance_upper':delta,'TP_residual':tp})

# Classical grouping channel |i><i| -> |f(i)><f(i)|. Every recovery has
# F_e<=d/k^2; choosing one input label per output group attains it. This
# includes replacements(d=1), complete dephasing(d=k), and d<k cases.
cq=[]
for k,d,labels in [(3,1,[0,0,0]),(3,2,[0,1,1]),(4,2,[0,0,1,1]),(3,3,[0,1,2])]:
    opt=F(d,k*k);U=unitary(d)
    Ks=[]
    for i,j in enumerate(labels):
        K=np.zeros((d,k),complex);K[j,i]=1;Ks.append(U@K)
    groups=[labels.count(j) for j in range(d)]
    for a in [F(1,100),F(1,10000)]:
        lam=2*k*d*a/(1+2*k*d*a)
        exact=sum(F(n)*((1-lam)+lam/d)/((1-lam)*n+lam*F(k,d)) for n in groups)/k**2
        learned,delta,tp=learned_petz(Ks,k,d,float(a));actual=fe(learned,Ks,k)
        assert abs(actual-float(exact))<2e-12
        assert actual>=float(opt*opt)-3*delta-1e-12
        cq.append({'k':k,'d':d,'group_sizes':groups,'exact_optimal_Fe':str(opt),'ridge_a':str(a),
                   'exact_learned_actual_Fe':str(exact),'matrix_Fe':actual,'model_distance_upper':delta,'TP_residual':tp})

result={'scalar_fidelity_inequalities':scalar,'low_support_factorization_and_decoder_extensions':factorization,
        'analytic_Pauli_optimum_cases':pauli,'analytic_classical_grouping_optimum_cases':cq,
        'scope':'Exact analytical optimum benchmarks plus independent finite matrix diagnostics for lossy channels, including d<k. No recovery SDP, unknown inverse, global-optimizer inference or hardware run.'}
(HERE/'INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print('Passed',scalar,'scalar cases,',len(factorization),'factorization cases, and',len(pauli)+len(cq),'analytic optimum benchmarks')
