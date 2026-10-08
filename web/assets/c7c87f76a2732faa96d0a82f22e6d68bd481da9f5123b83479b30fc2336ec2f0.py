"""Exact symbolic certificate for the derived 3:1:1 one-body dual.

No channel optimization or new finite weights. This evaluates polynomial
positivity on the three support-active regions for every axial t>=0.
"""
from pathlib import Path
import json
import sympy as s

OUT=Path(__file__).resolve().parent
t=s.symbols('t',nonnegative=True)

def symblock(w,K,i):
    j,k=[a for a in range(3) if a!=i]
    # 5 D_corr; sign flip on yj,yk makes all off-diagonal entries <=0.
    d=[5*K[i],3*K[i]+2*K[j],K[i]+4*K[j],3*K[i]+2*K[k],K[i]+4*K[k]]
    M=s.diag(*d)
    for a,b,v in [(0,2,-5*s.sqrt(2)*w[k]),(1,2,-5*s.sqrt(2)*w[k]),(0,4,-5*s.sqrt(2)*w[j]),(3,4,-5*s.sqrt(2)*w[j]),(2,4,-5*w[i])]:
        M[a,b]=v;M[b,a]=v
    # Reorder the three leaves first, giving positive first three pivots.
    return M[[0,1,3,2,4],[0,1,3,2,4]]

def oddblock(w,K):
    M=s.diag(*[2*K[i]+sum(K) for i in range(3)])
    for i in range(3):
        for j in range(i+1,3):
            k=3-i-j;M[i,j]=M[j,i]=-5*w[k]
    return M

def sign_certificate(p,lo,hi,probe):
    p=s.Poly(s.expand(p),t)
    content,factors=s.factor_list(p.as_expr(),t)
    records=[]
    sign=s.sign(content)
    for f,n in factors:
        q=s.Poly(f,t)
        roots=q.count_roots(lo,hi)
        value=q.eval(probe)
        # Even powers are globally nonnegative. Odd factors must have
        # no roots throughout the interval and a certified probe sign.
        if n%2:
            if roots!=0:
                raise AssertionError((p.as_expr(),f,n,lo,hi,roots))
            if value==0:raise AssertionError('zero probe')
            sign*=s.sign(value)
        records.append({'factor':str(f),'multiplicity':n,'interval_real_root_count':int(roots),'probe_value':str(value),'even_power':bool(n%2==0)})
    assert sign>0
    return {'polynomial':str(p.as_expr()),'factorization':str(s.factor(p.as_expr())),'content':str(content),'factors':records,'nonnegative_proved':True}

def run():
    w=[t*t,s.Integer(1),s.Integer(1)]
    regions=[('small',[s.Rational(4,3),s.Rational(2,3),s.Rational(2,3)],s.Integer(0),s.Rational(2,3),s.Rational(1,2)),('middle',[2-t,t,t],s.Rational(2,3),s.Integer(2),s.Rational(5,4)),('large',[s.Integer(0),t,t],s.Integer(2),s.oo,s.Integer(3))]
    report={'hypothesis':'Dcorr=(3/5)(L+G)A+(1/5)((L+G)B+(L+G)C)-W is PSD for every axial w=(t^2,1,1),t>=0','method':'Exact rational factorization and Sturm root counts for leading minors; no new channel SDP cases.','regions':[]}
    for name,z,lo,hi,probe in regions:
        K=[sum(w)-w[i]+z[i]**2 for i in range(3)]
        record={'name':name,'z':[str(a) for a in z],'K':[str(s.expand(a)) for a in K],'interval':[str(lo),str(hi)],'probe':str(probe),'minors':{}}
        for i in [0,1]:
            M=symblock(w,K,i)
            record[f'block_{i+1}']=[[str(a) for a in row] for row in M.tolist()]
            for q in [4,5]:
                p=s.factor(M[:q,:q].det(method='domain-ge'))
                certificate=sign_certificate(p,lo,hi,probe)
                record['minors'][f'parity{i+1}_leading{q}']=certificate
                print(name,f'parity{i+1}_leading{q}',certificate['factorization'],flush=True)
        M=oddblock(w,K)
        record['odd_block']=[[str(a) for a in row] for row in M.tolist()]
        for q in [2,3]:
            p=s.factor(M[:q,:q].det(method='domain-ge'))
            certificate=sign_certificate(p,lo,hi,probe)
            record['minors'][f'odd_leading{q}']=certificate
            print(name,f'odd_leading{q}',certificate['factorization'],flush=True)
        report['regions'].append(record)
    (OUT/'axial_exact_certificate.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':run()
