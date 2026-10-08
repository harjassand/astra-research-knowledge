# Independent time-domain RK4 cross-check of the closed-form matrix-exponential witness.
from math import exp
EDGES = [(0,1),(1,2),(2,0)]
def phases(A, delta):
    Es = [[0.,-A,0.],[0.,0.,-A],[-A,0.,0.]]
    Bs = [[0.,delta,delta],[delta,0.,delta],[delta,delta,0.]]
    return Es,Bs
def rates(E,B):
    out=[]
    for e,(i,j) in enumerate(EDGES):
        out.append((i,j,exp(-(B[e]-E[i])),exp(-(B[e]-E[j]))))
    return out
def step_rk4(y, rs, h):
    def rhs(y):
        d=[0.]*6
        p=y[:3]
        for e,(i,j,kij,kji) in enumerate(rs):
            je=kij*p[i]-kji*p[j]
            d[i]-=je; d[j]+=je
            d[3+e]=je
        return d
    k1=rhs(y)
    k2=rhs([y[i]+h*k1[i]/2 for i in range(6)])
    k3=rhs([y[i]+h*k2[i]/2 for i in range(6)])
    k4=rhs([y[i]+h*k3[i] for i in range(6)])
    return [y[i]+h*(k1[i]+2*k2[i]+2*k3[i]+k4[i])/6 for i in range(6)]
def cycle(p,A,delta,tau,steps):
    Es,Bs=phases(A,delta)
    Work=0.; flux=[0.]*3
    Eprev=Es[-1]
    for E,B in zip(Es,Bs):
        Work+=sum(p[i]*(E[i]-Eprev[i]) for i in range(3))
        y=p+[0.]*3
        rs=rates(E,B)
        h=tau/steps
        for _ in range(steps): y=step_rk4(y,rs,h)
        p=y[:3]
        flux=[flux[i]+y[3+i] for i in range(3)]
        Eprev=E
    return p,flux,Work
if __name__=='__main__':
    A=4.; tau=1.; delta=.01
    p=[1/3]*3
    for n in range(1000):
        pn,F,W=cycle(p,A,delta,tau,1000)
        err=sum(abs(pn[i]-p[i]) for i in range(3))
        p=pn
        if err<1e-14: break
    print('RK4 cycles to periodicity:',n+1,'closure L1:',err)
    print('RK4 p_start:',p)
    print('RK4 edge fluxes:',F)
    print('RK4 cycle current:',sum(F)/3)
    print('RK4 state-energy work kBT/cycle:',W)
    print('RK4 work/current kBT/product:',W/(sum(F)/3))
