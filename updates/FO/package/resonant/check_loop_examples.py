from fractions import Fraction as Q
import sympy as S
import json,time
from pathlib import Path
from profile_algebra import *
ROOT=Path(__file__).resolve().parent

def asrat(a):return S.Rational(a.numerator,a.denominator)
def loop_moments(n,m,path):
 F,N,C,det=averaged(n,m,True)
 zeroB={b:0 for b in B}; T=Q(len(path)-1)
 def integral(expr):return asrat(polygon_integral(S.expand(expr),path)/T)
 f=F.subs(zeroB)
 n4=integral(N.subs(zeroB))
 H=S.Matrix(4,4,lambda i,j:integral(S.diff(F,B[i],B[j]).subs(zeroB)))
 cubic=S.Matrix([integral(S.diff(F,bb).subs(zeroB)) for bb in B])
 covariance=S.Matrix(4,4,lambda i,j:integral(C[i,j].subs(zeroB)))
 cf=integral(f);df=integral(det.subs(zeroB))
 assert df==0
 assert all(H[:j,:j].det()>0 for j in range(1,5))
 opt=-H.inv()*cubic;gap=cf+(cubic.dot(opt))/2
 return {'C':covariance,'H':H,'b':cubic,'c':cf,'n4':n4,'gap':gap,'Bopt':opt}
def serial(z):return {k:([str(x) for x in v] if isinstance(v,S.MatrixBase) else str(v)) for k,v in z.items()}
if __name__=='__main__':
 start=time.time();out={}
 path=square_loop(Q(1),Q(1))
 for nm in [(1,-1),(1,3)]:
  z=loop_moments(*nm,path);zr=loop_moments(*nm,path[::-1]);assert z['b']==zr['b']==S.zeros(4,1)
  if nm==(1,3):
   assert z['C']==zr['C'];assert z['H']==zr['H']
  out[str(nm)+'_forward']=serial(z);out[str(nm)+'_reverse']=serial(zr)
  print(nm,'C',z['C'],'forward',z['c'],'reverse',zr['c'],'diff',z['c']-zr['c'],'n4',z['n4'],flush=True)
 path=cancelled_loop();z=loop_moments(1,2,path)
 assert z['gap']>=z['n4']/2
 out['eight_loop']=serial(z);out['eight_loop']['path']=[[str(x),str(y)] for x,y in path]
 print('eight-loop', 'b',z['b'],'c',z['c'],'n4',z['n4'],'gap',z['gap'],'ratio',z['gap']/z['n4'],'time',time.time()-start,flush=True)
 (ROOT/'loop_examples.json').write_text(json.dumps(out,indent=2))
