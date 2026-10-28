"""Independent replay of finite inverse-dissipation acquisition.

Uses exact Fraction arithmetic and expands powered defect states directly.
No parent matrix, PSD, interval, or expression helper is used in the replay.
The off-diagonal check calls only the new acquisition function as its target.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys

BASE = Path(__file__).resolve().parents[2]


def rational(x):
    if isinstance(x, dict) and "rational" in x:
        return F(x["rational"])
    if isinstance(x, list):
        return [rational(y) for y in x]
    return x


def matmul(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def trans(a):
    return [list(x) for x in zip(*a)]


def add(a, b, multiplier=F(1)):
    return [[x+multiplier*y for x,y in zip(ar,br)] for ar,br in zip(a,b)]


def scaled(a, s):
    return [[s*x for x in row] for row in a]


def ident(n):
    return [[F(i==j) for j in range(n)] for i in range(n)]


def power(a, n):
    out = ident(len(a))
    for _ in range(n):
        out = matmul(a, out)
    return out


def psd2(a, strict=False):
    assert len(a) in (1,2) and all(len(row)==len(a) for row in a)
    assert a == trans(a)
    if len(a)==1:
        return a[0][0]>0 if strict else a[0][0]>=0
    d = a[0][0]*a[1][1]-a[0][1]*a[1][0]
    if strict:
        return a[0][0]>0 and d>0
    return a[0][0]>=0 and a[1][1]>=0 and d>=0


def inv2(a):
    d = a[0][0]*a[1][1]-a[0][1]*a[1][0]
    assert d
    return [[a[1][1]/d,-a[0][1]/d],[-a[1][0]/d,a[0][0]/d]]


def canonical(w):
    return min(w,w[::-1])


def addterm(expr, word, coefficient):
    word = canonical(tuple(word))
    expr[word] = expr.get(word,F(0))+coefficient
    if not expr[word]:
        del expr[word]


def defect_states(dictionary, t, action):
    # States are vectors, so reversal equivalence is NOT used here.
    states=[]
    for column,word in enumerate(dictionary):
        state={tuple(word)+(action,):F(1)}
        for row,vword in enumerate(dictionary):
            state[tuple(vword)]=state.get(tuple(vword),F(0))-t[row][column]
        states.append({word:c for word,c in state.items() if c})
    return states


def finite_form_expressions(dictionary, t, action, depth, a):
    # Independently construct <A^k D e_j, A^k D e_l> from state expansions.
    states=defect_states(dictionary,t,action)
    output=[[{} for _ in states] for _ in states]
    for k in range(depth+1):
        weight=F(1) if k<depth else 1/(1-a*a)
        for j,left in enumerate(states):
            for l,right in enumerate(states):
                for lw,lc in left.items():
                    for rw,rc in right.items():
                        vl=lw+(action,)*k
                        vr=rw+(action,)*k
                        addterm(output[j][l],vr+vl[::-1],weight*lc*rc)
    return output


def interval(expr, records):
    lo=hi=F(0)
    for word,c in expr.items():
        l,u=records[word]
        lo += c*(l if c>=0 else u)
        hi += c*(u if c>=0 else l)
    return lo,hi


def upper_from_expressions(expressions, records):
    intervals=[[interval(expr,records) for expr in row] for row in expressions]
    mids=[[(l+u)/2 for l,u in row] for row in intervals]
    widths=[[(u-l)/2 for l,u in row] for row in intervals]
    assert mids==trans(mids)
    assert widths==trans(widths)
    rows=[sum(row,F(0)) for row in widths]
    return [[x+(rows[j] if j==k else 0) for k,x in enumerate(row)]
            for j,row in enumerate(mids)]


def response(actions, word):
    state=[[F(1)],[F(0)]]
    for i in word:
        state=matmul(actions[i],state)
    return state[0][0]


def actual_forms(a, v, t, depth, source_bound):
    d=add(matmul(a,v),matmul(v,t),F(-1))
    q=matmul(trans(d),matmul(inv2(add(ident(2),matmul(a,a),F(-1))),d))
    tail=scaled(matmul(trans(d),matmul(power(a,2*depth),d)),1/(1-source_bound**2))
    for k in range(depth):
        tail=add(tail,matmul(trans(d),matmul(power(a,2*k),d)))
    return q,tail


def source_warranty(a,bound):
    assert a==trans(a)
    assert psd2(add(scaled(ident(2),bound),a,F(-1)))
    assert psd2(add(scaled(ident(2),bound),a))


def decode_raw(row):
    raw=row["raw_records"]
    zero,one=raw[:2]
    assert zero["label"]=="standard_zero" and one["label"]=="standard_one"
    y0,y1=F(zero["report"]),F(one["report"])
    e0,e1=F(zero["error_bound"]),F(one["error_bound"])
    beta=(y0-e0,y0+e0)
    alpha=(y1-y0-e1-e0,y1-y0+e1+e0)
    assert alpha[0]>0
    out={}
    for rec in raw[2:]:
        y,e=F(rec["report"]),F(rec["error_bound"])
        numer=(y-e-beta[1],y+e-beta[0])
        corners=[n/a for n in numer for a in alpha]
        out[tuple(rec["label"])]=(min(corners),max(corners))
    supplied={tuple(r["word"]):(rational(r["interval"]["lo"]),rational(r["interval"]["hi"]))
              for r in row["decoded_records"]}
    assert out==supplied
    return out


def replay_scalar(row,group):
    g=rational(row["slow_scale_g"])
    bound=rational(row["source_norm_bound_premise"])
    depth=row["depth"]
    actions=[[[1-g,g],[g,F(1,4)]],[[1-2*g,-g],[-g,F(1,3)]]]
    maps=rational(row["maps"])
    records=decode_raw(row)
    dictionary=[tuple(w) for w in row["dictionary"]]
    assert dictionary==[()]
    assert set(records)=={(i,)*k for i in range(2) for k in range(2*depth+3)}
    for word,(lo,hi) in records.items():
        assert lo<=response(actions,word)<=hi
    assert row["source_readings"]==len(records)==4*depth+5
    assert row["total_readings"]==len(records)+2
    assert row["primitive_applications"]==sum(map(len,records))==(2*depth+2)*(2*depth+3)
    assert row["max_query_length"]==2*depth+2
    cert=row["dissipation_certificate"]
    assert rational(cert["source_norm_bounds_are_premises"])==[bound,bound]
    assert rational(cert["metric"])==[[F(1)]]
    maxima=[]
    for i,a in enumerate(actions):
        source_warranty(a,bound)
        t=maps[i]
        budget=add([[F(1)]],matmul(trans(t),t),F(-1))
        assert psd2(budget,strict=True)
        assert budget==rational(cert["computational_dissipation"][i])
        expressions=finite_form_expressions(dictionary,t,i,depth,bound)
        upper=upper_from_expressions(expressions,records)
        assert upper==rational(cert["inverse_source_dissipation_residual_upper"][i])
        actual_q,actual_tail=actual_forms(a,[[F(1)],[F(0)]],t,depth,bound)
        assert actual_q[0][0]==rational(row["checker_actual_inverse_dissipation_forms"][i])
        assert psd2(add(actual_tail,actual_q,F(-1)))
        assert psd2(add(upper,actual_tail,F(-1)))
        # Independently check the finite form against its scalar word expansion.
        value=sum((coefficient*response(actions,word)
                   for word,coefficient in expressions[0][0].items()),F(0))
        assert value==actual_tail[0][0]
        theta=rational(cert["per_action_theta_squared"][i])
        assert theta>=0 and psd2(add(scaled(budget,theta),upper,F(-1)))
        maxima.append(theta)
    theta=max(maxima)
    assert theta==rational(cert["theta_squared"])
    assert 2*theta==rational(cert["signed_remainder_bound_all_words"])
    measure=rational(row["old_uniform_certificate_same_model_and_data"]["all_word_measurement_bound"])
    total=2*theta+measure
    assert total==rational(row["new_total_all_word_bound"])
    return {"group":group,"g":str(g),"eta":str(rational(row["raw_adc_radius"])),
            "depth":depth,"source_readings":len(records),"operations":row["primitive_applications"],
            "new_total":float(total),"all_exact_checks_passed":True}


def off_diagonal_check():
    sys.path.insert(0,str(BASE/"core"))
    from echo_compiler import EchoCompiler,Interval
    from dissipation_certificate import acquire_dissipation_certificate
    actions=[[[F(1,2),F(1,8)],[F(1,8),F(1,3)]],
             [[F(1,4),F(-1,10)],[F(-1,10),F(-1,3)]]]
    dictionary=[(),(1,)]
    maps=[[[F(1,2),F(1,10)],[F(-1,20),F(1,3)]],
          [[F(2,5),F(1,12)],[F(0),F(1,4)]]]
    w=[[F(2),F(0)],[F(0),F(1)]]
    bound=F(3,4);depth=2;eta=F(1,10**8)
    words={canonical(tuple(right)+(i,)*k+tuple(left)[::-1])
           for left in dictionary for right in dictionary
           for i in range(2) for k in range(2*depth+3)}
    records={word:(response(actions,word)-eta,response(actions,word)+eta) for word in words}
    compiler=EchoCompiler(dictionary,2,{word:Interval(*ends) for word,ends in records.items()},maps)
    cert=acquire_dissipation_certificate(compiler,[bound,bound],depth,w)
    v=[[F(1),actions[1][0][0]],[F(0),actions[1][1][0]]]
    reviewed=[]
    for i,a in enumerate(actions):
        source_warranty(a,bound)
        budget=add(w,matmul(trans(maps[i]),matmul(w,maps[i])),F(-1))
        assert psd2(budget,strict=True)
        assert budget==cert["computational_dissipation"][i]
        expressions=finite_form_expressions(dictionary,maps[i],i,depth,bound)
        upper=upper_from_expressions(expressions,records)
        assert upper==cert["inverse_source_dissipation_residual_upper"][i]
        actual_q,actual_tail=actual_forms(a,v,maps[i],depth,bound)
        for j in range(2):
            for k in range(2):
                value=sum((c*response(actions,word) for word,c in expressions[j][k].items()),F(0))
                assert value==actual_tail[j][k]
        assert psd2(add(actual_tail,actual_q,F(-1)))
        assert psd2(add(upper,actual_tail,F(-1)))
        theta=cert["per_action_theta_squared"][i]
        assert psd2(add(scaled(budget,theta),upper,F(-1)))
        reviewed.append({"action":i,"theta_squared":str(theta),"all_exact_psd_checks_passed":True})
    assert cert["signed_remainder_bound_all_words"]==4*max(cert["per_action_theta_squared"])
    # Guards are part of the new all-action, nonnegative-depth contract.
    guard_results={}
    for label,bounds,k in [("missing_action",[bound],depth),("negative_depth",[bound,bound],-1)]:
        try:
            acquire_dissipation_certificate(compiler,bounds,k,w)
        except ValueError:
            guard_results[label]="rejected"
        else:
            guard_results[label]="not_rejected"
    assert all(value=="rejected" for value in guard_results.values())
    return {"dictionary_size":2,"non_symmetric_coefficient_maps":True,
            "negative_true_eigenvalue_in_second_action":True,
            "nonidentity_metric":True,"source_readings":len(records),
            "actions":reviewed,"input_guards":guard_results}


def main():
    path=BASE/"results"/"DISSIPATION_EXPERIMENT.json"
    data=json.loads(path.read_text())
    checks=[]
    for group in ["fixtures","fixed_source_noise_sweep","fixed_source_depth_sweep"]:
        checks.extend(replay_scalar(row,group) for row in data.get(group,[]))
    output={"independent_scalar_replays":checks,"off_diagonal_replay":off_diagonal_check(),
            "reviewed_sha256":{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest()
              for p in [BASE/"core"/"dissipation_certificate.py",
                        BASE/"core"/"run_dissipation_experiment.py",path]},
            "all_proof_inequalities_passed":True}
    dest=Path(__file__).with_name("DISSIPATION_REVIEW_CHECKS.json")
    dest.write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps(output,indent=2))


if __name__=="__main__":
    main()
