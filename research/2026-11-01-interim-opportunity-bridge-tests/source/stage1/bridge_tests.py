"""Discriminating construction tests for four research openings, 1 Nov 2026.

All writes stay in this research chat. These controls do not prove novelty,
hardware performance, an autonomous threshold, or a polynomial-time sampler.
"""
from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import math
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as Q
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "opportunity_comparison_20261101"


def memory_merger():
    spec = importlib.util.spec_from_file_location("native_young", ROOT/"work/coherent_young_barrier.py")
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)

    def f(s, m, L):
        graph = {}
        for y in range(L):
            for x in range(L):
                b,l,_,_ = native.pattern(s,x,y,L)
                for active,w in [(b,((x+1)%L,y)),(l,(x,(y+1)%L))]:
                    if active:
                        v=(x,y)
                        graph.setdefault(v,set()).add(w)
                        graph.setdefault(w,set()).add(v)
        vals=[]
        while graph:
            v=next(iter(graph)); todo=[v]; seen={v}
            for a in todo:
                for b in graph[a]:
                    if b not in seen: seen.add(b); todo.append(b)
            diameter=max(max(min(abs(a[k]-b[k]),L-abs(a[k]-b[k])) for k in [0,1])
                         for a in seen for b in seen)
            vals.append(diameter)
            for a in seen: del graph[a]
        return sum((Q(16)**(d-m) for d in vals),Q(0)),sorted(vals)

    rows=[]
    for ell in [3,6,10]:
        m,L=2*ell+1,8*ell+12
        row=2; gap=2+ell
        before=sum(1 << (row*L+x) for x in list(range(2,gap))+list(range(gap+1,gap+1+ell)))
        after=before ^ (1 << (row*L+gap))
        fv,db=f(before,m,L); fw,da=f(after,m,L)
        assert db==[ell,ell] and da==[m]
        drift=[]; nact=[]
        for s in [before,after]:
            qf=Q(0); count=0
            for y in range(L):
                for x in range(L):
                    if native.pattern(s,x,y,L)[:2]==(1,1):
                        qf += f(s ^ (1 << (y*L+x)),m,L)[0]-f(s,m,L)[0]
                        count+=1
            drift.append(qf); nact.append(count)
        assert nact==[2,1]
        assert drift==[-Q(15,16)*fv,-Q(15,16)*fw]
        h,gamma,eps=Q(1,32),Q(1,4),Q(8)**(-m)
        # NSD would require this principal determinant to be nonnegative.
        determinant=(drift[0]+gamma*fv-eps)*(drift[1]+gamma*fw-eps)-h*h*(fw-fv)**2
        assert determinant < 0
        rows.append(dict(ell=ell,m=m,L=L,component_diameters_before=db,
                         component_diameters_after=da,active_pairs=nact,
                         potential_before=str(fv),potential_after=str(fw),
                         attempted_exponential_source=str(eps),
                         principal_determinant=str(determinant)))
    return dict(controls=rows,scope="Refutes the additive independent-component potential, not the memory",
                asymptotic_source_floor="(sqrt((11/16)^2+4 h^2)-11/16)/2 for kappa=1")


def quantum_toom_reduction():
    L=3;N=L*L;checks=0
    for s in range(1<<N):
        for y in range(L):
            for x in range(L):
                own=(s>>(y*L+x))&1
                left=(s>>(y*L+(x-1)%L))&1
                down=(s>>(((y-1)%L)*L+x))&1
                bottom,left_edge=own^down,own^left
                assert (bottom==left_edge==1)==(left==down and own!=left)
                c=s^((1<<N)-1)
                ownc=(c>>(y*L+x))&1
                leftc=(c>>(y*L+(x-1)%L))&1
                downc=(c>>(((y-1)%L)*L+x))&1
                assert (ownc^downc,ownc^leftc)==(bottom,left_edge)
                checks+=1
    # Exact coherence test on one three-spin majority correction. Separate
    # up/down jumps have identical diagonal action but a different quantum map.
    down=sp.zeros(8);up=sp.zeros(8)
    down[0,1]=1;up[7,6]=1
    J=down+up
    flip=sp.zeros(8)
    for s in range(8): flip[s^7,s]=1
    assert J*flip==flip*J and down*flip!=flip*down
    dyad=sp.zeros(8);dyad[1,6]=1
    combined=J*dyad*J.T
    separate=down*dyad*down.T+up*dyad*up.T
    assert combined[0,7]==1 and separate==sp.zeros(8)
    v=sp.zeros(16,1);v[2,0]=1;v[13,0]=1
    target=sp.zeros(16,1);target[0,0]=1;target[15,0]=1
    rho=v*v.T/2;bell=target*target.T/2
    C=sp.kronecker_product(J,sp.eye(2))
    combined_state=C*rho*C.T
    separate_state=sp.zeros(16)
    for K in [down,up]:
        A=sp.kronecker_product(K,sp.eye(2));separate_state+=A*rho*A.T
    f1=sp.trace(bell*combined_state);f2=sp.trace(bell*separate_state)
    assert f1==1 and f2==sp.Rational(1,2)
    return dict(L=L,all_configuration_predicate_checks=checks,
                native_virtual_jump="X_i (I-Z_i Z_left)(I-Z_i Z_down)/4",
                native_transverse_fault="h_i X_i tensor B_i",
                combined_jump_strong_flip_symmetry=True,
                split_jump_same_diagonal_action=True,
                reference_bell_fidelity_combined=str(f1),reference_bell_fidelity_split=str(f2),
                scope="Exact one-CSS-plane reduction and generator distinction, not a phase or threshold theorem")


def fermionic_bridge():
    n=4
    F=sp.zeros(n)
    for i,j,v in [(0,1,1),(2,3,1),(0,2,sp.Rational(1,4096)),
                  (1,3,sp.I/4096)]: F[i,j]=F[j,i]=v

    def state(mat,pairs):
        ans={}
        for up in itertools.combinations(range(n),pairs):
            for down in itertools.combinations([i for i in range(n) if i not in up],pairs):
                a=mat.extract(up,down).det()
                inv=sum(j<i for i in up for j in down)
                s=sum(1 << (2*i) for i in up)+sum(1 << (2*j+1) for j in down)
                if a: ans[s]=(-1)**inv*a
        return ans

    def inner(a,b):
        return sp.simplify(sum(sp.conjugate(v)*b.get(s,0) for s,v in a.items()))

    def annihilate(a,indices):
        out={}
        for s,v in a.items():
            t=s; w=v
            for i in indices:
                if not ((t>>i)&1): w=0; break
                w*=(-1)**((t & ((1<<i)-1)).bit_count())
                t ^= 1 << i
            if w: out[t]=out.get(t,0)+w
        return {s:sp.simplify(v) for s,v in out.items() if v!=0}

    def delta(a,i,j):
        p=annihilate(a,[2*j+1,2*i]); q=annihilate(a,[2*j,2*i+1])
        return {s:sp.simplify(p.get(s,0)-q.get(s,0)) for s in set(p)|set(q)}

    full=state(F,2); norm=inner(full,full)
    bonds=list(itertools.combinations(range(n),2))
    ds=[delta(full,*b) for b in bonds]
    G=sp.Matrix([[sp.simplify(inner(a,b)/norm) for b in ds] for a in ds])
    assert all(G[i,j]==0 for i in range(len(bonds)) for j in range(len(bonds)) if i!=j)
    assert all(0<=G[i,i]<=2 for i in range(len(bonds)))
    D=sp.diag(2,2,1,1)
    scaled=state(D*F*D,2)
    assert all(sp.simplify(scaled.get(s,0)-4*v)==0 for s,v in full.items())
    # Product reference: the same diagonal transformation is no longer a gauge
    # when holes are admitted. It changes a physical occupation by order one.
    F0=sp.zeros(n); F0[0,1]=F0[1,0]=F0[2,3]=F0[3,2]=1
    p,q=state(F0,1),state(D*F0*D,1)
    def occupation(a,site):
        return sp.simplify(sum(sp.conjugate(v)*v*((s>>(2*site))&1 | (s>>(2*site+1))&1)
                               for s,v in a.items())/inner(a,a))
    occ0,occ1=occupation(p,0),occupation(q,0)
    assert occ0==sp.Rational(1,2) and occ1==sp.Rational(16,17)
    gd=sp.simplify(inner(delta(p,0,1),delta(p,2,3))/inner(p,p))
    assert gd==1
    return dict(sites=n,weak_row_envelope="1/4096",reference_dimer_graph_degree=1,
                full_occupancy_pair_gram_offdiagonal_zero=True,
                full_occupancy_pair_gram_diagonal=[str(G[i,i]) for i in range(len(bonds))],
                all_size_pair_eigenvalue_bound=2,
                full_occupancy_gauge_scalar=4,doped_occupation_before=str(occ0),
                doped_occupation_after_same_scaling=str(occ1),doped_pair_offdiagonal=str(gd),
                scope="No charge ODLRO at full occupancy; doping invalidates this gauge transfer")


def acquisition_bridge():
    A=sp.zeros(3);B=sp.zeros(3); A[0,1]=1;B[1,2]=1
    assert A*B-B*A != sp.zeros(3)
    a,b=sp.symbols("a b",commutative=True)
    assert a*b-b*a==0
    # A hidden needle word has a rank-(ell+1) weighted-automaton realization.
    # Each membership query can rule out only one of 2**ell equiprobable words.
    ell=8; target="01011010"
    transitions=[]
    for letter in "01":
        M=sp.zeros(ell+1)
        for i,c in enumerate(target):
            if c==letter: M[i,i+1]=1
        transitions.append(M)
    successes=[]
    for bits in itertools.product("01",repeat=ell):
        v=sp.zeros(1,ell+1); v[0,0]=1
        for c in bits: v=v*transitions[int(c)]
        if v[0,ell]: successes.append("".join(bits))
    assert successes==[target]
    return dict(scalar_commutator_alias=True,legal_nilpotent_matrix_query=[str(A),str(B)],
                matrix_commutator=str(A*B-B*A),needle_length=ell,hidden_rank=ell+1,
                tested_words=2**ell,nonzero_words=successes,
                general_membership_success_bound="q/2^ell for a uniformly hidden length-ell needle",
                scope="Exact word access and a rank promise do not acquire the L01 matrix oracle")


def quartic_data(W,z,zb,x,y):
    m=len(z); sub={z[j]:x[j]+sp.I*y[j] for j in range(m)}
    sub.update({zb[j]:x[j]-sp.I*y[j] for j in range(m)})
    C=sp.Matrix(m,m,lambda i,j:sp.expand(sp.diff(W,zb[i],zb[j]).subs(sub)))
    Re=C.applyfunc(lambda a:sp.simplify(sp.re(a)))
    Im=C.applyfunc(lambda a:sp.simplify(sp.im(a)))
    D=sp.Rational(1,2)*Im.row_join(-Re).col_join((-Re).row_join(-Im))
    return C,D


def symbolic_local_invariance():
    z=sp.symbols("z0:2"); zb=sp.symbols("b0:2")
    x=sp.symbols("x0:2",real=True);y=sp.symbols("y0:2",real=True)
    X=sp.Matrix(x+y); variables=x+y
    v=[z[0]**2,z[0]*z[1],z[1]**2]
    vb=[zb[0]**2,zb[0]*zb[1],zb[1]**2]
    basis=[vb[i]*v[i] for i in range(3)]
    for i,j in itertools.combinations(range(3),2):
        basis += [vb[i]*v[j]+vb[j]*v[i],sp.I*(vb[i]*v[j]-vb[j]*v[i])]
    residuals=[]
    for W in basis:
        C,D=quartic_data(W,z,zb,x,y)
        div=sp.Matrix([sum(sp.diff(D[i,j],variables[i]) for i in range(4)) for j in range(4)])
        expressions=[sp.trace(D),(X.T*D*X)[0],(X.T*div)[0],
                     sum(sp.diff(div[j],variables[j]) for j in range(4))]
        expressions += [sum(sp.diff(D[i,j],v,2) for v in variables) for i in range(4) for j in range(4)]
        vals=[sp.simplify(a) for a in expressions]
        assert all(a==0 for a in vals)
        residuals.append(len(vals))
    # The second divergence of g(S)D vanishes for arbitrary radial g:
    # g divdiv D + 4g' X.divD + 2g' trD + 4g'' X.D.X = 0.
    # A legal record-dependent SWAP demonstrates failure of local equilibrium
    # invariance under feedback: c E[S2(S2-S1)] = c nu**2 > 0.
    return dict(real_quartic_basis_dimension=len(basis),identities_per_basis=residuals,
                invariant_radial_cutoff_density=True,
                allowed_feedback_counterexample_d_mean_S1_dt="c nu^2 at equilibrium",
                scope="Open-loop invariant thermal marginal; arbitrary feedback is excluded")


def decimal_fraction(a,rounding):
    with localcontext() as ctx:
        ctx.prec=35;ctx.rounding=rounding
        return str(Decimal(a.numerator)/Decimal(a.denominator))


def local_tail_example():
    b=Q(32); N=256
    term=s=Q(1)
    for k in range(1,N+1): term*=b/k;s+=term
    tail=term*b/(N+1)/(1-b/(N+2))
    lo,hi=1/(s+tail),1/s
    sqrt2_lower=Q(1414213562373095,10**15)
    assert sqrt2_lower**2 < 2
    upper=Q(1000*100)/sqrt2_lower*hi
    assert upper < Q(1,10**9)
    return dict(modes=1000,T=100,kappa=64,theta=1,nu=1,g=1,eta="1/2",
                local_cutoff_B=32,local_record_TV_upper=decimal_fraction(upper,ROUND_CEILING),
                exp_minus_32_interval=[decimal_fraction(lo,ROUND_FLOOR),decimal_fraction(hi,ROUND_CEILING)],
                global_excess_tail_lower=968,
                old_global_certificate="vacuous: E(S-32)+ >= 1000-32",
                scope="Analytic continuous-law certificate, not runtime or physical validation")


def kernel_control():
    import numpy as np
    from scipy.linalg import eigvalsh
    z=sp.symbols("z0:2");zb=sp.symbols("b0:2")
    x=sp.symbols("x0:2",real=True);y=sp.symbols("y0:2",real=True)
    Ws=[zb[0]**2*z[0]**2/2,zb[0]*zb[1]*z[0]*z[1]/3,
        (zb[0]**2*z[1]**2+zb[1]**2*z[0]**2)/5]
    terms=[]
    for W in Ws:
        C,D=quartic_data(W,z,zb,x,y)
        terms.append((sp.lambdify(x+y,C,"numpy"),sp.lambdify(x+y,D,"numpy")))
    drift=sp.Matrix([-sp.I*sp.diff(sum(Ws),b) for b in zb])
    sub={z[j]:x[j]+sp.I*y[j] for j in range(2)}
    sub.update({zb[j]:x[j]-sp.I*y[j] for j in range(2)})
    drift=drift.subs(sub)
    funF=sp.lambdify(x+y,sp.Matrix([sp.re(a) for a in drift]+[sp.im(a) for a in drift]),"numpy")
    cut,inner=12,8
    a=np.diag(np.sqrt(np.arange(1,cut)),1);I=np.eye(cut)
    aa=[np.kron(a,I),np.kron(I,a)];ad=[p.conj().T for p in aa]
    kappa,nu,theta,eta=4.,1.,1.,.5
    H=(2/7)*(ad[0]@aa[1]+ad[1]@aa[0])+.5*(ad[0]@ad[0]@aa[0]@aa[0])
    H+=(ad[0]@aa[0]@ad[1]@aa[1])/3
    H+=(ad[0]@ad[0]@aa[1]@aa[1]+ad[1]@ad[1]@aa[0]@aa[0])/5
    keep=[i*cut+j for i in range(inner) for j in range(inner)]
    samples=[]
    for zz in [np.array([.4+.2j,-.3+.1j]),np.array([2+1j,-1+.5j])]:
        vecs=[np.array([np.exp(-abs(v)**2/2)*v**n/math.sqrt(math.factorial(n))
                         for n in range(cut)]) for v in zz]
        ket=np.kron(*vecs);K=np.outer(ket,ket.conj())
        coords=np.r_[zz.real,zz.imag]
        def deriv(M,i):
            j=i%2
            return ((ad[j]@M+M@aa[j]) if i<2 else 1j*(ad[j]@M-M@aa[j]))-2*coords[i]*M
        ds=[deriv(K,i) for i in range(4)]
        dds=[[deriv(ds[j],i)-(2*K if i==j else 0) for j in range(4)] for i in range(4)]
        D0=kappa*nu/2*np.eye(4); Dq=np.zeros((4,4));Dhat=D0.copy();residual_bound=0.
        q2s=[1.,1/6,2/5];qFs=[1.,1/(3*np.sqrt(2)),2/5]
        for t,(cf,df) in enumerate(terms):
            C=np.asarray(cf(*coords),complex);D=np.asarray(df(*coords),float)
            S=abs(zz[0])**2 if t==0 else float(np.vdot(zz,zz).real)
            B=eta*(1/3)*kappa*nu/q2s[t]
            chi=min(1.,B/S)
            Dq+=D;Dhat+=chi*D
            residual_bound+=np.sqrt(2)*qFs[t]*max(0.,S-B)
        f=np.asarray(funF(*coords),float).ravel()
        hflow=-1j*(2/7)*np.array([zz[1],zz[0]])
        f+=np.r_[hflow.real,hflow.imag]-kappa*coords/2
        lift=sum(f[i]*ds[i] for i in range(4))
        approx=lift.copy();exact=lift.copy()
        for i in range(4):
            for j in range(4):
                exact+=(D0+Dq)[i,j]*dds[i][j]/2
                approx+=Dhat[i,j]*dds[i][j]/2
        L=-1j*(H@K-K@H)
        for annihilator,creator in zip(aa,ad):
            for rate,J in [(kappa*(nu+theta)/theta,annihilator),(kappa*nu/theta,creator)]:
                A=J.conj().T@J
                L+=rate*(J@K@J.conj().T-(A@K+K@A)/2)
        block=lambda A:A[np.ix_(keep,keep)]
        error=float(np.linalg.norm(block(L-exact),"fro"))
        actual=float(np.linalg.norm(block(L-approx),ord="nuc"))
        assert error < 1e-10 and actual <= residual_bound+1e-10
        minimum=float(eigvalsh(Dhat)[0]);assert minimum>=1-1e-12
        samples.append(dict(z=[str(a) for a in zz],kernel_identity_interior_residual=error,
                            projected_defect_trace_norm=actual,full_analytic_defect_bound=residual_bound,
                            covariance_minimum_eigenvalue=minimum))
    return dict(fock_cutoff_per_mode=cut,interior_cutoff_per_mode=inner,samples=samples,
                scope="Pointwise finite-matrix control; no SDE discretization or complexity guarantee")


def interferometric_record_control():
    # With only pooled total counts, any number-conserving H is invisible.
    # A mixed output port is genuinely more informative. At thermal mean n,
    # a one-mode Kerr U/2 n1(n1-1) changes the two-click curvature by
    # -U^2 n^3(3n+1), even though the unconditioned state is stationary.
    n=sp.symbols("n",positive=True)
    m1=n;m2=2*n*n+n;m3=6*n**3+6*n*n+n
    q=n/(n+1)
    curvature=sp.simplify(-q*((m3+m2)*n+(m3-2*m2+m1)*(n+1))/4)
    assert sp.simplify(curvature+n**3*(3*n+1))==0
    # Direct Fock-matrix check for n=1/3, U=1, with an exponential thermal tail.
    import numpy as np
    cutoff=28;mu=1/3;r=mu/(mu+1)
    annih=np.diag(np.sqrt(np.arange(1,cutoff)),1)
    A=np.kron(annih.T,annih)
    nums=np.arange(cutoff)
    N1=np.repeat(nums,cutoff);N2=np.tile(nums,cutoff)
    obs=(np.diag(N1+N2)+A+A.T)/2
    probabilities=np.kron((1-r)*r**nums,(1-r)*r**nums)
    post=r*probabilities[:,None]*(obs+np.eye(cutoff**2))
    energy=N1*(N1-1)/2
    double=(energy[:,None]-energy[None,:])**2*obs
    direct=-float(np.sum(post.T*double))
    exact=-mu**3*(3*mu+1)
    assert abs(direct-exact)<1e-11
    return dict(exact_hamiltonian_curvature="-U^2 n^3(3 n+1)",
                thermal_mean="1/3",U=1,direct_fock_value=direct,
                exact_value=str(sp.Rational(-2,27)),cutoff_per_mode=cutoff,
                scope="Nontrivial interferometric record dependence, not a simulation-speed comparison")


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    result={"memory_merger":memory_merger(),"quantum_toom":quantum_toom_reduction(),
            "fermionic":fermionic_bridge(),
            "acquisition":acquisition_bridge(),"local_invariance":symbolic_local_invariance(),
            "local_tail":local_tail_example(),"kernel":kernel_control(),
            "interferometric_record":interferometric_record_control()}
    result["program_sha256"]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (OUT/"bridge_tests.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"output":str(OUT/"bridge_tests.json"),"checks":list(result)}))


if __name__=="__main__": main()
