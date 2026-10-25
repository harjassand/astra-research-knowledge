"""ASTRA Pro3 -- task-specific scalar readout and retained-information tradeoff.

A native bilinear scalar q,v -> v^T S q with ||q||,||v||<=1 and
adversarial absolute error<=eta can achieve the same sharp minimax scalar
late-task frontier as a full-vector q -> S q experiment with Euclidean
noise<=eta, assuming unrestricted programmable readouts and fixed symmetric
operator-norm prior. This does NOT imply that scalar measurements contain
as much reusable information for later unknown tasks.

The source-like matrices below are analytic software controls. No physical
programmable detector is claimed or simulated as calibrated hardware.
"""
from __future__ import annotations
from pathlib import Path
import json
import sympy as sp

ROOT=Path(__file__).resolve().parent


def sm(A):
    return A.applyfunc(sp.simplify) if isinstance(A,sp.MatrixBase) else sp.simplify(A)


def encode(x):
    if isinstance(x,sp.MatrixBase): return [[str(sm(x[i,j])) for j in range(x.cols)] for i in range(x.rows)]
    if isinstance(x,sp.Basic):return str(sm(x))
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [encode(v) for v in x]
    return x


def sym(q,v):return (q*v.T+v*q.T)/2


def rotation(n):
    P=sp.eye(n)
    for co in ([1,2,-1,2,3,-2],[2,-1,2,1,-3,1]):
        u=sp.Matrix(co)
        P=sm(P*(sp.eye(n)-2*u*u.T/(u.T*u)[0]))
    assert P.T*P==sp.eye(n)
    return P


def scalarized_frontier():
    n=6;eye=sp.eye(n);P=rotation(n)
    vals=[144,9,-25,-16,0,0]
    T=sm(P*sp.diag(*vals)*P.T)
    q1=sm(P*(12*eye[:,0]+5*eye[:,2])/13)
    v1=sm(P*(12*eye[:,0]-5*eye[:,2])/13)
    q2=sm(P*(3*eye[:,1]+4*eye[:,3])/5)
    v2=sm(P*(3*eye[:,1]-4*eye[:,3])/5)
    q=[q1,q2];v=[v1,v2];weights=[sp.Integer(169),sp.Integer(25)]
    assert all(sm(x.dot(x))==1 for x in q+v)
    assert sm(weights[0]*sym(q1,v1)+weights[1]*sym(q2,v2)-T)==sp.zeros(n)
    R=sp.Rational(1,4);eta=sp.Rational(1,10000);S0=2*eye
    scenarios=[]
    for k in range(3):
        observed_indices=([0,2] if k>=1 else [])+([1,3] if k>=2 else [])
        Hdiag=[(eta if i in observed_indices else R)*sp.sign(vals[i]) for i in range(n)]
        H=sm(P*sp.diag(*Hdiag)*P.T)
        Splus=S0+H;Sminus=S0-H
        reports=[];noise=[]
        for j in range(k):
            center=(v[j].T*S0*q[j])[0]
            assert sm((v[j].T*H*q[j])[0])==eta
            plus_reading=(v[j].T*Splus*q[j])[0]
            minus_reading=(v[j].T*Sminus*q[j])[0]
            assert sm(center-plus_reading)==-eta
            assert sm(center-minus_reading)==eta
            reports.append(center)
            noise.append(dict(plus_error=-eta,minus_error=eta))
        estim=sm(sp.trace(T*S0)+sum(weights[j]*(reports[j]-(v[j].T*S0*q[j])[0]) for j in range(k)))
        value_plus=sm(sp.trace(T*Splus));value_minus=sm(sp.trace(T*Sminus))
        tail=sum(abs(vals[i]) for i in range(n) if i not in observed_indices)
        head=sum(weights[:k]); assert head+tail==194
        bound=R*tail+eta*head
        assert sm(value_plus-estim)==bound
        assert sm(estim-value_minus)==bound
        assert sm(value_plus-value_minus)==2*bound
        scenarios.append(dict(native_scalar_calls=k,returned_scalar_values=k,
            matching_full_vector_calls=k,matching_full_vector_returned_scalar_values=k*n,
            exact_task=T,source_prior_center=S0,source_radius=R,readout_error_bound=eta,
            scalar_inputs=sp.Matrix.hstack(*q[:k]) if k else sp.zeros(n,0),
            programmed_unit_readouts=sp.Matrix.hstack(*v[:k]) if k else sp.zeros(n,0),
            decoder_scalar_weights=weights[:k],
            shared_reported_scalar_centers=reports,
            allowed_report_errors=noise,
            indistinguishable_plus_source=Splus,
            indistinguishable_minus_source=Sminus,
            attained_sharp_worst_error=bound,
            error_propagation_from_omitted_spectrum=R*tail,
            error_propagation_from_scalar_noise=eta*head,
            matched_witness_gap=2*bound,
            reported_task_estimate=estim,
            actual_plus_task_value=value_plus,
            actual_minus_task_value=value_minus))
    assert [r['attained_sharp_worst_error'] for r in scenarios]==[
        sp.Rational(194,4),
        sp.Rational(25,4)+sp.Rational(169,10000),
        sp.Rational(194,10000)]
    return dict(task=T,eigenvalues=vals,
        exact_scalarization=sm(sum([weights[j]*sym(q[j],v[j]) for j in range(2)],sp.zeros(n))),
        benchmark=scenarios,
        warning='Scalar readout is a native additional interface; calculating v.T*(S q) after first receiving all n coordinates does not save measurement bandwidth.')


def off_task_reuse_counterexample():
    n=2;R=sp.Rational(1,4);S0=2*sp.eye(n);eye=sp.eye(n)
    q=(eye[:,0]+eye[:,1])/sp.sqrt(2)
    v=(eye[:,0]-eye[:,1])/sp.sqrt(2)
    task1=sp.diag(1,-1)
    task2=q*q.T
    assert sm(2*sym(q,v))==task1
    assert sm(q.dot(v))==0
    Sminus=S0-R*eye;Splus=S0+R*eye
    scalar_minus=sm((v.T*Sminus*q)[0]);scalar_plus=sm((v.T*Splus*q)[0])
    assert scalar_minus==scalar_plus==0
    full_minus=Sminus*q;full_plus=Splus*q
    assert full_minus!=full_plus
    later_minus=sm(sp.trace(task2*Sminus));later_plus=sm(sp.trace(task2*Splus))
    assert later_plus-later_minus==2*R
    assert later_minus==2-R and later_plus==2+R
    return dict(old_known_task=task1,
       old_native_input=q,old_native_scalar_readout=v,
       old_native_scalar_measurement_for_both_sources=scalar_minus,
       future_new_task=task2,
       source1=Sminus,source2=Splus,
       full_vector_old_reading_source1=full_minus,
       full_vector_old_reading_source2=full_plus,
       future_task_values=[later_minus,later_plus],
       remaining_future_task_radius_after_scalar_history=R,
       remaining_future_task_radius_after_full_vector_history=0,
       conclusion='Sufficient scalar data for a known task need not preserve information for an unknown later task even though the same full-vector native action would.')


def universal_tomography_tradeoff():
    n=3; d=n*(n+1)//2;eye=sp.eye(n)
    catalogue=[(i,j) for i in range(n) for j in range(i,n)]
    assert len(catalogue)==d
    S0=2*eye; eps=sp.Rational(1,4)
    H=eps*eye[:,2]*eye[:,2].T
    Sminus=S0-H;Splus=S0+H
    # The first five scalar bilinear samples omit S22 and cannot distinguish.
    for i,j in catalogue[:-1]:
        assert (eye[:,i].T*Sminus*eye[:,j])[0]==(eye[:,i].T*Splus*eye[:,j])[0]
    assert (eye[:,2].T*Sminus*eye[:,2])[0]!=(eye[:,2].T*Splus*eye[:,2])[0]
    return dict(port_dimension=n,symmetric_matrix_parameter_dimension=d,
        required_native_scalar_calls_to_recover_every_symmetric_entry=d,
        explicit_scalar_tomography_catalogue=[dict(readout_index=i,input_index=j) for i,j in catalogue],
        full_vector_calls_to_recover_every_symmetric_entry=n,
        full_vector_total_scalar_outputs=n*n,
        scalar_tomography_total_scalar_outputs=d,
        partial_scalar_history_sources=[Sminus,Splus],
        exact_identical_first_five_readings=True,
        undecidable_late_task=eye[:,2]*eye[:,2].T,
        general_lower_bound='Any k < n(n+1)/2 scalar linear observations leave a nonzero null direction in the full symmetric source space. A future task aligned with that direction distinguishes compatible sources, even if the old scalar experiment policy was adaptive on a central-response branch.')


def main():
    res=dict(scalar_native_precision_frontier=scalarized_frontier(),
             unknown_future_task_information_loss=off_task_reuse_counterexample(),
             all_future_tasks_tomography_tradeoff=universal_tomography_tradeoff(),
             scope='Unrestricted true native bilinear scalar readout, symmetric operator ball, deterministic bounded absolute scalar error. No native scalar detector was physically acquired, and no cross-task universal superiority is claimed.')
    path=ROOT/'astra_scalar_readout_transfer_results.json'
    path.write_text(json.dumps(encode(res),indent=2))
    print('scalar frontier', [float(row['attained_sharp_worst_error']) for row in res['scalar_native_precision_frontier']['benchmark']])
    print('native scalar vs native vector returned values for k=2:',2,'vs',12)
    print('scalar old vs vector old future residual radii',
          float(res['unknown_future_task_information_loss']['remaining_future_task_radius_after_scalar_history']),
          float(res['unknown_future_task_information_loss']['remaining_future_task_radius_after_full_vector_history']))
    print('universal tomography n=3, scalar calls vs vector calls:',6,'vs',3)
    print('results',path)

if __name__=='__main__':main()
