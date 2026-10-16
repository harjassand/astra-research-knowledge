from pathlib import Path
from fractions import Fraction as F
import numpy as np,json
root=Path(__file__).parent
z=np.load(root/'cubic_fe_N12_s0_best.npz');v=z['phi'];N=int(z['N']);R=F(25,2)
for denominator in [20,50,100,200,500,1000]:
 a0=np.rint(v/np.max(abs(v))*denominator).astype(int)
 field=[[[F(int(a0[c,x,y]),denominator) for y in range(N)] for x in range(N)] for c in range(2)]
 A=C=Q=det=F(0);mean=[F(0) for _ in range(4)]
 for x in range(N):
  for y in range(N):
   o=[field[c][x][y] for c in range(2)];xx=[field[c][(x+1)%N][y] for c in range(2)];yy=[field[c][x][(y+1)%N] for c in range(2)];xy=[field[c][(x+1)%N][(y+1)%N] for c in range(2)]
   for direction in [0,1]:
    dx=[N*R*(xx[c]-o[c] if direction==0 else xy[c]-yy[c]) for c in range(2)]
    dy=[N*(xy[c]-xx[c] if direction==0 else yy[c]-o[c]) for c in range(2)]
    a,b,c,d=dx[0],dy[0],dx[1],dy[1];u=a*a+c*c;j=a*d-b*c;q=2*a+d
    A+=((a-d)**2+(b+c)**2)**2/8+j*j+u*j
    C+=u*(a+d)+2*j*q;Q+=q*q+c*c;det+=j
    for i,w in enumerate([a,b,c,d]):mean[i]+=w
 count=2*N*N;A/=count;C/=count;Q/=count;det/=count;mean=[w/count for w in mean]
 ratio=C*C/(4*A*Q)
 print(denominator,float(ratio),det,mean,flush=True)
 if ratio>F(2,3):
  result={'schema':'astra-exact-compatible-resonance/1','status':'POSITIVE_JENSEN_NOT_COUNTEREXAMPLE','N':N,'coordinate_x_scale':str(R),'node_denominator':denominator,'nodes':a0.tolist(),'triangulation':'diagonal (x,y) to (x+1,y+1); lower and upper triangles','A4':str(A),'C3':str(C),'Q2':str(Q),'ratio':str(ratio),'optimized_conformal_background':str(-C/(2*Q)),'optimized_Jensen_gap':str(A-C*C/(4*Q)),'mean_gradient':[str(w) for w in mean],'mean_determinant':str(det)}
  (root/'exact_resonance_fixture.json').write_text(json.dumps(result,indent=2));break
