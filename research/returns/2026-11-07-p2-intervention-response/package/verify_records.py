"""Independent exact-source audits of the saved finite construction.

The audit does not prove the infinite-class theorems. It checks all acquired
laminate records, feasible commands, nominal-error emulation, secant bounds,
and the returned global gaps against an independently known optimum.
"""
import json
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def read(name): return json.loads((ROOT/name).read_text())
def energy(theta,e):
    a=1+Q(theta[0]); b=Q(3,2)*(1+Q(theta[1]))
    return Q(e[0])**2*2*a*b/(a+b)+Q(e[1])**2*(a+b)/2
def energy_record(rec):
    assert abs(energy(rec["theta"],rec["loading"])-Q(rec["mid"]))<=Q(rec["error"])
def feasible(theta):
    theta=list(map(Q,theta)); assert min(theta)>=0 and sum(theta)<=Q(1,2)
def det2(a): return Q(a[0][0])*Q(a[1][1])-Q(a[0][1])*Q(a[1][0])
def spd2(a): assert Q(a[0][0])>0 and det2(a)>0 and a[0][1]==a[1][0]

def audit():
    counts={}; summary=read("EXECUTION_SUMMARY.json")
    baseline=read("BASELINE_RECORDS.json")
    for rec in baseline["records"]: energy_record(rec)
    counts["baseline"]=len(baseline["records"])
    model=read("PREDICTOR.json")
    n=model["parameters"]["n"]; k=model["parameters"]["k"]
    assert len(model["acquisitions"])==n**k
    count=0
    for acquisition in model["acquisitions"]:
        for rec in acquisition["records"]: energy_record(rec); count+=1
    counts["predictor"]=count
    pars=model["parameters"]
    max_error=max(Q(a["tensor_error"]) for a in model["acquisitions"])
    proof_bound=Q(pars["truncation"])+Q(pars["noise_gain"])*(max_error+
        (Q(pars["Ly"])+Q(pars["B0"])*k*n*n)*Q(pars["node_radius"]))
    assert proof_bound==Q(model["uniform_operator_error"])<=Q(pars["epsilon"])

    # Rational upper enclosure of the exact scalar optimum 75-30 sqrt(6).
    lo,hi=Q(2),Q(3)
    for _ in range(120):
        mid=(lo+hi)/2
        if mid*mid<=6: lo=mid
        else: hi=mid
    optimum_upper=75-30*lo

    fw=read("DESIGN_CERTIFICATE.json"); Ct=Q(fw["curvature_envelope"])
    transcript=fw["transcript"]
    for row in transcript:
        for rec in [row["baseline"]]+row["probes"]:
            energy_record(rec); feasible(rec["theta"])
    for before,after in zip(transcript,transcript[1:]):
        improvement=energy(after["theta"],[1,0])-energy(before["theta"],[1,0])
        assert improvement>=Q(fw["epsilon"])**2/(16*Ct)
    assert optimum_upper-energy(fw["theta"],[1,0])<=Q(fw["gap_upper"])<=Q(fw["epsilon"])
    counts["conditional_gradient"]=4*len(transcript)

    for filename,key in [("ELLIPSOID_DESIGN_CERTIFICATE.json","ellipsoid"),
                         ("ELLIPSOID_VOLUME_CERTIFICATE.json","ellipsoid_volume")]:
        cert=read(filename); nu=Q(cert["reading_radius"]); h=Q(cert["h"]); C=Q(cert["curvature"])
        loss=Q(cert["actuation_objective_loss_bound"])
        for rec in cert["records"]:
            energy_record(rec["energy_record"])
            feasible(rec["theta"]); feasible(rec["actuated_theta"])
            nominal=energy(rec["theta"],[1,0]); actual=energy(rec["actuated_theta"],[1,0])
            assert abs(nominal-actual)<=loss
            assert abs(nominal-Q(rec["objective_mid"]))<=Q(rec["objective_error"])<=nu
        vertices=[list(map(Q,v)) for v in cert["vertices"]]
        for row in cert["transcript"]:
            spd2(row["shape"])
            if row["kind"]=="measured objective cut":
                theta=list(map(Q,row["theta"])); a=1+theta[0]; b=Q(3,2)*(1+theta[1])
                gradient=[2*b*b/(a+b)**2,3*a*a/(a+b)**2]
                for v,secant in zip(vertices,row["secants"]):
                    true_direction=sum(g*(vj-tj) for g,vj,tj in zip(gradient,v,theta))
                    assert Q(secant)-2*nu/h<=true_direction<=Q(secant)+2*nu/h+C*h/2
        shapes=[row["shape"] for row in cert["transcript"]]
        if cert["reason"]=="rounded ellipsoid volume bound": shapes.append(cert["final_shape"])
        for before,after in zip(shapes,shapes[1:]):
            # A direct rational determinant check, stronger than the stated
            # exponential volume bound for this two-dimensional execution.
            assert det2(after)/det2(before)<Q(11,12)**2
        feasible(cert["theta"])
        assert optimum_upper-energy(cert["theta"],[1,0])<=Q(cert["gap_upper"])<=Q(cert["epsilon"])
        counts[key]=len(cert["records"])
    assert sum(counts.values())==summary["total_laminate_reader_records"]

    named=read("COEFFICIENT_NAME_ACQUISITION.json"); rec=named["record"]
    assert abs(Q(rec["mid"])-Q(135,94))<=Q(rec["error"])<=Q(1,32)
    finite=read("FINITE_QUADRATIC_ACQUISITION.json"); rec=finite["record"]
    assert abs(Q(rec["mid"])-Q(1139,1128))<=Q(rec["error"])<=Q(1,1000000)
    out=dict(all_checks_passed=True,laminate_records_checked=counts,
             total_laminate_records=sum(counts.values()),
             independent_coefficient_name_records=1,independent_finite_matrix_records=1,
             scope="Finite implementation audit; universal guarantees are proved in RESEARCH_REPORT.txt.")
    (ROOT/"AUDIT.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out))
if __name__=="__main__": audit()
