#!/usr/bin/env python3
"""Shape-independent primary Gaussians and their exact eight-state sequence.

Scope: beta != 0 and gcd(f(x),f(x+beta))=1.  The irreducible degree,
field degree, and total primary multiplicity may grow.  No matrices,
subspaces, or field points are enumerated by this evaluator.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_matrix_root','work_norm_frontier_agent','work_norm_slice_agent')]
from matrix_kloosterman import Field,pmul,padd,pgcd,factor_polynomial
from krylov_square_source import companion,quadratic_anf_sum
from simple_operator_quadratic import matrix_source_anf


def xor(values):
    result=0
    for value in values:result^=value
    return result


def shifted_polynomial(f,beta,F):
    result=[]
    for coefficient in reversed(f):result=padd(pmul(result,[beta,1],F),[coefficient])
    return result


def value(phi,x):
    return sum((x&monomial)==monomial for monomial in phi)%2


def linear_anf(F,square_coefficient,linear_coefficient):
    return {1<<i for i in range(F.a) if F.trace(
        F.mul(square_coefficient,F.mul(1<<i,1<<i))^
        F.mul(linear_coefficient,1<<i))}


class NonresonantPrimaryGaussian:
    def __init__(self,field_h,irreducible,beta,eta=0):
        self.F=F=Field(field_h);self.f=f=tuple(irreducible);self.d=d=len(f)-1
        if d<1 or f[-1]!=1 or any(type(x) is not int or not 0<=x<F.q for x in f):
            raise ValueError('monic polynomial over the supplied field required')
        if factor_polynomial(list(f),F)!=[(list(f),1)]:raise ValueError('irreducible polynomial required')
        if not 0<beta<F.q or not 0<=eta<F.q:raise ValueError('nonzero beta and valid eta required')
        translated=shifted_polynomial(f,beta,F)
        if pgcd(list(f),translated,F)!=[1]:raise ValueError('the primary is beta-resonant')
        self.beta=beta;self.eta=eta;self.S=S=companion(f)
        self.tau=tau=xor(S[i][i] for i in range(d))
        self.A=A=tau^(beta if (d*(d-1)//2)%2 else 0)
        self.linear=linear=F.mul(eta,tau)
        self.inverse_sqrt_beta=F.pow(F.inv(beta),F.q//2)
        if d%2:
            correction=linear_anf(F,A,linear)
            gaussian=quadratic_anf_sum(matrix_source_anf(S,F,beta,correction,eta),F.a*d*d)
            denominator=F.q**((d*d+1)//2)
            sign,remainder=divmod(gaussian,denominator)
            if remainder or sign not in (-1,1):raise AssertionError('odd trace-zero Gaussian is not nondegenerate')
            self.gamma=sign;self.single_gaussian=gaussian;self.trace_support=None
        else:
            gaussian=quadratic_anf_sum(matrix_source_anf(S,F,beta,set(),eta),F.a*d*d)
            denominator=F.q**(d*d//2)
            sign,remainder=divmod(gaussian,denominator)
            if remainder or sign not in (-1,1):raise AssertionError('even primary Gaussian is not nondegenerate')
            self.gamma=sign;self.single_gaussian=gaussian
            self.trace_support=F.mul(F.inv(beta),F.pow(A,F.q//2)^linear)
        self.metadata=dict(field_modulus=field_h,irreducible=list(f),residue_degree=d,
            beta=beta,eta=eta,translated_irreducible=translated,trace_of_companion=tau,
            diagonal_square_coefficient=A,trace_linear_coefficient=linear,
            single_block_sign=self.gamma,single_block_gaussian=self.single_gaussian,
            even_block_trace_support=self.trace_support,
            precomputed_matrix_gaussians=1,enumerated_field_elements=0,
            uniform_polynomial_time=True)

    def gaussian(self,multiplicity,phi=()):
        m=multiplicity;F=self.F;d=self.d;beta=self.beta;phi=set(phi)
        if type(m) is not int or m<0:raise ValueError('nonnegative explicit primary multiplicity required')
        if any(type(x) is not int or x<0 or x.bit_length()>F.a or x.bit_count()>2 for x in phi):
            raise ValueError('Boolean quadratic trace polynomial required')
        b=d*m
        if not d%2:
            support=self.trace_support
            phase=F.trace(F.mul(beta,F.mul(support,support))) if (m*(m-1)//2)%2 else 0
            phase^=value(phi,support if m%2 else 0)
            sign=self.gamma if m%2 else 1
            return sign*(1-2*phase)*F.q**(b*b//2)
        half=(m+1)//2
        epsilon=-1 if (F.a*(half*(half-1)//2))%2 else 1
        if not m%2:
            support=self.inverse_sqrt_beta if (m*(m-1)//2)%2 else 0
            phase=value(phi,support)^F.trace(
                F.mul(self.A,F.mul(support,support))^F.mul(self.linear,support))
            return epsilon*(1-2*phase)*F.q**(b*b//2)
        coefficient=self.A^(beta if (m*(m-1)//2)%2 else 0)
        reduced=phi^linear_anf(F,coefficient,self.linear)
        field_gaussian=quadratic_anf_sum(reduced,F.a)
        return self.gamma*epsilon*F.q**((b*b-1)//2)*field_gaussian

    def normalized(self,multiplicity,phi=()):
        b=self.d*multiplicity
        result,remainder=divmod(self.gaussian(multiplicity,phi),self.F.q**(b*(b-1)//2))
        if remainder:raise AssertionError('nonintegral normalized residual Gaussian')
        return result

    def eight_state(self,phi=()):
        """g_(m+8)=Q^4*g_m; return the eight actual initial weights."""
        return dict(initial=[self.normalized(m,phi) for m in range(8)],
                    recurrence_order=8,multiplier=self.F.q**(4*self.d),
                    algebra_relation='w^8=Q^4',Q=self.F.q**self.d)
