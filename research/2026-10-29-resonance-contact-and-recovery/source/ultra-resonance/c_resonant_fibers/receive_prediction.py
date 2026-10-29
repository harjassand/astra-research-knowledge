"""Compose the PAID errors into a finite original-Hamiltonian prediction.

Everything here is rational except the named physical mathematical constants,
which are enclosed by explicit Taylor or integer-square-root bounds. There
is no quantum-state/eigenvector/original-time trajectory oracle.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import math
import time
from acquire_quadrature import I

HERE=Path(__file__).resolve().parent


def exp_i(x):
    x=F(x);assert 0<=x<100
    term=F(1);s=term
    for n in range(1,257):term*=x/n;s+=term
    nxt=term*x/257
    tail=nxt/(1-x/258)
    return I(s,s+tail)


def sqrt_upper(x,bits=128):
    x=F(x);assert x>=0
    d=1<<bits;n=-((-x.numerator*d*d)//x.denominator)
    z=math.isqrt(n)
    if z*z<n:z+=1
    return F(z,d)


def fmt(q):return {'exact':str(q),'float_display':float(q)}


def main():
    started=time.perf_counter()
    acq=json.loads((HERE/'QUADRATURE_ACQUISITION.json').read_text())
    raw=json.loads((HERE/'TAYLOR_RAW.json').read_text())
    assert hashlib.sha256((HERE/'QUADRATURE.txt').read_bytes()).hexdigest()==acq['parameters_sha256']
    N=1<<128;A=F(4,3);tau=F(1,2);den=1<<raw['fixed_fractional_bits']
    q=acq['nodes'];assert q==48 and raw['steps']==512 and raw['order']==24
    # All exact signs/positive Gauss weights are acquired upstream, not assumed.
    endpoints=raw['returned_point_Bloch_fixed']
    value=I(0)
    for node,point in zip(acq['node_proofs'],endpoints):
        row=node['fixed_intervals']
        weight=I(F(row[0],den),F(row[1],den));f1=I(F(row[2],den),F(row[3],den))
        value+=weight*f1*F(int(point[1]),den)/4
    growth=exp_i(5*A*tau).u
    numerical=(F(1,den)+F(int(raw['sum_local_Euclidean_error_fixed_upper']),den))*growth/4
    # Ellipse rho=3/2 gives eta=5pi/24<55/84.
    e1=exp_i(F(55,84));e2=exp_i(F(55,42))
    sinh1=(e1.u-1/e1.u)/2;sinh2=(e2.u-1/e2.u)/2
    assert sinh1+sinh2/3<F(13,10)
    assert (e2.u+1/e2.l)/2<2
    analytic_M=2*(1+exp_i(F(39,10)).u)
    quad_moment=12*analytic_M*F(2,3)**(2*q)
    continuum_quad=quad_moment*(1+6*A*tau*growth)/4
    # Real-label derivative and endpoint strips for the finite paired grid.
    finite_grid=F(22,N)*(1+6*A*tau*growth)/4
    # Quantum product-marginal error for the exact finite-N secular block.
    chaos=sqrt_upper((exp_i(64*A*tau).u-1)/N)/4
    # Nonresonant antiderivative bound; lambda=N^-8 and J=1.
    unitary=F(A,32*N**3)*(1+2*A*N*tau)
    averaging=unitary # conservative: 2||O_N||<=1/2 would be stronger.
    total=numerical+continuum_quad+finite_grid+chaos+averaging
    prediction=I(value.l-total,value.u+total)
    assert prediction.u-prediction.l<F(1,1000000)
    result={'status':'QUALIFIED_MATHEMATICAL_PREDICTION_FOR_EXPLICIT_COMPACT_MODEL',
      'source':{'N':str(N),'N_compact':'2^128','J':'1','lambda':'2^-1024 = N^-8','interaction_weights':{'a1':'1','a2':'1/3'},
                'boundary':'periodic, zero flux','physical_time':'2^1023 in J^-1 model units','interaction_clock':'1/2',
                'initial_state':'Exact product over paired momenta k,pi-k of (sqrt(3)/2 + (1/2)c_k^dag c_(pi-k)^dag)|vac>; fixed points empty. Known pure Gaussian, parity even, not a generic thermal state.',
                'observable':'O_N=(C-C^dag)/(4iN), C=sum_j (-1)^j c_j c_(j+1); [H0,O_N]=0; ||O_N||<=1/4.',
                'Hilbert_dimension':'2^N; not instantiated','paired_band_dimension':'2^(N/2-1); not instantiated'},
      'quadrature_point_value':value.encode(),
      'error_budget':{'validated_numerical_flow':fmt(numerical),'continuum_quadrature':fmt(continuum_quad),
                      'finite_N_grid':fmt(finite_grid),'quantum_mean_field':fmt(chaos),
                      'original_H_averaging':fmt(averaging),'total':fmt(total)},
      'prediction_interval':prediction.encode(),'prediction_float_display':[float(prediction.l),float(prediction.u)],
      'width_float_display':float(prediction.u-prediction.l),
      'comparison':'A source-aware pre-relaxation/resonant-HFB solver can use the SAME collective equations. No generic speed/novelty or advantage over that informed method is established.',
      'unpaid_physical_scope':'No experimental calibration, preparation, boundary/dispersion accuracy or isolation over this duration is supplied. This is a precisely specified mathematical Hamiltonian, not an acquired physical system.',
      'no_generic_closure':'Exact finite resonance classification, explicit small-gap averaging bound, paired-subspace algebra and quantitative product-marginal bound pay the approximation. No ETH/GGE/Markov assumption.',
      'receiver_seconds_before_serialization':time.perf_counter()-started,
      'input_sha256':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ['QUADRATURE.txt','QUADRATURE_ACQUISITION.json','TAYLOR_RAW.json','EXACT_SOURCE_CHECK.json']}}
    (HERE/'PREDICTION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'prediction':result['prediction_float_display'],'width':result['width_float_display'],
                      'errors':{k:v['float_display'] for k,v in result['error_budget'].items()},'seconds':result['receiver_seconds_before_serialization']},indent=2))


if __name__=='__main__':main()
