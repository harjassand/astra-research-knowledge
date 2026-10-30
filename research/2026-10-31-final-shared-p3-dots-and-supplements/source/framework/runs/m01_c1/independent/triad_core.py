import sys
sys.dont_write_bytecode=True
import sympy as S

def moments(zs,ws):
    zs=[S.Matrix(z) for z in zs];ws=[S.Matrix(w) for w in ws]
    rr=[(z.T*z)[0] for z in zs];tt=[(w.T*w)[0] for w in ws]
    H=S.zeros(4);H[:2,:2]=2*sum(tt)*S.eye(2)
    H[:2,2:]=4*sum((zs[j]*ws[j].T for j in range(3)),S.zeros(2));H[2:,:2]=H[:2,2:].T
    H[2:,2:]=2*sum(rr[j]+tt[j] for j in range(3))*S.eye(2)+4*sum((ws[j]*ws[j].T for j in range(3)),S.zeros(2))
    vv=S.zeros(4,1);ww=S.zeros(4,1);ff=0;cc=0
    for j in range(3):
        k,l=[ii for ii in range(3) if ii!=j]
        vv[:2,0]+=2*zs[j]*(ws[k].dot(ws[l]))
        vv[2:,0]+=2*ws[j]*(zs[k].dot(zs[l])+ws[k].dot(ws[l]))
        u,v=ws[j];x,y=zs[j]
        ww[:2,0]+=S.Matrix([u*u-v*v,2*u*v])/2
        ww[2:,0]+=S.Matrix([[x,y],[y,-x]])*ws[j]
        cc+=S.Rational(1,2)*(zs[j][0]*(ws[k][0]*ws[l][0]-ws[k][1]*ws[l][1])+zs[j][1]*(ws[k][0]*ws[l][1]+ws[k][1]*ws[l][0]))
        ff+=S.Rational(3,8)*(tt[j]**2+2*rr[j]*tt[j])
    for i in range(3):
        for j in range(i+1,3):
            ff+=S.Rational(1,4)*(2*tt[i]*tt[j]+4*ws[i].dot(ws[j])**2+2*rr[i]*tt[j]+2*rr[j]*tt[i]+8*zs[i].dot(zs[j])*ws[i].dot(ws[j]))
    qq=S.Rational(3,32)*sum(rr[j]+tt[j] for j in range(3))
    N=H.row_join(vv).row_join(ww)
    N=N.col_join(vv.T.row_join(S.Matrix([[2*ff,cc]])))
    N=N.col_join(ww.T.row_join(S.Matrix([[cc,2*qq]])))
    return N.applyfunc(S.expand)

def conformal(output,k):
    a,b=output;c,d=k
    return S.Matrix([a*c+b*d,b*c-a*d]),S.Matrix([a*c-b*d,b*c+a*d])
