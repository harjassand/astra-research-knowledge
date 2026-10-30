"""Construct the actual six-term positive Hessian quadrature.

The construction is independent of the lower cubic and quadratic. The
displayed energy identity is also checked on the near-boundary fixture
F_*+C0+1859|A|^2. Global QC of that fixture is not inferred.
"""
from fractions import Fraction as R
from pathlib import Path
import argparse,json
from receive import m,b,dot,quadratic
HERE=Path(__file__).resolve().parent
def construct(amplitudes,mean=(0,0,0,0),phase_cos=R(1),nu=R(1859)):
    a,beta,c=list(map(R,amplitudes));mean=list(map(R,mean));kappa=R(phase_cos);nu=R(nu);assert len(mean)==4 and abs(kappa)<=1
    cert=json.loads((HERE/'certificate.json').read_text());rays=[list(map(R,r)) for r in cert['rays']]
    squares=[a*a,beta*beta,c*c];minimum=min(squares);index=squares.index(minimum)
    weights=[v/2-minimum/4 for v in squares]+[minimum/36,4*minimum/9,minimum/36]
    X=[list(map(R,row)) for row in cert['charts'][index]['X']]
    backgrounds=[[a*beta*c*kappa*v/w for v in row] if w else [R(0)]*4 for row,w in zip(X,weights)] if minimum else [[R(0)]*4 for _ in rays]
    F,C0,T=m.acquired();Q=m.scale(T,nu);P=b.add(F,C0,Q)
    HF=[[b.diff(b.diff(F,i),j) for j in range(4)] for i in range(4)];HP=[[b.diff(b.diff(P,i),j) for j in range(4)] for i in range(4)]
    cost=sum(w*quadratic([[b.evaluate(p,r) for p in row] for row in HF],A)/2 for w,r,A in zip(weights,rays,backgrounds))
    modes=[{'frequency':[1,0],'sine':[str(a),'0']},{'frequency':[0,1],'sine':['0',str(beta)]},{'frequency':[1,1],'sine':[str(c),str(c)]}];G=m.gradient(modes)
    f=m.average(F,G);T4=m.average(b.mul(T,T),G);budget=f-cost;assert budget>=T4/200
    CM=b.add(C0,*(b.scale(b.diff(F,i),mean[i]) for i in range(4)))
    QM=b.add(Q,*(b.scale(b.diff(C0,i),mean[i]) for i in range(4)),*(b.scale(HF[i][j],mean[i]*mean[j]/2) for i in range(4) for j in range(4)))
    # Arbitrary relative phase is represented exactly by kappa=cos(delta).
    # All quartic and quadratic moments are phase independent; every cubic
    # resonance has the same factor kappa, as checked by the receiver.
    actual=f+kappa*m.average(CM,G)+m.average(QM,G)
    terms=[];rhs=budget
    for w,r,A in zip(weights,rays,backgrounds):
        point=[x+y for x,y in zip(mean,A)];H=[[b.evaluate(p,point) for p in row] for row in HP];score=quadratic(H,r);rhs+=w*score/2
        terms.append({'weight':str(w),'rank_one_direction':list(map(str,r)),'background_offset':list(map(str,A)),
                      'actual_base':list(map(str,point)),'fixture_second_rank_one_derivative':str(score)})
    assert actual==rhs
    if nu>=1859:assert all(R(t['fixture_second_rank_one_derivative'])>=0 for t in terms)
    return {'amplitudes':list(map(str,(a,beta,c))),'mean':list(map(str,mean)),'relative_phase_cos':str(kappa),
      'chosen_minimum_chart':index,'terms':terms,'quartic_cost':str(cost),'quartic_energy':str(f),
      'positive_budget':str(budget),'fourth_gradient_moment':str(T4),'universal_lower_bound':str(T4/200),
      'fixture_nu':str(nu),'fixture_actual_energy_gap':str(actual),'exact_energy_identity':True,
      'scope':'A universal Hessian-quadrature identity for the stated resonant field. Nonnegativity of the Hessian terms uses global ROC. The default fixture has a sibling exact ROC certificate; global QC remains open.'}
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--amplitudes',nargs=3,default=['1','2','3']);parser.add_argument('--mean',nargs=4,default=['1','-2','0','1']);parser.add_argument('--phase-cos',default='1');parser.add_argument('--nu',default='1859');parser.add_argument('--out',type=Path);args=parser.parse_args()
    result=construct(args.amplitudes,args.mean,args.phase_cos,args.nu)
    if args.out:
        args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'saved':str(args.out.resolve()),'exact_energy_identity':True,'positive_budget':float(R(result['positive_budget'])),'universal_lower_bound':float(R(result['universal_lower_bound'])),'scope':result['scope']},indent=2))
    else:print(json.dumps(result,indent=2))
if __name__=='__main__':main()
