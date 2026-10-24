#!/usr/bin/env python3
"""Exact finite checks of the envelope inequality and full marked-map algebra.

Gaussian-rational arithmetic only. These finite matrices are NOT an oscillator
simulation or an experimental/threshold validation; the all-size Gaussian
skeleton is a separate proof input.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json

@dataclass(frozen=True)
class G:
    re: Q = Q(0)
    im: Q = Q(0)
    @staticmethod
    def of(x):
        return x if isinstance(x, G) else G(Q(x))
    def __add__(self, x):
        x=G.of(x); return G(self.re+x.re,self.im+x.im)
    __radd__=__add__
    def __neg__(self): return G(-self.re,-self.im)
    def __sub__(self,x): return self+-G.of(x)
    def __rsub__(self,x): return G.of(x)+-self
    def __mul__(self,x):
        x=G.of(x); return G(self.re*x.re-self.im*x.im,self.re*x.im+self.im*x.re)
    __rmul__=__mul__
    def conj(self): return G(self.re,-self.im)
    def abs2(self): return self.re*self.re+self.im*self.im
    def __truediv__(self,x):
        x=G.of(x); y=self*x.conj(); d=x.abs2(); return G(y.re/d,y.im/d)
    def __bool__(self): return bool(self.re or self.im)


def zeros(n): return [[G() for _ in range(n)] for _ in range(n)]
def eye(n):
    a=zeros(n)
    for i in range(n): a[i][i]=G.of(1)
    return a

def add(a,b): return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def scale(a,c): return [[x*c for x in row] for row in a]
def sub(a,b): return add(a,scale(b,-1))
def mul(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),G())
             for j in range(len(b[0]))] for i in range(len(a))]
def adj(a): return [[a[j][i].conj() for j in range(len(a))] for i in range(len(a[0]))]
def trace(a): return sum((a[i][i] for i in range(len(a))),G())
def outer(v): return [[x*y.conj() for y in v] for x in v]
def kron(a,b):
    return [[a[i//len(b)][j//len(b)]*b[i%len(b)][j%len(b)]
             for j in range(len(a)*len(b))] for i in range(len(a)*len(b))]

def det(a):
    a=[row[:] for row in a]; ans=G.of(1)
    for k in range(len(a)):
        pivot=next((i for i in range(k,len(a)) if a[i][k]),None)
        if pivot is None: return G()
        if pivot!=k: a[k],a[pivot]=a[pivot],a[k]; ans=-ans
        value=a[k][k]; ans=ans*value
        for i in range(k+1,len(a)):
            c=a[i][k]/value
            for j in range(k+1,len(a)): a[i][j]=a[i][j]-c*a[k][j]
            a[i][k]=G()
    return ans


def assert_psd_principals(a):
    assert a==adj(a)
    checked=0
    for size in range(1,len(a)+1):
        for selected in combinations(range(len(a)),size):
            d=det([[a[i][j] for j in selected] for i in selected])
            assert d.im==0 and d.re>=0,(selected,d)
            checked+=1
    return checked


def partial(rho, da, db, weights):
    return [[sum((weights[n]*rho[n*db+i][n*db+j] for n in range(da)),G())
             for j in range(db)] for i in range(db)]


def phase_gate(d, u):
    out=zeros(2*d)
    phase=G.of(1)
    for n in range(d):
        out[2*n][2*n]=phase
        out[2*n+1][2*n+1]=phase.conj()
        phase=phase*u
    return out


def main():
    # A three-level energy sector entangled with a two-level outside/system.
    vector=[G.of(1),G(0,Q(1)),G.of(2),G(1,-1),G.of(-1),G(0,Q(2))]
    norm=sum((x.abs2() for x in vector),Q(0))
    rho=scale(outer(vector),1/norm)
    energy_weights=[Q(1),Q(4),Q(16)]  # exp(beta E_n), beta=log4.
    qweights=[Q(1),Q(1,2),Q(1,4)]
    z=sum(qweights)
    omega=partial(rho,3,2,energy_weights)
    moment=trace(omega)
    assert moment.im==0 and moment.re>0
    qmat=zeros(3)
    for i,x in enumerate(qweights): qmat[i][i]=G.of(x)
    upper=scale(kron(qmat,omega),z)
    residual=sub(upper,rho)
    minor_count=assert_psd_principals(residual)
    tau=scale(qmat,1/z)
    sigma=scale(omega,1/moment.re)
    assert trace(tau)==G.of(1) and trace(sigma)==G.of(1)
    assert upper==scale(kron(tau,sigma),moment.re*z*z)

    # Exact two-mark inclusion/exclusion, with a selected unmarked contact
    # and a noncommuting system control retained in the intervening unitary.
    u1=phase_gate(3,G(Q(3,5),Q(4,5)))
    u2=phase_gate(3,G(Q(5,13),Q(12,13)))
    ry=[[G(Q(3,5)),G(Q(-4,5))],[G(Q(4,5)),G(Q(3,5))]]
    rotation=kron(eye(3),ry)
    ux=mul(mul(rotation,phase_gate(3,G(Q(8,17),Q(15,17)))),adj(rotation))
    mid=mul(ux,kron(eye(3),[[G(Q(5,13)),G(Q(-12,13))],
                              [G(Q(12,13)),G(Q(5,13))]]))
    ident=eye(6)
    for u in (u1,u2,mid): assert mul(adj(u),u)==ident
    full=mul(mul(u2,mid),u1)
    marked=add(sub(sub(full,mul(u2,mid)),mul(mid,u1)),mid)
    factor=mul(mul(sub(u2,ident),mid),sub(u1,ident))
    assert marked==factor
    effect=mul(adj(marked),marked)
    actual=trace(mul(rho,effect)); comparison=trace(mul(upper,effect))
    assert actual.im==0 and comparison.im==0 and actual.re<=comparison.re

    # Infinite-support thermal reference q=1/2; actual states have two
    # Schmidt coefficients. The new bound stays <8 while unchanged-marginal
    # comparison cost diverges with the selected high number N.
    schmidt=[]
    for n in range(1,11):
        t=Q(1,2**n); norm2=1+t*t
        p0=1/norm2; pn=t*t/norm2
        m=2/norm2
        c=m*4
        tau0=Q(1,2); taun=Q(1,2**(n+1))
        # Tilted sigma outside is I/2 for these states.
        matrix=[[G(c*tau0/2-p0),G(-t/norm2)],
                [G(-t/norm2),G(c*taun/2-pn)]]
        assert_psd_principals(matrix)
        forced=1/tau0+1/taun
        assert c<8 and forced==2+2**(n+1)
        schmidt.append({'N':n,'joint_moment':str(m),'tilted_C':str(c),
                        'unchanged_marginal_least_C':str(forced)})

    # A number-phase entangler preserves the joint count law and its MGF,
    # but gives a genuinely non-product pure state.
    single=[Q(1),Q(1,2),Q(1,4)]
    base=sum((x*x for x in single),Q(0))
    amps=[[single[i]*single[j]*((-1)**(i*j)) for j in range(3)] for i in range(3)]
    assert amps[0][0]*amps[1][1]!=amps[0][1]*amps[1][0]
    mone=sum((4**i*x*x for i,x in enumerate(single)),Q(0))/base
    joint=sum((4**(i+j)*amps[i][j]**2 for i in range(3) for j in range(3)),Q(0))/(base*base)
    assert joint==mone*mone
    output={
        'scope':'exact Gaussian-rational positive-order and marked-map identities; no device run or Gaussian-threshold numerical validation',
        'finite_energy_basis_dimension':3,
        'outside_dimension':2,
        'weighted_inequality_principal_minors_checked':minor_count,
        'weighted_joint_moment':str(moment.re),
        'finite_Z':str(z),
        'normalized_comparison_constant':str(moment.re*z*z),
        'same_two_mark_mobius_equals_full_factor':True,
        'noncommuting_unmarked_selected_contact_retained':True,
        'marked_effect_actual':str(actual.re),
        'marked_effect_comparison':str(comparison.re),
        'schmidt_marginal_failure_vs_tilted_comparison':schmidt,
        'number_phase_entangled_count_moments':{'single':str(mone),'joint':str(joint),
                                                'factorizes_exactly':True,'pure_state_is_not_product':True},
        'interpretation':'finite operator-order/coverage tests only; uniform circuit-size and continuum statements require the separate proof',
    }
    path=Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__=='__main__': main()
