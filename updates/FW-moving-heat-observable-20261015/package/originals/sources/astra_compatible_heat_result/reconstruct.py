"""Independent reconstruction of the displayed N850 rational certificate.
Data manually transcribed from GitHub source ranges; equality is checked below.
Not a byte-for-byte copy of the source JSON. Requires SymPy.
"""
import sympy as s, json
from itertools import combinations_with_replacement as cwr, combinations
from pathlib import Path
R=s.Rational
C=s.zeros(24,18)
rows=[{0:1},{5:-1,10:1,13:-1},{14:-1},{1:1},{3:1,7:-1,16:-1},{5:R(2,3),10:-R(2,3),17:-1},{2:1},{3:1},{5:R(2,3),8:1,10:-R(2,3)},{4:1},{5:1},{11:1},{6:1},{7:1},{8:1},{9:1},{10:1},{11:1},{12:1},{13:1},{14:1},{15:1},{16:1},{17:1}]
for i,row in enumerate(rows):
 for j,v in row.items(): C[i,j]=v
S=s.Matrix([[R(x) for x in row.split()] for row in '''
523979/10000 0 0 709409/40000 220727/10000 0 0 4223/200 0 208309/7500 0 111139/30000 -426039/10000 0 -379297/20000 0 390077/20000 0
0 523979/30000 63299/10000 0 0 -56919/8000 35787/5000 0 -51093/20000 0 -18219/2500 0 0 4277/800 0 -142013/10000 0 -88499/5000
0 63299/10000 14691/1250 0 0 136153/40000 142013/10000 0 1612477/120000 0 36693/10000 0 0 -55049/10000 0 -55341/10000 0 2121/2500
709409/40000 0 0 419699/20000 804071/40000 0 0 473/25 0 97519/5000 0 67377/20000 -180007/10000 0 -13807/2000 0 250937/20000 0
220727/10000 0 0 804071/40000 93043/2500 0 0 204507/10000 0 426039/10000 0 62701/4000 -199303/10000 0 -65267/20000 0 90003/5000 0
0 -56919/8000 136153/40000 0 0 191851/10000 26731/5000 0 453493/20000 0 17207/800 0 0 -214939/20000 0 1101/200 0 17591/1000
0 35787/5000 142013/10000 0 0 26731/5000 523979/30000 0 712597/40000 0 55189/10000 0 0 -71149/10000 0 -31649/5000 0 48791/20000
4223/200 0 0 473/25 204507/10000 0 0 395761/20000 0 228837/10000 0 77219/20000 -36699/2000 0 -18489/2500 0 52409/5000 0
0 -51093/20000 1612477/120000 0 0 453493/20000 712597/40000 0 96957/2500 0 514729/20000 0 0 -957/50 0 20509/20000 0 123461/5000
208309/7500 0 0 97519/5000 426039/10000 0 0 228837/10000 0 523979/10000 0 189649/10000 -27591/1250 0 -18523/5000 0 177351/10000 0
0 -18219/2500 36693/10000 0 0 17207/800 55189/10000 0 514729/20000 0 284251/10000 0 0 -65353/5000 0 11541/2000 0 17591/1000
111139/30000 0 0 67377/20000 62701/4000 0 0 77219/20000 0 189649/10000 0 15309/1250 -16317/5000 0 -989/5000 0 34517/5000 0
-426039/10000 0 0 -180007/10000 -199303/10000 0 0 -36699/2000 0 -27591/1250 0 -16317/5000 93043/2500 0 9797/625 0 -100509/5000 0
0 4277/800 -55049/10000 0 0 -214939/20000 -71149/10000 0 -957/50 0 -65353/5000 0 0 47963/2500 0 -17019/5000 0 -422511/20000
-379297/20000 0 0 -13807/2000 -65267/20000 0 0 -18489/2500 0 -18523/5000 0 -989/5000 9797/625 0 15309/1250 0 -67377/20000 0
0 -142013/10000 -55341/10000 0 0 1101/200 -31649/5000 0 20509/20000 0 11541/2000 0 0 -17019/5000 0 14691/1250 0 53041/4000
390077/20000 0 0 250937/20000 90003/5000 0 0 52409/5000 0 177351/10000 0 34517/5000 -100509/5000 0 -67377/20000 0 209851/10000 0
0 -88499/5000 2121/2500 0 0 17591/1000 48791/20000 0 123461/5000 0 17591/1000 0 0 -422511/20000 0 53041/4000 0 45927/1250
'''.strip().splitlines()])
W=s.Matrix([[R(x) for x in row.split()] for row in '''
379297/10000 0 0 -692801/10000 530413/20000 311371/5000 0 712597/20000 0 19594/625
788811/20000 0 0 -689599/10000 121253/4000 344799/5000 0 98601/2500 0 75783/2500
0 10717/2000 22999/10000 0 0 0 -483/100 0 -16477/10000 0
0 -16477/10000 -22999/10000 0 0 0 24149/5000 0 53583/10000 0
373193/10000 0 0 -168827/2500 312321/10000 168827/2500 0 373193/10000 0 312321/10000
356299/10000 0 0 -622741/10000 62701/2000 692803/10000 0 189649/5000 0 53041/2000
'''.strip().splitlines()])
x=s.Matrix(s.symbols('a b c d'));a,b,c,d=x
z=s.Matrix(s.symbols('z0:6'))
B1=s.Matrix([z[0],z[1],z[3],z[4]]);B2=s.Matrix([z[1],z[2],z[4],z[5]])
Z=s.kronecker_product(x,z)
u=a*a+c*c;v=b*b+d*d;j=a*d-b*c;w=a*b+c*d
G=3*(u+v-2*j)**2+R(35,24)*u*u+j*j-R(5,2)*j*u
D1=R(4897,5000);D2=R(5103,5000)
mons=s.Matrix([x[i]*x[k] for i,k in cwr(range(4),2)])
pairs=list(combinations(range(4),2));omega_polys=W*mons
O=s.zeros(4)
for (i,k),pol in zip(pairs,omega_polys):O[i,k]=pol;O[k,i]=-pol
Q=C*S*C.T

def heat(F):
 H=s.hessian(F,x)
 return s.expand(D1*(B1.T*H*B1)[0]+D2*(B2.T*H*B2)[0])
def correction(O):return s.expand((B1.T*O*B2)[0])
def verify():
 assert S==S.T
 assert C.rank()==18
 assert s.expand((Z.T*Q*Z)[0]-heat(G)-correction(O))==0
 closed=[s.expand(s.diff(O[k,l],x[i])-s.diff(O[i,l],x[k])+s.diff(O[i,k],x[l])) for i,k,l in combinations(range(4),3)]
 assert all(v==0 for v in closed)
 # alpha=(i_E omega)/4, components sum_i x_i omega_ij /4
 alpha=O.T*x/4
 assert all(s.expand(s.diff(alpha[k],x[i])-s.diff(alpha[i],x[k])-O[i,k])==0 for i,k in pairs)
 L,piv=S.LDLdecomposition(hermitian=False);assert all(v>0 for v in piv.diagonal())
 e=s.eye(18);v1=e[:,0]-e[:,12]+e[:,16];v2=-e[:,13]+e[:,17]
 K=12*D1*v1*v1.T+12*D2*v2*v2.T
 assert s.expand((Z.T*C*K*C.T*Z)[0]-heat((a-d)**4))==0
 T=12*(D1*(v1.T*S.inv()*v1)[0]+D2*(v2.T*S.inv()*v2)[0])
 assert 0<T<2000
 assert all(v>0 for v in (S-K/2000).LDLdecomposition(hermitian=False)[1].diagonal())
 print('Exact identity, closedness, primitive, rank18, 18 positive pivots, rank-two subtraction: PASS')
 print('T diagnostic',float(T))
 return {'identity':True,'closedness':True,'primitive':True,'C_rank':18,'S_positive_pivots':18,'rank_two_update':True,'T_exact':str(T)}
if __name__=='__main__':
 out=verify();Path(__file__).with_name('reconstruction_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
