from explore_heat import *
a,b,c,d,e,ff=S.symbols('ar ai br bi cr ci',real=True); hh=S.Matrix([a,b,c,d,e,ff]);
LL=S.Matrix([h[0]-h[2]+2*h[4],h[3]-h[5]-2*h[1],h[0]+h[2],h[3]+h[5],h[0]-h[2]-2*h[4],h[3]-h[5]+2*h[1]]).jacobian(h)
K=LL.inv()
LF=S.simplify(K.T*BF*K); LC=S.simplify(K.T*BC*K); LQ=S.simplify(K.T*BQ*K)
if __name__=='__main__':
 print('LF',LF);print('LC',LC);print('LQ',LQ)
