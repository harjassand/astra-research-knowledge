from fractions import Fraction as F
from itertools import combinations

def raw_graph(nsat,armed,aux,all_targets=False,perturb=False):
 n=nsat+1;z=lambda *ix:tuple(ix.count(i)for i in range(n));hs=[z(*e)for e in armed];out=[(z(),z(0),F(1)),(z(0),z(),F(1))]
 for e in armed+aux:h=z(*e);out.extend(((z(0,0),h,F(1)),(h,z(0,0),F(1))))
 incident={v for e in armed for v in e}
 pairs={(x,(x-1)%len(hs))for x in range(1,n)}|{(1,i)for i in range(len(hs))}
 if all_targets:pairs|={(x,i)for x in range(1,n)if x not in incident for i in range(len(hs))}
 for x,i in sorted(pairs):h=hs[i];out.extend(((z(0,x),h,F(1)),(h,z(0,x),F(2 if perturb and x==2 else 1))))
 return out

def production():
 m=24;n=m+3;z=lambda *ix:tuple(ix.count(i)for i in range(n));fs=range(3,n)
 es={tuple(sorted((3+i,3+(i+1)%m)))for i in range(m)}|{(3+i,3+j)for i in range(m)for j in range(i+1,m)if(31*i+17*j)%7<3}|{(3,4),(4,5),(3,5)}
 h=z(1,2);raw=[(z(),z(0),F(1)),(z(0),z(),F(1)),(z(0,0),h,F(1)),(h,z(0,0),F(1))]
 for x in range(1,n):raw.extend(((z(0,x),h,F(1)),(h,z(0,x),F(2 if x==2 else 1))))
 for u,v in sorted(es):raw.extend(((z(0,0),z(u,v),F(1,len(es))),(z(u,v),z(0,0),F(1,len(es)))))
 return raw

def state(r,U,a,balanced,Fcount=0,free_balanced=True):
 x=[0]*r['n'];x[r['a']]=a;vs=r['rare']if balanced else r['rare'][:1];left=U-a
 for i,v in enumerate(vs):x[v]=left//len(vs)+(i<left%len(vs))
 fs=r['free']if free_balanced else r['free'][:1]
 for i,v in enumerate(fs):x[v]=Fcount//len(fs)+(i<Fcount%len(fs))
 return tuple(x)
