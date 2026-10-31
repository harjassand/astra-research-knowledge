"""Construct explicit three-body Pauli/loss term lists by subdivision.

Rates must be qualified by the transfer inequalities for an intended
protected phase. The example scales below are illustrative, not a
qualified Tanner device or useful error threshold.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/arity_transfer_20261101'


def compile_terms(terms,qubits,omega,loss):
    """Each term is (real coefficient, {qubit_id: X/Y/Z})."""
    pending=list(terms);retained=[];records=[];next_id=qubits;layer=0
    while any(len(p)>3 for _,p in pending):
        new=[]
        for h,p in pending:
            if len(p)<=3:
                retained.append((h,p));continue
            ids=sorted(p);cut=(len(ids)+1)//2
            aa={j:p[j] for j in ids[:cut]};bb={j:p[j] for j in ids[cut:]}
            med=next_id;next_id+=1
            sign=-s.sign(h);coupling=s.sqrt(abs(h)*omega[layer]/2)
            # The omitted Omega/2 scalar has no generator action.
            retained.append((-omega[layer]/2,{med:'Z'}))
            aa[med]='X';bb[med]='X'
            new.extend([(coupling,aa),(sign*coupling,bb)])
            records.append({'id':med,'layer':layer,'gap':str(omega[layer]),'loss_rate':str(loss[layer]),
                            'parent_coefficient':str(h),'parent_weight':len(p),'coupler_strength':str(coupling)})
        pending=new;layer+=1
    retained.extend(pending)
    assert max((len(p) for _,p in retained),default=0)<=3
    return retained,records,next_id,layer


def serial(terms):
    return [{'coefficient':str(h),'pauli':{str(k):v for k,v in p.items()}} for h,p in terms]


def main():
    # Matches finite_generator_controls.py at loss=1024 and eps=2^-18.
    terms=[(s.Rational(5,1000),{j:'X' for j in range(4)}),
           (-s.Rational(3,1000),{0:'Z',1:'X',2:'X',3:'X'})]
    output,records,total,layers=compile_terms(terms,4,[s.Integer(2)**36],[s.Integer(1024)])
    assert len(records)==2 and total==6 and layers==1
    # Independent finite structural checks through weight 16, using exact
    # symbolic coefficients. These check the resource construction, not
    # effective dynamics or the asymptotic phase.
    counts=[]
    for weight in range(4,17):
        target={j:'XYZ'[j%3] for j in range(weight)}
        om=[s.Integer(2)**(20*(j+1)) for j in range(8)]
        gam=[s.Integer(2)**(5*(j+1)) for j in range(8)]
        compiled,meds,_,depth=compile_terms([(s.Rational(1,7),target)],weight,om,gam)
        leaves=[p for _,p in compiled if len(p)>1]
        assert len(meds)==weight-3 and len(leaves)==weight-2
        assert all(sum(q in p for p in leaves)==1 for q in range(weight))
        assert all(sum(m['id'] in p for p in leaves)==2 for m in meds)
        assert depth==(weight-3).bit_length()
        counts.append({'target_weight':weight,'mediators':len(meds),'three_body_couplers':len(leaves),'layers':depth})
    out={'example_target':serial(terms),'physical_H_terms':serial(output),
         'original_single_qubit_losses':[{'id':j,'rate':'1'} for j in range(4)],
         'mediators':records,'physical_qubits':total,'max_H_arity':3,'new_loss_arity':1,
         'tree_resource_checks':counts,'matches_finite_generator_fixture':True,
         'scale_scope':'Explicit finite fixture scales; not certified Tanner-family parameters',
         'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    OUT.mkdir(parents=True,exist_ok=True);path=OUT/'physical_construction.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'output':str(path),'passed':True,'tree_weight_range':[4,16],
                     'example_physical_H_terms':len(output),'example_mediators':len(records)}))


if __name__=='__main__':main()
