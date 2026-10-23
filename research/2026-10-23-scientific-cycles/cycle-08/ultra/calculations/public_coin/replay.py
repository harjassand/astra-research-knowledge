#!/usr/bin/env python3
"""Bounded exact admissions + executable classical controller/quantum decoder.

Standard library only. These checks are not the all-L/error proof in PROOF.txt.
RNG seeds are replay fixtures, not a source of uncharged correlated access.
"""
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import argparse, hashlib, json, math, random, time


def params(L, eps):
    H=(L-1).bit_length()
    T=math.ceil(2*H+20*math.log(3/eps))
    g=s=math.ceil(math.log2(3/eps))
    return dict(H=H,T=T,g=g,s=s,Q=15*T+s,w=15*T+s+g)


def rref(rows, ncols):
    """RREF over F2. Bit0 is the protected Bell site and always zero."""
    out=list(rows)
    r=0
    piv=[]
    for col in range(ncols):
        idx=next((i for i in range(r,len(out)) if out[i]>>col&1),None)
        if idx is None:
            continue
        out[r],out[idx]=out[idx],out[r]
        for i in range(len(out)):
            if i!=r and out[i]>>col&1:
                out[i]^=out[r]
        piv.append(col)
        r+=1
    return out[:r],piv


def affine_admissions():
    """Exact equal-amplitude support/decoder checks after adaptive projections.

    nu suffix is expanded as an actual classical mixture. Bell prefixes remain
    coherent lists of basis amplitudes, grouped by the actual two-party measured
    outcomes and by subsequently measured tail digits. No density approximation.
    """
    total=good=unsafe=0
    for L in range(2,6):
        mask=(1<<L)-1
        for k in range(1,L+1):
            suffix=L-k
            # Exhaust the entire nu suffix, including mismatched strings.
            for ya in range(1<<suffix):
                for yb in range(1<<suffix):
                    grouped=defaultdict(list)
                    for x in range(1<<k):
                        aa=x|(ya<<k); bb=x|(yb<<k)
                        hist=[]; rows=[]; U=L
                        for q in range(4):
                            # Adaptive path defined ONLY by past public outcomes.
                            j=2+((q+sum(a^b for a,b in hist))%(L-1))
                            row=((0b101101101101 >> q)&((1<<j)-1))&~1
                            a=(row&aa).bit_count()&1
                            b=(row&bb).bit_count()&1
                            rows.append(row); hist.append((a,b))
                            if a!=b: U=min(U,j-1)
                        c=max(1,U-1)
                        key=(tuple(hist),tuple(rows),c,aa>>c,bb>>c)
                        grouped[key].append((aa&((1<<c)-1),bb&((1<<c)-1)))
                    for (hist,rows,c,ta,tb),support in grouped.items():
                        total+=1
                        # site1 was not measured: exact Bell factor even unsafe.
                        supp=set(support)
                        assert len(supp)==len(support)
                        assert all((a^1,b^1) in supp for a,b in supp)
                        if c>k:
                            unsafe+=1
                            continue
                        good+=1
                        hc=[h&((1<<c)-1) for h in rows]
                        basis,piv=rref(hc,c)
                        assert 0 not in piv
                        r=len(piv)
                        assert len(support)==1<<(c-r)
                        assert all(a==b for a,b in support)
                        # All amplitudes were +1/sqrt(2^k); no phases introduced.
                        # The common code coset is mapped to pivots0/free coords.
                        rep=support[0][0]
                        synd=[(h&rep).bit_count()&1 for h in basis]
                        free=[i for i in range(c) if i not in piv]
                        decoded=[]
                        for a,b in support:
                            for h,u in zip(basis,synd):
                                assert ((h&a).bit_count()&1)==u
                            # Invertible row-coordinate map: parity coords + free.
                            residual=sum((((h&a).bit_count()&1)^u)<<i
                                         for i,(h,u) in enumerate(zip(basis,synd)))
                            assert residual==0
                            z=sum(((a>>i)&1)<<j for j,i in enumerate(free))
                            decoded.append(z)
                        assert set(decoded)==set(range(1<<(c-r)))
                        assert free[0]==0
    return dict(status='PASS',exact_projected_branches=total,
                exact_safe_affine_decoders=good,unsafe_first_Bell_checks=unsafe,
                model='all suffix strings, k and adaptive branches for L=2..5')


def tree_receiver(L,eps,e,rng):
    """Root's full fixed-time controller, actual fresh binary parity rows.

    e is only used by the replay's oracle; the receiver never receives e or K.
    row/outcome history is the executable specification of the local measurements.
    Full seed uses Q(L-1) bits; here generated lazily from a replay RNG.
    """
    pp=params(L,eps); U=L; rows=[]; thresholds=[]
    # A is sampled uniformly; B=A xor e has correct diagonal statistics.
    aa=rng.getrandbits(L); bb=aa^e
    outcomes=[]
    def raw(j):
        nonlocal U
        if j<=1: return True
        if j>L: return False
        h=(rng.getrandbits(L-1)<<1)&((1<<j)-1)
        a=(h&aa).bit_count()&1; b=(h&bb).bit_count()&1
        rows.append(h);thresholds.append(j);outcomes.append((a,b))
        if a!=b: U=min(U,j-1)
        return a==b
    def amp(j):
        vals=[raw(j) for _ in range(5)]  # no implicit early stop
        return all(vals)
    # Stack of ordinary interval nodes followed by repeated singleton nodes.
    stack=[(1,L)]
    for _ in range(pp['T']):
        a,b=stack[-1]
        low=amp(a); high=amp(b+1)
        if not (low and not high):
            if len(stack)>1: stack.pop()
        elif a==b:
            stack.append((a,b))
        else:
            mid=(a+b)//2
            stack.append((mid+1,b) if amp(mid+1) else (a,mid))
    a,b=stack[-1]; guess=a if a==b else 1
    for _ in range(pp['s']): raw(guess+1)
    c=max(1,U-pp['g'])
    basis,piv=rref([h&((1<<c)-1) for h in rows],c)
    n=c-len(piv)
    assert len(rows)<=pp['Q']
    assert n>=1 and 0 not in piv
    return dict(U=U,c=c,n=n,guess=guess,parities=len(rows),rank=len(piv),
                seed_reserved_bits=pp['Q']*(L-1),first_Bell_exact=True),pp


def tree_prob(L,J,steps):
    """Exact rational noisy-controller law (amplified false-YES=1/32).

    This is an independent finite DP. A state is the visited path; verification
    chain depth is encoded by repeated singleton leaves. It checks no unjustified
    independent-step approximation: the full current-node law is propagated.
    """
    p=F(1,32)
    def yes(j):
        if j<=J: return F(1)
        if j>L: return F(0)
        return p
    dist={((1,L),):F(1)}
    for _ in range(steps):
        nxt=defaultdict(F)
        for path,weight in dist.items():
            a,b=path[-1]
            passed=yes(a)*(1-yes(b+1))
            parent=path[:-1] if len(path)>1 else path
            nxt[parent]+=weight*(1-passed)
            if a==b:
                nxt[path+((a,b),)]+=weight*passed
            else:
                mid=(a+b)//2; pr=yes(mid+1)
                nxt[path+((mid+1,b),)]+=weight*passed*pr
                nxt[path+((a,mid),)]+=weight*passed*(1-pr)
        dist={k:v for k,v in nxt.items() if v}
    assert sum(dist.values())==1
    failure=sum(v for path,v in dist.items() if path[-1]!=(J,J))
    return failure,len(dist)


def exact_oracle_admissions():
    records=[]
    for L in range(2,9):
        for e in range(0,1<<L,2):
            J=((e&-e).bit_length()-1) if e else L
            for j in range(2,L+1):
                vals=[((h&e).bit_count()&1) for h in range(0,1<<j,2)]
                assert sum(vals)==(0 if j<=J else len(vals)//2)
    gamma=math.log(2)/4-math.log(F(9,8))
    assert gamma>.05
    # Shorter-than-declared steps are intentional finite admission checks of the
    # transition law; the all-parameter proof is (10)--(12), not this finite DP.
    for L,J,steps in [(2,1,16),(3,2,20),(5,4,24)]:
        fail,states=tree_prob(L,J,steps)
        bound=math.exp(-gamma*steps)
        assert float(fail)<=bound
        records.append(dict(L=L,J=J,steps=steps,exact_failure=str(fail),
                            theorem_bound=bound,DP_states=states,status='PASS'))
    return records


def run(out):
    tw=time.perf_counter(); tc=time.process_time()
    affine=affine_admissions(); exact=exact_oracle_admissions()
    rng=random.Random(2026102208); sims=[]
    for L,eps in [(32,1/16),(257,1/64),(4096,1/4096),(16384,1/16384)]:
        safe=0; correct=0; maxq=0; minret=L
        for trial in range(12):
            K=rng.randrange(1,L+1)
            e=rng.getrandbits(L-K)<<K
            J=((e&-e).bit_length()-1) if e else L
            ans,pp=tree_receiver(L,eps,e,rng)
            assert ans['U']>=J>=K
            assert ans['c']>=max(1,K-pp['g'])
            assert ans['n']>=max(1,K-pp['w'])
            safe+=ans['c']<=K
            correct+=ans['guess']==J
            maxq=max(maxq,ans['parities']);minret=min(minret,ans['n'])
        sims.append(dict(L=L,epsilon=eps,trials=12,safe_cuts=safe,
                         exact_J_guesses=correct,max_actual_raw_queries=maxq,
                         minimum_register_allocation=minret,parameters=pp,
                         scope='seeded control admission, not confidence evidence'))
    table=[]
    for power in [16,20,24,30,40]:
        L=1<<power;eps=1/L; pp=params(L,eps)
        # Geometric last-nonzero upper mean for D2 is 1.
        def geom(u):return (u+1)*math.log(u+1)-u*math.log(u) if u else 0
        h=-eps*math.log(eps)-(1-eps)*math.log1p(-eps)
        lower=(1-eps)*math.log(L)-geom(pp['w']+1)-h
        table.append(dict(L=L,epsilon=eps,parameters=pp,
                          conservative_score_loss_nats=(pp['w']+1)*math.log(2),
                          expected_stock_nats=(L+1)*math.log(2)/2,
                          online_bits_per_direction_upper=pp['Q'],
                          communication_nats_per_direction_lower=max(0,lower),
                          public_seed_bits_per_party=pp['Q']*(L-1),
                          worst_CNOTs_per_party_upper=pp['Q']*(L-1)))
    result=dict(status='PASS',affine_quantum_admission=affine,
                exact_oracle_and_tree_admissions=exact,
                seeded_executable_controller=sims,resource_table=table,
                scope='finite admissions + explicit resource formulas; not a physical run')
    out.mkdir(parents=True,exist_ok=True)
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    costs=dict(wall_seconds=time.perf_counter()-tw,cpu_seconds=time.process_time()-tc,
               randomized_physical_trials=0,hardware_calls=0,paid_compute=0,
               total_discovery_time='UNKNOWN',all_L_proof='PROOF.txt')
    (out/'TIMING.json').write_text(json.dumps(costs,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],**costs)))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,
                                              default=Path(__file__).parent)
    run(p.parse_args().output_dir)
