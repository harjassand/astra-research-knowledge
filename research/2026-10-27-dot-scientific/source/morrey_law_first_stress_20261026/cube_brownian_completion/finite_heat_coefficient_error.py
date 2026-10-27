from fractions import Fraction as Q
import numpy as np
from damped_arithmetic_primitives import I
def finite_coefficient_errors(M,C,E,mr,ht,k):
 k2=k*k;H1=ht[k2];H2=ht[k2[:,None]+k2[None,:]];H3=ht[k2[:,None,None]+k2[None,:,None]+k2[None,None,:]]
 rel=Q(1,2**36);HI=lambda x:I.div(I.exact(x),I.box(1-rel,1+rel));h1=HI(H1);h2=HI(H2);h3=HI(H3);Ti=I.add(I.exact(M),I.box(-mr,mr));ci=I.mul(tuple(t[2:,2:,2:]for t in Ti),h3);bi=I.div(I.rat(2),I.mul(I.PI,I.exact(k)));bsi={-1:bi,1:I.mul(bi,I.exact((-1.)**(k+1)))}
 def difference(c,box):
  z=I.sub(I.exact(c),box);return Q(float(I.sum_axis(I.exact(np.maximum(abs(z[0]),abs(z[1])).ravel()))[1]))
 cv=difference(C,ci);edge_error=Q();idx=0
 for moving in range(3):
  i,j=[z for z in range(3)if z!=moving];T=tuple(t.transpose(i,j,moving)for t in Ti);CC=tuple(t.transpose(i,j,moving)for t in ci)
  for s in[-1,1]:
   for q in[-1,1]:
    get=lambda i,j:tuple(t[i,j,2:]for t in T)
    L=I.mul(I.add(I.add(get(0,0),I.mul(I.rat(s),get(1,0))),I.add(I.mul(I.rat(q),get(0,1)),I.mul(I.rat(s*q),get(1,1)))),I.rat(Q(1,4)));L1=I.mul(I.add(tuple(t[2:,0,2:]for t in T),I.mul(I.rat(q),tuple(t[2:,1,2:]for t in T))),I.rat(Q(1,2)));L2=I.mul(I.add(tuple(t[0,2:,2:]for t in T),I.mul(I.rat(s),tuple(t[1,2:,2:]for t in T))),I.rat(Q(1,2)))
    x=I.mul(L,h1);term=I.sum_axis(I.mul(tuple(t[:,None]for t in bsi[s]),I.mul(L1,h2)),axis=0);x=I.sub(x,term);term=I.sum_axis(I.mul(tuple(t[:,None]for t in bsi[q]),I.mul(L2,h2)),axis=0);x=I.sub(x,term);term=I.mul(I.mul(tuple(t[:,None,None]for t in bsi[s]),tuple(t[None,:,None]for t in bsi[q])),CC);term=I.sum_axis(I.sum_axis(term,axis=0),axis=0);x=I.add(x,term);edge_error+=difference(E[idx],x);idx+=1
 return cv,edge_error
