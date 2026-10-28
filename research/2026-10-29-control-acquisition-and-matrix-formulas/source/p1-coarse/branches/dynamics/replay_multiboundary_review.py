"""Independent saved-count algebra and confidence review; no trajectories."""
from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache
from itertools import combinations
import json

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/"branches/physical/MULTIBOUNDARY_POSITIVE_EVENTS_RESULTS.json"


def decode(x):
    if isinstance(x,dict):
        if "fraction" in x:return F(x["fraction"])
        return {k:decode(v) for k,v in x.items()}
    if isinstance(x,list):return [decode(v) for v in x]
    return x


def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def tr(a):return list(map(list,zip(*a)))
def mm(a,b):return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in tr(b)] for row in a]
def add(a,b):return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def scale(a,c):return [[c*x for x in row] for row in a]
def sub(a,b):return add(a,scale(b,-1))
def vec(a,x):return [sum((v*w for v,w in zip(row,x)),F(0)) for row in a]
def dot(x,y):return sum((a*b for a,b in zip(x,y)),F(0))


def determinant(a):
    if not a:return F(1)
    if len(a)==1:return a[0][0]
    return sum(((-1)**j*a[0][j]*determinant(
        [[a[r][c] for c in range(len(a)) if c!=j] for r in range(1,len(a))])
        for j in range(len(a))),F(0))


def psd3(a):
    assert a==tr(a)
    return all(determinant([[a[i][j] for j in s] for i in s])>=0
               for k in (1,2,3) for s in combinations(range(3),k))


def inverse(a):
    n=len(a); aug=[row[:]+unit for row,unit in zip(a,eye(n))]
    for j in range(n):
        pivot=next(i for i in range(j,n) if aug[i][j])
        aug[j],aug[pivot]=aug[pivot],aug[j]
        d=aug[j][j];aug[j]=[x/d for x in aug[j]]
        for i in range(n):
            if i!=j:
                d=aug[i][j];aug[i]=[x-d*y for x,y in zip(aug[i],aug[j])]
    ans=[row[n:] for row in aug]
    assert mm(a,ans)==eye(n)
    return ans


@lru_cache(None)
def logs(z):
    assert z>0
    k=0
    while z<1:z*=2;k-=1
    while z>2:z/=2;k+=1
    u=(z-1)/(z+1); low=sum((2*u**(2*j+1)/F(2*j+1) for j in range(40)),F(0))
    high=low+2*u**81/(81*(1-u*u))
    if k:
        l2,h2=logs(F(2))
        low+=k*(l2 if k>0 else h2);high+=k*(h2 if k>0 else l2)
    return low,high


def check_endpoint(x,n,p,ell,side):
    h=F(x,n)
    if p in (0,1):return
    assert p<=h if side=="lower" else p>=h
    kl=(h*logs(h/p)[0] if h else 0)+((1-h)*logs((1-h)/(1-p))[0] if h!=1 else 0)
    assert n*kl>=ell


def review_stage(data,stage):
    cert=stage["certificate"]; ell=data["chernoff_exponent"]
    a=data["source_norm_warranty"]; tail=1/(1-a*a); z=data["depth"]+tail
    assert cert["mixture_tail_weight"]==tail and cert["mixture_normalizer"]==z
    endpoint_checks=0; missing_last_report=0
    for record in stage["receipts"]:
        n=record["trials"]; out=record["first_outside_length_histogram"]
        reject=sum(record["penultimate_inside_rejections_by_length"])
        assert sum(record["first_step_boundary_or_outside_counts"])==n
        assert sum(record["mixture_length_histogram"])==n
        assert sum(out)==record["first_step_boundary_or_outside_counts"][3]
        assert sum(record["terminal_boundary_or_outside_counts"])==n
        assert sum(record["positive_events_by_length"])==record["positive_events"]
        assert record["primitive_applications"]==n+sum((2*k+1)*x for k,x in enumerate(out))-reject
        assert record["categorical_boundary_observations"]==n+sum((1 if k==0 else 2)*x for k,x in enumerate(out))-reject
        base=n-record["known_returns_to_requested_boundary"]
        key="sampling_group_final_reports_equal_requested"
        if key in record:assert record["resets_with_boundary_reuse"]==base+record[key]
        else:
            missing_last_report+=1
            assert base<=record["resets_with_boundary_reuse"]<=base+record["independently_initialized_sampling_groups"]
    for mode,m in enumerate(cert["modes"]):
        records=[next(r for r in stage["receipts"] if r["mode"]==mode and r["start_boundary"]==j) for j in range(3)]
        n=records[0]["trials"]; observed=[r["first_step_boundary_or_outside_counts"] for r in records]
        t,lo,hi,rad=(m[k] for k in ("model","kernel_lower","kernel_upper","entry_radius"))
        assert t==tr(t) and lo==tr(lo) and hi==tr(hi) and rad==tr(rad)
        for j in range(3):
            for k in range(j,3):
                count=observed[j][j] if j==k else observed[j][k]+observed[k][j]
                count_n=n if j==k else 2*n
                assert t[j][k]==F(count,count_n)
                assert rad[j][k]==max(t[j][k]-lo[j][k],hi[j][k]-t[j][k])
                check_endpoint(count,count_n,lo[j][k],ell,"lower")
                check_endpoint(count,count_n,hi[j][k],ell,"upper");endpoint_checks+=2
        rowrad=[]
        for j in range(3):
            rl,rh=m["row_mass_intervals"][j];count=sum(observed[j][:3])
            check_endpoint(count,n,rl,ell,"lower");check_endpoint(count,n,rh,ell,"upper")
            endpoint_checks+=2
            rowrad.append(max(abs(rl-sum(t[j])),abs(rh-sum(t[j]))))
            event_hi=m["galerkin_form_diagonal_uppers"][j]/z
            check_endpoint(records[j]["positive_events"],n,event_hi,ell,"upper");endpoint_checks+=1
        r=sub(eye(3),mm(t,t));assert r==m["budget"] and psd3(r) and determinant(r)>0
        delta=max(map(sum,rad));assert delta==m["operator_error_upper"]
        qtrace=sum(m["galerkin_form_diagonal_uppers"]);assert qtrace==m["galerkin_form_trace_upper"]
        proposal=m["proposed_form_operator_upper"]
        difference=proposal-qtrace-delta*delta*tail
        assert difference>=0 and difference*difference>=4*delta*delta*qtrace*tail
        assert psd3(sub(scale(r,m["theta_squared"]),scale(eye(3),proposal)))
        assert psd3(sub(scale(r,m["correction_noise_zeta"]),scale(eye(3),delta)))
        pi=[[rowrad[j]+sum(rad[j][k] for k in range(3) if k!=j) if j==i else -rad[j][i]
             for i in range(3)] for j in range(3)]
        assert pi==m["structured_uncertainty_form"]
        assert psd3(sub(scale(r,m["structured_correction_noise_zeta"]),pi))
        rho=max(x[1] for x in m["row_mass_intervals"])
        assert rho==m["true_kernel_norm_upper"] and rho<1
        assert m["robust_galerkin_theta_squared"]==qtrace/(1-rho*rho)
    assert cert["uniform_all_word_bound"]==2*max(m["theta_squared"] for m in cert["modes"])+max(m["correction_noise_zeta"] for m in cert["modes"])
    assert cert["uniform_structured_all_word_bound"]==2*max(m["theta_squared"] for m in cert["modes"])+max(m["structured_correction_noise_zeta"] for m in cert["modes"])
    return {"confidence_endpoints_checked":endpoint_checks,
            "missing_last_report_fields":missing_last_report,
            "matrix_and_confidence_checks_passed":True}


def review_source_and_words(data,stage):
    sources=data["source_matrices_checker_only"]; cert=stage["certificate"]
    event_checks=0; word_checks=0
    for i,a in enumerate(sources):
        assert a==tr(a) and max(map(sum,a))<=data["source_norm_warranty"]
        m=cert["modes"][i]; t=m["model"]
        true_t=[row[:3] for row in a[:3]]
        delta=sub(true_t,t)
        dgal=[[F(0)]*3 if j<3 else a[j][:3] for j in range(6)]
        dprop=[delta[j] if j<3 else a[j][:3] for j in range(6)]
        resolvent=inverse(sub(eye(6),mm(a,a)))
        qgal=mm(tr(dgal),mm(resolvent,dgal))
        qprop=mm(tr(dprop),mm(resolvent,dprop))
        mixture=[[F(0)]*3 for _ in range(3)]
        image=dgal
        for k in range(data["depth"]+1):
            gram=mm(tr(image),image)
            for j in range(3):
                y=[dgal[l][j] for l in range(6)]
                for _ in range(2*k):y=vec(a,y)
                y[:3]=[F(0)]*3
                assert dot(a[j],y)==gram[j][j];event_checks+=1
            weight=cert["mixture_tail_weight"] if k==data["depth"] else 1
            mixture=add(mixture,scale(gram,weight))
            image=mm(a,image)
        assert psd3(sub(mixture,qgal))
        assert all(mixture[j][j]<=m["galerkin_form_diagonal_uppers"][j] for j in range(3))
        assert psd3(sub(scale(eye(3),m["galerkin_form_trace_upper"]),qgal))
        assert psd3(sub(scale(eye(3),m["proposed_form_operator_upper"]),qprop))
        assert psd3(sub(scale(m["budget"],m["theta_squared"]),qprop))
        pi=m["structured_uncertainty_form"]
        assert psd3(sub(pi,delta)) and psd3(add(pi,delta))
        true_budget=sub(eye(3),mm(true_t,true_t))
        assert psd3(sub(scale(true_budget,m["robust_galerkin_theta_squared"]),qgal))
    for comparison in stage["same_count_program_comparisons"]:
        for key in ("program_a","program_b"):
            p=comparison[key]; source=[F(j==p["start_boundary"]) for j in range(6)]
            lower=[F(j==p["start_boundary"]) for j in range(3)]; upper=lower[:]
            for i in p["word"]:
                source=vec(sources[i],source)
                lower=vec(cert["modes"][i]["kernel_lower"],lower)
                upper=vec(cert["modes"][i]["kernel_upper"],upper)
            end=p["end_boundary"]; exact=source[end]
            assert exact==p["checker_exact_source_response"]
            interval=(max(F(0),lower[end]),min(F(1),upper[end]+cert["robust_galerkin_uniform_dynamical_bound"]))
            assert list(interval)==p["robust_galerkin_source_interval"]
            assert interval[0]<=exact<=interval[1]
            correction=F(0)
            for i,c in enumerate(p["correction_coefficients"]):
                delta=sub([row[:3] for row in sources[i][:3]],cert["modes"][i]["model"])
                correction+=sum((c[j][k]*delta[j][k] for j in range(3) for k in range(3)),F(0))
            assert abs(exact-p["model_prediction"]-correction)<=p["finite_word_remainder_bound"]
            word_checks+=1
    return {"positive_event_path_identities_checked":event_checks,
            "bilinear_programs_checked":word_checks,
            "actual_source_and_comparator_checks_passed":True}


if __name__=="__main__":
    import hashlib
    from math import factorial
    raw=SOURCE.read_bytes(); data=decode(json.loads(raw))
    assert data["confidence_tail_count_including_both_fixed_checkpoints"]==84
    assert sum((F(12**k,factorial(k)) for k in range(50)),F(0))>88_000
    stages=[]
    for stage in data["stages"]:
        record=review_stage(data,stage)
        record.update(review_source_and_words(data,stage));stages.append(record)
    direct_checks=0
    for r in data["direct_endpoint_comparator"]["receipts"]:
        lo,hi=r["confidence_interval"]
        check_endpoint(r["target_returns"],r["trials"],lo,data["chernoff_exponent"],"lower")
        check_endpoint(r["target_returns"],r["trials"],hi,data["chernoff_exponent"],"upper")
        direct_checks+=2
    output={"source_file":str(SOURCE),"source_sha256":hashlib.sha256(raw).hexdigest(),
            "no_new_trajectories":True,"stages":stages,
            "direct_confidence_endpoints_checked":direct_checks,
            "all_checks_passed":True,
            "inference_plus_direct_failure_upper_below_one_per_thousand":True}
    path=Path(__file__).with_name("MULTIBOUNDARY_COMPILER_REVIEW_RESULTS.json")
    path.write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps(output,indent=2))
