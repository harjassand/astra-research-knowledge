"""Independent integer Fourier convolution and rational coefficient checks."""
from collections import defaultdict
from fractions import Fraction as F
import json
from pathlib import Path
import numpy as np


def mul(a,b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def moments(a):
    square, det = defaultdict(lambda:[0,0]), defaultdict(lambda:[0,0])
    for k, ak in a.items():
        for l, al in a.items():
            dest = (k[0]+l[0], k[1]+l[1])
            ss = [0,0]
            for j in range(4):
                z = mul(ak[j],al[j]); ss[0]+=z[0]; ss[1]+=z[1]
            dd = mul(ak[0],al[3]); ee = mul(ak[1],al[2])
            square[dest][0] += ss[0]; square[dest][1] += ss[1]
            det[dest][0] += dd[0]-ee[0]; det[dest][1] += dd[1]-ee[1]
    total_square = [0,0]; total_det = [0,0]
    for k, sk in square.items():
        nk = (-k[0],-k[1])
        z = mul(sk,square.get(nk,(0,0)))
        w = mul(sk,det.get(nk,(0,0)))
        total_square[0]+=z[0];total_square[1]+=z[1]
        total_det[0]+=w[0];total_det[1]+=w[1]
    assert total_square[1] == total_det[1] == 0
    mean = [v[0] for v in a[(0,0)]]
    assert all(v[1]==0 for v in a[(0,0)])
    sm = sum(v*v for v in mean)
    dm = mean[0]*mean[3]-mean[1]*mean[2]
    return total_square[0]-sm*sm, total_det[0]-sm*dm


def exact_field(path):
    data = np.load(path)
    u = data['u']; k = int(data['k']); n = u.shape[-1]
    uf = np.fft.fft2(u, axes=(-2,-1))/(n*n)
    denom = 2**20
    def zint(z): return int(round(z.real*denom)),int(round(z.imag*denom))
    a = {(0,0):[(int(round(m*denom)),0) for m in data['mean']]}
    for x in range(-k,k+1):
        for y in range(-k,k+1):
            if not (x>0 or (x==0 and y>0)): continue
            uu = [zint(uf[j,x%n,y%n]) for j in range(2)]
            g = []
            for rr,ii in uu:
                g.extend([(-x*ii,x*rr),(-y*ii,y*rr)])
            a[(x,y)] = g
            a[(-x,-y)] = [(rr,-ii) for rr,ii in g]
    un,vn = moments(a)
    norm = 0
    for mode,g in a.items():
        if mode==(0,0): continue
        ng = a[(-mode[0],-mode[1])]
        for z,w in zip(g,ng):
            zz = mul(z,w);assert zz[1]==0;norm+=zz[0]
    # Critical gamma=2/sqrt(3): E = U-(4 sqrt(3)/3)V.
    assert un>0 and vn>0 and 3*un*un>16*vn*vn
    return dict(denominator=denom, integer_fourier_modes=len(a),
                U_numerator=str(un),V_numerator=str(vn),
                common_denominator=str(denom**4),
                exact_sign_test='U>0,V>0,3U^2>16V^2: strictly positive',
                normalized_energy=float(un/norm**2-4/np.sqrt(3)*vn/norm**2),
                claim='One rationally reconstructed compatible field, at its rounded mean; not a universal bound.')


def main():
    u,v=F(5,9216),F(25,288)
    checks = {
        'B_exp_r1': -F(1,2)+F(1,10) <= -F(1,4),
        'B_exp_r2': -F(15,16)+7*u+3*v+F(1,180) <= -F(1,4),
        'B_log_r1': F(2,3)-F(2,10) >= F(1,3),
        'B_log_r2': F(4,3)-F(21,4)*u-4*v-F(2,180) >= F(1,3),
        'B_clock': F(49,600)>=F(1,13),
        'C_exp_r3': -F(1,2)+F(7,270) <= -F(1,4),
        'C_exp_r4': -F(7,8)+F(31,480) <= -F(1,4),
        'C_log_r3': F(1,2)-F(9,270) >= F(1,3),
        'C_log_r4': 1-F(35,3*480) >= F(1,3),
        'C_clock': F(49,300)>=F(1,7),
    }
    assert all(checks.values())
    # Exact compatible single-wave negative control at gamma=6/5.
    control={(0,0):[(20,0),(0,0),(0,0),(36,0)],
             (1,0):[(5,0),(0,0),(0,0),(0,0)],
             (-1,0):[(5,0),(0,0),(0,0),(0,0)]}
    un,vn=moments(control)
    neg=F(5*un-12*vn,5*20**4)
    assert neg==-F(117,3200)
    root=Path('outputs/capability_first_20261101')
    result=dict(rational_boundary_coefficients=checks,
                exact_non_roc_negative_control=str(neg),
                exact_critical_field=exact_field(root/'quartic_k8/best_field.npz'))
    (root/'exact_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()
