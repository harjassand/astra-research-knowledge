"""Finite exact rational diagnostics; not a formal/general proof."""
import random, json
from pathlib import Path
import sympy as S

def positive_definite(M):
    return all(S.simplify(M[:j,:j].det())>0 for j in range(1,M.rows+1))

def main():
    rng=random.Random(278103)
    checks=0; cases=[]
    for n in (2,3,4,5):
        for trial in range(5):
            kappa=S.Rational(4); g=S.Rational(1,2); b=kappa/4
            A=S.eye(n)/2; C=kappa*S.eye(n)
            for i in range(n-1):
                av=S.Rational(rng.randint(1,3),10)
                cv=S.Rational(rng.randint(1,6),10)
                for M,w in ((A,av),(C,cv)):
                    M[i,i]+=w;M[i+1,i+1]+=w;M[i,i+1]-=w;M[i+1,i]-=w
            amax=max(A[i,i]+sum(abs(A[i,j]) for j in range(n) if j!=i) for i in range(n))
            cmax=max(C[i,i]+sum(abs(C[i,j]) for j in range(n) if j!=i) for i in range(n))
            d=[S.Rational(rng.choice([-160,-31,-15,-7,-5,-3,-1,3,17,90]),4) for _ in range(n)]
            s=[]; ds=[]; dds=[]
            for x in d:
                if x<=-2*b: s.append(-3*b/2);ds.append(0);dds.append(0)
                elif x<-b: s.append(-3*b/2+(x+2*b)**2/(2*b));ds.append((x+2*b)/b);dds.append(1/b)
                else: s.append(x);ds.append(1);dds.append(0)
            H=A-S.I*(C+S.diag(*d));Ht=A-S.I*(C+S.diag(*s));G=Ht.inv()
            B=amax+cmax+3*kappa/8+8*(amax+cmax)**2/(5*kappa)
            count=sum(int(bool(x<-b)) for x in d)
            det=H.det(); dett=Ht.det()
            ratio=S.simplify(dett*S.conjugate(dett)/(det*S.conjugate(det)))
            assert ratio <= (2*B)**(2*count); checks+=1
            Hess=S.zeros(n)
            for i in range(n):
                for j in range(n):
                    Hess[i,j]=-g*ds[i]*ds[j]*S.re(G[i,j]**2)
                Hess[i,i]-=g*dds[i]*S.im(G[i,i])
            beta=224*g/(25*kappa*kappa)
            beta0=64*g/(25*kappa*kappa)
            assert positive_definite(beta*S.eye(n)+Hess);checks+=1
            assert positive_definite(beta0*S.eye(n)-Hess);checks+=1
            for i in range(n):
                assert S.re(G[i,i])>=0 and S.im(G[i,i])>=0;checks+=2
            cases.append(dict(n=n,trial=trial,defect_count=int(count)))
    out={'description':'Finite exact rational Schur/curvature diagnostics; not universal proof verification',
         'cases':len(cases),'assertions':checks,'all_passed':True,'case_metadata':cases}
    (Path(__file__).parent/'exact_algebra_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({k:v for k,v in out.items() if k!='case_metadata'}))
if __name__=='__main__':main()
