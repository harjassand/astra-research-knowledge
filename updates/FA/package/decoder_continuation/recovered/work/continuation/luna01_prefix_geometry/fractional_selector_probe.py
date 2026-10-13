"""Exact finite-game probe for convexified all-prefix completion sets.

Finite endpoint-noise interface: zeta in {-gamma,+gamma}; safety is a rational
coordinate cube; states, backward winning sets, and convex-hull membership are
computed with Fraction arithmetic. This is a diagnostic counterexample search,
not a continuous-noise theorem.
"""
from fractions import Fraction as F
from itertools import combinations, product
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
GAMMA = F(1, 2)
COEFFS = ((F(1)+GAMMA, F(1)-GAMMA), (-F(1)+GAMMA, -F(1)-GAMMA))


def cross2(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])


def hull2(points):
    p = sorted(set(points))
    if len(p) <= 1:
        return p
    lo=[]
    for x in p:
        while len(lo) >= 2 and cross2(lo[-2], lo[-1], x) <= 0:
            lo.pop()
        lo.append(x)
    hi=[]
    for x in reversed(p):
        while len(hi) >= 2 and cross2(hi[-2], hi[-1], x) <= 0:
            hi.pop()
        hi.append(x)
    return lo[:-1] + hi[:-1]


def in_hull2(x, points):
    h = hull2(points)
    if not h:
        return False
    if len(h) == 1:
        return x == h[0]
    if len(h) == 2:
        a,b=h
        return cross2(a,b,x)==0 and all(min(a[i],b[i])<=x[i]<=max(a[i],b[i]) for i in range(2))
    return all(cross2(h[i],h[(i+1)%len(h)],x) >= 0 for i in range(len(h)))


def solve_square(A, b):
    """Exact Gauss-Jordan; return solution or None if singular."""
    n=len(b)
    m=[list(A[i])+[b[i]] for i in range(n)]
    row=0
    piv=[]
    for col in range(n):
        q=next((r for r in range(row,n) if m[r][col]),None)
        if q is None:
            return None
        m[row],m[q]=m[q],m[row]
        z=m[row][col]
        m[row]=[v/z for v in m[row]]
        for r in range(n):
            if r!=row and m[r][col]:
                z=m[r][col]
                m[r]=[m[r][j]-z*m[row][j] for j in range(n+1)]
        piv.append(col)
        row+=1
    return [m[i][-1] for i in range(n)]


def in_hull3(x, points):
    """Exact Caratheodory test (at most four points)."""
    p=list(set(points))
    d=3
    if x in p:
        return True
    for k in range(2, min(4,len(p))+1):
        for q in combinations(p,k):
            # Solve sum_j lambda_j * (q_j,1) = (x,1), with lambda_k=1-sum_{j<k}.
            # This gives d equations in k-1 unknowns; enumerate square coordinate subsets.
            cols=[[q[j][i]-q[-1][i] for j in range(k-1)] for i in range(d)]
            rhs=[x[i]-q[-1][i] for i in range(d)]
            for rows in combinations(range(d), k-1):
                A=[cols[i] for i in rows]
                b=[rhs[i] for i in rows]
                lam=solve_square(A,b)
                if lam is None:
                    continue
                if any(sum(cols[i][j]*lam[j] for j in range(k-1)) != rhs[i] for i in range(d)):
                    continue
                tail=F(1)-sum(lam)
                weights=lam+[tail]
                if all(w>=0 for w in weights):
                    return True
    return False


def safe(s, R):
    return all(abs(a) <= R for a in s)


def plus(s, c, v):
    return tuple(a+c*b for a,b in zip(s,v))


def run_case(d, schedule, R):
    N=len(schedule)
    layers=[{tuple(F(0) for _ in range(d))}]
    for t,v in enumerate(schedule):
        nxt=set()
        for s in layers[-1]:
            for cs in COEFFS[0]+COEFFS[1]:
                nxt.add(plus(s,cs,v))
        layers.append(nxt)
    W=[set() for _ in range(N+1)]
    A=[set() for _ in range(N+1)]
    W[N]={s for s in layers[N] if safe(s,R)}
    A[N]=set(W[N])
    for t in range(N-1,-1,-1):
        W[t]=set()
        A[t]=set()
        for s in layers[t]:
            if not safe(s,R):
                continue
            for eps, cs in enumerate(COEFFS):
                exact_succ=[plus(s,c,schedule[t]) for c in cs]
                if all(q in W[t+1] for q in exact_succ):
                    W[t].add(s)
                    break
            hull_points=list(A[t+1])
            if not hull_points:
                continue
            inside = in_hull2 if d==2 else in_hull3
            for cs in COEFFS:
                relax_succ=[plus(s,c,schedule[t]) for c in cs]
                if all(inside(q,hull_points) for q in relax_succ):
                    A[t].add(s)
                    break
    origin=tuple(F(0) for _ in range(d))
    return {
        "origin_exact_winning": origin in W[0],
        "origin_one_step_hull_selector": origin in A[0],
        "layers": [len(x) for x in layers],
        "exact_winning_counts": [len(x) for x in W],
        "hull_selector_counts": [len(x) for x in A],
        "A": A,
        "W": W,
        "layers_raw": layers,
    }


def encode(v):
    if isinstance(v,F):
        return str(v)
    if isinstance(v,tuple):
        return [encode(x) for x in v]
    if isinstance(v,list):
        return [encode(x) for x in v]
    if isinstance(v,dict):
        return {k:encode(x) for k,x in v.items() if k not in {"A","W","layers_raw"}}
    return v


def fixtures(d):
    e=[tuple(F(int(i==j)) for i in range(d)) for j in range(d)]
    if d==2:
        return e+[ (F(3,5),F(4,5)), (F(4,5),F(-3,5)), (F(1,2),F(1,2)) ]
    return e+[ (F(1,3),F(2,3),F(2,3)), (F(2,3),F(1,3),F(2,3)) ]


def search():
    for d in (2,3):
        pool=fixtures(d)
        # Exhaust short ordered schedules and a small rational cube-radius grid.
        for N in range(2,6 if d==2 else 5):
            for schedule in product(pool, repeat=N):
                for R in (F(1), F(3,2), F(2), F(5,2), F(3)):
                    result=run_case(d,schedule,R)
                    if result["origin_one_step_hull_selector"] and not result["origin_exact_winning"]:
                        # Find a reachable state where hull selector promises a sign
                        # whose endpoint children are in the next hull but not in A.
                        origin=tuple(F(0) for _ in range(d))
                        eps_ok=[]
                        for eps,cs in enumerate(COEFFS):
                            succ=[plus(origin,c,schedule[0]) for c in cs]
                            inside=in_hull2 if d==2 else in_hull3
                            if all(inside(q,list(result["A"][1])) for q in succ):
                                eps_ok.append({"epsilon":1 if eps==0 else -1,
                                               "successors":succ,
                                               "successors_not_selector_closed":[q for q in succ if q not in result["A"][1]]})
                        packed={"dimension":d,"gamma":GAMMA,"radius_linf":R,
                                "schedule":schedule,"origin_exact_winning":False,
                                "origin_hull_selector":True,"layers":result["layers"],
                                "exact_winning_counts":result["exact_winning_counts"],
                                "hull_selector_counts":result["hull_selector_counts"],
                                "origin_actions_into_next_hull":eps_ok,
                                "selector_closed_children":{
                                    "A_next_count":len(result["A"][1]),
                                    "exact_next_count":len(result["W"][1])}}
                        return encode(packed)
    return {"found":False}


if __name__=="__main__":
    result=search()
    (OUT/"fractional_selector_probe.json").write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
