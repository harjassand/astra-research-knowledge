"""Compress a canonical finite covariance catalogue without increasing cost.

At most 9+8=17 atoms remain (often fewer in a restricted covariance
subspace). This algebraic operation does not optimize ray positions.
The stronger optimal-closed bound 16 uses the global dual contact set.
"""
from pathlib import Path
from fractions import Fraction as R
import argparse,json,sys
from verify_closed import prepare,verify
from receive import b,ca,dot,quadratic

def nullvector(A):
    rows=[list(row) for row in A];n=len(rows);m=len(rows[0]);pivot=0;pivots=[]
    for j in range(m):
        k=next((i for i in range(pivot,n) if rows[i][j]),None)
        if k is None:continue
        rows[pivot],rows[k]=rows[k],rows[pivot];p=rows[pivot][j];rows[pivot]=[v/p for v in rows[pivot]]
        for i in range(n):
            if i!=pivot and rows[i][j]:
                co=rows[i][j];rows[i]=[x-co*y for x,y in zip(rows[i],rows[pivot])]
        pivots.append(j);pivot+=1
        if pivot==n:break
    free=next((j for j in range(m) if j not in pivots),None)
    if free is None:return None,pivot
    out=[R(0)]*m;out[free]=1
    for i,j in enumerate(pivots):out[j]=-rows[i][free]
    assert all(dot(row,out)==0 for row in A)
    return out,pivot

def compress(payload):
    op=prepare(payload);weights=op['weights'][:];z=op['multiplier'][4:];covpairs=[(i,j) for i in range(4) for j in range(i,4) if (i,j)!=(1,2)]
    columns=[]
    for ray,K in zip(op['rays'],op['kernels']):
        tail=[dot(row[4:],z) for row in K[4:]];columns.append([ray[i]*ray[j] for i,j in covpairs]+tail)
    active=list(range(len(weights)));steps=0
    while True:
        A=[[columns[j][i] for j in active] for i in range(17)];v,rank=nullvector(A)
        if v is None:break
        assert any(x>0 for x in v) and any(x<0 for x in v)
        alpha=min(weights[j]/vv for j,vv in zip(active,v) if vv>0)
        for j,vv in zip(active,v):weights[j]-=alpha*vv;assert weights[j]>=0
        active=[j for j in active if weights[j]];steps+=1
    assert len(active)<=17
    W=ca.add(*(ca.scale(op['kernels'][j],weights[j]) for j in active));ell=op['field']['cubic_target'];lam=op['multiplier']
    assert [dot(row,lam) for row in W]==ell and quadratic(W,lam)/2==op['cost']
    result=dict(payload);result['canonical_multiplier']=list(map(str,lam));result['catalogue']=[dict(op['rows'][j],weight=str(weights[j])) for j in active]
    check=verify(result,op['field'])
    assert R(check['canonical_quartic_budget'])==op['field']['quartic_moment']-op['cost']
    result['compression']={'initial_atoms':len(op['rows']),'final_atoms':len(active),'independent_moment_rank':rank,'elimination_steps':steps,'maximum_weight_numerator_bits':max(weights[j].numerator.bit_length() for j in active),'maximum_weight_denominator_bits':max(weights[j].denominator.bit_length() for j in active),'actual_covariance_preserved':True,'all_twelve_cubic_targets_preserved':True,'canonical_cost_exactly_preserved':True,'ordinary_and_acoustic_limit_labels_preserved':True,'scope':'Algebraic compression on this supplied catalogue. No all-allocation optimization or QC decision is performed.'}
    return result,check

def main():
    if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',type=Path);parser.add_argument('--out',required=True,type=Path);args=parser.parse_args();result,check=compress(json.loads(args.input.read_text()));args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(result['compression'],verification_status=check['status']),indent=2))
if __name__=='__main__':main()
