"""Exact unrestricted35-coefficient /10-selector norm-support interfaces.
Stdlib only. This compiles a sufficient SDP, not a general PC/QC decision.
Executed levels0/1 are checked against the acquired dual/positive instance.
"""
from verify_dual import plus,times,scale,dx,var,invariants,energy,Q
from itertools import combinations_with_replacement as cw
from pathlib import Path
import json,argparse,time
ROOT=Path(__file__).resolve().parent
ONE={(0,)*8:Q(1)}
def multiply(items):
    p=ONE
    for item in items:p=times(p,item)
    return p
def compile_level(coefficients,level):
    if level<0:raise ValueError('nonnegative level required')
    a=[var(i) for i in range(4)];x=[var(i+4) for i in range(4)]
    f={tuple(e)+(0,)*4:Q(c) for e,c in coefficients.items() if Q(c)}
    if not all(len(e)==8 and sum(e)==4 and all(v>=0 for v in e) for e in f):raise ValueError('homogeneous quartic entries required')
    shifted=[plus(ai,xi) for ai,xi in zip(a,x)];shifted_f={}
    for e,c in f.items():shifted_f=plus(shifted_f,scale(multiply(shifted[i] for i in range(4) for _ in range(e[i])),c))
    breg=plus(shifted_f,scale(f,-1),*(scale(times(dx(f,i),x[i]),-1) for i in range(4)))
    sigma=plus(*(times(t,t) for t in x));weight=multiply([sigma]*level)
    target=times(weight,breg)
    zs=[times(ai,multiply(x[i] for i in indices)) for ai in a for indices in cw(range(4),level+1)]
    zs += [multiply(x[i] for i in indices) for indices in cw(range(4),level+2)]
    terms=[];rows={}
    for i in range(len(zs)):
        for j in range(i,len(zs)):
            product=times(zs[i],zs[j]);[(e,c)]=product.items();assert c==1
            terms.append((i,j));rows.setdefault(e,[]).append((len(terms)-1,1 if i==j else 2))
    selector_pairs=list(cw(range(4),2));qx=invariants(x)[3]
    for j,(s,t) in enumerate(selector_pairs):
        p=times(weight,times(times(a[s],a[t]),qx))
        for e,c in p.items():rows[e].append((len(terms)+j,c))
    monoms=sorted(rows)
    return {'status':'EXACT_NORM_SUPPORT_SDP_INTERFACE_NOT_A_DECISION',
      'level':level,'features':len(zs),'constraints':len(monoms),
      'homogeneous_quartic':[{'exponent':list(e),'coefficient':str(c)} for e,c in sorted(coefficients.items())],
      'selector_pairs':[list(pair) for pair in selector_pairs],
      'gram_upper_pairs':[list(pair) for pair in terms],
      'rows':[{'exponent':list(e),'entries':[[j,str(c)] for j,c in rows[e]],'rhs':str(target.get(e,0))} for e in monoms],
      'scope':'Unrestricted quadratic selector and symmetric PSD Gram; no invariance restriction. Strict-support completeness and its limitations are in HIERARCHY_PROOF.md.'}
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--level',type=int,default=1)
    parser.add_argument('--input');parser.add_argument('--output');args=parser.parse_args();start=time.monotonic()
    if args.input:
        source=json.loads(Path(args.input).read_text());coefficients={tuple(t['exponent']):Q(t['coefficient']) for t in source}
    else:coefficients={e[:4]:c for e,c in energy([var(i) for i in range(4)]).items()}
    data=compile_level(coefficients,args.level)
    acquired='NOT_CHECKED_OTHER_INPUT_OR_LEVEL'
    if not args.input and args.level==1:
        positive=json.loads((ROOT.parent/'quartic_alternative/sector_gap/EXACT_MULTIPLIER_SUPPORT.json').read_text())
        matrix=[list(map(Q,row)) for row in positive['gram']]
        a=[var(i) for i in range(4)];u,v,w,q=invariants(a)
        k=plus(scale(plus(u,scale(v,-1)),Q(positive['alpha'])),scale(q,Q(positive['delta'])))
        selectors=[]
        for s,t in data['selector_pairs']:
            [(e,c)]=times(a[s],a[t]).items();selectors.append(k.get(e,Q(0)))
        values=[matrix[i][j] for i,j in data['gram_upper_pairs']]+selectors
        assert all(sum((Q(c)*values[j] for j,c in row['entries']),Q(0))==Q(row['rhs']) for row in data['rows'])
        acquired='ALL_UNRESTRICTED_LEVEL1_AFFINE_EQUATIONS_PASS'
    if args.output:Path(args.output).write_text(json.dumps(data,separators=(',',':'))+'\n')
    print(json.dumps({'level':data['level'],'features':data['features'],'constraints':data['constraints'],
      'selector_coefficients':10,'gram_variables':len(data['gram_upper_pairs']),
      'acquired_instance':acquired,'seconds':time.monotonic()-start,
      'scope':data['scope']},indent=2))
if __name__=='__main__':main()
