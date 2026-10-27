"""Independent high-precision diagnostic, not an interval certificate.

The analytic proof is PROOF.md. The parent owns certified numerical signs.
"""
import mpmath as mp
from pathlib import Path
mp.mp.dps=70

def coefficients(r,A=mp.mpf(4),B=mp.mpf(2)):
    d=mp.sqrt((r*r+A)**2-4*B*r*r)
    s=mp.sqrt((r*r+A+d)/2)
    p=mp.sqrt(B*r*r/(s*s))
    ends=[p,r,s]
    fit=mp.lu_solve(mp.matrix([[x*x,x**4,1] for x in ends]),
                   mp.matrix([-x**5/mp.sinh(x)**2 for x in ends]))
    return ends,list(fit)

def main():
    lines=['FLOATING DIAGNOSTIC ONLY; not a rigorous sign or uniqueness certificate.']
    for label,r in [('target',mp.sqrt(8)),
                    ('a_zero',mp.findroot(lambda x:coefficients(x)[1][1],(5,6))),
                    ('stiff',mp.mpf(6))]:
        ends,fit=coefficients(r)
        lines.append(label)
        for key,val in [('r',r),('k',r*r/2),('C',2/r**2)]+list(zip(['p','r','s'],ends))+list(zip(['lambda','a','nu'],fit)):
            lines.append(f'{key} = {mp.nstr(val,60)}')
    out='\n'.join(lines)+'\n'
    Path(__file__).with_suffix('.txt').write_text(out)
    print(out)
if __name__=='__main__': main()
