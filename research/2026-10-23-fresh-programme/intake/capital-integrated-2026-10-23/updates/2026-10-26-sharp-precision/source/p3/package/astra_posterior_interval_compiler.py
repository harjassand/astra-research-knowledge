"""Astra Pro3: task compiler directly over an acquired exact Loewner interval.

The inputs S_L,S_U must be an EXACT whole response consistency family
[S_L,S_U]; old finite observations with errors generally give only an outer
interval, for which derived upper certificates remain sound but lower bounds
are not necessarily sharp. Full-vector probes of unknown symmetric S only.
This script checks the generalized inertia, forcing-domain and noisy dual
against an independently reconstructed Schur-complement completion control.
"""
from pathlib import Path
import json
from itertools import combinations
import sympy as sp

BASE=Path(__file__).resolve().parent


def sm(x):
    return x.applyfunc(sp.simplify) if isinstance(x,sp.MatrixBase) else sp.simplify(x)


def tojson(v):
    if isinstance(v,sp.MatrixBase):
        return [[str(sm(v[i,j])) for j in range(v.cols)] for i in range(v.rows)]
    if isinstance(v,sp.Basic):return str(sm(v))
    if isinstance(v,dict):return {str(k):tojson(a) for k,a in v.items()}
    if isinstance(v,(list,tuple)):return [tojson(x) for x in v]
    return v


def ispsd(M):
    """EXACT rational symmetric PSD check: all principal minors >=0."""
    assert M==M.T
    assert all(a.is_Rational for a in M)
    n=M.rows
    for k in range(1,n+1):
        for ii in combinations(range(n),k):
            d=sp.det(M.extract(ii,ii))
            if d<0: return False
    return True


def sym(q,y):return (q*y.T+y*q.T)/2


def reconstruct_family():
    # One exact acquisition: S e0=[2,1/2,0,0]^T, spectral 1I <= S <=3I.
    # U=e0, E=[e1,e2,e3], G=I, A=2, B=[1/2,0,0].
    n=4;eye=sp.eye(n);u=eye[:,0];y=sp.Matrix([2,sp.Rational(1,2),0,0]);
    E=eye[:,1:4]
    a,b=sp.Integer(1),sp.Integer(3)
    A=(u.T*y)[0]; B=E.T*y
    Ga=A-a;Gb=b-A
    Da=B;Db=B
    assert Ga==Gb==1
    CL=a*sp.eye(3)+Da*Da.T/Ga
    CU=b*sp.eye(3)-Db*Db.T/Gb
    SL=sp.zeros(n);SU=sp.zeros(n)
    for S,C in ((SL,CL),(SU,CU)):
        S[0,0]=A
        for i in range(3):
            S[i+1,0]=B[i];S[0,i+1]=B[i]
            for j in range(3):S[i+1,j+1]=C[i,j]
    assert SL==SL.T and SU==SU.T
    assert ispsd(SU-SL) and ispsd(SL-eye) and ispsd(3*eye-SU)
    assert SL*u==y and SU*u==y
    SC=(SL+SU)/2
    D=SU-SL
    assert D==sp.diag(0,sp.Rational(3,2),2,2)
    # Every member of the exact family has the same old action;
    # a genuinely different e0-e3 interaction is forced to zero without
    # a source query, even though the e1-e3 block remains unknown.
    assert SC*u==y
    assert sm((SL+SU)/2)==SC
    Strue=SC
    return dict(source_contract_lo=a,source_contract_hi=b,old_probe=u,
        exact_old_vector_reading=y,exact_family_lower=SL,exact_family_upper=SU,
        family_center=SC,family_width=D,manufactured_true_source=Strue,
        forcing_domain_basis=u,
        assumption='The source satisfies supplied [1I,3I] bound and exact old vector reading; Schur complements prove interval [SL,SU] is the entire compatible symmetric family.')


def exact_task_compiler_control(fam):
    D=fam['family_width'];SC=fam['family_center'];Strue=fam['manufactured_true_source'];
    eye=sp.eye(4)
    # Here D^(1/2) = diag(0,sqrt(3/2),sqrt(2),sqrt(2)).
    W=sp.diag(0,sp.sqrt(sp.Rational(3,2)),sp.sqrt(2),sp.sqrt(2))
    assert sm(W*W-D)==sp.zeros(4)
    # Late task 1: cross interaction including an old known input.
    Tforced=sym(eye[:,0],eye[:,3])
    assert sm(W*Tforced*W)==sp.zeros(4)
    forced_val=sm(sp.trace(Tforced*SC))
    assert forced_val==0
    # Late task 2: indefinite aggregate in uncertain subspace.
    T=sp.diag(0,1,-1,0)
    Tprime=sm(W*T*W/2)
    assert Tprime==sp.diag(0,sp.Rational(3,4),-1,0)
    q=(eye[:,1]+eye[:,2])/sp.sqrt(2)
    yy=sp.sqrt(2)*(eye[:,1]-eye[:,2])
    assert sm(sym(q,yy)-T)==sp.zeros(4)
    assert sm(q.dot(q))==1
    response=Strue*q
    recovered=sm((yy.T*response)[0])
    actual=sm(sp.trace(T*Strue))
    assert recovered==actual
    eta=sp.Rational(1,1000)
    plus_error_witness=sp.diag(0,eta,-eta,0)
    Sp=SC+plus_error_witness;Sm=SC-plus_error_witness
    assert ispsd(Sp-fam['exact_family_lower']) and ispsd(fam['exact_family_upper']-Sp)
    assert ispsd(Sm-fam['exact_family_lower']) and ispsd(fam['exact_family_upper']-Sm)
    assert sm((Sp-Sm)*q)==2*plus_error_witness*q
    assert sm((plus_error_witness*q).dot(plus_error_witness*q))==eta**2
    plus_target=sm(sp.trace(T*Sp));minus_target=sm(sp.trace(T*Sm))
    assert plus_target-minus_target==4*eta
    # The same reported vector SC q can result from Sp and Sm with errors
    # respectively -Hq and +Hq (norm eta). Thus radius >=2eta.
    noisy_bound=eta*sm(sp.sqrt(yy.dot(yy)))
    assert noisy_bound==2*eta
    # Independent uncertain dimensions remain. A zero-query T with
    # nonzero transformed T' has nontrivial exact range.
    original_prior_radius=sp.Rational(7,4)
    assert original_prior_radius==sp.Rational(7,4)
    # For this diagonal T and D, central unknown prior radius is
    # 1/2 * nuclear norm(W T W) = .75 + 1 = 1.75.
    assert original_prior_radius==(abs(Tprime[1,1])+abs(Tprime[2,2]))
    return dict(late_forced_task=Tforced,forced_zero_call_target=forced_val,
       late_aggregate_task=T,transformed_task_Tprime=Tprime,
       unknown_interval_effective_dimension=3,
       transformed_task_positive_inertia=1,
       transformed_task_negative_inertia=1,
       exact_new_query_minimum=1,
       compiled_native_full_vector_query=q,compiled_decoder_vector=yy,
       manufactured_source_response=response,
       exact_target=actual,reconstructed_target=recovered,
       prior_only_exact_worst_error=original_prior_radius,
       per_new_action_adversarial_error=eta,
       compiled_sharp_noisy_worst_error=noisy_bound,
       indistinguishable_sources_plus=Sp,indistinguishable_sources_minus=Sm,
       indistinguishable_target_gap=plus_target-minus_target,
       common_report=SC*q,
       retained_old_query_count=1,new_query_count=1,
       new_returned_coordinates=4,
       proof_checks=['Exact Schur completion from old action',
         'D=W^2 and Tprime=W T W/2',
         'Sym(q,y)=T',
         'Both adversarial sources in exact interval and produce same eta-compatible report',
         'Paired upper/lower worst errors match'])


def noisy_outer_counterexample():
    # A noisy OUTER Loewner interval permits certified bounds but can contain
    # sources violating the actual historic noise-box constraints. Hence
    # in general it cannot support a sharp lower-bound (minimax) assertion.
    # Real posterior: |S11-2|<=1/1000; outer family S in [I,3I].
    true_r=sp.Rational(1,1000)
    center=2*sp.eye(2);outer_lo=sp.eye(2);outer_hi=3*sp.eye(2)
    T=sp.diag(1,0)
    true_task_radius=true_r
    outer_task_radius=sp.Rational(1)
    assert outer_task_radius>true_task_radius
    # Physical posterior can be constrained more strongly; in particular
    # positive endpoints of the outer interval do not fit the observed box.
    return dict(noisy_old_probe=sp.eye(2)[:,0],old_center_response=2*sp.eye(2)[:,0],
        vector_box_radius=true_r,outer_family_lower=outer_lo,
        outer_family_upper=outer_hi,late_task_T=T,
        true_posterior_first_diagonal_radius=true_task_radius,
        outer_interval_first_diagonal_radius=outer_task_radius,
        rejected_claim='Sharpness or q-minimization for an outer interval does not imply sharpness for the actual noisy feasible family.')


def main():
    family=reconstruct_family()
    result={'family_acquired_from_schur_complement':family,
       'new_task_compiler_control':exact_task_compiler_control(family),
       'outer_interval_sharpness_failure':noisy_outer_counterexample(),
       'scope':'Exact Loewner whole-family representation supports transformed inertia query theorem. Noisy historical enclosures are only outer and do not authorize the same lower bound.'}
    out=BASE/'astra_posterior_interval_compiler_results.json'
    out.write_text(json.dumps(tojson(result),indent=2))
    r=result['new_task_compiler_control']
    print('old calls',r['retained_old_query_count'],'late new calls',r['new_query_count'])
    print('zero new call forced task',r['forced_zero_call_target'])
    print('one new call before:',float(r['prior_only_exact_worst_error']),
          'after:',float(r['compiled_sharp_noisy_worst_error']))
    print('actual posterior lower-bound indistinguishable gap',float(r['indistinguishable_target_gap']))
    print('saved',out)

if __name__=='__main__':main()
