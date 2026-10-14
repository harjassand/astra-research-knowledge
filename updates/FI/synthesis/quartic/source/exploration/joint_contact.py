import sympy as s
p,r,v=s.symbols('p r v', positive=True);x,y,z,w,t=s.symbols('x y z w t', real=True);V=(x,y,z,w)
f=(p-r)/8;a=p/3;la=(p-3*r)/2;g=v-(p-9*r)/24;be=p*p/(36*r)+3*r/4;de=(p-p*p/(9*r))/4;h=r
i=(x+w)/2;j=(z-y)/2;k=(x-w)/2;l=(z+y)/2
zz=i*i+j*j;ww=k*k+l*l;re=i*k+j*l;im=j*k-i*l
F=s.expand(f*zz**2+be*zz*ww+g*ww**2+de*(re**2-im**2)+a*zz*re+h*ww*re)
H=s.hessian(F,V);M0=s.hessian(H[1,1],V)/2;M1=s.hessian(2*H[0,1],V)/2;M2=s.hessian(H[0,0],V)/2
n=s.Matrix([0,-1,1,0]);U=s.Matrix([[1,0,0],[0,0,1],[0,0,1],[0,1,0]])
C=s.simplify(U.T*M0*U);b=s.simplify(U.T*M1*n);c=(n.T*M2*n)[0]
print('C',C,'det',s.factor(C.det()),'b',b,'c',s.factor(c),sep='\n',flush=True)
S=s.factor(c-(b.T*C.inv()*b)[0]);print('joint second order',S,flush=True)
print('ratio correction numerator',s.factor(S*C.det()),flush=True)
