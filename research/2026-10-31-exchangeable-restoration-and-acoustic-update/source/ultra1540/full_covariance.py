"""Add four actual Fourier modes to make covariance positive definite.

If a supplied polynomial already has negative compatible energy, retain
that strict sign by an explicit rational perturbation bound. This tool
DOES NOT admit the input polynomial as globally rank-one convex.
"""
from pathlib import Path
from fractions import Fraction as R
import argparse,json,sys
from fourier import gradient,average,m,Gaussian
from receive import r,b

def extra_modes(modes,epsilon):
    eps=R(epsilon);assert eps>0;N=1+max((abs(z) for mode in modes for z in mode['frequency']),default=0)
    return [{'frequency':[N,0],'sine':[str(eps/N),'0']},{'frequency':[N+1,0],'sine':['0',str(eps/(N+1))]},{'frequency':[0,N+2],'sine':[str(eps/(N+2)),'0']},{'frequency':[0,N+3],'sine':['0',str(eps/(N+3))]}]

def covariance(G):return [[average(b.mul(b.var(4,i),b.var(4,j)),G) for j in range(4)] for i in range(4)]

def perturb(modes,epsilon=R(1,16),polynomial=None,mean=(0,0,0,0)):
    G=gradient(modes);S=covariance(G);M=list(map(R,mean));eps=R(epsilon);energy0=None;actual=None
    if polynomial is not None:
        assert all(sum(pw)<=4 for pw in polynomial)
        H=gradient(extra_modes(modes,1));images=[]
        for g,h,mu in zip(G,H,M):
            image={(k[0],k[1],0):v for k,v in g.items()};image=r.m.add(image,{(0,0,0):mu},{(k[0],k[1],1):v for k,v in h.items()});images.append(image)
        raw=r.compose(polynomial,images,3);coeff={}
        for key,val in raw.items():
            if key[:2]!=(0,0):continue
            z=Gaussian.lift(val);assert not z.imag;coeff[key[2]]=z.real
        coeff[0]=coeff.get(0,R(0))-b.evaluate(polynomial,M);energy0=coeff[0];assert energy0<0
        L=sum(abs(v) for j,v in coeff.items() if j>0)
        bound=min(R(1),eps,-energy0/(2*(1+L)));assert bound>0
        n=max(0,bound.denominator.bit_length()-bound.numerator.bit_length()+1);eps=R(1,2**n)
        while eps>bound:eps/=2
        assert 0<eps<=bound
    newmodes=list(modes)+extra_modes(modes,eps);GN=gradient(newmodes);SN=covariance(GN)
    assert SN==[[S[i][j]+(eps*eps/2 if i==j else 0) for j in range(4)] for i in range(4)];b.pd(SN)
    if polynomial is not None:
        GM=[m.add(g,{(0,0):mu}) for g,mu in zip(GN,M)];actual=average(polynomial,GM)-b.evaluate(polynomial,M)
        assert actual==sum(v*eps**j for j,v in coeff.items()) and actual<=energy0/2<0
    return {'modes':newmodes,'perturbation_amplitude':str(eps),'exact_covariance_increment_diagonal':str(eps*eps/2),'positive_definite_covariance_verified':True,'input_negative_energy':None if energy0 is None else str(energy0),'output_negative_energy':None if actual is None else str(actual),'global_ROC_admission':'NOT_CHECKED_BY_THIS_OPERATION','scope':'An actual compatible-field perturbation. It preserves a strict negative energy when one is supplied, and leaves the polynomial unchanged. A QC separation additionally requires independent GLOBAL ROC admission.'}

def main():
    if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',type=Path);parser.add_argument('--epsilon',default='1/16');parser.add_argument('--out',required=True,type=Path);args=parser.parse_args();p=json.loads(args.input.read_text());poly=b.literal(p['negative_energy_polynomial'],4) if 'negative_energy_polynomial' in p else None
    out=perturb(p['modes'],args.epsilon,poly,p.get('mean',[0,0,0,0]));out['recorded_input_ROC_status']=p.get('global_ROC_status','NOT_PROVIDED');out['source_input']=str(args.input.resolve())
    if poly is not None:out['negative_energy_polynomial']=p['negative_energy_polynomial'];out['mean']=p.get('mean',[0,0,0,0])
    args.out.write_text(json.dumps(out,indent=2)+'\n');summary={k:out[k] for k in ('positive_definite_covariance_verified','global_ROC_admission','recorded_input_ROC_status')}
    summary['added_compatible_modes']=4;summary['perturbation_amplitude']=str(R(out['perturbation_amplitude']))
    for key in ('input_negative_energy','output_negative_energy'):summary[key]=None if out[key] is None else float(R(out[key]))
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
