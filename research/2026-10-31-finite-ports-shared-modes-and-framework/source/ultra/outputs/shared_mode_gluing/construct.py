"""Build positive Hessian quadrature for any amplitudes of the shared network."""
from pathlib import Path
from fractions import Fraction as R
import argparse,json
from receive import setup,m,b,dot,quadratic,compose
HERE=Path(__file__).resolve().parent

def rotate(v,cs):
    c,s=cs;return [c*v[0]-s*v[2],c*v[1]-s*v[3],s*v[0]+c*v[2],s*v[1]+c*v[3]]

def construct(amplitudes,phase_pairs=(1,0,1,0),mean=(0,0,0,0),output_rotation=(1,0),nu=1859):
    amps=list(map(R,amplitudes));assert len(amps)==4
    c1,s1,c2,s2=map(R,phase_pairs);assert c1*c1+s1*s1==1 and c2*c2+s2*s2==1
    M=list(map(R,mean));cs=tuple(map(R,output_rotation));nu=R(nu);assert len(M)==4 and len(cs)==2 and dot(cs,cs)==1
    data=setup();cert=json.loads((HERE/'certificate.json').read_text());squared=[x*x for x in amps]
    order=sorted(range(4),key=lambda i:(squared[i],i));case=next(row for row in cert['charts'] if row['order']==order)
    bi=case['base'];ids=[(0,1,2),(0,2,3)][bi];minimum=min(squared[i] for i in ids);eps=R(case['epsilon'])
    cubic_scalars=[amps[0]*amps[1]*amps[2]*c1,amps[0]*amps[2]*amps[3]*c2]
    if minimum:
        weights=[squared[i]/2-eps*minimum for i in ids]+[eps*minimum*eta for eta in data['eta']]+[squared[3 if bi==0 else 1]/2]
        rays=data['rays'][bi];sources=[[[R(v) for v in row] for row in X] for X in case['sources']]
        backgrounds=[]
        for i,w in enumerate(weights):
            z=[sum(cubic_scalars[e]*sources[e][i][j] for e in range(2)) for j in range(4)]
            if w:backgrounds.append([v/w for v in z])
            else:assert z==[0,0,0,0];backgrounds.append([R(0)]*4)
    else:
        # A common mode is absent, or both leaf modes are absent. The actual
        # cubic moment is zero. No covariance exchange is then required.
        assert cubic_scalars==[0,0]
        rays=data['original'];weights=[v/2 for v in squared];backgrounds=[[R(0)]*4 for _ in rays]
    phase_plus=c1*c2-s1*s2;phase_minus=c1*c2+s1*s2
    qa=amps[0]**2*amps[1]*amps[3];qc=amps[1]*amps[2]**2*amps[3]
    f=quadratic(data['FM'],squared)+data['u']*qa*phase_plus+data['v']*qc*phase_minus
    radial=quadratic(data['RM'],squared)+data['radial_u']*qa*phase_plus+data['radial_v']*qc*phase_minus
    cost=sum(w*quadratic([[b.evaluate(p,r) for p in row] for row in data['HF']],a)/2 for w,r,a in zip(weights,rays,backgrounds))
    budget=f-cost;assert budget>=radial/32
    covariance=[[sum(w*r[i]*r[j] for w,r in zip(weights,rays)) for j in range(4)] for i in range(4)]
    assert covariance==[[sum(squared[k]*r[i]*r[j]/2 for k,r in enumerate(data['original'])) for j in range(4)] for i in range(4)]
    F,C,T=m.acquired();Q=b.scale(T,nu);P=b.add(F,C,Q);HP=[[b.diff(b.diff(P,i),j) for j in range(4)] for i in range(4)]
    CM=b.add(C,*(b.scale(b.diff(F,i),M[i]) for i in range(4)))
    QM=b.add(Q,*(b.scale(b.diff(C,i),M[i]) for i in range(4)),*(b.scale(data['HF'][i][j],M[i]*M[j]/2) for i in range(4) for j in range(4)))
    images=[b.add(b.scale(b.var(4,0),cs[0]),b.scale(b.var(4,2),-cs[1])),b.add(b.scale(b.var(4,1),cs[0]),b.scale(b.var(4,3),-cs[1])),b.add(b.scale(b.var(4,0),cs[1]),b.scale(b.var(4,2),cs[0])),b.add(b.scale(b.var(4,1),cs[1]),b.scale(b.var(4,3),cs[0]))]
    Crot=compose(CM,images,4);cubic=sum(Crot.get(tuple(pw),0)*sum(row[e]*cubic_scalars[e] for e in range(2)) for pw,row in zip(data['powers'],data['targets']))
    q=sum(squared[i]*b.evaluate(QM,rotate(r,cs))/2 for i,r in enumerate(data['original']));actual=f+cubic+q
    rhs=budget;terms=[]
    for w,r,a in zip(weights,rays,backgrounds):
        if not w:continue
        rr=rotate(r,cs);aa=rotate(a,cs);point=[x+y for x,y in zip(M,aa)]
        score=quadratic([[b.evaluate(p,point) for p in row] for row in HP],rr);rhs+=w*score/2
        terms.append({'weight':str(w),'rank_one_direction':list(map(str,rr)),'base':list(map(str,point)),'fixture_rank_one_hessian':str(score)})
    assert actual==rhs
    if nu>=1859:assert all(R(t['fixture_rank_one_hessian'])>=0 for t in terms)
    return {'amplitudes':list(map(str,amps)),'phase_pairs':list(map(str,(c1,s1,c2,s2))),'mean':list(map(str,M)),'output_rotation':list(map(str,cs)),'selected_order':order,'covariance_exchange_amount':str(eps*minimum),'positive_hessian_terms':terms,'exact_covariance_identity':True,'exact_energy_identity':True,'quartic_budget':str(budget),'fourth_gradient_moment':str(radial),'universal_single_block_lower_bound':str(radial/32),'fixture_actual_energy_gap':str(actual),'scope':'All real relative amplitudes and phases of this shared-mode network. The fixture is F+C0+nu|A|^2; global ROC is independently admitted for nu>=1859. Full-face QC remains unresolved.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--amplitudes',nargs=4,default=['2','-3','1','1/2']);parser.add_argument('--phase-pairs',nargs=4,default=['3/5','4/5','-5/13','12/13']);parser.add_argument('--mean',nargs=4,default=['1','-2','0','1']);parser.add_argument('--rotation',nargs=2,default=['3/5','4/5']);parser.add_argument('--nu',default='1859');parser.add_argument('--out',type=Path);args=parser.parse_args()
    result=construct(args.amplitudes,args.phase_pairs,args.mean,args.rotation,args.nu)
    if args.out:
        args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'saved':str(args.out.resolve()),'positive_hessian_terms':len(result['positive_hessian_terms']),'exact_energy_identity':True,'quartic_budget':float(R(result['quartic_budget'])),'universal_single_block_lower_bound':float(R(result['universal_single_block_lower_bound']))},indent=2))
    else:print(json.dumps(result,indent=2))
if __name__=='__main__':main()
