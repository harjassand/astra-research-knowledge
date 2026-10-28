"""Independent full physical four-site reference for the block readout map.

The reference Hamiltonians/gates are built here in the physical spin basis,
all sectors included. The producer's transfer function is called only as
the object being compared against this independent physical reference.
"""
from pathlib import Path
from itertools import product
import importlib.util
import sys
import json
import time
import numpy as np
from scipy.linalg import eigh

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'corpus_first/cold_interval_bridge/code'


def physical_h(n,bonds):
    states=list(product(range(-2,3),repeat=n))
    index={q:i for i,q in enumerate(states)}
    h=np.zeros((len(states),len(states)))
    for col,q in enumerate(states):
        for i,j in bonds:
            h[col,col]+=q[i]*q[j]
            for sign in (-1,1):
                m,k=q[i],q[j]
                if -2<=m+sign<=2 and -2<=k-sign<=2:
                    r=list(q);r[i]+=sign;r[j]-=sign
                    # Marshall gauge on the actual even bipartite ring.
                    h[index[tuple(r)],col]-=np.sqrt(
                        (6-m*(m+sign))*(6-k*(k-sign)))/2
    assert np.array_equal(h,h.T)
    return states,h


def full_exp(states,h,beta):
    result=np.zeros_like(h)
    mass=np.array(list(map(sum,states)))
    for m in sorted(set(mass)):
        ix=np.flatnonzero(mass==m)
        eig,vec=eigh(h[np.ix_(ix,ix)])
        result[np.ix_(ix,ix)]=(vec*np.exp(-beta*eig))@vec.T
    return result


def main():
    started=time.monotonic()
    sys.path.insert(0,str(SOURCE))
    spec=importlib.util.spec_from_file_location('tested_block_readout',SOURCE/'block_purity_readout.py')
    tested=importlib.util.module_from_spec(spec);spec.loader.exec_module(tested)
    two,h2=physical_h(2,[(0,1)])
    four,h4=physical_h(4,[(0,1),(1,2),(2,3)])
    _,hclosing=physical_h(4,[(3,0)])
    assert np.allclose(np.linalg.eigvalsh(h2),
        np.repeat([-6,-5,-3,0,4],[1,3,5,7,9]),atol=2e-14)
    records=[]
    for beta in (.125,.75):
        f=full_exp(two,h2,beta)
        g=full_exp(four,h4,beta)
        # Literal endpoint gate insertion; interior physical labels agree.
        seam=np.zeros_like(g)
        index2={q:i for i,q in enumerate(two)}
        for i,aa in enumerate(four):
            for j,bb in enumerate(four):
                if aa[1:3]==bb[1:3]:
                    seam[i,j]=f[index2[(aa[3],aa[0])],index2[(bb[3],bb[0])]]
        fg=seam@g
        physical_z=float(np.trace(fg))
        physical_q=float(np.einsum('ij,ji->',fg,fg))
        # The tested implementation now accepts only positive arrays. The
        # independent eigensolver reference can have tiny negative roundoff
        # on far-off-diagonal entries; retain its magnitude and leave the
        # physical reference traces above unmodified.
        clipped=max(0.,-float(g.min()),-float(f.min()))
        assert clipped<1e-12
        t1,t2=tested.transfers(np.maximum(g,0),np.maximum(f,0))
        transfer_z=float(np.trace(t1))
        transfer_q=float(np.trace(t2))
        e1=abs(transfer_z/physical_z-1)
        e2=abs(transfer_q/physical_q-1)
        assert e1<5e-13 and e2<5e-13,(beta,e1,e2)
        # Absolute normalization is required for a genuine Gibbs trace bound.
        gs,_,rg=tested.local_positive_exponential(4,beta)
        fs,_,rf=tested.local_positive_exponential(2,beta)
        t1s,t2s=tested.transfers(gs,fs)
        logscale=(rg['normalizing_binary_exponent']+
                  rf['normalizing_binary_exponent'])*np.log(2)-16*beta
        abs1=np.log(np.trace(t1s))+logscale
        abs2=np.log(np.trace(t2s))+2*logscale
        le1=float(abs(abs1-np.log(physical_z)))
        le2=float(abs(abs2-np.log(physical_q)))
        assert le1<2e-10 and le2<2e-10
        exact_ring_z=float(np.trace(full_exp(four,h4+hclosing,2*beta)))
        twiceg=full_exp(four,h4,2*beta)
        twice_seam=full_exp(four,hclosing,2*beta)
        gt1=float(np.trace(twice_seam@twiceg))
        assert exact_ring_z<=physical_q*(1+2e-13)
        assert physical_q<=gt1*(1+2e-13)
        records.append({'beta':beta,'physical_sites':4,'physical_dimension':625,
                        'sectors_omitted':0,'transfer_dimensions':[len(t1),len(t2)],
                        'relative_trace1_difference':e1,'relative_trace2_difference':e2,
                        'maximum_clipped_reference_negative_roundoff':clipped,
                        'restored_absolute_log_trace1_difference':le1,
                        'restored_absolute_log_trace2_difference':le2,
                        'true_ring_Z_2beta':exact_ring_z,
                        'ALT2_upper':physical_q,'GT1_upper':gt1,
                        'ansatz_purity':physical_q/physical_z**2})
    out={'status':'INDEPENDENT_FULL_PHYSICAL_FOUR_SITE_READOUT_CONTROL_PASS',
         'records':records,'seconds':time.monotonic()-started,
         'scope':'Independent physical reference confirms endpoint orientation and both closed trace maps at one full block, two beta controls. This is not the all-size algebraic proof, an independent interval-arithmetic audit, or an acquired uniform-chain Gibbs purity.'}
    (ROOT/'PHYSICAL_READOUT_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
