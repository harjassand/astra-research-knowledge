"""Exact synthetic two-cycle witness for finite-bath enhancement.

No material parameters are fitted. All chemical rate ratios are R, one
affinity log(R) per signed chemical event, and all bath rates are gamma.
"""
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import json

root=Path(__file__).parent
spec=importlib.util.spec_from_file_location('exact_projection',root/'projection_exact_witnesses.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

def derive(u=F(1,10),v=F(1000),w=F(10),z=F(100),R=F(100),gamma=F(1)):
    DA=u*gamma+u*v+v*gamma/R
    DB=w*z/R+w*gamma/R+gamma*z
    ra=(v*gamma+(u/R)*(gamma+v))/DA
    re=(gamma*(u+v/R)+u*v/R**2)/DA
    rb=(w*(z+gamma)+gamma*z/R)/DB
    rc=(gamma*w+(w/R+gamma)*z/R)/DB
    x=1/(1+2*ra+re+rb+rc)
    IA=gamma*x*u*v*(1-1/R**2)/DA
    IB=gamma*x*w*z*(1-1/R**2)/DB
    J=2*(IA+IB)
    Ainf=(v+u/R)/(u+v/R)
    Binf=(w+z/R)/(w/R+z)
    xinf=1/(2+2*Ainf+2*Binf)
    JAinf=xinf*u*v*(1-1/R**2)/(u+v/R)
    JBinf=xinf*w*z*(1-1/R**2)/(w/R+z)
    Jinf=2*(JAinf+JBinf)
    edges=[(1,4,u,u/R,1),(5,1,v,v/R,1),(4,2,w,w/R,1),(3,4,z,z/R,1)]
    inp={'states':3,'gamma':str(gamma),'R':str(R),'edges':[[a,b,str(c),str(d),r] for a,b,c,d,r in edges]}
    exact=mod.evaluate(inp)
    assert F(exact['J']['fraction'])==J
    assert F(exact['Jth']['fraction'])==Jinf
    expected=[x*ra,x*ra,x*rb,x*rc,x,x*re]
    assert [F(p) for p in exact['pi']]==expected
    exact['closed_form']={key:{'fraction':str(val),'decimal':float(val)} for key,val in {
        'D_A':DA,'D_B':DB,'p_d':x,'I_A':IA,'I_B':IB,
        'p_d_infinite_bath':xinf,'I_A_infinite_bath':JAinf,'I_B_infinite_bath':JBinf,
        'actual_A_occupancy':2*ra*x,'thermal_A_occupancy':2*Ainf*xinf,
        'actual_B_occupancy':(rb+rc)*x,'thermal_B_occupancy':2*Binf*xinf,
    }.items()}
    return exact

if __name__=='__main__':
    result=derive()
    (root/'projection_two_cycle_witness_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['J','Jth','gain','gain_bound_max','closed_form']},indent=2))
