"""Construct and certify a neighborhood of the finite two-resonance optimum.

High-precision arithmetic proposes roots; exact rational intervals establish
existence and legality. The general root-count theorem in FAMILY_PROOF.md
owns the all-frequency/global claims. Nine points do not prove a continuum;
the analytic inverse theorem does.
"""
from fractions import Fraction as Q
from pathlib import Path
import mpmath as mp
from intervals import I,full_conductance
from certify_joint_cap import design

HERE=Path(__file__).resolve().parent
mp.mp.dps=75

def propose_h(C,kappa,start=('.055','.075')):
    C=mp.mpf(C.numerator)/C.denominator
    kappa=mp.mpf(kappa.numerator)/kappa.denominator
    def f(h):
        b=1-h
        H=(C*kappa-1+2*h+mp.sqrt((1-2*h-C*kappa)**2-4*C*kappa*h*h))/(2*C)
        k=kappa-H
        m=[mp.mpf(1),h,b];L=mp.matrix(3)
        for j,v in enumerate([H,k],1):
            L[0,0]+=v;L[j,j]+=v;L[0,j]-=v;L[j,0]-=v
        D0=mp.matrix([[L[i,j]/mp.sqrt(m[i]*m[j])for j in range(3)]for i in range(3)])
        Dpi=D0.copy();Dpi[0,0]+=4
        al,_=mp.eigsy(D0);be,_=mp.eigsy(Dpi)
        edges=[mp.sqrt(be[0]),mp.sqrt(al[1]),mp.sqrt(be[1]),mp.sqrt(al[2]),mp.sqrt(be[2])]
        def g(w):return(w/mp.sinh(w))**2
        lm=mp.lu_solve(mp.matrix([[w*w,2*w**4,4*w**6,-1]for w in edges[:4]]),
                       mp.matrix([-w**3*g(w)for w in edges[:4]]))
        w=edges[4]
        return w**3*g(w)+lm[0]*w*w+2*lm[1]*w**4+4*lm[2]*w**6-lm[3]
    return mp.findroot(f,tuple(mp.mpf(s) for s in start))

def main():
    lines=['Exact rational neighborhood certificates; full spectrum integrated.',
           'C | kappa | h interval | J interval | eta interval | nu interval']
    for Cs in ['.049','.05','.051']:
        for Ks in ['23.5','24','24.5']:
            C,kappa=Q(Cs),Q(Ks)
            h=propose_h(C,kappa)
            sc=10**40;center=int(mp.floor(h*sc))
            lo,hi=Q(center-1,sc),Q(center+2,sc)
            left,right=design(lo,C,kappa),design(hi,C,kappa)
            assert left['res'].lo>0>right['res'].hi
            row=design(I(lo,hi),C,kappa)
            assert all(row[k].lo>0 for k in ['h','b','H','k','eta','nu'])
            J=full_conductance(row['edges'])
            lines.append(' | '.join([Cs,Ks,row['h'].decimal(18),J.decimal(18),
                                      row['eta'].decimal(18),row['nu'].decimal(18)]))
    lines += ['PASS: all nine exact root brackets, costs, multiplier signs and',
              'full Bose integrals certified. Globality uses the five-root theorem.']
    text='\n'.join(lines)+'\n'
    (HERE/'CERTIFIED_JOINT_FAMILY.txt').write_text(text)
    print(text)

if __name__=='__main__':main()
