"""Compile an explicit flag-conditioned qubit Hamiltonian to degree three.

The exact term/graph construction uses the preserved damped subdivision
and fork recipes. Example scales are illustrative, not phase-qualified.
The independent quantum check verifies the flag-number symmetry of a
four-to-three subdivision and its analytical frame.
"""
from __future__ import annotations
from collections import Counter
import hashlib,json,sys
from pathlib import Path
import numpy as np
import sympy as s
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/latched_gate_20261101'
sys.path.insert(0,str(ROOT/'work/arity_transfer_20261101'))
from degree_compiler_controls import Build,encode
from pauli_tree_compiler import compile_terms

def conditional(h,p,site,flag):
    axis=p[site];partner=1-site
    if (site==0 and axis=='Z') or (site==1 and axis=='X'):return [(h,p)]
    other='X' if site==0 else 'Z'
    assert partner not in p and flag not in p
    return [(h/2,p.copy()),(h/2,{**p,flag:'Z'}),
            (h/2,{**p,partner:other}),(-h/2,{**p,partner:other,flag:'Z'})]

def main():
    flag=8;roots=[]
    for site in (0,1):
        for axis_id,axis in enumerate('XYZ'):
            port=2+3*site+axis_id
            roots+=conditional(s.Rational(1,2+port),{site:axis,port:'X'},site,flag)
            roots+=conditional(s.Rational(1,17+port),{site:axis},site,flag)
    roots += [(s.Rational(1,11),{2:'X',3:'X',4:'X'}),
              (s.Rational(-1,13),{5:'X',6:'X',7:'X'}),
              (s.Rational(-1,2),{flag:'Z'})]
    assert max(len(p) for _,p in roots)==4
    arity,records,total,layers=compile_terms(roots,9,[s.Integer(2)**20],[s.Integer(16)])
    assert layers==1
    fields=[(h,p) for h,p in arity if len(p)==1]
    couplings=[(h,p) for h,p in arity if len(p)>1]
    b=Build(total);terms=[]
    for h,p in couplings:
        current=(h,p.copy())
        for stage,q in enumerate(sorted(p)):
            val,tail=current
            endpoint,current=b.subdivide(val,{q:tail[q]},{j:r for j,r in tail.items() if j!=q},stage,'old_site_port')
            terms.append(endpoint)
        terms.append(current)
    rounds=0
    while True:
        groups={}
        for i,(h,p) in enumerate(terms):
            old=[q for q in p if q<b.old]
            if old:
                assert len(old)==1 and len(p)==2
                q=old[0];port=next(j for j in p if j!=q)
                groups.setdefault((q,p[q]),[]).append((i,h,port))
        pairs=[(key,edges[j],edges[j+1]) for key,edges in groups.items() for j in range(0,len(edges)-1,2)]
        if not pairs:break
        removed=set();added=[]
        for (q,p),first,second in pairs:
            fresh=[]
            for index,h,port in (first,second):
                removed.add(index)
                endpoint,other=b.subdivide(h,{q:p},{port:'X'},3+2*rounds,'fresh_fork_port')
                val,ep=endpoint;u=next(j for j in ep if j!=q)
                fresh.append((val,u));added.append(other)
            (aa,u),(bb,v)=fresh;f,gap=b.mediator(4+2*rounds,'fork');scale=s.sqrt(gap/2)
            added += [(scale,{q:p,f:'X'}),(-aa*scale,{u:'X',f:'X'}),
                      (-bb*scale,{v:'X',f:'X'}),(aa*bb,{u:'X',v:'X'})]
        terms=[t for j,t in enumerate(terms) if j not in removed]+added;rounds+=1
    inc=Counter();neighbors={q:set() for q in range(b.next)}
    for _,p in terms:
        assert 2<=len(p)<=3
        if len(p)==3:assert all(q>=b.old and ax=='X' for q,ax in p.items())
        if flag in p:assert p[flag]=='Z'
        for q in p:inc[q]+=1;neighbors[q].update(j for j in p if j!=q)
    assert max(inc.values())<=3 and max(map(len,neighbors.values()))<=3
    assert inc[flag]==1
    assert all(p.get(flag,'Z')=='Z' for _,p in fields+b.fields)
    # Full quantum normal-form check, DATA A,B, flag F, controller C, new M.
    ii=np.eye(2,dtype=complex);xx=np.array([[0,1],[1,0]],complex)
    yy=np.array([[0,-1j],[1j,0]],complex);zz=np.diag([1,-1]).astype(complex)
    def ten(*args):
        a=np.ones((1,1),complex)
        for v in args:a=np.kron(a,v)
        return a
    nf=ten(ii,ii,(ii-zz)/2,ii,ii);nm=ten(ii,ii,ii,ii,(ii-zz)/2)
    aa=ten(xx,xx,ii,ii);bb=ten(ii,ii,zz,xx)
    kk=(aa-bb)/np.sqrt(2);gg=ten(kk,yy);vv=ten(kk,xx)
    eps=.03125;r=expm(-1j*eps*gg);hh=nm/eps**2+vv/eps
    symmetry=float(np.linalg.norm(r@nf-nf@r,2))
    hsym=float(np.linalg.norm(hh@nf-nf@hh,2))
    assert symmetry<1e-13 and hsym<1e-13
    # Conjugating the ORIGINAL flag loss is not omitted: it is a paid
    # local perturbation after the compiler, never a noiseless free bath.
    loss=ten(ii,ii,np.array([[0,1],[0,0]],complex),ii,ii)
    dressed_loss_difference=float(np.linalg.norm(r@loss@r.conj().T-loss,2))
    assert dressed_loss_difference>1e-4
    paths=[Path(__file__),ROOT/'work/arity_transfer_20261101/degree_compiler_controls.py',
           ROOT/'work/arity_transfer_20261101/pauli_tree_compiler.py']
    out={'scope':'exact illustrative construction and finite symmetry algebra, not qualified phase scales',
         'target_qubits':9,'flag_id':flag,'target_H_arity':4,'target':encode(roots),
         'physical_qubits':b.next,'physical_couplings':encode(terms),
         'one_body_fields':encode(fields+b.fields),'initial_subdivision_mediators':records,
         'additional_mediators':b.records,'pairing_rounds':rounds,
         'maximum_H_arity':max(len(p) for _,p in terms),'maximum_coupling_count':max(inc.values()),
         'maximum_graph_degree':max(map(len,neighbors.values())),'flag_coupling_count':inc[flag],
         'all_flag_axes_are_Z':True,'nominal_losses_one_body':True,
         'new_frame_flag_number_commutator':symmetry,'physical_H_flag_number_commutator':hsym,
         'dressed_flag_loss_operator_difference':dressed_loss_difference,
         'program_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'compiler_flag_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({key:val for key,val in out.items() if key not in ('target','physical_couplings','one_body_fields','initial_subdivision_mediators','additional_mediators')},indent=2))
if __name__=='__main__':main()
