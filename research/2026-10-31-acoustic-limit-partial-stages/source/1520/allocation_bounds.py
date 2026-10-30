"""Keep fixed-catalogue and all-allocation information separate.

A feasible supplied catalogue gives an UPPER bound on the globally least
capacity cost. A globally ROC-admitted polynomial orbit gives a LOWER
bound on that same cost. Only a lower bound above the actual quartic
moment would certify an actual ROC/QC separation, reconstructed directly.
"""
from pathlib import Path
from fractions import Fraction as R
import importlib.util,argparse,json,sys,contextlib,io
from fourier import moments,average,m
from kernel import data
from verify_closed import prepare
from receive import r,b,ca,dot,quadratic
HERE=Path(__file__).resolve().parent

def bounds(payload,replay_admission=True):
    if replay_admission:
        spec=importlib.util.spec_from_file_location('roc_admission',HERE.parent/'quadratic_boundary/receive.py');ad=importlib.util.module_from_spec(spec);spec.loader.exec_module(ad)
        with contextlib.redirect_stdout(io.StringIO()):ad.main()
    dd=data();field=moments(payload['modes']);G=field['gradient'];F,C0,T=r.m.acquired();f=field['quartic_moment'];H=[[average(p,G) for p in row] for row in dd['HF']];v=field['cubic_target'][:4]
    w=[average(b.diff(C0,i),G) for i in range(4)];c=average(C0,G);q=1859*average(T,G);K=[row+[w[i]] for i,row in enumerate(H)]+[w+[2*q]];d=v+[c];r.psd(K)
    try:
        sol,_=ca.solve_range(K,[[x] for x in d]);sol=[row[0] for row in sol];x=[-z for z in sol];lower=dot(d,sol)/2;orbit_gap=f-lower
    except ca.RangeObstruction as obstruction:
        null=obstruction.annihilator;pairing=dot(null,d);assert pairing
        x=[-(f+1)*z/pairing for z in null];lower=None;orbit_gap=R(-1)
    M=x[:4];lam=x[4];assert orbit_gap==f+dot(v,M)+quadratic(H,M)/2+lam*(c+dot(w,M))+lam*lam*q
    upper=None;catalogue_status='NOT_SUPPLIED'
    if payload.get('catalogue'):
        try:
            op=prepare(payload,field);upper=op['cost'];catalogue_status='FEASIBLE_CATALOGUE';assert lower is not None and lower<=upper
        except ca.RangeObstruction:catalogue_status='FIXED_CATALOGUE_RANGE_OBSTRUCTION'
    negative=orbit_gap<0
    if negative:
        P=b.add(F,b.scale(C0,lam),b.scale(T,1859*lam*lam));GM=[m.add(g,{(0,0):z}) for g,z in zip(G,M)]
        actual=average(P,GM)-b.evaluate(P,M);assert actual==orbit_gap and actual<0
    result={'global_capacity_cost_lower_bound':None if lower is None else str(lower),'supplied_catalogue_cost_upper_bound':None if upper is None else str(upper),'actual_quartic_moment':str(f),'catalogue_status':catalogue_status,'lower_bound_source':'The globally ROC orbit F+lambda*C0+1859*lambda^2*T, with arbitrary argument translation.','admission_source':'../quadratic_boundary/receive.py: exact global 16x16 biform Gram for F+C0+1859*T.','admission_replayed':replay_admission,'ROC_orbit_mean':list(map(str,M)),'ROC_orbit_cubic_scale':str(lam),'ROC_orbit_exact_energy_gap':str(orbit_gap),'negative_actual_compatible_energy':negative,'status':'ACTUAL_GLOBALLY_ROC_SEPARATION' if negative else ('UNIVERSAL_FIELD_BOUND_CERTIFIED' if upper is not None and upper<=f else 'BRACKET_ONLY'),'all_allocation_negative_gap_certified':negative,'full_face_QC':'NOT_RESOLVED','scope':'The lower bound applies to EVERY admissible ordinary or closed covariance allocation. A supplied catalogue only bounds the optimum from above. A nonnegative ROC-orbit gap does not prove the fixture globally QC. A negative status requires the explicitly admitted orbit and a directly reconstructed actual compatible energy.'}
    return result

def main():
    if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',type=Path);parser.add_argument('--out',type=Path);args=parser.parse_args();result=bounds(json.loads(args.input.read_text()))
    if args.out:args.out.write_text(json.dumps(result,indent=2)+'\n')
    summary={k:result[k] for k in ('status','catalogue_status','admission_replayed','negative_actual_compatible_energy')}
    for key in ('global_capacity_cost_lower_bound','supplied_catalogue_cost_upper_bound','actual_quartic_moment','ROC_orbit_exact_energy_gap'):
        summary[key]=None if result[key] is None else float(R(result[key]))
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
