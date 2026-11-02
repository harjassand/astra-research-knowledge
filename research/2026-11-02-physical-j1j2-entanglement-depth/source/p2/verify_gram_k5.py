#!/usr/bin/env python3
"""A posteriori entirely integer certificate: not dependent on Cholesky/eigsh.
Check 45 induced connected five-site interaction motifs at alpha=1/2.

Certifies W_B+(91/200)5 I positive definite by a rational Gram + strictly
row-diagonally-dominant remainder on Sz_total=0. SU(2) means every eigenvalue
of the full 10-qubit scalar W_B appears in Sz_total=0 (integer total spin).

The signed 64-bit NumPy multiplication is EXACT under the explicit 2^62 bound.
"""
import numpy as np
from pathlib import Path
from fractions import Fraction
import json
from verify_replica_exact import shapes,replica_matrix

LIMIT=1<<62

def build_integer_independent(w):
    k=len(w);n=2*k
    full=replica_matrix(w)  # independent rational Pauli/bond assembly
    ix=[s for s in range(1<<n) if s.bit_count()==k]
    M=np.array([[int(full[i].get(j,Fraction(0))*400) for j in ix] for i in ix],dtype=np.int64)
    assert all((full[i].get(j,Fraction(0))*400).denominator==1 for i in ix for j in ix)
    assert np.array_equal(M,M.T)
    return M

def check_gram(M,R,S):
    if R.dtype!=np.dtype('int64') or R.shape!=M.shape or not np.array_equal(R,np.tril(R)):
        return {'pass':False,'why':'invalid triangular integer witness'}
    n=M.shape[0]; maxR=int(np.max(np.abs(R.astype(object))))
    maxM=int(np.max(np.abs(M.astype(object))))
    if n*maxR*maxR >= LIMIT or S*S*maxM>=LIMIT:
        return {'pass':False,'why':'integer overflow safety check failed'}
    product=R@R.T # exact signed-64bit because no partial sum can overflow
    E=S*S*M-product
    emax=int(np.max(np.abs(E.astype(object))))
    if n*emax>=LIMIT:
        return {'pass':False,'why':'absolute row sum overflow guard failed'}
    absE=np.abs(E)
    diag=np.diag(E)
    gap=diag-(np.sum(absE,axis=1)-np.abs(diag))
    m=int(np.min(gap))
    return {'pass':m>0,'gershgorin_min_slack':m,'dimension':n,
            'maxR':maxR,'maxM':maxM}

def run():
    base=Path(__file__).resolve().parent
    manifest=json.loads((base/'K5_GRAM_MANIFEST.json').read_text())
    assert manifest['k']==5 and manifest['scale_int']==400
    S=int(manifest['R_denominator']);assert S==1<<18
    items=list(shapes(5)[5].items()); assert len(items)==45
    result={'method':'Exact signed-64-bit integer Gram + diagonally dominant residual',
            'shift_per_site':'91/200','k':5,'cases':[]}
    with np.load(base/'K5_GRAM_WITNESSES.npz',allow_pickle=False) as files:
        for i,((key,data),entry) in enumerate(zip(items,manifest['cases'])):
            assert i==entry['index'] and list(key)==entry['weighted_graph_key']
            R=files[entry['id']]
            M=build_integer_independent(data['w'])
            out=check_gram(M,R,S)
            if not out['pass']:raise AssertionError({'case':i,'graph':key,'check':out})
            # bind all manifest entries to this independent recomputation
            assert out['gershgorin_min_slack']==entry['gershgorin_integer_margin']
            result['cases'].append({'case':i,'graph':list(key),**out})
            print('EXACT GRAM PASS',i,'dim',out['dimension'],'slack',out['gershgorin_min_slack'],flush=True)
        R=files['witness_000'].copy()
        R[0,0]+=100000000
        assert not check_gram(build_integer_independent(items[0][1]['w']),R,S)['pass']
    result['count']=len(result['cases'])
    result['negative_tampered_witness_rejected']=True
    result['minimum_integer_gershgorin_slack']=min(x['gershgorin_min_slack'] for x in result['cases'])
    (base/'K5_VERIFICATION_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print('ALL 45 FIVE-SITE GRAM CERTIFICATES PASS; TAMPER REJECTED')
if __name__=='__main__':run()
