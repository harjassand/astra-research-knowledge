"""Independent dense exact small-chain check of new weighted-CG certificate."""
from pathlib import Path
from fractions import Fraction as F
import sys,json
sys.dont_write_bytecode=True
sys.set_int_max_str_digits(0)
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'interacting_rare_review_20261027'))
from independent_check import exact

def main():
    records=[]
    for theta,clocks in [([F(1,3),F(2,5),F(3,7),F(4,9)],[F(2,3),F(5,4),F(7,6)]),
       ([F(1,2),F(2,3),F(3,5),F(4,7),F(5,9),F(6,11)],[F(4,5),F(1),F(6,5),F(7,5),F(8,5)])]:
      for delta in (F(0),F(1,20),F(1,2)):
        p,cap,truth,(states,Q,w)=exact(theta,clocks,delta)
        rho=w[-1];u=[rho]+[F(0)]*(len(states)-2)+[F(-1)]
        def dot(a,b):return sum(x*y*z for x,y,z in zip(w,a,b))
        def H(a):return [-sum(x*y for x,y in zip(row,a)) for row in Q]
        gap=min(clocks)*min(2*a*b/(1+a*b) for a,b in zip(theta,theta[1:]))
        y=[F(0)]*len(states);r=u[:];d=r[:];rr=dot(r,r);steps=[]
        for k in range(1,5):
          hd=H(d);alpha=rr/dot(d,hd)
          y=[a+alpha*b for a,b in zip(y,d)]
          r=[a-alpha*b for a,b in zip(r,hd)];nr=dot(r,r)
          hy=H(y);L=(2*dot(u,y)-dot(y,hy))/rho;U=L+nr/(rho*gap)
          assert L<=truth<=U
          assert r==[a-b for a,b in zip(u,hy)]
          width=float(U/L-1) if L>0 else None
          steps.append({'degree':k,'relative_integral_width':width,'exact_containment':'PASS'})
          if not nr:break
          beta=nr/rr;d=[a+beta*b for a,b in zip(r,d)];rr=nr
        records.append({'M':len(theta),'delta':str(delta),'true_p':str(p),
          'backward_orientation_and_weighted_residual':'PASS','steps':steps})
    result={'scope':'NEW direct-variational operation, independent exact dense small checks; not a sparse large implementation or physical claim','records':records}
    (HERE/'EXACT_PAIR_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([{'M':r['M'],'delta':r['delta'],'last_width':r['steps'][-1]['relative_integral_width']} for r in records]))

if __name__=='__main__':main()
