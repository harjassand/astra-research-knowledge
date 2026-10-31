#!/usr/bin/env python3
"""Sound-incomplete source-derived charge search for centered creation.
All supplied generator terms are verified, not only the proposing jump subset.
"""
import argparse, hashlib, importlib.util, itertools, json, math
from pathlib import Path
import sympy as S

HERE=Path(__file__).resolve().parent
RAWPATH=HERE.parent/'raw_local_operator_acquisition_20261031'/'acquire_operator_certificate.py'
RAW_SHA='35acdcdcc533f523cc78c558153f97fcb800711bbd4ff0f57b8a2ea50d60ee35'
if hashlib.sha256(RAWPATH.read_bytes()).hexdigest()!=RAW_SHA:raise RuntimeError('frozen raw component hash mismatch')
ms=importlib.util.spec_from_file_location('_frozen_raw_operator',RAWPATH)
raw=importlib.util.module_from_spec(ms);ms.loader.exec_module(raw)
FORMAT='source-derived-centered-certificate-v1'


def parse(spec):
    raw.exactkeys(spec,['format','operator_model','candidate_budget'])
    if type(spec['format']) is not str or spec['format']!=FORMAT:raise raw.InputError('centered format')
    raw.exactkeys(spec['candidate_budget'],['max_subset_size','max_subsets_per_cell','max_joint_candidates','max_lp_attempts'])
    for k,v in spec['candidate_budget'].items():raw.integer(v,1)
    if spec['candidate_budget']['max_subset_size']>8:raise raw.InputError('subset implementation limit')
    if any(v>10000 for k,v in spec['candidate_budget'].items() if k!='max_subset_size'):raise raw.InputError('candidate implementation limit')
    return raw.parse(spec['operator_model'])


def kernel_projector(dim,matrices):
    if not matrices:return S.eye(dim)
    basis=S.Matrix.vstack(*matrices).nullspace()
    if not basis:return S.zeros(dim)
    X=S.Matrix.hstack(*basis)
    P=raw.normalized_matrix(X*(X.H*X).inv()*X.H)
    if P!=P.H or raw.normalized_matrix(P*P)!=P:raise raw.InputError('projector arithmetic failure')
    if any(raw.normalized_matrix(L*P)!=S.zeros(dim) for L in matrices):raise raw.InputError('kernel arithmetic failure')
    return P


def catalog(spec,parsed=None):
    dims,Bs,terms,_,_,_=parsed or parse(spec)
    budget=spec['candidate_budget'];result=[];summary=[]
    for cell,dim in enumerate(dims):
        available=[]
        for ti,(e,H,js) in enumerate(terms):
            if e==[cell]:
                available.extend(((ti,ji),L) for ji,(rate,L) in enumerate(js) if rate>0)
        maxsize=min(len(available),budget['max_subset_size'])
        total=sum(math.comb(len(available),r) for r in range(maxsize+1))
        tested=0;retained=[];seen=set()
        stop=False
        for r in range(maxsize+1):
            for inds in itertools.combinations(range(len(available)),r):
                if tested>=budget['max_subsets_per_cell']:stop=True;break
                tested+=1;P=kernel_projector(dim,[available[j][1] for j in inds])
                if P==S.zeros(dim):continue
                if any(raw.normalized_matrix(P*B*P)!=S.zeros(dim) for B in Bs[cell]):continue
                encoded=raw.encmat(P);key=raw.canonical(encoded)
                if key in seen:continue
                seen.add(key);retained.append({'subset':[list(available[j][0]) for j in inds],'P':P,'Q':S.eye(dim)-P})
            if stop:break
        result.append(retained)
        summary.append({'positive_rate_one_cell_jumps':len(available),'possible_subsets_at_requested_size':total,
                        'subsets_checked':tested,'retained_projectors':len(retained),'subset_budget_truncated':tested<total,
                        'subset_size_cap':maxsize})
    return result,summary


def position(indices,sizes):
    z=0
    for i,n in zip(indices,sizes):z=z*n+i
    return z+1


def record_base(spec,parsed,cat,summary,indices):
    dims,_,_,_,_,norms=parsed
    chosen=[cc[i] for cc,i in zip(cat,indices)]
    return {'format':FORMAT,'external_input_sha256':raw.digest(spec),'task':spec['operator_model']['task'],
            'raw_component_sha256':RAW_SHA,'status':'CERTIFIED','reason':'EXACT_ALL_TERM_PSD_AND_CENTERED_COMPRESSION',
            'catalog_summary':summary,'selected_catalog_indices':list(indices),
            'candidate_position':position(indices,[len(x) for x in cat]),
            'proposals':[x['subset'] for x in chosen],
            'projectors':[{'P':raw.encmat(x['P']),'Q':raw.encmat(x['Q']),'transparent_rank':int(S.trace(x['P']))} for x in chosen],
            'coupling_norm_upper':[raw.encq(x) for x in norms], 'allocations':[],
            'scope':'Exact known finite-operator centered drift certificate; all generator terms checked; not a circuit or hardware admission.'}


def acquire(spec):
    parsed=parse(spec);dims,Bs,terms,gap,cap,norms=parsed
    cat,summary=catalog(spec,parsed)
    unknown={'format':FORMAT,'external_input_sha256':raw.digest(spec),'status':'UNKNOWN','catalog_summary':summary,
             'reason':'NO_CENTERED_SOURCE_DERIVED_CANDIDATE','joint_candidates_checked':0}
    if any(not x for x in cat):return unknown
    limit=min(spec['candidate_budget']['max_joint_candidates'],spec['candidate_budget']['max_lp_attempts'])
    for indices in itertools.islice(itertools.product(*(range(len(x)) for x in cat)),limit):
        unknown['joint_candidates_checked']+=1
        Qs=[x[j]['Q'] for x,j in zip(cat,indices)]
        lp=raw.build_lp(dims,Qs,terms,gap,cap)
        if lp is None:continue
        objective,constr,allocs,counts=lp;budget=spec['operator_model']['search_budget']
        if counts['lp_constraints']>budget['max_lp_constraints'] or counts['lp_variables']>budget['max_lp_variables']:continue
        try:_,sol=raw.budgeted_lp(objective,constr,budget['max_lp_seconds'])
        except (raw.InfeasibleLPError,raw.UnboundedLPError,raw.SearchLimit,ValueError,TypeError,ZeroDivisionError):continue
        rec=record_base(spec,parsed,cat,summary,indices);rec['lp_description']=counts
        for M,a in allocs:
            syms=set(M.free_symbols)|set().union(*(x.free_symbols for x in a))
            vals={s:sol.get(s,S.Integer(0)) for s in syms}
            rec['allocations'].append({'M':[[raw.encq(x) for x in row] for row in M.subs(vals).tolist()],
                                       'activation':[raw.encq(x.subs(vals)) for x in a]})
        if verify_certificate(spec,rec):return rec
    unknown['reason']='BOUNDED_SUFFICIENT_SEARCH_DID_NOT_CERTIFY'
    return unknown


def verified_parameters(spec,record):
    """Internal exact checker; raises on invalid certificates, returns M,a,P,Q."""
    parsed=parse(spec);dims,Bs,terms,gap,cap,norms=parsed;cat,summary=catalog(spec,parsed)
    if type(record) is not dict or record.get('status')!='CERTIFIED':raise raw.InputError('not certified')
    inds=record.get('selected_catalog_indices')
    if type(inds) is not list or len(inds)!=len(dims) or any(type(i) is not int or not 0<=i<len(c) for i,c in zip(inds,cat)):
        raise raw.InputError('candidate indices')
    expected=record_base(spec,parsed,cat,summary,inds)
    if set(record) not in (set(expected),set(expected)|{'lp_description'}):raise raw.InputError('certificate keys')
    for k,v in expected.items():
        if k!='allocations' and not raw.strict_equal(record[k],v):raise raw.InputError('bound certificate field')
    if expected['candidate_position']>min(spec['candidate_budget']['max_joint_candidates'],spec['candidate_budget']['max_lp_attempts']):
        raise raw.InputError('candidate outside declared budget')
    Qs=[c[i]['Q'] for c,i in zip(cat,inds)];Ps=[c[i]['P'] for c,i in zip(cat,inds)]
    # Catalog proves subset provenance and PBP=0; ALL actual terms below earn drift.
    als=record['allocations']
    if type(als) is not list or len(als)!=len(terms):raise raw.InputError('allocations')
    total=S.zeros(len(dims));aa=[S.Integer(0) for _ in dims]
    for term,al in zip(terms,als):
        raw.exactkeys(al,['M','activation']);e=term[0];m=len(e)
        if type(al['M']) is not list or len(al['M'])!=m or any(type(r) is not list or len(r)!=m for r in al['M']):raise raw.InputError('M shape')
        if type(al['activation']) is not list or len(al['activation'])!=m:raise raw.InputError('activation shape')
        M=S.Matrix([[raw.rat(v) for v in row] for row in al['M']]);a=[raw.rat(x) for x in al['activation']]
        if any(x<0 for x in a) or any(M[i,j]<0 for i in range(m) for j in range(m) if i!=j):raise raw.InputError('sign')
        if not all(raw.psd(A) for A in raw.local_coefficients(dims,Qs,term,M,a).values()):raise raw.InputError('local PSD')
        for i,gi in enumerate(e):
            aa[gi]+=a[i]
            for j,gj in enumerate(e):total[gi,gj]+=M[i,j]
    if any(aa[i]>cap or sum(total[i,j] for j in range(len(dims)))>-gap or sum(total[j,i] for j in range(len(dims)))>-gap for i in range(len(dims))):
        raise raw.InputError('global margins')
    if 'lp_description' in record:
        lp=raw.build_lp(dims,Qs,terms,gap,cap)
        if lp is None or not raw.strict_equal(record['lp_description'],lp[3]):raise raw.InputError('LP description')
    return parsed,total,aa,Ps,Qs


def verify_certificate(external_spec,record):
    try:verified_parameters(external_spec,record);return True
    except (raw.InputError,ValueError,TypeError,KeyError,IndexError,AttributeError,ZeroDivisionError):return False


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('--verify');p.add_argument('--output');args=p.parse_args()
    try:
        spec=raw.load(Path(args.input).read_text())
        if args.verify:
            ok=verify_certificate(spec,raw.load(Path(args.verify).read_text()));print(json.dumps({'verified':ok}));return 0 if ok else 1
        out=acquire(spec);txt=json.dumps(out,sort_keys=True,indent=2)+'\n'
        if args.output:Path(args.output).write_text(txt)
        else:print(txt,end='')
        return 0 if out['status']=='CERTIFIED' else 1
    except (raw.InputError,ValueError,OSError) as exc:
        print(json.dumps({'status':'REJECTED','reason':str(exc)}));return 2
if __name__=='__main__':raise SystemExit(main())
