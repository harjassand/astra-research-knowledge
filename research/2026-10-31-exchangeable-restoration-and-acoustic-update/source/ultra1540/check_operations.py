"""Replay the distinctions and the retained actual-field operations exactly."""
from pathlib import Path
from fractions import Fraction as R
import json,sys,time
from kernel import data,capacity_kernel,feature_factor
from receive import r,b,ca,dot,quadratic
from fourier import moments,gradient,average,m
from verify_closed import prepare,verify
from jet_normalize import normalize
HERE=Path(__file__).resolve().parent

def main():
    if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
    start=time.perf_counter();dd=data();cert=json.loads((HERE/'certificate.json').read_text())
    # Exact quotient coordinates, not just a dimension count.
    for j,C in enumerate(cert['unit_charge_basis']):
        nf=normalize(C);charges=list(map(R,nf['first_acoustic_binary_cubic']+nf['second_acoustic_binary_cubic']));assert charges==[R(int(i==j)) for i in range(8)]
    roots=[]
    for side in (0,1):
        for x,y in ((1,0),(0,1),(1,1),(1,-1)):
            ray=[R(x),0,R(y),0] if side==0 else [0,R(x),0,R(y)];ordinary=capacity_kernel(ray,'ordinary');closed=capacity_kernel(ray,'closed');Delta=ca.add(closed,ca.scale(ordinary,-1));assert b.rank(Delta)==1 and all(not Delta[i][j] for i in range(4) for j in range(12))
            for kind,K in (('ordinary',ordinary),('closed',closed)):
                scaled=capacity_kernel([R(-2,3)*v for v in ray],kind);assert scaled==ca.scale(K,R(4,9))
            feature_factor(ray,'closed');roots.append(ray)
    # The full-rank fixed catalogue really fails COST, and another positive
    # allocation on the same actual field repairs it with no virtual atoms.
    bad=json.loads((HERE/'catalogue_obstruction_input.json').read_text());good=json.loads((HERE/'catalogue_repair_input.json').read_text());assert bad['modes']==good['modes']
    bd=prepare(bad);gv=verify(good,bd['field']);bv=verify(bad,bd['field']);assert bd['rank']==12 and R(bv['canonical_quartic_budget'])<0 and gv['status']=='CERTIFIED_FIELD_CLOSED_CAPACITY' and gv['acoustic_limit_atoms']==0
    # A stored 21-to-17 compression is independently checked using its exact
    # multiplier on BOTH catalogues. No inverse of the expanded weights.
    raw=json.loads((HERE/'compression_input.json').read_text());compressed=json.loads((HERE/'compressed_example.json').read_text());assert raw['modes']==compressed['modes'];field=moments(raw['modes']);b.pd(field['covariance']);raw['canonical_multiplier']=compressed['canonical_multiplier']
    before=prepare(raw,field);after=prepare(compressed,field);assert before['cost']==after['cost'] and len(before['rays'])==21 and len(after['rays'])==17 and after['kinds']==['ordinary']*17
    cv=verify(compressed,field);assert cv['status']=='CERTIFIED_FIELD_CLOSED_CAPACITY' and cv['acoustic_limit_atoms']==0
    bracket=json.loads((HERE/'full_covariance_allocation_bracket.json').read_text());lower=R(bracket['global_capacity_cost_lower_bound']);upper=R(bracket['supplied_catalogue_cost_upper_bound']);assert lower<=upper==after['cost']<field['quartic_moment']
    # The negative controls remain explicitly NON-ROC. Full covariance and
    # a negative actual energy alone must not be promoted to separation.
    old=json.loads((HERE/'jet_calibration.json').read_text());full=json.loads((HERE/'full_covariance_calibration.json').read_text());assert old['global_ROC_status']==full['recorded_input_ROC_status']=='FALSE_EXACT_RANK_ONE_OBSTRUCTION'
    assert old['negative_energy_polynomial']==full['negative_energy_polynomial'] and old['mean']==full['mean']
    P=b.literal(old['negative_energy_polynomial'],4);M=list(map(R,old['mean']));t=R(old['nearby_rational_slope']);ray=[1,t,0,0];HP=[[b.diff(b.diff(P,i),j) for j in range(4)] for i in range(4)];assert quadratic([[b.evaluate(p,M) for p in row] for row in HP],ray)==R(old['negative_rank_one_Hessian'])<0
    G=gradient(full['modes']);GM=[m.add(g,{(0,0):z}) for g,z in zip(G,M)];energy=average(P,GM)-b.evaluate(P,M);assert energy==R(full['output_negative_energy'])<0
    GS=gradient(old['modes']);S=lambda V:[[average(b.mul(b.var(4,i),b.var(4,j)),V) for j in range(4)] for i in range(4)];S0,S1=S(GS),S(G);eps=R(full['perturbation_amplitude']);assert S1==[[S0[i][j]+(eps*eps/2 if i==j else 0) for j in range(4)] for i in range(4)];b.pd(S1)
    result={'unit_jet_coordinates_reconstructed':8,'rank_one_kernel_jump_and_homogeneity_checks':len(roots),'fixed_completed_catalogue_full_rank_cost_failure_verified':True,'same_actual_field_repaired_by_six_ordinary_atoms':True,'full_covariance_actual_fourier_modes':12,'ordinary_catalogue_compression':[21,17],'all_twelve_targets_and_exact_canonical_cost_preserved':True,'expanded_matrix_reinversion_not_used':True,'global_lower_bound_and_fixed_catalogue_upper_bound_consistent':True,'negative_control_polynomial_globally_ROC':False,'negative_energy_preserved_with_full_covariance':True,'genuine_ROC_QC_separation_found':False,'full_face_QC':'NOT_RESOLVED','seconds':time.perf_counter()-start}
    (HERE/'operations_replay.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
