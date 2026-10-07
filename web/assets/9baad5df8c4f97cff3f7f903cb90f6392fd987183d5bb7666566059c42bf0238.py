"""Exact count compiler for an acquired bounded-frontier support ordering.

In addition to validating supplied orderings, a bounded balanced-separator
search acquires logarithmic-frontier orderings. For fixed separator budget q,
every graph of treewidth <= q-1 is admitted, without a supplied decomposition.
Rejection is rejection of this admission protocol, not a treewidth lower bound.
"""
from itertools import combinations
from representation_compiler import C,Q,matrix
from banded_hard_bcs import pair_gate,add,local_masks,capped_rational_bit


def support_graph(f):
    f=matrix(f); n=len(f)
    if any(len(row) != n for row in f): raise ValueError('F must be square')
    graph=[set() for _ in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            if f[i][j] or f[j][i]: graph[i].add(j);graph[j].add(i)
    return f,graph


def components(graph,vertices):
    unseen=set(vertices); result=[]
    while unseen:
        start=min(unseen); unseen.remove(start); reached={start}; stack=[start]
        while stack:
            v=stack.pop()
            for u in graph[v]&unseen: unseen.remove(u); reached.add(u);stack.append(u)
        result.append(reached)
    return result


def separator_ordering(f,budget=3):
    """Exact polynomial admission for fixed budget; acquired ordering/certificate."""
    if budget < 1: raise ValueError('separator budget must be positive')
    f,graph=support_graph(f); n=len(f); nodes=[]; candidate_queries=0
    def recurse(vertices,depth):
        nonlocal candidate_queries
        if len(vertices) <= budget:
            nodes.append({'vertices':sorted(vertices),'separator':sorted(vertices),
                          'components':[],'depth':depth})
            return sorted(vertices)
        selected=None
        for size in range(budget+1):
            for sep in combinations(sorted(vertices),size):
                candidate_queries+=1
                pieces=components(graph,vertices-set(sep))
                if all(2*len(piece) <= len(vertices) for piece in pieces):
                    selected=(list(sep),pieces);break
            if selected is not None: break
        if selected is None: raise ValueError(sorted(vertices))
        sep,pieces=selected
        nodes.append({'vertices':sorted(vertices),'separator':sep,
                      'components':[sorted(piece) for piece in pieces],'depth':depth})
        ordered=[]
        for piece in pieces: ordered.extend(recurse(piece,depth+1))
        return ordered+sep
    try:
        order=recurse(set(range(n)),0)
    except ValueError as error:
        return {'status':'REJECTED_SEPARATOR_PROTOCOL','budget':budget,
                'failed_induced_vertices':error.args[0],'candidate_queries':candidate_queries}
    certificate=recognize_frontier(f,order)
    assert certificate['width'] <= budget*max(1,n.bit_length())
    return {'status':'ACCEPTED','budget':budget,'order':order,'width':certificate['width'],
            'separator_certificate':nodes,'candidate_queries':candidate_queries,
            'recognition_scope':'balanced-separator admission, not exact treewidth recognition'}


def recognize_frontier(f,order=None,cap=None):
    f,graph=support_graph(f); n=len(f)
    order=list(range(n)) if order is None else list(order)
    if sorted(order) != list(range(n)): raise ValueError('order must be a site permutation')
    live=set(); boundaries=[]; peak=0; peak_index=None
    for i,site in enumerate(order):
        future=set(order[i+1:])
        live=(live|graph[site])&future
        boundaries.append(sorted(live))
        if len(live) > peak: peak=len(live);peak_index=i
    return {'status':'ACCEPTED' if cap is None or peak <= cap else 'REJECTED_FRONTIER_WIDTH',
            'order':order,'width':peak,'peak_after_index':peak_index,
            'boundaries':boundaries,'F':f,'graph':graph}


def compile_admission(f,separator_budget=3):
    """Acquires a logarithmic-frontier certificate or reports admission unknown.

    For fixed q, every treewidth <= q-1 input is admitted; other inputs may
    also be admitted when a checked ordering has frontier <= q*bit_length(n).
    This is not a minimum-treewidth or minimum-pathwidth oracle.
    """
    if separator_budget < 1: raise ValueError('separator budget must be positive')
    bound=separator_budget*max(1,len(f).bit_length())
    natural=recognize_frontier(f,cap=bound)
    if natural['status'] == 'ACCEPTED':
        return {'status':'ACCEPTED','method':'INPUT_ORDER','order':natural['order'],
                'width':natural['width'],'frontier_bound':bound,
                'separator_budget':separator_budget}
    acquired=separator_ordering(f,separator_budget)
    if acquired['status'] != 'ACCEPTED':
        return {'status':'UNKNOWN_ADMISSION','frontier_bound':bound,
                'failed_separator_search':acquired}
    return {'status':'ACCEPTED','method':'ACQUIRED_SEPARATOR_ORDER',
            'order':acquired['order'],'width':acquired['width'],
            'frontier_bound':bound,'separator_budget':separator_budget,
            'separator_certificate':acquired['separator_certificate'],
            'candidate_queries':acquired['candidate_queries']}


def insert_vacuum(rho,position):
    mask=(1 << (2*position))-1; out={}
    for (a,b,q),weight in rho.items():
        aa=(a&mask)|((a&~mask) << 2)
        bb=(b&mask)|((b&~mask) << 2)
        out[aa,bb,q]=weight
    return out


def count_coefficients(f,mode_constraints=None,site_constraints=None,order=None,
                       frontier_cap=None,collect_stats=False):
    certificate=recognize_frontier(f,order,frontier_cap)
    if certificate['status'] != 'ACCEPTED': raise ValueError(certificate)
    order=certificate['order']; f=certificate['F']; n=len(f)
    position={site:i for i,site in enumerate(order)}
    ff=[[f[i][j] for j in order] for i in order]
    graph=[{position[j] for j in certificate['graph'][site]} for site in order]
    modes=None if mode_constraints is None else {(position[site],spin):bit for (site,spin),bit in mode_constraints.items()}
    sites=None if site_constraints is None else {position[site]:occupations for site,occupations in site_constraints.items()}
    allowed=local_masks(n,modes,sites)
    rho={(0,0,0):C(1)}; live=[]; peak=1; live_peak=0; gates=0
    for i in range(n):
        needed={i}|{j for j in graph[i] if j>i}
        for j in sorted(needed-set(live)):
            insertion=sum(v<j for v in live)
            rho=insert_vacuum(rho,insertion);live.insert(insertion,j)
        assert live[0] == i
        live_peak=max(live_peak,len(live))
        for j in sorted(graph[i]):
            if j <= i: continue
            p=live.index(j)
            for coefficient,left,right in ((ff[i][j],0,2*p+1),(ff[j][i],2*p,1)):
                if coefficient:
                    rho=pair_gate(rho,coefficient,left,right);gates+=1
                    peak=max(peak,len(rho))
        out={}
        for (a,b,q),weight in rho.items():
            occupation=a&3
            if occupation == (b&3) and occupation in allowed[i]:
                add(out,(a >> 2,b >> 2,q+occupation.bit_count()),weight)
        rho=out;live.pop(0)
        peak=max(peak,len(rho))
        assert set(order[j] for j in live) == set(certificate['boundaries'][i])
    polynomial=[Q(0)]*(n+1)
    for (a,b,q),weight in rho.items():
        assert a == b == 0 and weight.im == 0 and weight.re >= 0
        polynomial[q]+=weight.re
    assert all(not polynomial[q] for q in range(1,n+1,2))
    result={'coefficients':[polynomial[2*k] for k in range(n//2+1)],
            'width':certificate['width'],'order':order}
    if collect_stats:
        result['stats']={'maximum_live_sites':live_peak,'peak_density_coefficients':peak,
                         'pair_creation_gates':gates,'status':'exact rational count contraction'}
    return result


def prefix_count(f,k,mode_constraints=None,site_constraints=None,order=None,frontier_cap=None):
    if k < 0 or 2*k > len(f): return Q(0)
    return count_coefficients(f,mode_constraints,site_constraints,order,frontier_cap)['coefficients'][k]


def sample_born(f,k,getrandbits,epsilon=Q(1,1000000),order=None,frontier_cap=None):
    """Uniform finite-budget sampler; fair bits required for its TV guarantee."""
    f=matrix(f); n=len(f); epsilon=Q(epsilon)
    if not 0 < epsilon <= 1: raise ValueError('invalid epsilon')
    z=prefix_count(f,k,order=order,frontier_cap=frontier_cap)
    if not z: return {'status':'ZERO','norm':z}
    attempts=0
    while Q(2*n,1 << attempts) > epsilon: attempts+=1
    prefix={};fallback=False;coin_bits=0;queries=1
    for site,spin in ([(i,'U') for i in range(n)]+[(i,'D') for i in range(n)]):
        zero=dict(prefix);zero[site,spin]=0
        one=dict(prefix);one[site,spin]=1
        z0=prefix_count(f,k,zero,order=order,frontier_cap=frontier_cap)
        z1=prefix_count(f,k,one,order=order,frontier_cap=frontier_cap);queries+=2
        assert z0+z1 > 0
        if fallback: bit=int(bool(z1))
        else:
            bit,used=capped_rational_bit(z1/(z0+z1),getrandbits,attempts);coin_bits+=used
            if bit is None: fallback=True;bit=int(bool(z1))
        prefix[site,spin]=bit
    up=[i for i in range(n) if prefix[i,'U']];down=[i for i in range(n) if prefix[i,'D']]
    assert len(up) == len(down) == k and not set(up)&set(down)
    return {'status':'SAMPLE','up':up,'down':down,'norm':z,'fallback':fallback,
            'coin_bits':coin_bits,'attempt_cap':attempts,'exact_count_queries':queries,
            'randomness_contract':'independent fair random bits'}
