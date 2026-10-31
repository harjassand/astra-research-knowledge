"""Logical error effects and the actual coherent Toom generator, 1 Nov 2026.

Exact algebra is separated from floating semigroup controls. No state reset,
physical measurement, noise floor, package installation or outside edit.
"""
from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path

import numpy as np
import sympy as s
from scipy.linalg import eigvalsh
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import expm_multiply

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"outputs/logical_phase_20261101"
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
PS=[I,X,Y,Z]


def dagger(A): return A.conjugate().T


def psd2(A):
    assert A==dagger(A)
    assert s.simplify(A[0,0])>=0 and s.simplify(A[1,1])>=0 and s.simplify(A.det())>=0


def rotations(P,t):
    t=s.Rational(t)
    return ((1-t*t)*s.eye(P.rows)-2*s.I*t*P)/(1+t*t)


def coefficients(K,k):
    d=2**k;db=K.rows//d
    basis=[]
    for labels in itertools.product(range(4),repeat=k):
        P=s.kronecker_product(*(PS[j] for j in labels))
        B=s.zeros(db)
        for a in range(d):
            for b in range(d):
                B+=P[b,a]*K[a*db:(a+1)*db,b*db:(b+1)*db]/d
        basis.append((labels,P,s.simplify(B)))
    return basis


def exact_receivers():
    U=s.kronecker_product(I,s.diag(1,0))+s.kronecker_product(
        rotations(X,s.Rational(1,100)),s.diag(0,1))
    U=rotations(s.kronecker_product(X,X),s.Rational(1,70))*U
    assert dagger(U)*U==s.eye(4)
    assert U*s.kronecker_product(X,I)==s.kronecker_product(X,I)*U
    bs=coefficients(U,1)
    A,B=bs[0][2],bs[1][2]
    assert bs[2][2]==s.zeros(2) and bs[3][2]==s.zeros(2)
    E=s.simplify(dagger(B)*B)
    assert s.simplify(dagger(A)*A+E)==I
    assert s.simplify(dagger(A)*B+dagger(B)*A)==s.zeros(2)
    assert E[0,0]!=E[1,1]
    psd2(E);psd2(I-E)
    # One logical basis state's wrong-output effect is exactly E, not an
    # average over bath preparations or a reduced-bath error metric.
    flip=U[2:4,0:2]
    assert s.simplify(dagger(flip)*flip-E)==s.zeros(2)
    delta=float(np.linalg.eigvalsh(np.array(E,complex))[-1])

    # Two complementary basis effects for two logical qubits, common bath.
    U2=rotations(s.kronecker_product(X,Z,Y),s.Rational(1,80))
    U2=rotations(s.kronecker_product(Z,Y,X),s.Rational(1,90))*U2
    U2=rotations(s.kronecker_product(Y,I,Z),s.Rational(1,100))*U2
    terms=coefficients(U2,2)
    Eall=s.zeros(2);EZ=s.zeros(2);EX=s.zeros(2);Eboth=s.zeros(2)
    for labels,P,Bc in terms:
        C=dagger(Bc)*Bc
        zbad=any(j in [1,2] for j in labels)
        xbad=any(j in [2,3] for j in labels)
        if any(labels): Eall+=C
        if zbad: EZ+=C
        if xbad: EX+=C
        if zbad and xbad:Eboth+=C
    Eall,EZ,EX,Eboth=map(s.simplify,[Eall,EZ,EX,Eboth])
    assert s.simplify(EZ+EX-Eall-Eboth)==s.zeros(2)
    psd2(Eboth)
    # Compute the operational averaged effects directly, not only by labels.
    directZ=s.zeros(2);directX=s.zeros(2)
    H=s.Matrix([[1,1],[1,-1]])/s.sqrt(2)
    HX=s.kronecker_product(H,H)
    for transform,acc in [(s.eye(4),"Z"),(HX,"X")]:
        effect=s.zeros(2)
        Uc=s.kronecker_product(dagger(transform),I)*U2*s.kronecker_product(transform,I)
        for a in range(4):
            for b in range(4):
                if a!=b:
                    block=Uc[2*b:2*b+2,2*a:2*a+2]
                    effect+=dagger(block)*block/4
        if acc=="Z":directZ=s.simplify(effect)
        else:directX=s.simplify(effect)
    assert s.simplify(directZ-EZ)==s.zeros(2)
    assert s.simplify(directX-EX)==s.zeros(2)
    return dict(one_basis_error_effect=str(E),one_basis_delta_preview=delta,
                one_basis_joint_bound_preview=min(2,2*math.sqrt(delta)+2*delta),
                two_basis_operator_identity_verified=True,
                exact_nonidentity_effect=str(Eall),
                scope="Exact finite receiver algebra; no dynamical threshold or optimized diamond norm")


def receiver_countermodels():
    # Dephasing Z has perfect Z-basis populations and weak X covariance,
    # while its Choi Bell overlap is 1/2. It does not strongly preserve X.
    bell=s.Matrix([1,0,0,1]);rho=bell*bell.T/2
    deph=(rho+s.kronecker_product(Z,I)*rho*s.kronecker_product(Z,I))/2
    assert s.trace(rho*deph)==s.Rational(1,2)
    # A bath flag can hide an arbitrarily bad channel in a small average.
    U=s.kronecker_product(I,s.diag(1,0))+s.kronecker_product(X,s.diag(0,1))
    E=dagger(U[2:4,0:2])*U[2:4,0:2]
    assert E==s.diag(0,1)
    # A wrong final decoder Z itself has zero basis-population error but
    # anticommutes with the conserved-X representation.
    assert Z*X==-X*Z
    return dict(weak_covariance_counterexample=dict(Z_basis_error=0,Bell_fidelity="1/2"),
                bath_average_counterexample=dict(averaged_error="1/1000",worst_bath_error=1),
                decoder_intertwiner_required=True,
                conserved_observable_alone_counterexample="X dephasing preserves X but loses Z-basis information")


def strip_pair_process():
    spec=importlib.util.spec_from_file_location("native_young",ROOT/"work/coherent_young_barrier.py")
    native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
    rows=[]
    for ell in [1,3,8]:
        L=4*ell+8;row=2
        for j in range(ell+1):
            left=sum(1 << (row*L+x) for x in range(j,ell))
            right=left ^ (1 << (row*L+ell))
            active=[]
            for state in [left,right]:
                active.append({(x,y) for y in range(L) for x in range(L)
                               if native.pattern(state,x,y,L)[:2]==(1,1)})
            if j<ell:assert active==[{(j,row)},{(j,row)}]
            else:assert active==[set(),{(ell,row)}]
        for model,last in [("completed",s.Integer(1)),("active",s.Rational(1,2))]:
            K=s.zeros(ell+1)
            for j in range(ell): K[j,j]=-1;K[j+1,j]=1
            K[ell,ell]=-last
            initial=s.zeros(ell+1,1);initial[0,0]=1
            integrated=-K.inv()*initial
            mean=sum(integrated)
            assert mean==ell+1/last
            z=s.symbols('z',positive=True)
            laplace=s.simplify(sum((z*s.eye(ell+1)-K).inv()*initial))
            expected=s.simplify((1-(1/(1+z))**ell*last/(last+z))/z)
            assert s.simplify(laplace-expected)==0
            rows.append(dict(ell=ell,model=model,mean_coherence_survival=str(mean),
                             laplace_transform=str(laplace)))
    return dict(cases=rows,completed_survival="exp(-kappa*t) sum_{j=0}^ell (kappa*t)^j/j!",
                general_pair_rule="xor disagreement is constant; mismatched active predicates kill a dyad",
                scope="Exact native unperturbed propagator between coherent insertions; full Hamiltonian is not removed from the model")


def absolute_pair_norm_counter():
    t=s.Rational(1,100)
    c=(1-t*t)/(1+t*t);u=2*t/(1+t*t)
    factor=s.simplify((c+u)**2)
    assert factor>1
    return dict(one_site_absolute_density_factor=str(factor),
                product_state_N_site_norm="(1+abs(sin(2 h T)))^N",
                actual_grouped_generator_initial_right_derivative="2 N h for scalar positive h",
                scope="Refutes a uniform absolute dyad norm, not logical protection")


def native_control(model,T=100.):
    L=2;N=L*L;dm=1<<N;db=2;D=dm*db
    eye=np.eye(D)
    ix=np.array(X,complex);iy=np.array(Y,complex);iz=np.array(Z,complex)
    ib=np.eye(2);H=np.kron(np.eye(dm),ix/8+iz/16)
    Gmem=np.zeros((dm,dm))
    for a in range(dm):Gmem[a^ (dm-1),a]=1
    symmetry=np.kron(Gmem,ib)
    js=[]
    for y in range(L):
        for x in range(L):
            i=y*L+x;left=y*L+(x-1)%L;down=((y-1)%L)*L+x
            A=np.zeros((dm,dm));P=np.zeros((dm,dm));F=np.zeros((dm,dm))
            for a in range(dm):
                F[a^(1<<i),a]=1
                z=(a>>i)&1;l=(a>>left)&1;d=(a>>down)&1
                if z!=l and z!=d:A[a^(1<<i),a]=1;P[a,a]=1
            B=[(ib+iz)/2,ix,iy,iz][i]
            H+=np.kron(F,B)/64
            js.append(np.kron(A,ib))
            if model=="completed":js.append(np.kron(np.eye(dm)-P,ib))
    assert np.linalg.norm(H@symmetry-symmetry@H)==0
    assert all(np.linalg.norm(J@symmetry-symmetry@J)==0 for J in js)
    G=-1j*(np.kron(eye,H)-np.kron(H.T,eye))
    for J in js:
        A=J.conj().T@J
        G+=np.kron(J.conj(),J)-(np.kron(eye,A)+np.kron(A.T,eye))/2
    traceG=np.trace(G);G=csr_matrix(G)
    # One fixed syndrome decoder, resolved before selecting H or T. In this
    # finite plane fixture the fallback chooses the smaller representative,
    # with integer order breaking ties. Its Kraus are physical Z fillings.
    reps=[a for a in range(dm) if (a.bit_count(),a)<=((a^(dm-1)).bit_count(),a^(dm-1))]
    ds=[]
    for a in reps:
        dec=np.zeros((2,dm));dec[0,a]=1;dec[1,a^(dm-1)]=1
        ds.append(np.kron(dec,ib))
    logicalsym=np.kron(ix,ib)
    assert all(np.linalg.norm(d@symmetry-logicalsym@d)==0 for d in ds)
    enc=np.zeros((D,4),complex)
    for logical,m in [(0,0),(1,dm-1)]:
        for b in range(db):enc[m*db+b,logical*db+b]=1
    init=[]
    for col in range(16):
        a,b=col%4,col//4
        state=np.outer(enc[:,a],enc[:,b].conj())
        init.append(state.reshape(-1,order="F"))
    evolved=expm_multiply(G*T,np.array(init).T,traceA=traceG*T)
    phi=np.empty((16,16),complex)
    for col in range(16):
        rho=evolved[:,col].reshape(D,D,order="F")
        out=sum(d@rho@d.conj().T for d in ds)
        phi[:,col]=out.reshape(-1,order="F")
    effect=np.zeros((2,2),complex)
    for a in range(2):
        for b in range(2):
            out=phi[:,a+4*b].reshape(4,4,order="F")
            effect[b,a]=np.trace(out[2:4,2:4])
    effect=(effect+effect.conj().T)/2
    delta=float(eigvalsh(effect)[-1])
    # Choi test and the norm of Kraus components outside {I,X} x bath.
    choi=np.zeros((16,16),complex)
    for a in range(4):
        for b in range(4):
            out=phi[:,a+4*b].reshape(4,4,order="F")
            choi[a*4:(a+1)*4,b*4:(b+1)*4]=out
    ev,V=np.linalg.eigh((choi+choi.conj().T)/2)
    outside=0.;eff2=np.zeros((2,2),complex)
    for k in range(16):
        if ev[k]>1e-14:
            K=np.sqrt(ev[k])*V[:,k].reshape(4,4,order="F")
            # The Choi convention above uses vec(K) in input-major order.
            A=(K[:2,:2]+K[2:,2:])/2
            B=(K[:2,2:]+K[2:,:2])/2
            approx=np.kron(ib,A)+np.kron(ix,B)
            outside+=np.linalg.norm(K-approx,"fro")**2
            eff2+=B.conj().T@B
    # Equivalent bath projection channel is CPTP even though individual
    # coherent cross terms need not be CP.
    trace_error=max(abs(np.trace(phi[:,a+4*b].reshape(4,4,order="F"))-(a==b))
                    for a in range(4) for b in range(4))
    assert trace_error<1e-9 and ev[0]>-1e-10 and outside<1e-10
    assert np.linalg.norm(eff2-effect)<1e-9
    return dict(L=L,model=model,T=T,h_over_kappa="1/64",persistent_bath_dimension=2,
                error_effect_real=effect.real.tolist(),error_effect_imag=effect.imag.tolist(),
                worst_bath_error_preview=delta,joint_bound_preview=min(2,2*math.sqrt(max(0,delta))+2*delta),
                trace_residual=float(trace_error),minimum_choi_eigenvalue=float(ev[0]),
                kraus_outside_commutant_squared=float(outside),
                scope="Floating full-generator control, not an interval certificate, scaling law or optimized diamond norm")


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    result=dict(exact_receivers=exact_receivers(),countermodels=receiver_countermodels(),
                pair_process=strip_pair_process(),absolute_pair_norm=absolute_pair_norm_counter(),
                actual_generator=[native_control(m) for m in ["active","completed"]])
    result['program_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (OUT/'controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'output':str(OUT/'controls.json'),'checks':list(result)}))


if __name__=='__main__':main()
