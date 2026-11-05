"""Independent finite matrix checks for retained-R-and-A block Gram laws."""
import json
import math
from pathlib import Path
import numpy as np
from verify_crossed_statistic import I, P, PHI, SWAP, coefficients, formula, embed_two


def gram_formula(theta, b):
    u,v,w,h=coefficients(theta,b)
    d=math.sqrt((1-u)*(1+3*u))
    p=(1-v)**2/(2*(1-u))+((1-v)**2+4*h*h)/(2*d)
    q=(6*u+v+5*w)**2/(36*(1+3*u))
    q+=(36*h*h+27*u*u-24*u*v-30*u*w+7*v*v+10*v*w+10*w*w)/(36*(1-u))
    q+=(36*h*h+9*u*u+12*u*v-30*u*w+4*v*v-20*v*w+25*w*w)/(36*d)
    return p,q


def invsqrt(a):
    values,vectors=np.linalg.eigh(a)
    assert values.min()>0
    return (vectors/np.sqrt(values))@vectors.conj().T


def gram_parts(baseline,delta):
    d=baseline.shape[0]//2
    exported=np.kron(I/2,np.trace(delta.reshape(2,d,2,d),axis1=0,axis2=2))
    residual=delta-exported
    weight=invsqrt(baseline)
    return (float(np.trace(exported@weight@exported@weight).real),
            float(np.trace(residual@weight@residual@weight).real))


def physical_block(matrix,theta,b):
    """Exact block output via Bell-folded isometry, fresh RA every block.

    Only within a fully retained block is folding used. The intermediate
    virtual updates are not claimed to be physical on the compressed state.
    """
    c,s=math.cos(theta),math.sin(theta)
    old_qubits=round(math.log2(matrix.shape[0]))
    state=np.kron(matrix,PHI)
    n=old_qubits+3
    source=embed_two(c*np.eye(4)+1j*s*SWAP,0,n-1,n)
    crossed=embed_two(c*np.eye(4)-2j*s*PHI,n-2,n-1,n)
    operation=crossed@source
    dim=2**(n-1)
    for _ in range(b):
        expanded=operation@np.kron(state,I/2)@operation.conj().T
        state=np.trace(expanded.reshape(dim,2,dim,2),axis1=1,axis2=3)
    return state


def main():
    maximum_one_block_error=0.0
    for theta in [.03,.1,.3,.7,1.1]:
        for b in [1,2,3,10,100]:
            base,delta=formula(theta,b)
            direct=gram_parts(base,delta)
            predicted=gram_formula(theta,b)
            maximum_one_block_error=max(maximum_one_block_error,
                                        max(abs(x-y) for x,y in zip(direct,predicted)))
    repeated=[]
    for theta,b in [(.1,1),(.3,1),(.3,2),(.7,3)]:
        base,delta=I/2,P[2]/2
        p,q=gram_formula(theta,b)
        for k in range(1,3):
            base=physical_block(base,theta,b)
            delta=physical_block(delta,theta,b)
            measured_p,measured_q=gram_parts(base,delta)
            predicted_p=p*(1-q**k)/(1-q)
            repeated.append({'theta':theta,'block_size':b,'blocks':k,
                             'direct_p':measured_p,'predicted_p':predicted_p,
                             'direct_q':measured_q,'predicted_q':q**k})
    maximum_repeated_error=max(max(abs(r['direct_p']-r['predicted_p']),
                                   abs(r['direct_q']-r['predicted_q'])) for r in repeated)
    operating=[]
    for b in [1,100,1000,3000,10000,40000]:
        p,q=gram_formula(.1,b)
        efficiency=p/(1-q)
        operating.append({'theta':.1,'block_size':b,'p':p,'q':q,
                          'loss':1-p-q,'loss_per_export':(1-p-q)/p,
                          'infinite_block_petz_visibility':efficiency,
                          'arbitrary_final_decoder_halfdiamond_error_lower_bound':
                          .75*(1-math.sqrt(efficiency))})
    result={'scope':'Both R and Bell purifier A retained after each reverse-decoded block',
            'maximum_one_block_gram_error':maximum_one_block_error,
            'maximum_repeated_block_gram_error':maximum_repeated_error,
            'repeated_block_checks':repeated,'operating_points':operating}
    assert maximum_one_block_error<1e-11
    assert maximum_repeated_error<1e-11
    Path(__file__).with_name('purified_block_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='repeated_block_checks'},indent=2))


if __name__=='__main__':
    main()
