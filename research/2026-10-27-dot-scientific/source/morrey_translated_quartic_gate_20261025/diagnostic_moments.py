import numpy as np, json
N=512
x=(np.arange(N)+.5)*2*np.pi/N;y=x
u=np.cos(x[:,None]);v=np.cos(y[None,:]);w=np.cos(x[:,None]+y[None,:]);u=np.broadcast_to(u,(N,N));v=np.broadcast_to(v,(N,N))
b=-9+8*u-4*v-4*w;c=2*u-2*v*w-4*v+4*u*w-4*w+4*u*v
rr=2*c/(3*np.sqrt(np.maximum(b*b+32*c,0))-b)
U=u-rr;V=v+2*rr;W=w+2*rr
X=(U+V+2*W)/2;Y=(U-V)/2;Z=W
h2=Y*Y+Z*Z
mean=lambda a:float(np.mean(a))
m={'k':mean(X*X),'CY':[[mean(Y*Y),mean(Y*Z)],[mean(Y*Z),mean(Z*Z)]],'c':[mean(X*Y),mean(X*Z)],'m1':mean(X**3),'m2':mean(X*h2),'m3':[mean(X*X*Y),mean(X*X*Z)],'m4':[mean(h2*Y),mean(h2*Z)],'A4':mean(X**4),'B4':mean(X*X*h2),'C4':mean(h2*h2),'s':mean(rr*rr)}
print(json.dumps(m,indent=2));
for a in [-1,-.9,-.75,-.5,-.25,0,.25,.5,.75,.9,1]:
 al=6*a*a+8*a+2;be=12*(1-a*a);ga=6*a*a-8*a+2
 k=m['k'];CY=np.array(m['CY']);co=np.array(m['c']);
 K=np.zeros((3,3));K[0,0]=k*(6*al+be);K[0,1:]=K[1:,0]=2*be*co;K[1:,1:]=k*(be+2*ga)*np.eye(2)+4*ga*CY
 ell=np.r_[4*al*m['m1']+2*be*m['m2'],2*be*np.array(m['m3'])+4*ga*np.array(m['m4'])]
 const=al*m['A4']+be*m['B4']+ga*m['C4']
 ki=np.linalg.pinv(K,rcond=1e-12);bg=-ki@ell/2;gap=const-ell@ki@ell/4
 print('a',a,'gap',gap,'background',bg.tolist(),'evals',np.linalg.eigvalsh(K).tolist())
open('morrey_translated_quartic_gate_20261025/diagnostic_moments.json','w').write(json.dumps(m,indent=2)+'\n')
