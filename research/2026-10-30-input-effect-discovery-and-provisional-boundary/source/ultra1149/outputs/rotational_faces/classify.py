"""Decide the ACTUAL lower quadratic boundary on a complete polynomial face.

The leading part is F_s. Input --cubic and --quadratic JSON coefficient lists
in the monomial orders in certificate.json. No arguments demonstrate a
translated leading quartic plus a DEGNERATE ROC quadratic, not a large
stabilizing multiple of |A|^2. Standard library only.
"""
from fractions import Fraction as R
from pathlib import Path
import json,argparse
from receive import b,add,mul,scale,diff,constant
HERE=Path(__file__).resolve().parent
def monic(p):
    if not p:return {}
    return scale(p,1/p[max(p)])
def divide(p,q):
    assert q;rem=dict(p);quot={};dq=max(e[0] for e in q);lq=q[dq,]
    while rem and max(e[0] for e in rem)>=dq:
        degree=max(e[0] for e in rem)-dq;co=rem[degree+dq,]/lq;quot[degree,]=quot.get((degree,),R(0))+co
        rem=add(rem,scale(mul({(degree,):R(1)},q),-co))
    return quot,rem
def gcd(p,q):
    while q:p,q=q,b.polynomial_rem(p,q)
    return monic(p)
def exactdivide(p,q):
    ans,rem=divide(p,q);assert not rem;return ans
def nonnegative(p):
    if not p:return True
    degree=max(e[0] for e in p)
    if degree%2 or p[degree,]<0:return False
    if degree==0:return True
    p=monic(p);c=gcd(p,diff(p,0));w=exactdivide(p,c);i=1
    while max(e[0] for e in w)>0:
        y=gcd(w,c);part=exactdivide(w,y)
        if i%2 and max(e[0] for e in part)>0 and b.root_count(part)>0:return False
        w=y;c=exactdivide(c,y);i+=1
    return True
def quadratic_ROC(Q):
    aa={};bb={};cc={}
    for e,co in Q.items():
        key=(e[1]+e[3],);output_y=e[2]+e[3];target=(aa,bb,cc)[output_y]
        target[key]=target.get(key,R(0))+co/(2 if output_y==1 else 1)
    determinant=add(mul(aa,cc),scale(mul(bb,bb),-1))
    tests={'first_diagonal':aa,'second_diagonal':cc,'determinant':determinant}
    return all(nonnegative(p) for p in tests.values()),{key:[[e[0],str(c)] for e,c in p.items()] for key,p in tests.items()}
def solve(M,rhs):
    n=len(rhs);a=[list(row)+[rhs[i]] for i,row in enumerate(M)]
    for j in range(n):
        i=next(i for i in range(j,n) if a[i][j]);a[i],a[j]=a[j],a[i];co=a[j][j];a[j]=[v/co for v in a[j]]
        for i in range(n):
            if i!=j:
                co=a[i][j];a[i]=[u-co*v for u,v in zip(a[i],a[j])]
    return [row[-1] for row in a]
def classify(s,cubic=None,quadratic=None):
    s=R(s);assert abs(s)<1 and abs(s)!=R(1,3),'Outside the proved cubic-rigid parameter scope'
    cert=json.loads((HERE/'certificate.json').read_text());cp=cert['cubic_powers'];qp=[tuple(p) for p in __import__('itertools').product(range(3),repeat=4) if sum(p)==2]
    F={tuple(pw):b.evaluate(b.literal(poly,1),[s]) for pw,poly in zip(cert['quartic_powers'],cert['F'])};F={e:c for e,c in F.items() if c}
    trans=[[b.evaluate(b.literal(p,1),[s]) for p in col] for col in cert['translation_cubics']]
    if cubic is None:
        V0=list(map(R,(1,-2,0,1)));cubic=[sum(trans[j][i]*V0[j] for j in range(4)) for i in range(20)]
    cubic=list(map(R,cubic));assert len(cubic)==20
    if quadratic is None:
        assert cubic==[sum(trans[j][i]*R((1,-2,0,1)[j]) for j in range(4)) for i in range(20)],'Supply a quadratic for a nondefault cubic'
        V0=list(map(R,(1,-2,0,1)))
        Q0={(2,0,0,0):R(1),(0,0,0,2):R(1),(1,0,0,1):R(3),(0,1,1,0):R(-1)}
        Q=add(Q0,*(scale(diff(diff(F,i),j),V0[i]*V0[j]/2) for i in range(4) for j in range(4)))
    else:
        quadratic=list(map(R,quadratic));assert len(quadratic)==10;Q={pw:co for pw,co in zip(qp,quadratic) if co}
    indices=cert['translation_minor']['rows'];V=solve([[trans[j][i] for j in range(4)] for i in indices],[cubic[i] for i in indices])
    C={tuple(pw):co for pw,co in zip(cp,cubic) if co}
    if cubic!=[sum(trans[j][i]*V[j] for j in range(4)) for i in range(20)]:
        return {'parameter':str(s),'ROC':False,'QC':False,'reason':'The cubic is outside the exact translation kernel; no lower quadratic can repair it.'}
    Qres=add(Q,*(scale(diff(diff(F,i),j),-V[i]*V[j]/2) for i in range(4) for j in range(4)))
    admitted,tests=quadratic_ROC(Qres)
    return {'parameter':str(s),'translation':list(map(str,V)),
      'normal_form':'F_s(A+V)+Q_reduced(A)+affine; affine terms are immaterial',
      'quadratic_powers':[list(pw) for pw in qp],'reduced_quadratic_coefficients':[str(Qres.get(pw,0)) for pw in qp],
      'ROC':admitted,'QC':admitted,'quadratic_binary_polynomial_tests':tests,
      'nonPC':True if abs(s)>R(1,3) else 'NOT_DECIDED',
      'scope':'Exact entire-face classification at the given rational parameter. Includes weak quadratic boundaries. No all-quartic-neighborhood claim.'}
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--parameter',default='2/3');parser.add_argument('--cubic',type=Path);parser.add_argument('--quadratic',type=Path);args=parser.parse_args()
    print(json.dumps(classify(args.parameter,json.loads(args.cubic.read_text()) if args.cubic else None,json.loads(args.quadratic.read_text()) if args.quadratic else None),indent=2))
if __name__=='__main__':main()
