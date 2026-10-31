"""Finite qualitative receiving interface; no quantitative polynomial is materialized.
Exact mathematical input validation, not an adversarial-service security claim.
"""
from fractions import Fraction as F
import hashlib,json
import projective_mass as proposer
PROOF_SHA='439c727065e56787308d9b0007d76a504c05cb8d1c1eeb75077578de06624014'
FAMILY='one-open-coordinate-leading-support-v1'
CONCLUSIONS=['nonexplosion from every initial state','positive recurrence of every communicating class','every finite exponential total-count moment for each classwise invariant probability']

def need(condition,message):
    if not condition:raise ValueError(message)
def normalized(species,raw):
    need(isinstance(species,(list,tuple)) and len(species)>=2,'n>=2 required')
    need(all(type(s)==str and s for s in species) and len(set(species))==len(species),'unique nonempty species names required')
    n=len(species);out=[]
    for row in raw:
        need(len(row)==3,'reaction triple required');u,v,k=row
        need(len(u)==len(v)==n and all(type(x)==int and x>=0 for x in (*u,*v)),'integer stoichiometry required')
        need(type(k)==int or isinstance(k,F),'exact int/Fraction rate required');need(k>0,'positive rate required')
        if tuple(u)!=tuple(v):out.append((tuple(u),tuple(v),F(k)))
    return out

def raw_digest(species,raw):
    payload={'species':list(species),'raw':[[list(u),list(v),str(k)] for u,v,k in raw]}
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def acquire(species,raw):
    raw=normalized(species,raw);rec=proposer.recognize(species,raw)
    if not rec['accepted']:
        return {'status':'UNSUPPORTED_RAW_ARCHITECTURE','network_stability':'UNKNOWN','recognition':rec}
    support=proposer.support_certificate(rec,include_formal_bounds=False)
    out={'family':FAMILY,'theorem_sha256':PROOF_SHA,'raw_sha256':raw_digest(species,raw),
      'role':{'pivot':rec['pivot'],'n':len(species),'leading_order':rec['leading_order'],
              'immigration':str(rec['immigration']),'death':str(rec['death'])},
      'support_witness':support,'quantitative_output':'not acquired by this interface',
      'work':{'normalized_nonnull_channels':len(raw),'support_reaction_tests':support['support_reaction_tests'],
              'support_coordinate_tests_upper':2*len(species)*support['support_reaction_tests'],
              'polynomial_degrees_searched':0,'Euler_steps_executed':0,'stationary_fiber_laws_used':0}}
    if support['accessible']:
        out.update(status='QUALITATIVE_CERTIFIED',conclusions=CONCLUSIONS)
    else:
        out.update(status='STRICT_TOP_CONE_OBSTRUCTED',network_stability='UNKNOWN',conclusions=['no degree in the stated strict raw-top-order cone can succeed'])
    verify(species,raw,out)
    return out

def verify(species,raw,receipt):
    """Recheck raw architecture, graph returns, and finite support chains independently."""
    raw=normalized(species,raw);n=len(species);role=receipt['role'];A=role['pivot']
    need(receipt['family']==FAMILY and receipt['theorem_sha256']==PROOF_SHA,'wrong theorem binding')
    need(receipt['raw_sha256']==raw_digest(species,raw),'raw list binding mismatch')
    need(type(A)==int and 0<=A<n and role['n']==n,'invalid role')
    zero=(0,)*n;unit=tuple(int(j==A) for j in range(n));lam=death=F(0);internal=[]
    for u,v,k in raw:
        if u==zero and v==unit:lam+=k
        elif u==unit and v==zero:death+=k
        else:
            need(sum(u)==sum(v),'nonconservative internal channel');internal.append((u,v,k))
    need(lam>0 and death>0 and F(role['immigration'])==lam and F(role['death'])==death,'open core mismatch')
    p=max([2]+[sum(u) for u,v,k in internal]);need(role['leading_order']==p,'wrong raw leading order')
    # Separate graph closure calculation: every directed edge has a return route.
    vertices={u for u,v,k in raw}|{v for u,v,k in raw};adj={u:set() for u in vertices}
    for u,v,k in raw:adj[u].add(v)
    visited_edges=0;reach={}
    for start in vertices:
        reached={start};front={start}
        while front:
            following=set()
            for v in front:following.update(adj[v]);visited_edges+=len(adj[v])
            front=following-reached;reached.update(front)
        reach[start]=reached
    need(all(u in reach[v] for u,v,k in raw),'graph is not weakly reversible')
    sw=receipt['support_witness'];need(sw['leading_order']==p,'support order mismatch')
    # Independently replay the deterministic proposer scan to verify paid work,
    # not merely path validity. Each accepted path is also checked below.
    leading=[(i,u,v) for i,(u,v,k) in enumerate(internal) if sum(u)==p]
    expected=[];reaction_tests=0
    for seed in range(n):
        active={seed};path=[]
        while A not in active:
            chosen=None
            for row,u,v in leading:
                reaction_tests+=1
                if not any(u[j] and j not in active for j in range(n)):
                    newly={j for j in range(n) if v[j]}-active
                    if newly:chosen=(row,newly);break
            if chosen is None:break
            row,newly=chosen;path.append({'internal_row':row,'before':sorted(active),'added':sorted(newly)})
            active|=newly
        expected.append({'seed':seed,'support':sorted(active),'steps':path,'reaches_open_species':A in active})
        if A not in active:break
    need(sw['trials']==expected,'support scan trace mismatch')
    need(type(sw['support_reaction_tests'])==int and sw['support_reaction_tests']==reaction_tests,'support witness work count mismatch')
    need(receipt['work']['support_reaction_tests']==reaction_tests,'support receipt work count mismatch')

    need(receipt['quantitative_output']=='not acquired by this interface','qualitative/numerical output confused')
    need(receipt['work']['normalized_nonnull_channels']==len(raw),'channel work count mismatch')
    need(receipt['work']['support_coordinate_tests_upper']==2*n*sw['support_reaction_tests'],'support work upper bound mismatch')
    need(receipt['work']['polynomial_degrees_searched']==0 and receipt['work']['Euler_steps_executed']==0 and receipt['work']['stationary_fiber_laws_used']==0,'unsupported execution claim')
    if receipt['status']=='QUALITATIVE_CERTIFIED':
        need(sw['accessible'] is True and receipt['conclusions']==CONCLUSIONS,'qualitative conclusion mismatch')
        need([trial['seed'] for trial in sw['trials']]==list(range(n)),'one witness per seed required')
        checks=0
        for trial in sw['trials']:
            support={trial['seed']};need(len(trial['steps'])<=n-1,'support chain too long')
            for step in trial['steps']:
                i=step['internal_row'];need(type(i)==int and 0<=i<len(internal),'invalid reaction index')
                u,v,k=internal[i]
                need(sum(u)==p and all(not u[j] or j in support for j in range(n)),'source not in current top support')
                new={j for j in range(n) if v[j] and j not in support}
                need(new and step['before']==sorted(support) and step['added']==sorted(new),'support enlargement mismatch')
                support.update(new);checks+=1
            need(A in support and trial['support']==sorted(support) and trial['reaches_open_species'] is True,'A not reached')
        return {'verified':True,'status':'QUALITATIVE_CERTIFIED','support_steps_verified':checks,
                'graph_vertices':len(vertices),'graph_outgoing_edges_scanned':visited_edges,'support_reaction_scans_replayed':reaction_tests,'numeric_Foster_constants_returned':False}
    need(receipt['status']=='STRICT_TOP_CONE_OBSTRUCTED' and sw['accessible'] is False,'unknown status')
    face=sw['closed_face_support'];need(face==sorted(set(face)) and face and all(type(j)==int and 0<=j<n for j in face) and A not in face,'invalid A-free face')
    S=set(face)
    for u,v,k in internal:
        if sum(u)==p and all(not u[j] or j in S for j in range(n)):
            need(all(not v[j] or j in S for j in range(n)),'face is not invariant')
    need(receipt['network_stability']=='UNKNOWN' and sw['all_degree_strict_cone_impossible'] is True,'obstruction is not an instability proof')
    need(receipt['conclusions']==['no degree in the stated strict raw-top-order cone can succeed'],'wrong obstruction conclusion')
    return {'verified':True,'status':'STRICT_TOP_CONE_OBSTRUCTED','closed_face_support':face,'support_reaction_scans_replayed':reaction_tests,'network_stability':'UNKNOWN'}

if __name__=='__main__':
    species,raw=proposer.demo_network();r=acquire(species,raw)
    print(json.dumps({'receipt':r,'independent_raw_receiving_pass':verify(species,raw,r)},indent=2,sort_keys=True))
