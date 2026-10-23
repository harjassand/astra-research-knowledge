# Preserved source of the exploratory scalar command, not rerun on saving.
from decimal import Decimal, localcontext
import time
c0=time.process_time()
with localcontext() as ctx:
    ctx.prec=70
    D=Decimal
    r=(-D(1)).exp()
    def F(c): return c*((1-c).ln()*(1-c)/c).exp()
    lo=D('0.01'); hi=D('.99')
    for _ in range(240):
        m=(lo+hi)/2
        if F(m)<r: lo=m
        else: hi=m
    c=(lo+hi)/2
    h=D('.001'); H=-h*h.ln()-(1-h)*(1-h).ln(); delta=(-(1+H)/(1-h)).exp()
    theta=D('.05'); f=F(D('.5'))
    rho=(1+D('0.5')*(1-delta)*(theta*D(2).ln()).exp()+D('.5')*((1-theta)*(1+f).ln()+theta*D(2).ln()).exp())/2
    print({'c_star':str(c),'Lambda_new':str(1/c),'delta_h':str(delta),'rho_eta_01_c05':str(rho),'S':str(1+1/(2*(1-rho))),'cpu_s':time.process_time()-c0})
