from mpmath import mp
mp.dps=60
B=mp.mpf(2);A0=mp.mpf(4)
g=lambda w:(w/mp.sinh(w))**2

def ends(r,A=4,B=2):
 d=mp.sqrt((r*r+A)**2-4*B*r*r)
 s=mp.sqrt((r*r+A+d)/2);p=mp.sqrt(B)*r/s
 return p,s

def dual(r,A=4,B=2):
 p,s=ends(r,A,B)
 la,mu,nu=mp.lu_solve(mp.matrix([[w*w,2*w**4,1] for w in [p,r,s]]),mp.matrix([-w**3*g(w) for w in [p,r,s]]))
 return la,mu,nu

def J(r,A=4,B=2):
 p,s=ends(r,A,B)
 return mp.quad(g,[0,p])+mp.quad(g,[r,s])

if __name__=='__main__':
 rt=mp.findroot(lambda r:dual(r)[1],(4,6))
 print('transition_r',mp.nstr(rt,50),'C',mp.nstr(2/rt**2,50),'dual',list(map(lambda v:mp.nstr(v,30),dual(rt))))
 for cs in ['.25','.1','.05','.02','.01','.001']:
  C=mp.mpf(cs);r0=mp.sqrt(2/C)
  print('CAP',C,'r0',r0,'Jpend',J(r0),'dualpend',dual(r0))
  if dual(r0)[1]<0:
   rr=mp.findroot(lambda r:dual(r,B+C*r*r,B)[1],(mp.mpf(4.5),mp.mpf(6)))
   Ae=B+C*rr*rr
   print(' RELAX',rr,'Ae',Ae,'J',J(rr,Ae,B),'dual',dual(rr,Ae,B))
   for L in [10,20,100]:
    delta=A0-Ae;bb=B/(1+delta/L**2);aa=Ae
    Tin=1/B+C/2
    dd=Tin-1/bb+delta/(L**2*(L**2+delta))
    if dd<=0:
     print(' L',L,'INFEASIBLE: inverse-moment denominator nonpositive');continue
    r2=(aa-bb)/(bb*dd)
    rrL=mp.sqrt(r2);pp,ss=ends(rrL,aa,bb)
    if ss>=L:
     print(' L',L,'INFEASIBLE: high band does not strictly follow low bands');continue
    jj=J(rrL,aa,bb)+mp.quad(g,[L,mp.sqrt(L**2+delta)])
    print(' L',L,'r',rrL,'bands',pp,ss,'J',jj,'saving',J(r0)-jj)
