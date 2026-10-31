#!/usr/bin/env python3
"""Verify the mathematical certificate, not timing/ledger metadata."""
import math
from fractions import Fraction
import re
import sympy as sp
from learn import metric, measure, sum_kernel, inner


def rational(s):
    if type(s) is not str or re.fullmatch(r'-?[0-9]+(?:/[1-9][0-9]*)?',s) is None:
        raise ValueError('malformed rational string')
    f=Fraction(s)
    return sp.Rational(f.numerator,f.denominator)


def matrix(rows, n=None, k=None):
    if type(rows) is not list or not rows or any(type(row) is not list for row in rows):
        raise ValueError('matrix shape')
    if n is not None and len(rows)!=n:raise ValueError('matrix rows')
    width=len(rows[0])
    if width==0 or (k is not None and width!=k):raise ValueError('matrix columns')
    out=[]
    for row in rows:
        if len(row)!=width:raise ValueError('ragged')
        r=[]
        for item in row:
            if type(item) is not list or len(item)!=2:raise ValueError('rational pair')
            a,b=item
            if type(a) is not int or type(b) is not int or b<=0 or math.gcd(a,b)!=1:
                raise ValueError('noncanonical integer pair')
            r.append(sp.Rational(a,b))
        out.append(r)
    return sp.Matrix(out)


def verify(matrices,b,c,record,*,expected_length,expected_tolerance):
    try:
        if type(record) is not dict: return False
        if type(expected_length) is not int or expected_length<0:return False
        if isinstance(expected_tolerance,(bool,float)):return False
        requested=sp.Rational(expected_tolerance)
        if requested<=0:return False
        n=matrices[0].rows
        pi,adj,alpha=metric(matrices)
        V=matrix(record['basis'],n);r=V.cols
        if r>n:return False
        G=V.T*sp.diag(*pi)*V
        if G!=sp.diag(*[G[i,i] for i in range(r)]) or any(G[i,i]<=0 for i in range(r)):
            return False
        if G!=matrix(record['gram'],r,r) or pi!=matrix(record['pi'],n,1):return False
        u=matrix(record['right'],r,1);v=matrix(record['left'],r,1)
        if V*u!=b or V*v!=c:return False
        # The gap proof needs the constant observable in the acquired space.
        if V*(G.inv()*V.T*pi)!=sp.ones(n,1):return False
        if rational(record['alpha'])!=alpha:return False
        if type(record['operators']) is not list or len(record['operators'])!=len(matrices):return False
        for A,B in zip(matrices,record['operators']):
            if matrix(B,r,r)!=G.inv()*V.T*sp.diag(*pi)*A*V:return False
        images=[[[A*V[:,j] for j in range(r)] for A in operators] for operators in (matrices,adj)]
        (in2,out2),_=measure([V[:,j] for j in range(r)],images,pi,len(matrices))
        length=record['length']
        if type(length) is not int or length!=expected_length:return False
        tol=rational(record['tolerance'])
        if tol!=requested:return False
        scale=inner(b,b,pi)*inner(c,c,pi)
        qbound=((in2+out2)/2)**2*sum_kernel(length,alpha)**2*scale
        sbound=length**2*in2*scale
        if rational(record['quadratic_error_bound_squared'])!=qbound:return False
        if rational(record['state_error_bound_squared'])!=sbound:return False
        rule=record['stopping']
        if rule not in ('quadratic','state'):return False
        return bool((qbound if rule=='quadratic' else sbound)<=tol**2)
    except (KeyError,ValueError,TypeError,IndexError,AttributeError,AssertionError,ZeroDivisionError):
        return False
