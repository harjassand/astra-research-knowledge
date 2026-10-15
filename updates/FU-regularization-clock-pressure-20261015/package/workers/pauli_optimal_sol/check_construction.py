"""Finite diagnostics for the analytic construction; no optimality certificate."""
from pathlib import Path
import json, math
import numpy as np

def diagnostic(h=.002, cutoff=24.):
    unit=round(1/h); n=round(cutoff/h); s=np.arange(n+1)*h
    G=np.ones(n+1)
    for j in range(2*unit+1,n+1):
        # Positive implicit trapezoid discretization of the exact integral identity.
        window=G[j-2*unit:j]
        G[j]=h*(window.sum()-.5*window[0])/(2*(s[j]-1)-h/2)
    J=[float(np.trapezoid(s**k*G,s)) for k in range(4)]
    C=1/(2*J[1]); v=J[3]/(3*J[1]); v_formula=23/9-1/(9*J[1])
    r=s[unit:-unit]; q=C*r*(G[:-2*unit]+G[2*unit:])
    def sinc(x):return np.sinc(x/np.pi)
    def j1(x):
        small=np.abs(x)<.02; ans=np.empty_like(x)
        ans[small]=x[small]/3-x[small]**3/30+x[small]**5/840-x[small]**7/45360
        ans[~small]=(np.sin(x[~small])-x[~small]*np.cos(x[~small]))/x[~small]**2
        return ans
    transforms=[]
    for k in [.1,.7,math.pi/2,2.1,4.3]:
        phi=float(np.trapezoid(2*C*s*G*sinc(k*s),s))
        a=float(np.trapezoid(q*sinc(k*r),r));b=float(np.trapezoid(q*j1(k*r),r))
        transforms.append({'k':k,'phi':phi,'scalar_residual':a-phi*math.cos(k),'spin_residual':b-phi*math.sin(k)})
    result={'status':'finite_diagnostics_not_certificate','h':h,'cutoff':cutoff,'J':J,'C':C,'variance':v,'variance_exact_formula_evaluated':v_formula,'moment_identity_residuals':[J[1]-2*J[0]+1,J[2]-5*J[0]+8/3,J[3]-(46/3)*J[0]+8],'q_mass':float(np.trapezoid(q,r)),'q_mean':float(np.trapezoid(r*q,r)),'q_second_moment':float(np.trapezoid(r*r*q,r)),'minimum_sampled_G':float(G.min()),'tail_G_at_cutoff':float(G[-1]),'transforms':transforms,'analytic_coarse_upper':160/63,'analytic_lower':2+16/(3*math.pi**3)}
    assert G.min()>0
    assert abs(v-v_formula)<2e-5
    assert max(abs(t[key]) for t in transforms for key in ['scalar_residual','spin_residual'])<2e-5
    assert result['q_mass']>0.99999 and result['q_mass']<1.00001
    return result

if __name__=='__main__':
    result=diagnostic()
    (Path(__file__).parent/'construction_diagnostics.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
