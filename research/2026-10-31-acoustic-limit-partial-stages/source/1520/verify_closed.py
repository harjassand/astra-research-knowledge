"""Exact closed-capacity verification for an actual finite Fourier field.

Closed acoustic atoms use limiting global ROC inequalities. They must not
be confused with finite-background Hessian evaluations at singular rays.
A failed catalogue does not rule out other covariance allocations.
"""
from pathlib import Path
from fractions import Fraction as R
import argparse,json,sys
from kernel import data,capacity_kernel,acoustic_side
from fourier import moments,average
from receive import r,b,ca,dot,quadratic
HERE=Path(__file__).resolve().parent

def prepare(payload,field=None):
    field=moments(payload['modes']) if field is None else field;rows=[row for row in payload['catalogue'] if R(row['weight'])]
    weights=[R(row['weight']) for row in rows];rays=[list(map(R,row['rank_one_direction'])) for row in rows];kinds=[row.get('kind','closed') for row in rows]
    assert weights and all(w>0 for w in weights)
    S=[[sum(w*v[i]*v[j] for w,v in zip(weights,rays)) for j in range(4)] for i in range(4)]
    if S!=field['covariance']:raise ValueError('The catalogue does not match the actual field covariance.')
    kernels=[capacity_kernel(ray,kind) for ray,kind in zip(rays,kinds)];W=ca.add(*(ca.scale(K,w) for K,w in zip(kernels,weights)))
    if 'canonical_multiplier' in payload:
        lam=list(map(R,payload['canonical_multiplier']));assert len(lam)==12 and [dot(row,lam) for row in W]==field['cubic_target'];rank=None
    else:
        sol,rank=ca.solve_range(W,[[v] for v in field['cubic_target']]);lam=[row[0] for row in sol]
    cost=dot(field['cubic_target'],lam)/2
    assert cost==quadratic(W,lam)/2
    return {'field':field,'rows':rows,'weights':weights,'rays':rays,'kinds':kinds,'kernels':kernels,'capacity':W,'multiplier':lam,'rank':rank,'cost':cost}

def verify(payload,field=None):
    try:op=prepare(payload,field)
    except ValueError as exc:
        if isinstance(exc,ca.RangeObstruction):
            return {'status':'FIXED_CATALOGUE_RANGE_OBSTRUCTION','annihilator':list(map(str,exc.annihilator)),'nonzero_target_pairings':list(map(str,exc.target_values)),'scope':'Only this ordinary/closed catalogue fails; no all-allocation or QC failure follows.'}
        raise
    dd=data();field=op['field'];f=field['quartic_moment'];T4=field['radial_fourth_moment'];budget=f-op['cost'];gap=R(payload.get('requested_L4_gap','0'));assert gap>=0
    W=op['capacity'];H=[row[:4] for row in W[:4]];B=[row[4:] for row in W[:4]];D=[row[4:] for row in W[4:]]
    v=field['cubic_target'][:4];cc=field['cubic_target'][4:];Hv,hrank=ca.solve_range(H,[[x] for x in v]);HB,_=ca.solve_range(H,B)
    Lambda=ca.add(D,ca.scale(ca.mm(ca.transpose(B),HB),-1));rr=[cc[i]-dot(ca.transpose(B)[i],[row[0] for row in Hv]) for i in range(8)];z=op['multiplier'][4:]
    assert [dot(row,z) for row in Lambda]==rr
    a=2*f-dot(v,[row[0] for row in Hv]);assert a-dot(rr,z)==2*budget
    passed=budget>=gap*T4
    # Each kernel is explicitly PSD. Its positive sum W has a PSD Schur
    # complement Lambda. The identities Lambda*z=r and
    # a-r.z=2*budget factor the 9x9 LMI into positive terms exactly.
    if passed:assert a-2*gap*T4-dot(rr,z)>=0
    # A literal identity for the independently globally ROC-admitted fixture.
    # This uses limiting Schur slacks at jet atoms, not invented finite bases.
    qc=json.loads((HERE.parent/'quadratic_boundary/certificate.json').read_text());c0=list(map(R,qc['example_cubic_coefficients']));operator=[list(map(R,row)) for row in qc['normal_form_operator']];z=[dot(row,c0) for row in operator]
    Q=b.scale(dd['T'],1859);slacks=[2*b.evaluate(Q,ray)-quadratic(K,z) for ray,K in zip(op['rays'],op['kernels'])];assert all(v>=0 for v in slacks)
    zz=[x+y for x,y in zip(z,op['multiplier'])];rhs=budget+quadratic(op['capacity'],zz)/2+sum(w*s/2 for w,s in zip(op['weights'],slacks))
    C0={tuple(pw):co for pw,co in zip(dd['powers'],c0) if co};actual=average(b.add(dd['F'],C0,Q),field['gradient']);assert actual==rhs
    jets=sum(kind=='closed' and acoustic_side(ray) is not None for ray,kind in zip(op['rays'],op['kinds']))
    return {'status':'CERTIFIED_FIELD_CLOSED_CAPACITY' if passed else 'FIXED_CATALOGUE_BUDGET_INSUFFICIENT','actual_compatible_fourier_modes':len(payload['modes']),'covariance_rank':b.rank(field['covariance']),'catalogue_atoms':len(op['rays']),'acoustic_limit_atoms':jets,'capacity_rank':op['rank'],'quotient_capacity_rank':'NOT_REQUIRED_FOR_MULTIPLIER_CERTIFICATE','translation_rank':hrank,'canonical_quartic_budget':str(budget),'fourth_gradient_moment':str(T4),'requested_L4_gap':str(gap),'requested_lower_bound':str(gap*T4),'nine_by_nine_capacity_LMI_verified':passed,'actual_fixture_energy_identity':True,'all_fixture_ROC_slacks_nonnegative':True,'all_allocations_status':'NOT_TESTED','full_face_QC':'NOT_RESOLVED','scope':'A passing result proves the requested bound for this actual field at every mean and overall amplitude, for every globally ROC polynomial over F. Closed acoustic atoms are limiting inequalities. A failed catalogue is not an all-allocation failure or a QC counterexample.'}

def main():
    if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',type=Path);parser.add_argument('--out',type=Path);args=parser.parse_args();result=verify(json.loads(args.input.read_text()))
    if args.out:
        args.out.write_text(json.dumps(result,indent=2)+'\n');summary={k:result[k] for k in ('status','actual_compatible_fourier_modes','covariance_rank','catalogue_atoms','acoustic_limit_atoms','capacity_rank','nine_by_nine_capacity_LMI_verified','actual_fixture_energy_identity') if k in result}
        for key in ('canonical_quartic_budget','requested_lower_bound'):
            if key in result:summary[key]=float(R(result[key]))
        print(json.dumps(summary,indent=2))
    else:print(json.dumps(result,indent=2))
if __name__=='__main__':main()
