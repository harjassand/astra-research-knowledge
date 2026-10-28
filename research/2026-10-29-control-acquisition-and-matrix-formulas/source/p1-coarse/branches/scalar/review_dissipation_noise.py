"""Scoped independent check of dissipation-normalized midpoint noise.

Reuses only exact arithmetic helpers from the prior independent review.
Does not rerun its acquisition, source-tail, or physical-energy checks.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import itertools
import json
import sys

from review_dissipation_certificate import (
    matmul, trans, add, scaled, psd2, canonical, interval, addterm, response,
)

BASE=Path(__file__).resolve().parents[2]


def decode(x):
    if isinstance(x,dict) and "rational" in x:
        return F(x["rational"])
    if isinstance(x,dict):
        return {k:decode(v) for k,v in x.items()}
    if isinstance(x,list):
        return [decode(v) for v in x]
    return x


def mv(a,x):
    return [sum((u*v for u,v in zip(row,x)),F(0)) for row in a]


def bilinear(x,a,y):
    return sum((u*v for u,v in zip(x,mv(a,y))),F(0))


def diag(entries):
    return [[v if j==k else F(0) for k in range(len(entries))]
            for j,v in enumerate(entries)]


def native_forms(dictionary,maps):
    r=len(dictionary)
    gram=[[{} for _ in range(r)] for _ in range(r)]
    forms=[]
    for j in range(r):
        for k in range(r):
            addterm(gram[j][k],dictionary[k]+dictionary[j][::-1],F(1))
    for i,t in enumerate(maps):
        f=[[{} for _ in range(r)] for _ in range(r)]
        for j in range(r):
            for k in range(r):
                addterm(f[j][k],dictionary[k]+(i,)+dictionary[j][::-1],F(1))
                for l in range(r):
                    addterm(f[j][k],dictionary[l]+dictionary[j][::-1],-t[l][k])
        forms.append(f)
    return gram,forms


def interval_matrix(forms,records):
    return [[interval(expr,records) for expr in row] for row in forms]


def mids(entries):
    return [[(lo+hi)/2 for lo,hi in row] for row in entries]


def radii(entries):
    return [[(hi-lo)/2 for lo,hi in row] for row in entries]


def verify_certificate(dictionary,maps,metric,records,cert):
    r=len(dictionary)
    gram,forms=native_forms(dictionary,maps)
    gintervals=interval_matrix(gram,records)
    gr=radii(gintervals)
    assert gr==trans(gr)
    gamma=cert["gram_uncertainty_bound"]
    gd=diag([sum(row,F(0)) for row in gr])
    assert gamma>=0 and psd2(add(scaled(metric,gamma),gd,F(-1)))
    budgets=[];fmids=[];asymmetric_radius=False
    assert len(cert["witnesses"])==len(maps)
    for i,t in enumerate(maps):
        budget=add(metric,matmul(trans(t),matmul(metric,t)),F(-1))
        assert psd2(budget,strict=True)
        entries=interval_matrix(forms[i],records)
        rs=radii(entries)
        asymmetric_radius |= rs!=trans(rs)
        rows=[sum(row,F(0)) for row in rs]
        cols=[sum((rs[j][k] for j in range(r)),F(0)) for k in range(r)]
        d=diag([max(x,y) for x,y in zip(rows,cols)])
        zeta=cert["weak_defect_uncertainty_bounds"][i]
        witness=cert["witnesses"][i]
        assert witness["computational_dissipation"]==budget
        assert witness["entry_radius_bilinear_dominator"]==d
        assert witness["zeta"]==zeta
        assert zeta>=0 and psd2(add(scaled(budget,zeta),d,F(-1)))
        budgets.append(budget)
        fmids.append(mids(entries))
    initial=[F(1)]+[F(0)]*(r-1)
    bound=bilinear(initial,metric,initial)*(gamma+max(cert["weak_defect_uncertainty_bounds"]))
    assert bound==cert["all_word_correction_noise_bound"]
    return gram,forms,mids(gintervals),fmids,budgets,asymmetric_radius


def check_word(word,maps,metric,records,cert,derived):
    gram,forms,gmid,fmids,budgets,_=derived
    r=len(metric);c=[F(1)]+[F(0)]*(r-1)
    forward=[c]
    for i in word:
        forward.append(mv(maps[i],forward[-1]))
    backward=[None]*(len(word)+1)
    backward[-1]=c
    for t in range(len(word)-1,-1,-1):
        backward[t]=mv(maps[word[t]],backward[t+1])
    ef=sum((bilinear(forward[t],budgets[i],forward[t])
            for t,i in enumerate(word)),F(0))
    eb=sum((bilinear(backward[t+1],budgets[i],backward[t+1])
            for t,i in enumerate(word)),F(0))
    norm=bilinear(c,metric,c)
    assert ef==norm-bilinear(forward[-1],metric,forward[-1])
    assert eb==norm-bilinear(backward[0],metric,backward[0])
    assert 0<=ef<=norm and 0<=eb<=norm
    expression={}
    center=bilinear(c,gmid,forward[-1])
    for j in range(r):
        for k in range(r):
            for native,coefficient in gram[j][k].items():
                addterm(expression,native,c[j]*forward[-1][k]*coefficient)
    for t,i in enumerate(word):
        center += bilinear(backward[t+1],fmids[i],forward[t])
        for j in range(r):
            for k in range(r):
                for native,coefficient in forms[i][j][k].items():
                    addterm(expression,native,backward[t+1][j]*forward[t][k]*coefficient)
    lo,hi=interval(expression,records)
    assert (lo+hi)/2==center
    assert (hi-lo)/2<=cert["all_word_correction_noise_bound"]
    return (hi-lo)/2


def main():
    old_path=BASE/"results"/"DISSIPATION_EXPERIMENT.json"
    new_path=BASE/"results"/"DISSIPATION_NOISE_REFINEMENT.json"
    old=decode(json.loads(old_path.read_text()))
    new=decode(json.loads(new_path.read_text()))
    assert len(new)==12
    indexed={}
    for family,rows in old.items():
        if isinstance(rows,list):
            for row in rows:
                indexed[(family,row["slow_scale_g"],row["raw_adc_radius"],row["depth"])]=row
    checked=[]
    words=[(),(0,),(1,),(0,1,1,0),(1,0)*10,(0,)*32]
    for row in new:
        key=(row["family"],row["g"],row["eta"],row["depth"])
        source=indexed[key]
        dictionary=[tuple(w) for w in source["dictionary"]]
        records={tuple(d["word"]):(d["interval"]["lo"],d["interval"]["hi"])
                 for d in source["decoded_records"]}
        metric=[[F(1)]]
        cert=row["noise_certificate"]
        derived=verify_certificate(dictionary,source["maps"],metric,records,cert)
        for word in words:
            check_word(word,source["maps"],metric,records,cert,derived)
        assert row["new_source_queries"]==0
        assert row["previous_total_bound"]==source["new_total_all_word_bound"]
        assert row["refined_all_word_total_bound"]==(
            source["dissipation_certificate"]["signed_remainder_bound_all_words"]
            +cert["all_word_correction_noise_bound"])
        checked.append({"family":row["family"],"g":str(row["g"]),"eta":str(row["eta"]),
                        "depth":row["depth"],
                        "noise_bound":str(cert["all_word_correction_noise_bound"]),
                        "refined_total":str(row["refined_all_word_total_bound"]),
                        "all_exact_inequalities_passed":True})

    # An off-diagonal case exercises unequal row and column radius sums.
    sys.path.insert(0,str(BASE/"core"))
    from echo_compiler import EchoCompiler,Interval
    from dissipation_noise import noise_certificate
    dictionary=[(),(1,)]
    maps=[[[F(1,2),F(1,10)],[F(-1,20),F(1,3)]],
          [[F(2,5),F(1,12)],[F(0),F(1,4)]]]
    metric=[[F(2),F(0)],[F(0),F(1)]]
    actions=[[[F(1,2),F(1,8)],[F(1,8),F(1,3)]],
             [[F(1,4),F(-1,10)],[F(-1,10),F(-1,3)]]]
    eta=F(1,10**8)
    needed={canonical(right+(i,)*k+left[::-1])
            for left in dictionary for right in dictionary for i in range(2) for k in range(3)}
    records={}
    for word in needed:
        center=response(actions,word)+eta*F((-1)**(len(word)+sum(word)),2)
        records[word]=(center-eta,center+eta)
    compiler=EchoCompiler(dictionary,2,{w:Interval(*v) for w,v in records.items()},maps)
    cert=noise_certificate(compiler,metric)
    derived=verify_certificate(dictionary,maps,metric,records,cert)
    assert derived[-1]  # The weak-defect radius matrix is genuinely nonsymmetric.
    tested=[w for n in range(7) for w in itertools.product(range(2),repeat=n)]
    tested += [(1,0)*12,(0,)*64,(1,)*64]
    max_radius=max(check_word(w,maps,metric,records,cert,derived) for w in tested)

    # At T=I fixed nonzero F uncertainty would sum to H*delta. The required
    # domination cannot hold: R=0 while D=delta>0. This is a boundary check.
    assert not psd2([[-F(1,1000)]])
    out={"replayed_receipts":checked,
         "off_diagonal_case":{"words_checked":len(tested),
                              "nonsymmetric_entry_radii":derived[-1],
                              "forward_and_reverse_telescopes_exact":True,
                              "native_midpoint_identity_exact":True,
                              "maximum_checked_native_radius":str(max_radius),
                              "uniform_noise_bound":str(cert["all_word_correction_noise_bound"]),
                              "all_checks_passed":True},
         "reviewed_sha256":{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest()
             for p in [BASE/"core"/"dissipation_noise.py",new_path,old_path]},
         "all_checks_passed":True}
    dest=Path(__file__).with_name("DISSIPATION_NOISE_REVIEW_CHECKS.json")
    dest.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))


if __name__=="__main__":
    main()
