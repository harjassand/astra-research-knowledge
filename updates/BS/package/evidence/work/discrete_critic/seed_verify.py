#!/usr/bin/env python3
"""Independent exact replay of the ten-state seed using only Fraction.

Checks the finite algebraic certificate. This is not a verification of the
analytic realization/closure arguments or of novelty.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import itertools
import json
import math

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "work/hidden_equilibrium/certificate.txt"
OUT = Path(__file__).with_name("SEED_CHECK.json")
raw = SOURCE.read_bytes()
c = json.loads(raw)

def vec(x):
    return [F(t) for t in x]

def mat(x):
    return [vec(r) for r in x]

def trans(x):
    return [list(r) for r in zip(*x)]

def mul(x, y):
    yt = trans(y)
    return [[sum(a*b for a,b in zip(r,s)) for s in yt] for r in x]

def scale(x, s):
    return [[s*a for a in r] for r in x]

def add(x, y):
    return [[a+b for a,b in zip(r,s)] for r,s in zip(x,y)]

def sub(x, y):
    return add(x, scale(y, -1))

def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]

def dot(x, y):
    return sum(a*b for a,b in zip(x,y))

def rank(x):
    a = [r[:] for r in x]
    row = 0
    for col in range(len(a[0])):
        piv = next((i for i in range(row,len(a)) if a[i][col]), None)
        if piv is None:
            continue
        a[row], a[piv] = a[piv], a[row]
        d = a[row][col]
        a[row] = [v/d for v in a[row]]
        for i in range(len(a)):
            if i != row:
                d = a[i][col]
                a[i] = [u-d*v for u,v in zip(a[i],a[row])]
        row += 1
        if row == len(a):
            break
    return row

def det(x):
    a = [r[:] for r in x]
    out = F(1)
    for k in range(len(a)):
        piv = next((i for i in range(k,len(a)) if a[i][k]), None)
        if piv is None:
            return F(0)
        if piv != k:
            a[k],a[piv] = a[piv],a[k]
            out = -out
        d = a[k][k]
        out *= d
        for i in range(k+1,len(a)):
            ratio = a[i][k]/d
            a[i] = [u-ratio*v for u,v in zip(a[i],a[k])]
    return out

def inverse2(x):
    d=det(x)
    return [[x[1][1]/d,-x[0][1]/d],[-x[1][0]/d,x[0][0]/d]]

def solve(x, b):
    a=[r[:]+[t] for r,t in zip(x,b)]
    n=len(x)
    for k in range(n):
        piv=next(i for i in range(k,n) if a[i][k])
        a[k],a[piv]=a[piv],a[k]
        d=a[k][k]
        a[k]=[t/d for t in a[k]]
        for i in range(n):
            if i != k:
                d=a[i][k]
                a[i]=[u-d*w for u,w in zip(a[i],a[k])]
    return [r[-1] for r in a]

def psd2(x):
    return x==trans(x) and x[0][0]>=0 and x[1][1]>=0 and det(x)>=0

def norminf(x):
    return max(sum(abs(v) for v in r) for r in x)

def frob2(x):
    return sum(v*v for r in x for v in r)

def value(x):
    return {"exact":str(x),"decimal":float(x)}

checks={}
def check(name, condition):
    checks[name]=bool(condition)

v=mat(c["points"])
z=mat(c["farkas_z"])
Q=mat(c["Q"])
H=mat(c["H"])
M=mat(c["M"])
L=mat(c["L"])
P=add(eye(10),scale(Q,F(1,2)))
T=add(eye(8),scale(L,F(1,2)))
check("Q_shape_10_by_10",len(Q)==10 and all(len(r)==10 for r in Q))
check("Q_rows_zero",all(sum(r)==0 for r in Q))
check("Q_columns_zero",all(sum(r)==0 for r in trans(Q)))
check("Q_offdiagonal_nonnegative",all(Q[i][j]>=0 for i in range(10) for j in range(10) if i!=j))
check("Q_nonsymmetric",Q != trans(Q))
check("P_nonnegative",all(x>=0 for r in P for x in r))
check("P_rows_one",all(sum(r)==1 for r in P))
check("P_columns_one",all(sum(r)==1 for r in trans(P)))
check("QH_equals_HL",mul(Q,H)==mul(H,L))
check("PH_equals_HT",mul(P,H)==mul(H,T))
check("M_equals_HTH_over_10",M==scale(mul(trans(H),H),F(1,10)))
check("ML_equals_LTM",mul(M,L)==mul(trans(L),M))
check("MT_equals_TTM",mul(M,T)==mul(trans(T),M))
check("H_rank_8",rank(H)==8)

mean=[sum(r[j] for r in v)/5 for j in range(2)]
cent=[[a-b for a,b in zip(r,mean)] for r in v]
C=scale(mul(trans(cent),cent),F(1,5))
B=mat(c["B"])
D0=mul(B,inverse2(C))
D=add(D0,scale(eye(2),F(c["reset_rate"])))
check("mean_matches",mean==vec(c["mean"]))
check("covariance_matches",C==mat(c["covariance"]))
check("covariance_positive_definite",C[0][0]>0 and det(C)>0)
check("B_positive_definite",B[0][0]>0 and det(B)>0)
check("internal_D_is_B_Cinv_plus_reset",D==mat(c["internal_D"]))
check("D_C_symmetric",mul(D,C)==mul(C,trans(D)))
check("unit_circle_vertices",all(dot(r,r)==1 for r in v))
check("vertices_distinct",len(set(tuple(r) for r in v))==5)

order=c["ccw_order"]
facets=[]
for i in range(5):
    a,b=v[order[i]],v[order[(i+1)%5]]
    dx,dy=b[0]-a[0],b[1]-a[1]
    facets.append([dy*a[0]-dx*a[1],-dy,dx])
facet_eval=[[dot(f,[F(1)]+r) for r in v] for f in facets]
check("facets_match_ccw_determinants",facets==mat(c["facets"]))
check("all_vertices_inside_each_facet",all(x>=0 for r in facet_eval for x in r))
check("each_facet_vanishes_exactly_on_edge",all([j for j,x in enumerate(r) if x==0]==sorted([order[k],order[(k+1)%5]]) for k,r in enumerate(facet_eval)))
check("facet_coefficients_rank_3",rank(facets)==3)
check("facet_sum_constant_positive",sum(f[0] for f in facets)>0 and all(sum(f[j] for f in facets)==0 for j in [1,2]))
momentmat=[[F(1),r[0],r[1],r[0]**2,r[0]*r[1]] for r in v]
check("moment_determinant_matches",det(momentmat)==F(c["five_point_moment_determinant"]))

flows=[[F(0) for j in range(5)] for i in range(5)]
for (i,j),w in zip(c["base_directed_edges"],c["base_directed_flows"]):
    flows[i][j]=F(w)
check("base_flows_positive",all(F(w)>0 for w in c["base_directed_flows"]))
check("base_flows_stationary",all(sum(flows[i])==sum(flows[j][i] for j in range(5)) for i in range(5)))
base_drift=[[sum(flows[i][j]*(v[i][k]-v[j][k]) for j in range(5)) for k in range(2)] for i in range(5)]
check("base_flow_drift_matches_D0",base_drift==scale(mul(cent,trans(D0)),F(1,5)))
Qre=[[F(0) for j in range(10)] for i in range(10)]
for i in range(5):
    for j in range(5):
        if i!=j:
            Qre[i][j]=5*flows[i][j]+F(c["reset_rate"])/5
    for k in range(5):
        Qre[i][5+k]=Qre[5+k][i]=F(c["marker_eta"])*facet_eval[k][i]
for i in range(10):
    Qre[i][i]=-sum(Qre[i])
check("Q_reconstructed_exactly_from_flows_and_facets",Qre==Q)

Z=[[F(0)]+z[i]+[dot(z[i],v[i])]*5 for i in range(5)]+[[F(0)]*8 for i in range(5)]
pairings={}
for i,j in itertools.combinations(range(10),2):
    pairings[f"{i},{j}"]=dot([a-b for a,b in zip(Z[i],Z[j])],[a-b for a,b in zip(H[i],H[j])])
internalpairs=[pairings[f"{i},{j}"] for i,j in itertools.combinations(range(5),2)]
check("planar_pairings_match",internalpairs==vec(c["monotonicity_pairings"]))
check("all_45_extension_pairings_nonnegative",all(a>=0 for a in pairings.values()))
check("10_internal_pairings_strictly_positive",all(a>0 for a in internalpairs))
check("35_other_pairings_zero",all(a==0 for k,a in pairings.items() if any(int(t)>=5 for t in k.split(','))))
internal_drift=mul(cent,trans(D))
rawpair=sum(dot(z[i],internal_drift[i]) for i in range(5))/5
generator_pair=sum(dot(Z[i],r) for i,r in enumerate(scale(mul(Q,H),-1)))/10
step_pair=sum(dot(Z[i],r) for i,r in enumerate(sub(H,mul(P,H))))/10
check("drift_pairing_matches",rawpair==F(c["farkas_drift_pairing"]))
check("generator_pair_is_half_stored_drift",generator_pair==rawpair/2)
check("one_step_pair_is_quarter_stored_drift",step_pair==rawpair/4)
check("one_step_pair_strictly_negative",step_pair<0)
beta=sum(sum(abs(a) for a in r) for r in Z)/10
maxZ2=max(dot(r,r) for r in Z)
check("beta_below_2",beta<2)
check("Q_infinity_at_most_2",norminf(Q)<=2)
check("L_Frobenius_below_3",frob2(L)<9)
check("max_Z_Euclidean_below_3",maxZ2<9)

# The full Euler step and the orthogonal projection off the constant feature.
# H_i dot constant_feature = 1 for every state, so subtracting any scalar
# multiple of this vector from each field row preserves all pairings/drifts.
P1=add(eye(10),Q)
T1=add(eye(8),L)
K=trans(T1)
constant_feature=[F(1),F(0),F(0)]+[F(1)]*5
Zp=[]
for i in range(5):
    ti=dot(z[i],v[i])
    Zp.append([-F(5,6)*ti]+z[i]+[ti/6]*5)
Zp += [[F(0)]*8 for i in range(5)]
check("epsilon1_P_nonnegative",all(a>=0 for r in P1 for a in r))
check("epsilon1_P_rows_one",all(sum(r)==1 for r in P1))
check("epsilon1_P_columns_one",all(sum(r)==1 for r in trans(P1)))
check("epsilon1_PH_equals_HT",mul(P1,H)==mul(H,T1))
check("constant_feature_evaluates_to_one",all(dot(r,constant_feature)==1 for r in H))
check("L_constant_feature_zero",all(dot(r,constant_feature)==0 for r in L))
check("Zprime_is_orthogonal_projection",Zp==[[r[j]-dot(r,constant_feature)*constant_feature[j]/dot(constant_feature,constant_feature) for j in range(8)] for r in Z])
check("Zprime_orthogonal_to_constant",all(dot(r,constant_feature)==0 for r in Zp))
projected_pairings={}
for i,j in itertools.combinations(range(10),2):
    projected_pairings[f"{i},{j}"]=dot([a-b for a,b in zip(Zp[i],Zp[j])],[a-b for a,b in zip(H[i],H[j])])
check("Zprime_pairings_equal_original",projected_pairings==pairings)
projected_generator_by_state=[dot(Zp[i],r) for i,r in enumerate(scale(mul(Q,H),-1))]
original_generator_by_state=[dot(Z[i],r) for i,r in enumerate(scale(mul(Q,H),-1))]
check("Zprime_generator_drift_equal_each_state",projected_generator_by_state==original_generator_by_state)
projected_step_by_state=[dot(Zp[i],r) for i,r in enumerate(sub(H,mul(P1,H)))]
full_step_pair=sum(projected_step_by_state)/10
check("Zprime_epsilon1_step_drift_equal_each_state",projected_step_by_state==original_generator_by_state)
check("Zprime_epsilon1_step_pair_half_stored_drift",full_step_pair==rawpair/2)
check("Zprime_epsilon1_step_pair_negative",full_step_pair<0)
maxZp2=max(dot(r,r) for r in Zp)
check("Zprime_max_l2_below_3_over_2",maxZp2<F(9,4))
planarz=z+[[F(0),F(0)]]
planar_diameter2=max(sum((a-b)**2 for a,b in zip(r,s)) for r,s in itertools.combinations(planarz,2))
check("planar_field_diameter_below_41_over_20",planar_diameter2<F(1681,400))
Zp_drift_coeffs=mul(Zp,sub(eye(8),K))
maxplanardrift2=max(r[1]**2+r[2]**2 for r in Zp_drift_coeffs)
check("Zprime_IminusK_xy_max_l2_below_3_over_2",maxplanardrift2<F(9,4))

# Hoffman bound: every projection face has either a singleton active normal or
# one adjacent pair of active normals. Each inverse singular-value bound is
# certified by a rational 2-by-2 positive-semidefinite test.
hoffman=F(11,5)
hoffman_pair_matrices=[]
for k in range(5):
    N=[facets[k][1:],facets[(k+1)%5][1:]]
    certificate=sub(scale(mul(N,trans(N)),hoffman**2),eye(2))
    hoffman_pair_matrices.append(certificate)
check("Hoffman_11_over_5_all_adjacent_normal_pairs",all(psd2(a) for a in hoffman_pair_matrices))
check("Hoffman_11_over_5_all_singleton_normals",all(hoffman**2*dot(r[1:],r[1:])>=1 for r in facets))

# q(v_i)=b_i, with b_i the full-step projected-field drift. The interpolation
# polynomial is q0+q1*x+q2*y+q3*x*x+q4*x*y.
qcoeff=solve(momentmat,projected_step_by_state[:5])
check("interpolation_matches_all_five_points",[dot(r,qcoeff) for r in momentmat]==projected_step_by_state[:5])
qlin2=qcoeff[1]**2+qcoeff[2]**2
qA=[[qcoeff[3],qcoeff[4]/2],[qcoeff[4]/2,F(0)]]
qA_upper=sub(scale(eye(2),F(7,20)),qA)
qA_lower=add(scale(eye(2),F(7,20)),qA)
check("interpolation_linear_norm_below_4_over_5",qlin2<F(16,25))
check("interpolation_A_opnorm_below_7_over_20",psd2(qA_upper) and det(qA_upper)>0 and psd2(qA_lower) and det(qA_lower)>0)

# Independent rational enumeration of polygon/Voronoi-cell vertices. In cell i,
# g_i(y)=||y-v_i|| + C||y||^2-C is convex. Its maximum is attained at a vertex,
# so these vertex checks certify dist(y,{v_i}) <= C(1-||y||^2) on the polygon.
circleC=F(16,5)
voronoi_cells=[]
circle_ok=True
for i,p in enumerate(v):
    constraints=facets+[[F(0)]+[a-b for a,b in zip(p,q)] for j,q in enumerate(v) if j!=i]
    cell=[]
    for a,b in itertools.combinations(constraints,2):
        normals=[a[1:],b[1:]]
        if det(normals)==0:
            continue
        y=solve(normals,[-a[0],-b[0]])
        if any(l[0]+dot(l[1:],y)<0 for l in constraints) or y in cell:
            continue
        cell.append(y)
    rows=[]
    for y in cell:
        delta=1-dot(y,y)
        dist2=sum((a-b)**2 for a,b in zip(y,p))
        passed=delta>=0 and dist2<=circleC**2*delta**2
        circle_ok=circle_ok and passed
        rows.append({"point":list(map(str,y)),"circle_deficit":str(delta),"distance_squared":str(dist2),"ratio_squared":str(dist2/delta**2) if delta else None,"passed":passed})
    voronoi_cells.append(rows)
check("polygon_Voronoi_cells_nonempty",all(voronoi_cells))
check("polygon_circle_rounding_constant_16_over_5",circle_ok)

# A constant planar shift followed by the same constant-feature projection.
# The shift preserves pairwise monotonicity. It changes individual drifts but
# preserves the stationary average, checked here without an analytic premise.
planar_shift=[F(4,5),F(0)]
zshift=[[a-b for a,b in zip(r,planar_shift)] for r in z]
Zshift=[]
for i in range(5):
    ti=dot(zshift[i],v[i])
    Zshift.append([-F(5,6)*ti]+zshift[i]+[ti/6]*5)
Zshift += [[F(0)]*8 for i in range(5)]
shiftpairings={}
for i,j in itertools.combinations(range(10),2):
    shiftpairings[f"{i},{j}"]=dot([a-b for a,b in zip(Zshift[i],Zshift[j])],[a-b for a,b in zip(H[i],H[j])])
check("shifted_all_45_pairings_equal_original",shiftpairings==pairings)
check("shifted_field_orthogonal_to_constant",all(dot(r,constant_feature)==0 for r in Zshift))
shift_step_by_state=[dot(Zshift[i],r) for i,r in enumerate(sub(H,mul(P1,H)))]
shift_step_pair=sum(shift_step_by_state)/10
check("shifted_stationary_pairing_unchanged",shift_step_pair==full_step_pair)
check("shifted_stationary_pairing_negative",shift_step_pair<0)
maxZshift2=max(dot(r,r) for r in Zshift)
check("shifted_max_l2_below_6_over_5",maxZshift2<F(36,25))
planarzshift=zshift+[[F(0),F(0)]]
shift_diameter2=max(sum((a-b)**2 for a,b in zip(r,s)) for r,s in itertools.combinations(planarzshift,2))
check("shifted_planar_diameter_below_41_over_20",shift_diameter2<F(1681,400))
shift_drift_coeffs=mul(Zshift,sub(eye(8),K))
maxshiftdrift2=max(r[1]**2+r[2]**2 for r in shift_drift_coeffs)
check("shifted_drift_xy_gradient_below_8_over_15",maxshiftdrift2<F(64,225))
shiftq=solve(momentmat,shift_step_by_state[:5])
check("shifted_interpolation_exact",[dot(r,shiftq) for r in momentmat]==shift_step_by_state[:5])
shift_qlin2=shiftq[1]**2+shiftq[2]**2
shift_A=[[shiftq[3],shiftq[4]/2],[shiftq[4]/2,F(0)]]
shift_Aupper=sub(scale(eye(2),F(7,20)),shift_A)
shift_Alower=add(scale(eye(2),F(7,20)),shift_A)
check("shifted_q_linear_norm_below_1_over_5",shift_qlin2<F(1,25))
check("shifted_A_opnorm_below_7_over_20",psd2(shift_Aupper) and det(shift_Aupper)>0 and psd2(shift_Alower) and det(shift_Alower)>0)
check("shifted_A_equals_unshifted_A",shift_A==qA)
circle_coeff=(F(41,20)+F(8,15)+F(1,5)+2*F(7,20))*F(16,5)
d_coeff=F(41,20)+F(8,15)+F(1,5)+F(7,20)
x_coeff=F(7,20)+2*circle_coeff
final_bound2=22**2*(d_coeff**2+x_coeff**2)
check("shifted_Ccircle_equals_836_over_75",circle_coeff==F(836,75))
check("shifted_dcoeff_equals_47_over_15",d_coeff==F(47,15))
check("shifted_xcoeff_equals_6793_over_300",x_coeff==F(6793,300))
check("shifted_final_bound_strictly_below_503",final_bound2<503**2)

result={
    "status":"ALL_EXACT_CHECKS_PASS" if all(checks.values()) else "CHECK_FAILURE",
    "scope":"Independent standard-library Fraction replay; finite algebra only, not analytic realization/closure proof or novelty.",
    "source_path":str(SOURCE),
    "source_sha256":hashlib.sha256(raw).hexdigest(),
    "checks":checks,
    "check_count":len(checks),
    "failed_checks":[k for k,b in checks.items() if not b],
    "numbers":{
        "P_min_entry":value(min(a for r in P for a in r)),
        "P_min_positive_entry":value(min(a for r in P for a in r if a>0)),
        "P_min_diagonal":value(min(P[i][i] for i in range(10))),
        "Q_infinity":value(norminf(Q)),
        "Q_one_norm":value(norminf(trans(Q))),
        "L_infinity":value(norminf(L)),
        "L_one_norm":value(norminf(trans(L))),
        "L_Frobenius_squared":value(frob2(L)),
        "L_Frobenius_decimal":math.sqrt(float(frob2(L))),
        "Z_max_l1":value(norminf(Z)),
        "Z_beta":value(beta),
        "Z_max_l2_squared":value(maxZ2),
        "Z_max_l2_decimal":math.sqrt(float(maxZ2)),
        "internal_monotonicity_min":value(min(internalpairs)),
        "stored_internal_pairing":value(rawpair),
        "generator_pairing":value(generator_pair),
        "P_one_step_pairing":value(step_pair),
        "facet_sum_constant":value(sum(f[0] for f in facets)),
        "moment_determinant":value(det(momentmat)),
        "M_determinant":value(det(M)),
        "max_H_entry_absolute":value(max(abs(a) for r in H for a in r)),
        "max_H_row_l2_squared":value(max(dot(r,r) for r in H)),
        "epsilon1_P_min_diagonal":value(min(P1[i][i] for i in range(10))),
        "epsilon1_P_min_positive_entry":value(min(a for r in P1 for a in r if a>0)),
        "epsilon1_projected_step_pairing":value(full_step_pair),
        "Zprime_max_l2_squared":value(maxZp2),
        "Zprime_max_l2_decimal":math.sqrt(float(maxZp2)),
        "planar_field_diameter_squared":value(planar_diameter2),
        "planar_field_diameter_decimal":math.sqrt(float(planar_diameter2)),
        "Zprime_IminusK_xy_max_l2_squared":value(maxplanardrift2),
        "Zprime_IminusK_xy_max_l2_decimal":math.sqrt(float(maxplanardrift2)),
        "interpolation_linear_norm_squared":value(qlin2),
        "interpolation_linear_norm_decimal":math.sqrt(float(qlin2)),
        "interpolation_A_opnorm_decimal":(abs(float(qcoeff[3]))+math.sqrt(float(qcoeff[3]**2+qcoeff[4]**2)))/2,
        "Hoffman_constant":value(hoffman),
        "circle_rounding_constant":value(circleC),
        "shifted_stationary_pairing":value(shift_step_pair),
        "shifted_Zmax_l2_squared":value(maxZshift2),
        "shifted_Zmax_l2_decimal":math.sqrt(float(maxZshift2)),
        "shifted_planar_diameter_squared":value(shift_diameter2),
        "shifted_planar_diameter_decimal":math.sqrt(float(shift_diameter2)),
        "shifted_drift_xy_gradient_squared":value(maxshiftdrift2),
        "shifted_drift_xy_gradient_decimal":math.sqrt(float(maxshiftdrift2)),
        "shifted_q_linear_norm_squared":value(shift_qlin2),
        "shifted_q_linear_norm_decimal":math.sqrt(float(shift_qlin2)),
        "shifted_A_opnorm_decimal":(abs(float(shiftq[3]))+math.sqrt(float(shiftq[3]**2+shiftq[4]**2)))/2,
        "shifted_Ccircle":value(circle_coeff),
        "shifted_dcoeff":value(d_coeff),
        "shifted_xcoeff":value(x_coeff),
        "shifted_final_bound_squared":value(final_bound2),
        "shifted_final_bound_decimal":math.sqrt(float(final_bound2)),
    },
    "pairing_counts":{"positive":sum(x>0 for x in pairings.values()),"zero":sum(x==0 for x in pairings.values()),"negative":sum(x<0 for x in pairings.values())},
    "one_step_pairing_formula":"(1/10) sum_i <Z_i, H_i - (PH)_i> = farkas_drift_pairing / 4",
    "epsilon1_step_pairing_formula":"For P1=I+Q, (1/10) sum_i <Zprime_i, H_i - (P1H)_i> = farkas_drift_pairing / 2",
    "interpolation":{
        "monomial_order":["1","x","y","x^2","xy"],
        "qcoeff_exact":list(map(str,qcoeff)),
        "qcoeff_decimal":list(map(float,qcoeff)),
        "rhs_b_exact":list(map(str,projected_step_by_state[:5])),
        "quadratic_A_exact":[list(map(str,r)) for r in qA],
        "upper_PSD_diagonals_and_determinant":list(map(str,[qA_upper[0][0],qA_upper[1][1],det(qA_upper)])),
        "lower_PSD_diagonals_and_determinant":list(map(str,[qA_lower[0][0],qA_lower[1][1],det(qA_lower)])),
    },
    "Hoffman_adjacent_pair_PSD_certificates":[[list(map(str,r)) for r in a] for a in hoffman_pair_matrices],
    "circle_rounding_Voronoi_cells":voronoi_cells,
    "shifted_interpolation":{
        "planar_shift_exact":list(map(str,planar_shift)),
        "monomial_order":["1","x","y","x^2","xy"],
        "qcoeff_exact":list(map(str,shiftq)),
        "qcoeff_decimal":list(map(float,shiftq)),
        "rhs_b_exact":list(map(str,shift_step_by_state[:5])),
        "quadratic_A_exact":[list(map(str,r)) for r in shift_A],
        "upper_PSD_diagonals_and_determinant":list(map(str,[shift_Aupper[0][0],shift_Aupper[1][1],det(shift_Aupper)])),
        "lower_PSD_diagonals_and_determinant":list(map(str,[shift_Alower[0][0],shift_Alower[1][1],det(shift_Alower)])),
    },
}
OUT.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
