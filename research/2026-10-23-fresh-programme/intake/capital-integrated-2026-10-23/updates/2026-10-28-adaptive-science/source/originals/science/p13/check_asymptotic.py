"""Executed arbitrary-precision diagnostics for the proved small-C law.

This code checks the full three-band networks, not only a limiting indicator.
It supplements the proof and exact interval certificates; it is not itself
an all-network bound or a finite-precision interval certificate.
"""
from pathlib import Path
import mpmath as mp

mp.mp.dps=85
HERE=Path(__file__).resolve().parent

def g(w):return (w/mp.sinh(w))**2

def tail(a):
    z=mp.exp(-2*a)
    return 2*a*a*z/(1-z)-2*a*mp.log1p(-z)+mp.polylog(2,z)

def J_edges(edges):
    return mp.pi**2/6+sum((-1 if j%2==0 else 1)*tail(a) for j,a in enumerate(edges))

def one(C):
    r=mp.sqrt(2/C);d=mp.sqrt((r*r+4)**2-8*r*r)
    s=mp.sqrt((r*r+4+d)/2);p=mp.sqrt(2*r*r/(s*s))
    return J_edges([p,r,s])

def actual(C,r0):
    b=2*C*r0*r0/(2+C*r0*r0);h=1-b
    H=1/(C*C);k=b*b/(C-h*h/H)
    masses=[mp.mpf(1),h,b];springs=[H,k]
    L=mp.matrix(3)
    for j,spring in enumerate(springs,1):
        L[0,0]+=spring;L[j,j]+=spring;L[0,j]-=spring;L[j,0]-=spring
    D0=mp.matrix([[L[i,j]/mp.sqrt(masses[i]*masses[j]) for j in range(3)]for i in range(3)])
    Dpi=D0.copy();Dpi[0,0]+=4
    alpha,_=mp.eigsy(D0);beta,_=mp.eigsy(Dpi)
    assert abs(alpha[0])<mp.mpf('1e-60')
    edges=[mp.sqrt(beta[0]),mp.sqrt(alpha[1]),mp.sqrt(beta[1]),mp.sqrt(alpha[2]),mp.sqrt(beta[2])]
    assert abs(h*h/H+b*b/k-C)<mp.mpf('1e-75')
    assert abs(sum(beta)-sum(alpha)-4)<mp.mpf('1e-60')
    J=J_edges(edges)
    return dict(J=J,edges=edges,H=H,k=k,h=h,b=b)

def main():
    a=mp.sqrt(2)
    def gain_slope(r):return r*r/(2*(r*r-2))*(a*g(a)-r*g(r))
    r0=mp.findroot(lambda r:mp.diff(gain_slope,r),(5,6))
    sharp=gain_slope(r0);ordinary=g(a)/a;Jrig=J_edges([a])
    lines=['Arbitrary precision 85-decimal diagnostic, every band included.',
           'C | (Jrig-J_two)/C | (Jrig-J_one)/C | H | total stiffness']
    previous=None
    for c in ['.01','.003','.001','.0003','.0001','.00003','.00001']:
        C=mp.mpf(c);row=actual(C,r0)
        sl=(Jrig-row['J'])/C;os=(Jrig-one(C))/C
        if previous is not None:assert abs(sharp-sl)<previous
        previous=abs(sharp-sl)
        lines.append(' | '.join([c,mp.nstr(sl,25),mp.nstr(os,25),
                                 mp.nstr(row['H'],12),mp.nstr(row['H']+row['k'],14)]))
    lines += ['Sharp predicted slope '+mp.nstr(sharp,50),
              'One-pendant predicted slope '+mp.nstr(ordinary,50),
              'PASS: exact compliance and trace checked numerically at high precision;',
              'the actual all-band slopes approach the proved coefficients.']
    text='\n'.join(lines)+'\n'
    (HERE/'ASYMPTOTIC_CHECK.txt').write_text(text)
    print(text)

if __name__=='__main__':main()
