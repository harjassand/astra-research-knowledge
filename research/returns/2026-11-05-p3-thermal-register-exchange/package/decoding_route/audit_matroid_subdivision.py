"""Independent RX square-grid and cylinder construction, with no BDL code import."""
import json
from pathlib import Path

def rank(vectors):
    piv={}
    for v in vectors:
        while v:
            k=v.bit_length()-1
            if k in piv: v^=piv[k]
            else: piv[k]=v; break
    return len(piv)

def build(s):
    checks={}; groups={}; qubits={}; incidence=[]
    def c(label,group):
        if label not in checks: checks[label]=len(checks); groups[label]=group
        return label
    def attach(check,edges):
        for e in edges:
            if e not in qubits: qubits[e]=len(qubits)
            incidence.append((check,e))
    def h(x,b,i,j): return ('x',x,'h',b,i,j)
    def v(x,b,i,j): return ('x',x,'v',b,i,j)
    def br(x,i,j): return ('x',x,'bridge',i,j)
    pairs=[(0,1),(1,2)]
    for x,(qa,qb) in enumerate(pairs):
        for b in (0,1):
            for i in range(s):
                for j in range(s):
                    z=c(('face',x,b,i,j),4*x+b)
                    attach(z,[h(x,b,i,j),v(x,b,i+1,j),h(x,b,i,j+1),v(x,b,i,j)])
        for which,q in enumerate([qa,qb]):
            for t in range(s):
                z=c(('side',x,q,t),4*x+2+which)
                if which==0: attach(z,[v(x,0,s,t),v(x,1,s,t),br(x,s,t),br(x,s,t+1)])
                else: attach(z,[h(x,0,t,s),h(x,1,t,s),br(x,t,s),br(x,t+1,s)])
    for q in range(3):
        for b in (0,1):
            for t in range(s):
                z=c(('qedge',q,b,t),8+3*q+b)
                attach(z,[('qvertex',q,b,t),('qvertex',q,b,t+1)])
                for x,pair in enumerate(pairs):
                    if q==pair[0]: attach(z,[v(x,b,s,t)])
                    if q==pair[1]: attach(z,[h(x,b,t,s)])
        z=c(('qbridge',q),8+3*q+2)
        attach(z,[('qvertex',q,0,s),('qvertex',q,1,s)])
        for x,pair in enumerate(pairs):
            if q in pair: attach(z,[br(x,s,s)])
    for b in (0,1):
        z=c(('zpoint',b),17+b)
        attach(z,[('qvertex',q,b,s) for q in range(3)])
    r=len(checks)
    cols=[1<<j for j in range(r)]+[0]*len(qubits)
    for z,e in incidence: cols[r+qubits[e]]^=1<<checks[z]
    group=[None]*r; rep=[None]*19
    for z,j in checks.items():
        group[j]=groups[z]
        if rep[group[j]] is None: rep[group[j]]=j
    contract=[]
    # Dual grid tree: join all cells horizontally, then join rows in one column.
    for x in range(2):
        for b in (0,1):
            for i in range(1,s):
                for j in range(s): contract.append(r+qubits[v(x,b,i,j)])
            for j in range(1,s): contract.append(r+qubits[h(x,b,0,j)])
        for t in range(1,s):
            contract.extend([r+qubits[br(x,s,t)],r+qubits[br(x,t,s)]])
    for q in range(3):
        for b in (0,1):
            for t in range(1,s): contract.append(r+qubits[('qvertex',q,b,t)])
    # Coarse qubit representatives in the exact order of the 53-element cert.
    for x in range(2):
        for kind in ('bottom','right','left','top'):
            for b in (0,1):
                e={'bottom':h(x,b,0,0),'right':v(x,b,s,0),
                   'left':v(x,b,0,0),'top':h(x,b,0,s)}[kind]
                rep.append(r+qubits[e])
        rep.extend(r+qubits[e] for e in [br(x,s,0),br(x,0,s),br(x,s,s)])
    for q in range(3):
        rep.extend(r+qubits[('qvertex',q,b,t)] for t in (0,s) for b in (0,1))
    def project(value):
        out=0
        while value:
            low=value&-value; out^=1<<group[low.bit_length()-1]; value^=low
        return out
    assert len(rep)==53 and len(contract)==r-19
    assert rank([cols[j] for j in contract])==r-19
    assert all(project(cols[j])==0 for j in contract)
    return r,cols,contract,rep,[project(cols[j]) for j in rep],group

def main():
    cert=json.loads((Path(__file__).resolve().parents[1]/'sampler_route'/'two_square_fano.json').read_text())
    psmall=[int(x,16) for x in cert['projection_rows_hex']]
    canonical=None; results=[]
    for s in (1,2,3,4):
        r,cols,c0,rep,coarse,groups=build(s)
        if canonical is None: canonical=coarse
        assert coarse==canonical
        contract=c0+[rep[i] for i in cert['contract']]
        retain=[rep[i] for i in cert['retain']]
        prows=[sum(((p>>g)&1)<<j for j,g in enumerate(groups)) for p in psmall]
        assert rank(prows)==3
        assert rank([cols[j] for j in contract])==r-3
        assert all((p&cols[j]).bit_count()%2==0 for p in prows for j in contract)
        image=[sum(((p&cols[j]).bit_count()%2)<<i for i,p in enumerate(prows)) for j in retain]
        assert image==list(range(1,8)) and not set(contract)&set(retain)
        results.append({'ell':2*s+1,'check_rows':r,'augmented_columns':len(cols),
                        'coarsening_contraction_rank':len(c0),
                        'full_contraction_rank':r-3,'Fano_images':image})
    Path(__file__).with_name('matroid_subdivision_audit.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
if __name__=='__main__': main()
