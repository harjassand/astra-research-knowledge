"""Search actual scalar-minor support cuts, not a QC counterexample."""
import json,time
from pathlib import Path
import numpy as np
import sympy as s
from scipy.optimize import differential_evolution,minimize

def main():
    start=time.perf_counter()
    z,t,A,D,aa,bb=s.symbols('z t A D aa bb',real=True)
    p=1+z*A;q=-t+z*D
    f=(p*p+q*q)**2+aa*p*p*q*q+bb*p*q*(p*p-q*q)
    c=[s.expand(f).coeff(z,i) for i in range(3)]
    lf=s.lambdify((A,D,t,aa,bb),(c[2]-c[1]**2/(4*c[0]))/(-t),'numpy')
    records=[]
    for a,b in [(12,3.975),(12,3.978),(10.08,3.915),(10.08,3.918),(10.08,3.96)]:
        def gap(v):
            xi,lt=v;A=np.exp(xi);D=np.exp(-xi);t=np.exp(lt)
            TA=A*A+D*D;xA=A*A-D*D
            upper=2*np.sqrt(4*TA*TA-b*b)+2*a+b*xA
            return lf(A,D,t,a,b)-upper
        fit=differential_evolution(lambda v:-gap(v),[(-2,2),(-4,4)],seed=102,maxiter=1000,popsize=12,tol=1e-11)
        records.append(dict(a=a,b=b,gap=gap(fit.x),xi=float(fit.x[0]),t=float(np.exp(fit.x[1])),optimizer_success=fit.success))
    result=dict(records=records,seconds=time.perf_counter()-start,scope='Only offdiagonal positive cuts and diagonal negative cuts, no PC conclusion from a negative result')
    Path(__file__).with_name('NONPC_PROPOSALS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
