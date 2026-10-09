"""New finite-p checks on the frozen complex physical fixture; stdout only."""
import json
import math
import numpy as np
import check_nonreversible_entropy_gram as m

rows=[]
for p in [1.2,1.5,2.,3.,7.]:
    r=1/p;a=.5-r
    sa=np.diag(m.svals**a);sma=np.diag(m.svals**(-a))
    h=sa@m.power(m.rho,r)@sa
    g=sma@m.power(m.rho,1-r)@sma
    direct=float(np.trace(g@m.H(h)).real)
    gram=0j
    def kernel(x,y):
        z=(x+y)/2;hh=(x-y)/2
        if abs(hh)<1e-12:
            return (1-r)*np.exp(-z)+r*np.exp(z)-np.exp((2*r-1)*z)
        return (np.exp(-z)*np.sinh(2*(1-r)*hh)+np.exp(z)*np.sinh(2*r*hh))/np.sinh(2*hh)-np.exp((2*r-1)*z)
    for i in range(4):
        for k in range(4):
            beta=math.log(m.q[i]/m.q[k]);v=np.array([part[i,k] for part in m.coeff])
            x=[beta-w for w in m.freq]
            mat=np.array([[kernel(xx,yy) for yy in x] for xx in x])
            gram+=m.q[i]*m.q[k]*np.vdot(v,mat@v)
    eta=math.tan(math.pi*min(r,1-r)/2)
    row={'p':p,'T_direct':direct,'T_gram':float(gram.real),'imag':float(gram.imag),
         'error':float(abs(direct-gram)),'candidate_gap':direct-eta*m.e}
    assert row['error']<1e-10
    assert row['candidate_gap']>-1e-10
    rows.append(row)
print(json.dumps({'scope':'Five fixed finite-p identity controls, not a proof of the universal comparison','checks':rows},indent=2))
