#!/usr/bin/env python3
"""Directed enclosure of a passing-action derivative over a parameter volume.

This encloses the analytic action, not full particle confinement.  The chosen
rectangle covers the source ellipse Q<=1.  kappa=mu/E in [0,kappa_max].
"""
from pathlib import Path
import sys,json,math,time
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'positive_current_operation'/'vendor'))
from mpmath import iv
iv.dps=30


def lower(x):return math.nextafter(float(x.a),-math.inf)
def upper(x):return math.nextafter(float(x.b),math.inf)


def metric_derivative(l,b,c,s,c2):
    t=iv.sqrt(l);d=1+l
    f1=4*t*(1-l)/d**2
    f2=-4*l-8*l/d**2
    g1=4*t/d;g2=2*l+4*l/d
    fp1=2*(1-3*l)/(t*d**2)-8*t*(1-l)/d**3
    fp2=-4-8*(1-l)/d**3
    gp1=2*(1-l)/(t*d**2);gp2=2+4/d**2
    re=2*b+f1*c+f2*c*s;im=g1*s+g2*c2
    rep=fp1*c+fp2*c*s;imp=gp1*s+gp2*c2
    rad=iv.sqrt(re*re+im*im)
    h=t*rad/d
    hp=(1-l)*rad/(2*t*d**2)+t*(re*rep+im*imp)/(d*rad)
    return h,hp


def main():
    start=time.monotonic();nl=8;nb=8;nphi=512;kap=iv.mpf(1)/10
    phi=[]
    for k in range(nphi):
        p=iv.mpf([2*k,2*(k+1)])*iv.pi/nphi
        phi.append((iv.cos(p),iv.sin(p),iv.cos(2*p)))
    dl=iv.mpf(1)/15/nl;db=iv.mpf(1)/5/nb
    records=[];fail=[];hglobal=math.inf
    for i in range(nl):
        l=iv.mpf([iv.mpf(7)/60+i*dl,iv.mpf(7)/60+(i+1)*dl])
        for j in range(nb):
            b=iv.mpf([-iv.mpf(2)/25+j*db,-iv.mpf(2)/25+(j+1)*db])
            total=iv.mpf(0);hmin=math.inf;reason=None
            for c,s,c2 in phi:
                h,hp=metric_derivative(l,b,c,s,c2)
                hmin=min(hmin,lower(h))
                if lower(h)<=upper(kap):reason='passing margin not enclosed';break
                # Uniform bound in kappa: dJ/dlambda = h_lambda F,
                # F=(2-r)/(2 sqrt(1-r)), r=kappa/h, 1<=F<=Fmax.
                ratio=kap/h.a;fmax=(2-ratio)/(2*iv.sqrt(1-ratio))
                factor=iv.mpf([1,fmax.b])
                total+=hp*factor
            if reason:
                fail.append({'lambda_box':i,'beta_box':j,'reason':reason,'h_lower':hmin});continue
            total*=2*iv.pi/nphi
            row={'lambda_box':i,'beta_box':j,'action_derivative_lower':lower(total),'action_derivative_upper':upper(total),'h_lower':hmin}
            records.append(row);hglobal=min(hglobal,hmin)
            if row['action_derivative_lower']<=0:fail.append(row)
        print(json.dumps({'completed_lambda_strips':i+1,'total':nl,'failed_boxes':len(fail)}),flush=True)
    result={'status':'ENCLOSED' if not fail else 'NOT_ENCLOSED','lambda_box_count':nl,'beta_box_count':nb,'phi_interval_count':nphi,'kappa_interval':[0,.1],
            'label_rectangle':[[7/60,11/60],[-.08,.12]],'ellipse_covered':'Q=900(lambda-.15)^2+100(beta-.02)^2<=1',
            'minimum_action_derivative_lower_bound':min((r['action_derivative_lower'] for r in records),default=None),
            'minimum_h_lower_bound':hglobal,'failed_boxes':fail,'box_bounds':records,'runtime_seconds':time.monotonic()-start,
            'scope':'Passing guiding-center transit action J=integral sqrt(h^2-kappa*h) dphi at E=1/2. No full-orbit, finite-epsilon, perturbation or plasma confinement theorem is claimed.'}
    (ROOT/'passing_action_interval.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='box_bounds'},indent=2))


if __name__=='__main__':main()
