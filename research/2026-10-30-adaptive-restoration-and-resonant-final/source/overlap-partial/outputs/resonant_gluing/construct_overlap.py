"""Construct the eight positive Hessian terms for an overlapping network."""
from pathlib import Path
from fractions import Fraction as R
import argparse,json
from receive import m,b,quadratic
HERE=Path(__file__).resolve().parent
def construct(cos1,sin1,cos2,sin2,mean=(0,0,0,0),amplitude=R(1),nu=R(1859)):
    c1,s1,c2,s2=map(R,(cos1,sin1,cos2,sin2));assert c1*c1+s1*s1==1 and c2*c2+s2*s2==1
    M=list(map(R,mean));rho=R(amplitude);nu=R(nu);assert len(M)==4
    cert=json.loads((HERE/'overlap_certificate.json').read_text());powers=json.loads((HERE.parent/'graded_stabilization/certificate.json').read_text())['cubic_powers']
    rays=[list(map(R,r)) for r in cert['rays']];weights=list(map(R,cert['weights']));XX=[list(map(R,r)) for r in cert['X']];YY=[list(map(R,r)) for r in cert['Y']]
    A=[[rho*(c1*x+c2*y) for x,y in zip(xx,yy)] for xx,yy in zip(XX,YY)];F,C,T=m.acquired();Q=m.scale(T,nu);P=b.add(F,C,Q)
    HF=[[b.diff(b.diff(F,i),j) for j in range(4)] for i in range(4)];HP=[[b.diff(b.diff(P,i),j) for j in range(4)] for i in range(4)]
    f0,fc,fs=map(R,cert['quartic_phase_coefficients']);f=rho**4*(f0+fc*c1*c2+fs*s1*s2)
    cost=sum(rho*rho*w*quadratic([[b.evaluate(p,r) for p in row] for row in HF],a)/2 for r,w,a in zip(rays,weights,A));budget=f-cost
    rad0,radc,rads=map(R,cert['radial_phase_coefficients']);T4=rho**4*(rad0+radc*c1*c2+rads*s1*s2);assert budget>=T4/200
    CM=b.add(C,*(b.scale(b.diff(F,i),M[i]) for i in range(4)));QM=b.add(Q,*(b.scale(b.diff(C,i),M[i]) for i in range(4)),*(b.scale(HF[i][j],M[i]*M[j]/2) for i in range(4) for j in range(4)))
    targets=[list(map(R,row)) for row in cert['cubic_targets']];cm=[CM.get(tuple(pw),R(0)) for pw in powers]
    cubic=rho**3*sum(co*(t[0]*c1+t[1]*c2) for co,t in zip(cm,targets))
    original=[[R(1),0,0,0],[0,0,0,R(1)],[R(1)]*4,[R(1),R(1,2),R(1,2),R(1,4)]]
    q=rho*rho*sum(b.evaluate(QM,r)/2 for r in original);actual=f+cubic+q;rhs=budget;terms=[]
    for w,r,a in zip(weights,rays,A):
        point=[x+y for x,y in zip(M,a)];score=quadratic([[b.evaluate(p,point) for p in row] for row in HP],r);rhs+=rho*rho*w*score/2
        terms.append({'weight':str(rho*rho*w),'rank_one_direction':list(map(str,r)),'base':list(map(str,point)),'fixture_rank_one_hessian':str(score)})
    assert actual==rhs
    if nu>=1859:assert all(R(t['fixture_rank_one_hessian'])>=0 for t in terms)
    return {'relative_phase_pairs':list(map(str,(c1,s1,c2,s2))),'mean':list(map(str,M)),'overall_amplitude':str(rho),'terms':terms,
      'positive_budget':str(budget),'fourth_gradient_moment':str(T4),'universal_L4_lower_bound':str(T4/200),
      'fixture_actual_energy_gap':str(actual),'exact_energy_identity':True,
      'scope':'All-phase overlapping-network Hessian quadrature. Global ROC is the premise for term nonnegativity; unrestricted global QC is not inferred.'}
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--phase-pairs',nargs=4,default=['3/5','4/5','-5/13','12/13']);parser.add_argument('--mean',nargs=4,default=['1','-2','0','1']);parser.add_argument('--amplitude',default='1');parser.add_argument('--nu',default='1859');parser.add_argument('--out',type=Path);args=parser.parse_args()
    result=construct(*args.phase_pairs,args.mean,args.amplitude,args.nu)
    if args.out:
        args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'saved':str(args.out.resolve()),'exact_energy_identity':True,'positive_budget':float(R(result['positive_budget'])),'universal_lower_bound':float(R(result['universal_L4_lower_bound'])),'scope':result['scope']},indent=2))
    else:print(json.dumps(result,indent=2))
if __name__=='__main__':main()
