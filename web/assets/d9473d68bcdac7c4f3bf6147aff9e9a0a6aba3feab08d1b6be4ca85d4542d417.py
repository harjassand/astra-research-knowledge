"""Acquire the phase-corrected Foster/event certificate on depth-four forests.

Roots may jointly catalyze a middle species. Each next species has one middle
parent and each fourth-layer leaf one third-layer parent. No other reactions.
See FOUR_LAYER_FOREST_ADDENDUM.txt; finite diagnostics are not the all-state proof.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
import random
import time
from four_layer_phase_certificate import interval, ceilq, cubic_envelope, dumpable


def acquire(spec):
    if not isinstance(spec, dict) or set(spec) != {"roots", "middle", "third", "fourth"}:
        raise ValueError("Full four-layer forest syntax required")
    roots, middle, third, fourth = (spec[k] for k in ("roots", "middle", "third", "fourth"))
    groups = [(roots, {"name", "birth", "death"}), (middle, {"name", "parents"}),
              (third, {"name", "parent", "birth", "death"}),
              (fourth, {"name", "parent", "birth", "death"})]
    if any(not isinstance(xs, list) or any(not isinstance(z, dict) or set(z) != keys for z in xs)
           for xs, keys in groups):
        raise ValueError("Unknown or missing species fields")
    names = [z["name"] for xs, _ in groups for z in xs]
    if (not roots or not fourth or any(not isinstance(x, str) or not x for x in names)
            or len(set(names)) != len(names)):
        raise ValueError("Distinct species, nonempty roots and fourth layer required")
    rr = {z["name"]: (interval(z["birth"]), interval(z["death"])) for z in roots}
    mids = {}
    for z in middle:
        ps = z["parents"]
        if (not isinstance(ps, dict) or not ps or not set(ps) <= set(rr)
                or any(not isinstance(v, dict) or set(v) != {"birth", "death"} for v in ps.values())):
            raise ValueError("Middle species need nonempty root parent sets")
        es = {i: (interval(v["birth"]), interval(v["death"])) for i, v in ps.items()}
        blo = sum(rr[i][0][0] for i in es)
        dhi = max(rr[i][1][1] for i in es)
        al = min(x[0][0] for x in es.values()); ah = max(x[0][1] for x in es.values())
        bl = min(x[1][0] for x in es.values()); bh = max(x[1][1] for x in es.values())
        cb = min(Q(1), bl / (2 * dhi)); gamma = min(cb * blo / 2, bl / 4)
        mids[z["name"]] = {"edges": es, "blo": blo, "dhi": dhi, "al": al,
                           "ah": ah, "bl": bl, "bh": bh, "c": cb,
                           "gamma": gamma, "G": 1 + cb, "cube": cubic_envelope(ah, bl)}
    thirds = {}
    for z in third:
        parent = z["parent"]
        if parent not in mids:
            raise ValueError("Third-layer species need exactly one middle parent")
        a, t = interval(z["birth"]), interval(z["death"])
        m = mids[parent]
        s = 1 + 4 * m["dhi"] / m["al"]
        c = min(Q(1), (t[0]/2)/(m["dhi"]/s+m["bh"]))
        gamma = min(c*m["blo"]/(s*(s+1)), c*m["al"]/(4*(s+1)), t[0]/4)
        thirds[z["name"]] = {"parent": parent, "birth": a, "death": t, "s": s,
                              "c": c, "gamma": gamma, "G": 1+c/s,
                              "cube": cubic_envelope(a[1], t[0])}
    fourths = {}
    for z in fourth:
        parent = z["parent"]
        if parent not in thirds:
            raise ValueError("Fourth-layer species need exactly one third-layer parent")
        e, u = interval(z["birth"]), interval(z["death"])
        t = thirds[parent]; m = mids[t["parent"]]
        s = 1 + m["dhi"]/m["bl"] + 2*m["dhi"]/m["al"]
        K = 2*m["ah"]+3*m["bh"]
        kap = min(m["bl"]/(s+1), m["blo"]/(2*s*(s+1)))
        J = m["blo"]/(s*(s+1)); gh = min(J, m["al"]/(2*(s+1)))
        eps = t["birth"][0]/(4*K)
        F = eps*J+(eps*K+t["death"][1]/2)**2/(4*eps*kap)
        M = 1+(F+1)/(u[0]/2)
        gamma = min(eps*gh, t["birth"][0]/4, Q(1))
        cube = cubic_envelope(e[1], u[0])
        fourths[z["name"]] = {"parent": parent, "middle": t["parent"], "birth": e,
                               "death": u, "s": s, "epsilon": eps, "M": M,
                               "gamma": gamma, "cube": cube,
                               "tB": cube*4*eps/(3*s),
                               "tC": cube*(M+1+8*eps/(3*s))}
    wc = {k:(1+sum(f["tC"] for f in fourths.values() if f["parent"]==k))/t["gamma"]
          for k,t in thirds.items()}
    wb = {j:(1+sum(f["tB"] for f in fourths.values() if f["middle"]==j)
             +sum(wc[k]*t["G"]*t["cube"] for k,t in thirds.items() if t["parent"]==j))/m["gamma"]
          for j,m in mids.items()}
    wa = {i:2*(1+sum(wb[j]*m["G"]*m["cube"] for j,m in mids.items() if i in m["edges"]))/r[1][0]
          for i,r in rr.items()}
    constant = sum(wa[i]*cubic_envelope(r[0][1], r[1][0]) for i,r in rr.items())
    kap = min([Q(1), *[f["gamma"] for f in fourths.values()]])
    cert = {"spec":spec, "names":names, "roots":rr, "middle":mids, "third":thirds,
            "fourth":fourths, "root_weights":wa, "middle_weights":wb,
            "third_weights":wc, "constant":constant, "kappa":kap,
            "core_radius":max(1,ceilq((2*constant+2)/kap))}
    turnover = sum(bounds[1] for _,_,bounds in raw(cert))
    cert["turnover"] = turnover
    cert["firing_bound_factor"] = 2*len(names)*turnover/kap
    return cert


def acquire_from_reactions(species, reactions):
    if (not isinstance(species, list) or not species
            or any(not isinstance(x,str) or not x for x in species)
            or len(set(species))!=len(species) or not isinstance(reactions,list)):
        raise ValueError("Complete explicit species/reaction table required")
    n=len(species); buckets={}
    for r in reactions:
        if not isinstance(r,dict) or set(r)!={"source","target","rate"}:
            raise ValueError("Exactly source/target/rate required")
        src,dst=r["source"],r["target"]
        if (not isinstance(src,(tuple,list)) or not isinstance(dst,(tuple,list))
                or len(src)!=n or len(dst)!=n
                or any(isinstance(x,bool) or not isinstance(x,int) or x<0 for x in (*src,*dst))):
            raise ValueError("Nonnegative integer vectors required")
        changes=[i for i in range(n) if src[i]!=dst[i]]
        if len(changes)!=1 or abs(dst[changes[0]]-src[changes[0]])!=1:
            raise ValueError("Only unit changes admitted")
        j=changes[0];sign=dst[j]-src[j];residual=src if sign>0 else dst
        if sum(residual) not in (0,1):
            raise ValueError("Only zero/one unchanged catalyst admitted")
        i=None if sum(residual)==0 else residual.index(1)
        if i==j:
            raise ValueError("Self-catalysis rejected")
        bounds=interval(r["rate"]);key=(j,i,sign);old=buckets.get(key,(Q(0),Q(0)))
        buckets[key]=tuple(a+b for a,b in zip(old,bounds))
    pairs={(j,i) for j,i,_ in buckets}
    if any((j,i,1) not in buckets or (j,i,-1) not in buckets for j,i in pairs):
        raise ValueError("Positive reverse required for every channel")
    roots={j for j,i in pairs if i is None}
    ps={j:{i for k,i in pairs if k==j and i is not None} for j in range(n)}
    if not roots or any(ps[j] for j in roots):
        raise ValueError("Root cannot have a catalytic incoming edge")
    rest=set(range(n))-roots
    if any(not ps[j] for j in rest):
        raise ValueError("Unused/disconnected species rejected")
    middle={j for j in rest if ps[j]<=roots};rest-=middle
    third={j for j in rest if len(ps[j])==1 and ps[j]<=middle};rest-=third
    fourth={j for j in rest if len(ps[j])==1 and ps[j]<=third};rest-=fourth
    if rest or not fourth:
        raise ValueError("Deeper, cyclic or multi-parent downstream graph rejected")
    def rates(j,i):
        return {"birth":list(map(str,buckets[(j,i,1)])),"death":list(map(str,buckets[(j,i,-1)]))}
    spec={"roots":[{"name":species[j],**rates(j,None)} for j in sorted(roots)],
          "middle":[{"name":species[j],"parents":{species[i]:rates(j,i) for i in sorted(ps[j])}}
                    for j in sorted(middle)],
          "third":[{"name":species[j],"parent":species[next(iter(ps[j]))],**rates(j,next(iter(ps[j])))}
                   for j in sorted(third)],
          "fourth":[{"name":species[j],"parent":species[next(iter(ps[j]))],**rates(j,next(iter(ps[j])))}
                    for j in sorted(fourth)]}
    return acquire(spec)


def raw(c):
    n=len(c["names"]);out=[]
    def pair(parent,child,birth,death):
        src=[0]*n
        if parent is not None:src[c["names"].index(parent)]=1
        dst=src.copy();dst[c["names"].index(child)]=1
        out.extend([(tuple(src),tuple(dst),birth),(tuple(dst),tuple(src),death)])
    for i,(b,d) in c["roots"].items():pair(None,i,b,d)
    for j,m in c["middle"].items():
        for i,(b,d) in m["edges"].items():pair(i,j,b,d)
    for group in [c["third"],c["fourth"]]:
        for k,t in group.items():pair(t["parent"],k,t["birth"],t["death"])
    return out


def gateD(c,k,x):
    f=c["fourth"][k];m=c["middle"][f["middle"]]
    S=sum(x[i] for i in m["edges"])
    return f["M"]+Q(1,x[f["parent"]]+1)+f["epsilon"]*(x[f["middle"]]-1)**2/(S+f["s"])


def V(c,state):
    x=dict(zip(c["names"],state));v=sum(w*x[i]**3 for i,w in c["root_weights"].items())
    for j,m in c["middle"].items():
        S=sum(x[i] for i in m["edges"])
        v+=c["middle_weights"][j]*(1+m["c"]/(S+1))*x[j]**3
    for k,t in c["third"].items():
        m=c["middle"][t["parent"]];S=sum(x[i] for i in m["edges"])
        v+=c["third_weights"][k]*(1+t["c"]/((S+t["s"])*(x[t["parent"]]+1)))*x[k]**3
    for k in c["fourth"]:v+=gateD(c,k,x)*x[k]**3
    return v


def generator(c,state,f):
    value=f(state);lv=Q(0)
    for src,dst,bounds in raw(c):
        propensity=1
        for x,y in zip(state,src):
            for k in range(y):propensity*=max(0,x-k)
        if propensity:
            nxt=tuple(x+z-y for x,y,z in zip(state,src,dst));jump=f(nxt)-value
            lv+=propensity*(bounds[1] if jump>0 else bounds[0])*jump
    return lv


def acquire_positive_target(c,q):
    """Compact exact recovery/event certificate for all counts >= q.

    alpha**H is retained symbolically: expanding it may require exponentially
    many bits in binary q. The accompanying proof charges that output cost.
    """
    if isinstance(q,bool) or not isinstance(q,int) or q<1:
        raise ValueError("Positive integer target count required")
    d=len(c["names"]);R=c["core_radius"];T0=c["turnover"];kap=c["kappa"]
    coef=sum(c["root_weights"].values())
    coef+=sum(c["middle_weights"][j]*m["G"] for j,m in c["middle"].items())
    coef+=sum(c["third_weights"][k]*t["G"] for k,t in c["third"].items())
    coef+=sum(t["M"]+1+t["epsilon"]*(R+1)**2/t["s"] for t in c["fourth"].values())
    Vcore=R**3*coef
    H=d*q;D=R-1+H;Qtotal=T0*(D+1)**2
    low=min(bounds[0] for _,_,bounds in raw(c));alpha=low/(2*Qtotal);t0=Q(H)/Qtotal
    time_cycle=Vcore+(c["constant"]+1)*t0
    event_cycle=T0*t0+3*d*T0/kap*(Vcore+c["constant"]*t0)
    return {"target_min_each":q,"word_length_upper":H,"path_count_upper":D,
            "path_rate_upper":Qtotal,"step_probability_lower":alpha,
            "success_probability_lower":{"base":alpha,"exponent":H},"attempt_duration":t0,
            "core_potential_upper":Vcore,"mean_time_bound_expression":"V(x)+time_cycle/alpha**H",
            "time_cycle":time_cycle,"mean_all_event_bound_expression":"firing_bound_factor*V(x)+event_cycle/alpha**H",
            "event_cycle":event_cycle,"firing_bound_factor":c["firing_bound_factor"],
            "status":"COMPACT_EXACT_RATIONAL_POWER_CERTIFICATE; expanded output cost depends on numeric q"}


def verify():
    start=time.perf_counter();rng=random.Random(130)
    fixtures=[{"roots":[{"name":"A","birth":[1,1],"death":[1,1]}],
               "middle":[{"name":"B","parents":{"A":{"birth":[1,1],"death":[1,1]}}}],
               "third":[{"name":"C","parent":"B","birth":[1,1],"death":[1,1]}],
               "fourth":[{"name":"D","parent":"C","birth":[1,1],"death":[1,1]}]},
              {"roots":[{"name":"A","birth":[1,3],"death":[2,4]},
                        {"name":"E","birth":["1/2",2],"death":[1,5]}],
               "middle":[{"name":"B","parents":{"A":{"birth":[1,3],"death":[1,4]},
                                                     "E":{"birth":[2,4],"death":["1/2",3]}}},
                         {"name":"F","parents":{"E":{"birth":[1,2],"death":[2,5]}}}],
               "third":[{"name":"C","parent":"B","birth":[1,4],"death":[1,3]},
                        {"name":"G","parent":"F","birth":[2,3],"death":[1,2]}],
               "fourth":[{"name":"D","parent":"C","birth":[1,2],"death":[1,4]},
                         {"name":"H","parent":"G","birth":[2,4],"death":[1,3]}]}]
    checks=killed=admission=rejected=0;records=[]
    for fi,spec in enumerate(fixtures):
        c=acquire(spec);n=len(c["names"])
        states=list(product(range(5 if n==4 else 2),repeat=n))
        states.extend(tuple(rng.randrange(60) for _ in range(n)) for _ in range(64))
        for state in states:
            x=dict(zip(c["names"],state))
            f=sum(x[i]**3 for i in c["names"] if i not in c["fourth"])
            f+=sum(t["gamma"]*x[i]**3 for i,t in c["fourth"].items())
            assert generator(c,state,lambda z:V(c,z))<=c["constant"]-f
            checks+=1
        for k,t in c["fourth"].items():
            for A,B,C in product([0,1,2,1000],[0,1,2,1000],[0,1,2]):
                x={i:0 for i in c["names"]};roots=list(c["middle"][t["middle"]]["edges"])
                x[roots[0]]=A;x[t["middle"]]=B;x[t["parent"]]=C
                state=tuple(x[i] for i in c["names"])
                q=gateD(c,k,x)
                lv=generator(c,state,lambda z:gateD(c,k,dict(zip(c["names"],z))))
                assert lv-t["death"][0]/2*C*q<=-t["gamma"]
                killed+=1
        rs=[{"source":list(a),"target":list(b),"rate":list(map(str,k))} for a,b,k in raw(c)]
        c2=acquire_from_reactions(c["names"],rs)
        assert V(c2,(3,)*n)==V(c,(3,)*n)
        assert c2["constant"]==c["constant"]
        admission+=1
        # A declared fifth-layer species and its paired catalytic reactions
        # must reject, even though each individual reaction is bimolecular.
        extended=[]
        for r in rs:
            extended.append({"source":r["source"]+[0],"target":r["target"]+[0],"rate":r["rate"]})
        src=[0]*(n+1);src[c["names"].index(next(iter(c["fourth"])))] = 1
        dst=src.copy();dst[-1]=1
        extended.extend([{"source":src,"target":dst,"rate":[1,1]},
                         {"source":dst,"target":src,"rate":[1,1]}])
        try:acquire_from_reactions(c["names"]+["UNADMITTED_FIFTH"],extended)
        except ValueError:rejected+=1
        else:raise AssertionError("Fifth layer silently admitted")
        # Input species/columns may be supplied in arbitrary order.
        flipped=[{"source":r["source"][::-1],"target":r["target"][::-1],"rate":r["rate"]} for r in rs]
        c3=acquire_from_reactions(c["names"][::-1],flipped)
        named={name:j+2 for j,name in enumerate(c["names"])}
        assert V(c3,tuple(named[x] for x in c3["names"]))==V(c,tuple(named[x] for x in c["names"]))
        assert c3["constant"]==c["constant"]
        admission+=1
        records.append({"certificate":dumpable(c),"state_checks":len(states),
                        "positive_target_certificate":dumpable(acquire_positive_target(c,1))})
    return {"status":"EXACT_FINITE_DIAGNOSTICS_PASSED","raw_generator_states":checks,
            "killed_gate_states":killed,"raw_admission_fixtures":admission,"fifth_layer_rejections":rejected,"fixtures":records,
            "elapsed_seconds":time.perf_counter()-start,"scope":"Finite diagnostics; all-state argument in addendum"}


if __name__=="__main__":
    out=verify();Path(__file__).with_name("four_layer_forest_checks.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:out[k] for k in ["status","raw_generator_states","killed_gate_states",
                                        "raw_admission_fixtures","fifth_layer_rejections","elapsed_seconds"]},indent=2))
