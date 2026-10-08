"""All-weight symbolic attempt from the exact support active-set cones.

This performs no numerical weight evaluations and no additional SDPs.
It asks whether the explicit dual's necessary block determinants have
nonnegative polynomial coefficients after a sorted-cone parametrization.
Negative coefficients are retained as a failed certificate, not as a
refutation of PSD.
"""
from pathlib import Path
import json,time
import sympy as s

OUT=Path(__file__).resolve().parent
p,q,r=s.symbols('p q r',nonnegative=True)

def symblock(w,K,i):
    j,k=[a for a in range(3) if a!=i]
    d=[5*K[i],3*K[i]+2*K[j],K[i]+4*K[j],3*K[i]+2*K[k],K[i]+4*K[k]]
    M=s.diag(*d)
    for a,b,v in [(0,2,-5*s.sqrt(2)*w[k]),(1,2,-5*s.sqrt(2)*w[k]),(0,4,-5*s.sqrt(2)*w[j]),(3,4,-5*s.sqrt(2)*w[j]),(2,4,-5*w[i])]:M[a,b]=M[b,a]=v
    return M[[0,1,3,2,4],[0,1,3,2,4]]

def oddblock(w,K):
    M=s.diag(*[2*K[i]+sum(K) for i in range(3)])
    for i in range(3):
        for j in range(i+1,3):M[i,j]=M[j,i]=-5*w[3-i-j]
    return M

def check(poly):
    P=s.Poly(s.expand(poly),p,q,r)
    negative=[{'powers':list(v),'coefficient':str(c)} for v,c in P.terms() if c<0]
    positive=[{'powers':list(v),'coefficient':str(c)} for v,c in P.terms() if c>0]
    return {'polynomial':str(P.as_expr()),'degree':P.total_degree(),'nonnegative_coefficients':not negative,'negative_terms':negative,'positive_terms':positive,'term_count':len(P.terms())}

def run():
    cones=[
        ('A_allactive',[2*p+3*q+r,p+3*q+r,p+2*q+r],None),
        ('B1_twoactive',[2*p+2*q+r,p+q+r,p],None),
        ('B2_twoactive',[2*p+3*q+r,p+3*q+r,p+2*q],None),
        ('C_oneactive',[2*p+2*q+r,p+q,p],None),
    ]
    report={'method':'Exact polynomial coefficient signs on four simplicial sorted support cones; no new numerical weight cases','dual':'5D=3KA+KB+KC-5W','cones':[]}
    for name,a,_ in cones:
        started=time.perf_counter()
        if name.startswith('A'):z=[a[1]+a[2]-a[0],a[0]+a[2]-a[1],a[0]+a[1]-a[2]]
        elif name.startswith('B'):z=[s.Rational(2,3)*(2*a[1]-a[0]),s.Rational(2,3)*(2*a[0]-a[1]),s.Rational(2,3)*(a[0]+a[1])]
        else:z=[s.Integer(0),a[0],a[0]]
        w=[x*x for x in a];K=[sum(w)-w[i]+z[i]**2 for i in range(3)]
        rec={'name':name,'a':[str(x) for x in a],'z':[str(s.expand(x)) for x in z],'K':[str(s.expand(x)) for x in K],'minors':{}}
        for i in range(3):
            M=symblock(w,K,i)
            for n in [4,5]:
                P=check(M[:n,:n].det(method='domain-ge'))
                rec['minors'][f'parity{i+1}_leading{n}']=P
                print(name,f'parity{i+1}_leading{n}',P['nonnegative_coefficients'],'negative',len(P['negative_terms']),'terms',P['term_count'],flush=True)
        M=oddblock(w,K)
        for n in [2,3]:
            P=check(M[:n,:n].det(method='domain-ge'))
            rec['minors'][f'odd_leading{n}']=P
            print(name,f'odd_leading{n}',P['nonnegative_coefficients'],'negative',len(P['negative_terms']),'terms',P['term_count'],flush=True)
        rec['seconds']=time.perf_counter()-started
        report['cones'].append(rec)
        (OUT/'triaxial_symbolic_certificate.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':run()
