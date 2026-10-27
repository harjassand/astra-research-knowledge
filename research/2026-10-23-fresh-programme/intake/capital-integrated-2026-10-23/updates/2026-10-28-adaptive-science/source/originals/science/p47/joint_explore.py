from mpmath import mp
mp.dps=65
C=mp.mpf(1)/20;KAP=mp.mpf(1001)/50

def design(delta,H):
 A=4-delta;B=2*H/(H+delta)
 t=(A-B)/(B*((1+C)/2-1/B+delta/(H*(H+delta))))
 disc=mp.sqrt((t+A)**2-4*B*t)
 s2=(t+A+disc)/2;p2=B*t/s2
 c=(B*t+(t+A)*(H+delta)-t*H)/4
 kap=t+H-c
 edges=[mp.sqrt(p2),mp.sqrt(t),mp.sqrt(s2),mp.sqrt(H),mp.sqrt(H+delta)]
 return edges,kap

def fit(edges):
 g=lambda w:(w/mp.sinh(w))**2
 e=edges[:4]
 nu,la,a,b=mp.lu_solve(mp.matrix([[1,w*w,w**4,w**6] for w in e]),mp.matrix([-w**3*g(w) for w in e]))
 last=edges[4];res=last**3*g(last)+nu+la*last**2+a*last**4+b*last**6
 return res,(nu,la,a,b)

def objective(edges):
 g=lambda w:(w/mp.sinh(w))**2
 p,r,s,u,v=edges
 return mp.quad(g,[0,p])+mp.quad(g,[r,s])+mp.quad(g,[u,v])

if __name__=='__main__':
 delta,H=mp.findroot(lambda de,h:(design(de,h)[1]-KAP,fit(design(de,h)[0])[0]),(.007,75))
 e,kap=design(delta,H);res,dual=fit(e)
 print('delta,H',mp.nstr(delta,55),mp.nstr(H,55))
 print('edges',*[mp.nstr(w,45) for w in e])
 print('dual nu lambda a b',*[mp.nstr(w,45) for w in dual]);print('res',res,'kap',kap)
 print('J',mp.nstr(objective(e),55))
 nu,la,a,b=dual
 for n in range(12):
  d=lambda j:mp.mpf(2)**(2*j-1)/mp.factorial(2*j) if j>=1 else mp.mpf(0)
  cf=nu*d(n+1)+la*d(n)+a*d(n-1)+b*d(n-2)
  print(n,mp.nstr(cf,30))
