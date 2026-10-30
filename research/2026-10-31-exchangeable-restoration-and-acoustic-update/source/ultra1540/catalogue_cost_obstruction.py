"""Exact matched control: completed original rays fail; another allocation passes."""
from pathlib import Path
from fractions import Fraction as R
import sys,json
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'outputs/acoustic_capacity'))
from receive import r,b,ca,dot,quadratic
from verify_closed import verify,prepare
from kernel import data,capacity_kernel,feature_factor
D=data();sd=r.setup();direct=json.loads((root/'work/closed_fourwave_direct.json').read_text());X=[[R(v) for v in row] for row in direct['profiles'][0]]
# The original three closed feature maps are square and invertible.
# Their exact unique profile gives E=e0*B*C+e1*A*C+e2*A*B.
# Reconstruct e_i from K_i and the actual cubic target via canonical cost
# at three rational amplitude points; this independently checks the source
# profile cost formula and avoids importing producer Hessian factors.
energies=[]
for amp in ((1,1,1),(2,1,1),(1,2,1)):
    a,bb,h=map(R,amp);payload={'modes':[{'frequency':[1,0],'sine':[str(a),'0']},{'frequency':[0,1],'sine':['0',str(bb)]},{'frequency':[1,1],'sine':[str(h),str(h)]}],'catalogue':[{'weight':str(v*v/2),'rank_one_direction':list(map(str,ray)),'kind':'closed'} for v,ray in zip((a,bb,h),sd['original'][:3])]};op=prepare(payload);energies.append(op['cost']);assert op['rank']==12
M=[[R(1),R(1),R(1)],[R(1),R(4),R(4)],[R(4),R(1),R(4)]];e=r.m.linear_solve(M,energies)
# The interval formula is certified from the unique symbolic source profile,
# not inferred from three sample values.
factors=[feature_factor(ray,'closed') for ray in sd['original'][:3]]
L=[[factors[i][1][j][k] for i in range(3) for j in range(4)] for k in range(12)]
target=[dot(row,[v[0] for v in sd['targets']]) for row in D['basis']];sol,feature_rank=ca.solve_range(L,[[v] for v in target]);assert feature_rank==12
XX=[[sol[4*i+j][0] for j in range(4)] for i in range(3)]
assert e==[quadratic(factors[i][0],XX[i]) for i in range(3)]
Fm=sd['FM'];p0=Fm[0][0]+Fm[1][1]+2*Fm[0][1]-e[2];p2=2*(Fm[0][2]+Fm[1][2])-e[0]-e[1];p4=Fm[2][2]
upper=p0+max(p2,0)/16+max(p4,0)/256;assert upper<R(-1,5)
# Both cubic resonances now remain active, with all four amplitudes nonzero.
amps=list(map(R,['1','1','1/10','1/1000']));modes=[{'frequency':list(k),'sine':list(map(str,v))} for k,v in zip(((1,0),(0,1),(1,1),(2,1)),((amps[0],0),(0,amps[1]),(amps[2],amps[2]),(2*amps[3],amps[3])))]
old={'modes':modes,'catalogue':[{'weight':str(a*a/2),'rank_one_direction':list(map(str,ray)),'kind':'closed'} for a,ray in zip(amps,sd['original'])],'requested_L4_gap':'0'}
old_op=prepare(old);old_result=verify(old,old_op['field']);assert old_result['status']=='FIXED_CATALOGUE_BUDGET_INSUFFICIENT' and old_op['rank']==12
outers=[[ray[i]*ray[j] for i in range(4) for j in range(i,4)] for ray in sd['original']];assert b.rank(outers)==4
# The retained all-amplitude ordinary exchange supplies a different positive
# allocation of the SAME actual covariance. The proportional extra leaf ray
# is merged with the middle auxiliary direction using degree-two homogeneity.
cert=json.loads((root/'outputs/shared_mode_gluing/certificate.json').read_text());A=[x*x for x in amps];order=sorted(range(4),key=lambda i:(A[i],i));case=next(x for x in cert['charts'] if x['order']==order);bi=case['base'];assert bi==0;ids=(0,1,2);m=min(A[i] for i in ids);eps=R(case['epsilon']);weights=[A[i]/2-eps*m for i in ids]+[eps*m*eta for eta in sd['eta']];weights[4]+=16*A[3]/2
new={'modes':modes,'catalogue':[{'weight':str(w),'rank_one_direction':list(map(str,ray)),'kind':'ordinary'} for w,ray in zip(weights,sd['rays'][0][:6])],'requested_L4_gap':'1/32'}
new_op=prepare(new,old_op['field']);new_result=verify(new,old_op['field']);assert new_result['status']=='CERTIFIED_FIELD_CLOSED_CAPACITY' and new_result['acoustic_limit_atoms']==0
summary={'third_wave_interval':'0<|h|<=1/4 with a=b=1 and d=0','three_closed_original_rays_capacity_rank':12,'unique_three_ray_source_profile':[list(map(str,row)) for row in XX],'three_ray_least_cost_pair_coefficients':list(map(str,e)),'three_ray_quartic_budget_coefficients_in_h2':list(map(str,(p0,p2,p4))),'uniform_three_ray_budget_upper_bound':str(upper),'four_wave_original_closed_catalogue_atoms':4,'four_wave_original_catalogue_weights_unique_for_actual_covariance':True,'four_wave_original_capacity_rank':12,'four_wave_original_quartic_budget':old_result['canonical_quartic_budget'],'same_actual_field_repaired_by_ordinary_atoms':6,'repaired_quartic_budget':new_result['canonical_quartic_budget'],'repaired_L4_gap':'1/32','scope':'A genuine cost failure for EVERY covariance weighting on the fixed original three/four directions, with actual compatible fields. A different six-ray positive allocation certifies the same four-wave field for every admitted ROC polynomial. No all-allocation failure or QC separation is present.'}
out=root/'outputs/acoustic_capacity';(out/'catalogue_obstruction_input.json').write_text(json.dumps(old,indent=2)+'\n');(out/'catalogue_repair_input.json').write_text(json.dumps(new,indent=2)+'\n');(out/'catalogue_cost_obstruction.json').write_text(json.dumps(summary,indent=2)+'\n');(out/'catalogue_obstruction_verification.json').write_text(json.dumps(old_result,indent=2)+'\n');(out/'catalogue_repair_verification.json').write_text(json.dumps(new_result,indent=2)+'\n')
print(json.dumps({'closed_three_ray_failure_interval':summary['third_wave_interval'],'uniform_budget_upper_bound':float(upper),'closed_four_wave_original_catalogue_budget':float(R(old_result['canonical_quartic_budget'])),'six_ordinary_ray_repaired_budget':float(R(new_result['canonical_quartic_budget'])),'all_allocation_failure':False,'QC_separation':False},indent=2))
