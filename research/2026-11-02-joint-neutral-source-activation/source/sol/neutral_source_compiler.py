#!/usr/bin/env python3
"""Acquire and verify finite raw neutral-source closure certificates.

All scientific claims are scoped in NEUTRAL_CLOSURE_RAW_CERTIFICATE.md.
Finite budget/grammar refusal means UNKNOWN, never chemical instability.
"""
from fractions import Fraction as F
from collections import deque,defaultdict
from itertools import product
from pathlib import Path
from math import prod,comb,factorial
import json,time,hashlib
from support_receiver_certificate import canon

P=Path(__file__).resolve().parent
OLD=P/'sources/N1567/exact_terminal_gap.py'
LEGACY={'__name__':'accepted_N1567_readonly'}
exec(compile(OLD.read_text(),str(OLD),'exec'),LEGACY)

class Budget(Exception):pass
def ff(a,b):return 0 if a<b else prod(range(a-b+1,a+1))
def falling(x,y):return prod(ff(a,b) for a,b in zip(x,y))
def rawdigest(raw):return hashlib.sha256(json.dumps([(y,z,str(c)) for y,z,c in raw],separators=(',',':')).encode()).hexdigest()
def profs(O,M):return product(*(range(M[i]+1) for i in O))
def encode_profile(O,b,M):return [{'coordinate':i,'kind':'tail' if v==M[i] else 'exact','value':v} for i,v in zip(O,b)]
def profile_key(profile):return tuple((v['coordinate'],v['kind'],v['value']) for v in profile)
def profile_matches(profile,z):return all(z[v['coordinate']]>=v['value'] if v['kind']=='tail' else z[v['coordinate']]==v['value'] for v in profile)

def rawpaths(C,raw):
    adj=defaultdict(list)
    for j,(y,z,k) in enumerate(raw):adj[y].append((z,j))
    out={}
    for y in C:
        todo=deque([y]);back={y:None}
        while todo:
            v=todo.popleft()
            for w,j in adj[v]:
                if w not in back:back[w]=(v,j);todo.append(w)
        for z in back:
            w=z;word=[]
            while back[w] is not None:w0,j=back[w];word.append(j);w=w0
            out[y,z]=list(reversed(word))
    return out

def make_node(t,profile):return (tuple(t),tuple(v['value'] for v in profile if v['kind']=='exact'))
def neutral_step(node,index,I,profile,raw):
    t,rho=node;s,u,k=raw[index];symbolic=set(I)|{v['coordinate'] for v in profile if v['kind']=='tail'}
    if any(s[i]!=t[i] for i in symbolic):return None
    exact=[v['coordinate'] for v in profile if v['kind']=='exact'];xs=[z+t[i] for i,z in zip(exact,rho)]
    if any(x<s[i] for i,x in zip(exact,xs)):return None
    if prod(ff(x,s[i]) for i,x in zip(exact,xs))!=prod(ff(x,t[i]) for i,x in zip(exact,xs)):return None
    newrho=tuple(x-s[i] for i,x in zip(exact,xs))
    return tuple(u),newrho

def source_available(node,a,profile):
    t,rho=node;it=iter(rho)
    for v in profile:
        i=v['coordinate'];z=next(it) if v['kind']=='exact' else v['value']
        if a[i]>z+t[i]:return False
    return True

def cone(terms,k,stats):
    # One strictly positive gap already supplies an acquired one-column witness.
    for term in terms:
        gap=term['gap']
        if min(gap)>0:return [(term,F(1,min(gap)))],0
    unique={tuple(term['gap']):term for term in terms};chosen=list(unique.values());gaps=[tuple(t['gap']) for t in chosen]
    if not gaps:return None,0
    upper=comb(len(gaps)+k,k)
    if stats['new_lp_upper_work']+upper>2000000:raise Budget('new exact cone basis budget')
    stats['new_lp_upper_work']+=upper
    cols=gaps+[tuple(-int(i==j) for i in range(k)) for j in range(k)]
    sol,n=LEGACY['nonnegative_solve'](cols,[1]*k);stats['new_exact_bases_tested']+=n
    if sol is None:return None,n
    return [(t,a) for t,a in zip(chosen,sol) if a],n

def search_row(t,I,profile,M,C,raw,word_budget,stats):
    root=make_node(t,profile);queue=deque([(root,[])]);seen={root};terms=[]
    debt_product=prod(factorial(z) for z in root[1]);debt_bound=max(1,sum(root[1]))
    node_bound=len(C)*(debt_bound+1)**len(root[1])
    stats['largest_proved_profile_graph_bound']=max(stats.get('largest_proved_profile_graph_bound',0),node_bound)
    while queue:
        node,word=queue.popleft();stats['new_nodes_expanded']+=1
        if stats['new_nodes_expanded']>100000:raise Budget('neutral graph node budget')
        mark,rho=node
        for a in C:
            if source_available(node,a,profile):
                gap=tuple(a[i]-mark[i] for i in I)
                if any(gap):
                    term={'word':word,'terminal_mark':mark,'competing_source':a,'gap':gap};terms.append(term)
                    if min(gap)>0:return {'terms':[{**term,'weight':str(F(1,min(gap)))}],'graph_closed':False}
        for j in range(len(raw)):
            stats['neutral_edge_checks']+=1;dest=neutral_step(node,j,I,profile,raw)
            if dest is not None and dest not in seen:
                if any(z>debt_bound for z in dest[1]) or prod(factorial(z) for z in dest[1])!=debt_product:raise AssertionError('neutral factorial debt invariant failed')
                if word_budget is not None and len(word)+1>word_budget:raise Budget('neutral shortest-word resource budget')
                seen.add(dest);queue.append((dest,word+[j]))
                if len(seen)>node_bound:raise AssertionError('proved finite neutral graph bound failed')
    solution,n=cone(terms,len(I),stats)
    if solution is not None:return {'terms':[{**t,'weight':str(a)} for t,a in solution],'graph_closed':False}
    # The COMPLETE factorial-debt graph has been exhausted; no depth truncation.
    closed=all((dest:=neutral_step(node,j,I,profile,raw)) is None or dest in seen for node in seen for j in range(len(raw)))
    gaps=list({tuple(t['gap']) for t in terms})
    dual=None
    if gaps:
        cols=[tuple(g[i] for g in gaps)+(1,) for i in range(len(I))]
        cols += [tuple(int(i==j) for i in range(len(gaps)))+(0,) for j in range(len(gaps))]
        ds,n=LEGACY['nonnegative_solve'](cols,[0]*len(gaps)+[1]);stats['new_exact_bases_tested']+=n
        if ds is not None:dual=list(map(str,ds[:len(I)]))
    return {'terms':None,'graph_closed':closed,'neutral_states_reached':len(seen),'dual_weight':dual,'terminal_gaps':gaps}

def compile_certificate(raw,word_budget=8):
    start=time.monotonic();stats={'new_nodes_expanded':0,'neutral_edge_checks':0,'new_exact_bases_tested':0,'new_lp_upper_work':0}
    try:
        d,raw=canon(raw);C,Ls,wr=LEGACY['linkage_classes']([(y,z) for y,z,k in raw])
        if not wr:return {'status':'UNKNOWN','reason':'raw list is not weakly reversible'}
        M=[max(y[i] for y in C) for i in range(d)]
        if d>4 or len(C)>8 or len(raw)>12 or max(M)>8:raise Budget('prototype dimension/complex/coordinate budget')
        if word_budget is not None and (type(word_budget) is not int or not 1<=word_budget<=64):raise Budget('invalid prototype shortest-word budget')
        if any(max(k.numerator.bit_length(),k.denominator.bit_length())>65536 for y,z,k in raw):raise Budget('input rational bit budget')
        paths=rawpaths(C,raw);diam=max(map(len,paths.values()))
        if word_budget is not None and diam>word_budget:raise Budget('word budget below ordinary raw graph diameter')
        base=LEGACY['compile_cones']([(y,z) for y,z,k in raw]);stats['inherited_exact_bases_tested']=base['exact_basis_candidates_tested']
        records=[];exclusions=[]
        for bits in range(1,2**d):
            I=[i for i in range(d) if bits>>i&1];O=[i for i in range(d) if i not in I]
            rows=[r for r in base['records'] if r['I']==I]
            if len(rows)==1 and not rows[0]['admissible']:
                exclusions.append({'I':I,'invariant':rows[0]['excluding_invariant']});continue
            for li,L in enumerate(Ls):
                inherited=next(r for r in rows if r['linkage']==li)
                if inherited['accepted']:
                    records.append({'I':I,'linkage':li,'mode':'inherited_all_profiles','terms':inherited['certificate']});continue
                profiles=(prod(M[i]+1 for i in O))*len(L)
                if profiles>5000:raise Budget('outside profile/mark coverage budget')
                for b in profs(O,M):
                    profile=encode_profile(O,b,M)
                    for t in L:
                        ans=search_row(t,I,profile,M,C,raw,word_budget,stats)
                        if ans['terms'] is None:
                            return {'status':'UNKNOWN_SUFFICIENT_RULE','reason':'no cone in the finite neutral-source search',
                                    'raw_sha256':rawdigest(raw),'failed_face':I,'initial_mark':t,'profile':profile,
                                    'refusal':ans,'costs':stats,'elapsed_seconds':time.monotonic()-start,
                                    'not_claimed':'recurrence failure; a closed graph only certifies failure of this neutral grammar'}
                        records.append({'I':I,'linkage':li,'mode':'neutral_profile','initial_mark':t,'profile':profile,'terms':ans['terms']})
        h=max([diam]+[len(term['word']) for row in records if row['mode']=='neutral_profile' for term in row['terms']])
        outgoing=defaultdict(F)
        for y,z,k in raw:outgoing[y]+=k
        ratio=max(outgoing.values())/min(outgoing.values());q0=min(k for y,z,k in raw)/max(outgoing.values())
        cert={'status':'ADMITTED_NEUTRAL_CLOSURE','raw_sha256':rawdigest(raw),'dimension':d,
              'raw':[(y,z,str(k)) for y,z,k in raw],'complexes':C,'linkages':Ls,'M':M,'maximum_designated_edges':h,
              'ordinary_paths':[{'from':a,'to':b,'word':w} for (a,b),w in sorted(paths.items())],
              'excluded_faces':exclusions,'coverage':records,'costs':stats,'elapsed_seconds':time.monotonic()-start,
              'predecessor_whole_cone_accepted':base['accepted'],'shortest_word_resource_budget':word_budget,
              'scope':'Raw finite sufficient certificate and exact statewise selector, same-principal author extension; no independent audit or novelty claim.',
              'consequence':'Classwise nonexplosion/positive recurrence; some fractional-factorial stationary genuine-activity moment and positive exponential physical-return moment on nonabsorbing classes. Absorbing singletons are separate elementary cases.',
              'scalar_recipe':{'m':len(C),'R_exact':str(ratio),'q0_exact':str(q0),'h':h,'kappa_min_exact':str(min(k for y,z,k in raw)),
                    'real_recursion':'L0=1; L(j+1)=q0^(-1)*exp(log(m*R)+2*Lj), j=0,...,h-1',
                    'alpha':'1/(4*Lh)','eta':'alpha','beta_physical_factorial_moment':'alpha/2',
                    'terminal_threshold':'(m*R)^(-1)*2^(-1/alpha)',
                    'physical_contract':'W=(product residual factorials)^alpha; F=(1+q)*W; C=[(h+1)*(1+1/kappa_min)+1]/alpha; U=C*W outside the proved finite head and zero inside; E[integral F+U(actual output)]<=U(input)-1'},
              'numerical_scalar_exponent':'NOT_MATERIALIZED; defined by proved finite real recursion',
              'finite_head_radius':'NOT_ACQUIRED; finite by proved complete raw face coverage',
              'numerical_stationary_normalizer':'NOT_ACQUIRED','unrestricted_weak_reversibility':'NOT_ACHIEVED'}
        if not verify_certificate(raw,cert):raise AssertionError('new complete certificate failed exact verifier')
        return cert
    except Budget as e:return {'status':'REFUSED_BUDGET','reason':str(e),'costs':stats,'elapsed_seconds':time.monotonic()-start,'recurrence':'UNKNOWN'}

def verify_certificate(raw,cert):
    try:
        d,raw=canon(raw)
        if cert.get('status')!='ADMITTED_NEUTRAL_CLOSURE' or cert['raw_sha256']!=rawdigest(raw):return False
        bound_raw=[(tuple(y),tuple(z),F(k)) for y,z,k in cert['raw']]
        if bound_raw!=raw or cert['dimension']!=d:return False
        C,Ls,wr=LEGACY['linkage_classes']([(y,z) for y,z,k in raw]);M=[max(y[i] for y in C) for i in range(d)]
        if not wr or list(map(tuple,cert['complexes']))!=C or cert['M']!=M:return False
        if [[tuple(t) for t in L] for L in cert['linkages']]!=Ls:return False
        paths={(tuple(r['from']),tuple(r['to'])):r['word'] for r in cert['ordinary_paths']};h=cert['maximum_designated_edges']
        if type(h) is not int or h<1:return False
        expected_paths={(a,b) for L in Ls for a in L for b in L}
        if set(paths)!=expected_paths or len(paths)!=len(cert['ordinary_paths']):return False
        valid_faces={tuple(i for i in range(d) if bits>>i&1) for bits in range(1,2**d)}
        excluded_keys=[tuple(r['I']) for r in cert['excluded_faces']]
        if len(set(excluded_keys))!=len(excluded_keys) or any(I not in valid_faces for I in excluded_keys):return False
        for row in cert['coverage']:
            if tuple(row['I']) not in valid_faces or tuple(row['I']) in excluded_keys:return False
            if type(row['linkage']) is not int or not 0<=row['linkage']<len(Ls):return False
            if row['mode'] not in ['inherited_all_profiles','neutral_profile']:return False
        def check_path(t,c):
            word=paths.get((tuple(t),tuple(c)))
            if word is None or len(word)>h:return False
            mark=tuple(t)
            for j in word:
                if type(j) is not int or not 0<=j<len(raw):return False
                s,u,k=raw[j]
                if s!=mark:return False
                mark=u
            return mark==tuple(c)
        if any(not check_path(a,b) for a,b in expected_paths):return False
        for bits in range(1,2**d):
            I=[i for i in range(d) if bits>>i&1];O=[i for i in range(d) if i not in I]
            excluded=[r for r in cert['excluded_faces'] if r['I']==I]
            if excluded:
                if len(excluded)!=1:return False
                ell=list(map(F,excluded[0]['invariant']))
                if len(ell)!=d or any(sum(ell[i]*(z[i]-y[i]) for i in range(d)) for y,z,k in raw):return False
                if any(ell[i]<0 for i in I) or sum(ell[i] for i in I)<=0:return False
                continue
            for li,L in enumerate(Ls):
                rows=[r for r in cert['coverage'] if r['I']==I and r['linkage']==li]
                inherited=[r for r in rows if r['mode']=='inherited_all_profiles']
                if inherited:
                    if len(rows)!=1:return False
                    gain=[F(0)]*len(I)
                    for term in inherited[0]['terms']:
                        a,t=tuple(term['source']),tuple(term['terminal']);weight=F(term['weight'])
                        if a not in C or t not in L or weight<0 or any(a[i]>t[i] for i in O):return False
                        if any(not check_path(t0,t) for t0 in L):return False
                        gain=[g+weight*(a[i]-t[i]) for g,i in zip(gain,I)]
                    if min(gain)<1:return False
                    continue
                expected={(tuple(t),profile_key(encode_profile(O,b,M))) for b in profs(O,M) for t in L}
                actual={(tuple(r['initial_mark']),profile_key(r['profile'])) for r in rows}
                if actual!=expected or len(rows)!=len(expected):return False
                for row in rows:
                    t=tuple(row['initial_mark']);profile=row['profile'];gain=[F(0)]*len(I)
                    for term in row['terms']:
                        node=make_node(t,profile);word=term['word'];weight=F(term['weight'])
                        if weight<0 or len(word)>h:return False
                        for j in word:
                            if type(j) is not int or not 0<=j<len(raw):return False
                            node=neutral_step(node,j,I,profile,raw)
                            if node is None:return False
                        a=tuple(term['competing_source']);mark=node[0]
                        if a not in C or not source_available(node,a,profile):return False
                        if tuple(term['terminal_mark'])!=mark:return False
                        gain=[g+weight*(a[i]-mark[i]) for g,i in zip(gain,I)]
                    if min(gain)<1:return False
        return True
    except (KeyError,ValueError,TypeError,IndexError,ZeroDivisionError):return False

def select(cert,x,t):
    raw=[(tuple(y),tuple(z),F(k)) for y,z,k in cert['raw']];x=tuple(x);t=tuple(t)
    if len(x)!=cert['dimension'] or any(type(a) is not int or a<0 for a in x) or any(a<b for a,b in zip(x,t)):raise ValueError('invalid actual marked launch')
    C={tuple(c) for c in cert['complexes']}
    if t not in C:raise ValueError('mark is not a raw complex')
    z=tuple(a-b for a,b in zip(x,t));words={tuple(p['word']) for p in cert['ordinary_paths'] if tuple(p['from'])==t}
    for row in cert['coverage']:
        if row['mode']=='neutral_profile' and tuple(row['initial_mark'])==t and profile_matches(row['profile'],z):
            words.update(tuple(term['word']) for term in row['terms'])
    outgoing=defaultdict(F)
    for y,u,k in raw:outgoing[y]+=k
    options=[]
    for word in words:
        state=x;mark=t;prefix=[]
        for j in word:
            s,u,k=raw[j];a=falling(state,s);b=falling(state,mark)
            if not a or a!=b:raise AssertionError('certificate candidate is not an actual neutral source word')
            prefix.append({'population':state,'carried_mark':mark,'channel':j,'selected_source':s,'equal_falling_factor':str(a)})
            state=tuple(v-a+b for v,a,b in zip(state,s,u));mark=u
        q=sum(k*falling(state,y) for y,u,k in raw);pt=outgoing[mark]*falling(state,mark)/q
        options.append((pt,len(word),word,state,mark,prefix))
    pt,depth,word,state,mark,prefix=min(options,key=lambda v:(v[0],v[1],v[2]))
    return {'input_population':x,'actual_initial_mark':t,'residual':z,'candidate_count':len(options),
            'selected_designated_word':word,'actual_designated_prefixes':prefix,
            'terminal_population_before_ordinary_jump':state,'terminal_actual_mark':mark,
            'terminal_actual_mark_probability':str(pt),'maximum_genuine_jumps':depth+1,
            'stopping_rule':'Stop immediately after any unexpected channel; otherwise take one ordinary genuine jump at the terminal and stop at its actual new mark.',
            'selector_requires_head_or_scalar_exponent':False}

def overlap():
    C=[(0,0,0),(1,1,0),(2,1,1),(3,2,2)];raw=[]
    for i,y in enumerate(C):raw.append((tuple(y)+(0,),tuple(C[(i+1)%4])+(0,),F(2 if i==3 else 1)))
    for i,y in enumerate(C):raw.append(((0,)+tuple(y),(0,)+tuple(C[(i+1)%4]),F(3 if i==3 else 1)))
    return raw

if __name__=='__main__':
    raw=overlap();cert=compile_certificate(raw);assert cert['status']=='ADMITTED_NEUTRAL_CLOSURE'
    (P/'results/neutral_source_overlap_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
    inputs=[((0,1000,0,0),(0,0,0,0)),((0,10**100,0,0),(0,0,0,0)),
            ((0,1001,1,0),(0,1,1,0)),((3,1002,2,0),(3,2,2,0)),
            ((10**20,0,0,0),(0,0,0,0)),((0,0,10**20,0),(0,0,0,0)),
            ((0,0,0,10**20),(0,0,0,0)),((10**10,10**10,10**10,10**10),(0,0,0,0))]
    selections=[select(cert,x,t) for x,t in inputs]
    (P/'results/neutral_source_selections.json').write_text(json.dumps(selections,indent=2)+'\n')
    tampered=json.loads(json.dumps(cert));first=next(r for r in tampered['coverage'] if r['mode']=='neutral_profile');first['terms'][0]['weight']='0'
    assert not verify_certificate(raw,tampered)
    raw_tamper=json.loads(json.dumps(cert));raw_tamper['raw'][0][2]='99'
    assert not verify_certificate(raw,raw_tamper)
    path_tamper=json.loads(json.dumps(cert));path_tamper['ordinary_paths'][0]['word']=[-1]
    assert not verify_certificate(raw,path_tamper)
    from max_source_envelope import ordered
    refused=compile_certificate(ordered(3,[1,1,1,2]))
    assert refused['status']=='UNKNOWN_SUFFICIENT_RULE'
    (P/'results/neutral_source_controls.json').write_text(json.dumps({'weight_tamper_rejected':True,'raw_binding_tamper_rejected':True,'path_tamper_rejected':True,'ordered_stable_refusal':refused},indent=2)+'\n')
    counts={mode:sum(r['mode']==mode for r in cert['coverage']) for mode in ['inherited_all_profiles','neutral_profile']}
    print(json.dumps({'status':cert['status'],'coverage_rows':counts,'costs':cert['costs'],
                      'verified':verify_certificate(raw,cert),'selectors':len(selections),'maximum_selected_designated_length':max(len(s['selected_designated_word']) for s in selections),
                      'scalar_exponent':cert['numerical_scalar_exponent'],'head':cert['finite_head_radius'],
                      'negative_control':{'status':refused['status'],'face':refused['failed_face'],'closed_neutral_graph':refused['refusal']['graph_closed']}},indent=2))
