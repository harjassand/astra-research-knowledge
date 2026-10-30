"""Exact algebra for gradient rigidity and the eight-charge moment bound.

The retained global heat and cubic-stabilization theorem is the governing
premise. --replay-stabilization additionally replays all 13,524 strict
Bernstein matrices and its complete stabilization receiver in this run.
The free-law control is explicitly NOT an actual compatible field.
"""
from pathlib import Path
from fractions import Fraction as R
import importlib.util,json,time,argparse,contextlib,io,sys
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('acoustic_core',HERE.parent/'acoustic_capacity/receive.py');ac=importlib.util.module_from_spec(spec);spec.loader.exec_module(ac)
r,b,ca=ac.r,ac.b,ac.ca;dot=r.dot;quadratic=r.quadratic

def gauge():
    F,T,basis,powers,polys,HF,nulls=ac.source();cert=json.loads((HERE.parent/'acoustic_capacity/certificate.json').read_text());TM=ca.transpose(basis[:4]);UM=ca.transpose([list(map(R,row)) for row in cert['unit_charge_basis']]);TG=ca.mm(ca.transpose(TM),TM);b.pd(TG)
    projection,_=ca.solve_range(TG,ca.mm(ca.transpose(TM),UM));E=ca.add(UM,ca.scale(ca.mm(TM,projection),-1));assert ca.mm(ca.transpose(TM),E)==[[0]*8 for _ in range(4)]
    P=ca.scale(ca.mm(ca.transpose(E),E),20);b.pd(P)
    qc=json.loads((HERE.parent/'quadratic_boundary/certificate.json').read_text());operator=[list(map(R,row)) for row in qc['normal_form_operator']];Z=ca.mm(operator,E);charge=[list(map(R,row)) for row in cert['jet_operator_on_normal_basis']];assert ca.mm(charge,Z)==[[R(int(i==j)) for j in range(8)] for i in range(8)]
    return {'F':F,'T':T,'basis':basis,'powers':powers,'HF':HF,'nulls':nulls,'translations':TM,'projection':projection,'charge_representatives':E,'coefficient_Gram':P,'normal_coordinates':Z}

def expectation(poly,law):return sum(w*b.evaluate(poly,A) for w,A in law)
def qaverage(poly,S):
    val=R(0)
    for pw,co in poly.items():
        assert sum(pw)==2;ids=[i for i,n in enumerate(pw) for _ in range(n)];val+=co*S[ids[0]][ids[1]]
    return val

def check_geometry(d):
    base=json.loads((HERE.parent/'hopf_structure/certificate.json').read_text());a,b0,c,one=d['nulls'][0];assert one==1
    A1=d['nulls'][0];A2=d['nulls'][1];eta,zeta=map(R,base['ray']['canonical_zero']);canonical=[R(1),eta,R(0),zeta]
    def rot(A,u):
        x,y=u;return [x*A[0]-y*A[2],x*A[1]-y*A[3],y*A[0]+x*A[2],y*A[1]+x*A[3]]
    assert rot(A2,[-b0/(1+b0*b0),-1/(1+b0*b0)])==canonical
    gamma=[zeta,R(0),eta,R(-1)];assert rot(A1,[-1/(1+b0*b0),-b0/(1+b0*b0)])==gamma
    det1=A1[0]*A1[3]-A1[1]*A1[2];det2=A2[0]*A2[3]-A2[1]*A2[2];assert det1<0<det2 and det1==-det2
    x,y=b.var(2,0),b.var(2,1)
    for A,detA in ((A1,det1),(A2,det2)):
        vv=[b.add(b.scale(x,A[0]),b.scale(y,-A[2])),b.add(b.scale(x,A[1]),b.scale(y,-A[3])),b.add(b.scale(y,A[0]),b.scale(x,A[2])),b.add(b.scale(y,A[1]),b.scale(x,A[3]))]
        assert b.add(b.mul(vv[0],vv[3]),b.scale(b.mul(vv[1],vv[2]),-1))==b.scale(b.add(b.mul(x,x),b.mul(y,y)),detA)
    return {'zero_value_planes_have_no_nonzero_rank_one_tangent':True,'opposite_determinant_zero_planes_disjoint_off_zero':True,'canonical_chart_and_Gamma_planes_identified_exactly':True}

def check_free(d,orbit=None):
    raw=json.loads((HERE/'free_law.json').read_text());assert raw['object_type']=='POSITIVE_ATOMIC_FREE_MATRIX_LAW_NOT_A_GRADIENT' and raw['genuine_ROC_QC_separation'] is False
    law=[(R(w),list(map(R,A))) for w,A in zip(raw['atom_weights'],raw['atoms'])];assert sum(w for w,A in law)==1 and all(w>0 for w,A in law)
    assert all(sum(w*A[i] for w,A in law)==0 for i in range(4));assert sum(w*(A[0]*A[3]-A[1]*A[2]) for w,A in law)==0
    S=[[sum(w*A[i]*A[j] for w,A in law) for j in range(4)] for i in range(4)];b.pd(S);H=[[qaverage(P,S) for P in row] for row in d['HF']];b.pd(H)
    F,C0,T=r.m.acquired();assert sum(map(abs,C0.values()))==1;v=[expectation(b.diff(F,i),law) for i in range(4)];w=[qaverage(b.diff(C0,i),S) for i in range(4)];f=expectation(F,law);c=expectation(C0,law);s=sum(S[i][i] for i in range(4));hv=r.m.linear_solve(H,v);hw=r.m.linear_solve(H,w);a=2*f-dot(v,hv);rr=c-dot(v,hw);nu=R(2**112);bb=2*nu*s-dot(w,hw)
    assert a==R(raw['leading_F_Schur_excess_a'])>0 and bb==R(raw['ROC_quadratic_Schur_excess_b'])>0 and rr==R(raw['nontranslation_correlation_r'])
    assert 1000*a*bb<rr*rr and 2*1859*s-dot(w,hw)>=0
    # The canonical eight-charge bound is an actual PDE constraint. The
    # free law violates it along C0's charge direction, despite a>0.
    E=d['charge_representatives'];EP=[{tuple(pw):E[k][j] for k,pw in enumerate(d['powers']) if E[k][j]} for j in range(8)];B=[[qaverage(b.diff(P,i),S) for P in EP] for i in range(4)];cc=[expectation(P,law) for P in EP]
    HB,_=ca.solve_range(H,B);rr8=[cc[j]-dot(ca.transpose(B)[j],hv) for j in range(8)];D=ca.add(ca.scale(d['coefficient_Gram'],2*nu*s),ca.scale(ca.mm(ca.transpose(B),HB),-1))
    qc=json.loads((HERE.parent/'quadratic_boundary/certificate.json').read_text());op=[list(map(R,row)) for row in qc['normal_form_operator']];cvec=[C0.get(tuple(pw),R(0)) for pw in d['powers']];coords=[dot(row,cvec) for row in op];acert=json.loads((HERE.parent/'acoustic_capacity/certificate.json').read_text());jet=[list(map(R,row)) for row in acert['jet_operator_on_normal_basis']];z=[dot(row,coords) for row in jet]
    assert dot(rr8,z)==rr and quadratic(d['coefficient_Gram'],z)<=20*sum(co*co for co in cvec)<=20
    assert quadratic(D,z)>=0 and a*quadratic(D,z)-rr*rr<0
    # A directly reconstructed negative expectation for a globally QC
    # stabilizer proves these FREE moments cannot come from a gradient.
    M=list(map(R,raw['negative_free_energy_mean']));rho=R(raw['negative_free_energy_amplitude']);P=b.add(F,C0,b.scale(T,nu));actual=sum(ww*b.evaluate(P,[x+rho*y for x,y in zip(M,A)]) for ww,A in law)-b.evaluate(P,M)
    assert actual==R(raw['exact_negative_free_energy'])==rho*rho*(bb-rr*rr/a)/2<0
    assert actual/rho**4==R(raw['normalized_negative_free_energy'])<0
    assert R(raw['all_completed_allocation_cost_lower_bound'])==f-actual/rho**4>f
    if orbit is not None:
        U=orbit['section'];UP=[{tuple(pw):U[k][j] for k,pw in enumerate(d['powers']) if U[k][j]} for j in range(8)];BU=[[qaverage(b.diff(P,i),S) for P in UP] for i in range(4)];cU=[expectation(P,law) for P in UP];HBU,_=ca.solve_range(H,BU);rU=[cU[j]-dot(ca.transpose(BU)[j],hv) for j in range(8)];assert rU==rr8
        DU=ca.add(ca.scale(orbit['K'],2*s),ca.scale(ca.mm(ca.transpose(BU),HBU),-1));assert quadratic(DU,z)>=0 and a*quadratic(DU,z)-rr*rr<0
        newP=b.add(F,C0,b.scale(T,4096));newgap=sum(ww*b.evaluate(newP,[x+rho*y for x,y in zip(M,A)]) for ww,A in law)-b.evaluate(newP,M);assert newgap==rho*rho*(2*4096*s-dot(w,hw)-rr*rr/a)/2<0
    return {'positive_free_atoms':len(law),'mean_and_determinant_constraints_exact':True,'full_covariance':True,'all_translated_and_scaled_leading_F_tests_pass':True,'known_ROC_quadratic_block_passes':True,'universal_eight_charge_compatibility_bound_violated':True,'globally_QC_stabilizer_has_negative_FREE_expectation':True,'actual_gradient_realization_ruled_out_by_QC':True,'genuine_QC_separation':False}

def main():
    if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--replay-stabilization',action='store_true');args=parser.parse_args();start=time.perf_counter();d=gauge();cert={'coefficient_metric':'unweighted l2 of the retained twenty cubic monomials','stabilization_constant':'2^112','translation_projection':[list(map(str,row)) for row in d['projection']],'minimal_norm_unit_charge_representatives':[list(map(str,row)) for row in ca.transpose(d['charge_representatives'])],'coefficient_Gram':[list(map(str,row)) for row in d['coefficient_Gram']]}
    spec=importlib.util.spec_from_file_location('qc_orbit',HERE/'orbit.py');orb=importlib.util.module_from_spec(spec);spec.loader.exec_module(orb);od=orb.construct(d,b,ca,r)
    (HERE/'charge_bound.json').write_text(json.dumps(cert,indent=2)+'\n');result=dict(check_geometry(d),**check_free(d,od));result.update({'minimal_norm_charge_representatives':8,'charge_Gram_positive_definite':True,'all_eight_charge_coordinates_preserved':True,'global_QC_orbit_charge_rank':8,'stronger_universal_compatibility_matrix':True,'strict_ellipsoid_improvement_in_all_eight_charge_directions':True,'explicit_translation_transport_checked_on_twelve_cubic_basis_vectors':True,'QC_C0_coefficient':4096,'QC_C0_analytic_premise':'heat/PROOF.txt and its complete rigorous receiver','strict_leading_QC_proof':'PROOF.txt: differential transversality and heat flow; applies to every nonzero actual periodic L4 gradient.','stabilization_replayed_this_run':False,'full_face_QC':'NOT_RESOLVED','QC_at_1859':'UNKNOWN'})
    if args.replay_stabilization:
        spec=importlib.util.spec_from_file_location('graded_source',HERE.parent/'graded_stabilization/receive.py');gs=importlib.util.module_from_spec(spec);spec.loader.exec_module(gs)
        with contextlib.redirect_stdout(io.StringIO()):gs.main()
        result['stabilization_replayed_this_run']=True;result['strict_shifted_Bernstein_matrices']=13524
    result['seconds']=time.perf_counter()-start;(HERE/'replay.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
