"""Exact rational orthogonal Jacobi approximation with certified descent.
No floating eigenvalue, eigenvector, angle, or gap is used.
Inputs must be a rational symmetric matrix and rational tau>0.
The caller supplies PSD/contraction support; diagonalization itself does not
need those promises. Every accepted rotation preserves exact orthogonality
and decreases squared off-diagonal Frobenius norm by at least pivot^2.
"""
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
import json,datetime,time

def floor_log2(x):
    assert x>0
    k=x.numerator.bit_length()-x.denominator.bit_length()
    if k>=0:
        if x.numerator < (x.denominator<<k):k-=1
    elif (x.numerator<<(-k))<x.denominator:k-=1
    return k

def sqrt_dyadic_interval(x,bits):
    assert x>=0 and bits>=0
    k=isqrt((x.numerator << (2*bits))//x.denominator)
    lo=Q(k,1<<bits)
    if lo*lo==x:return lo,lo
    return lo,Q(k+1,1<<bits)

def round_dyadic(x,bits):
    s=1<<bits
    k=(x.numerator*s)//x.denominator
    if x-Q(k,s)>Q(1,2*s):k+=1
    return Q(k,s)

def proposed_circle_parameter(a,b,d,bits):
    assert b
    z=(d-a)/(2*b)
    if z==0:t=Q(1)
    else:
        lo,hi=sqrt_dyadic_interval(1+z*z,bits)
        r=(lo+hi)/2
        t=Q(1 if z>0 else -1)/(abs(z)+r)
    lo,hi=sqrt_dyadic_interval(1+t*t,bits)
    tc=t/(1+(lo+hi)/2)
    return round_dyadic(tc,bits)

def off2(A):return sum((A[i][j]**2 for i in range(len(A)) for j in range(len(A)) if i!=j),Q(0))
def mm(A,B):
    n=len(A)
    return [[sum((A[i][k]*B[k][j] for k in range(n)),Q(0)) for j in range(n)] for i in range(n)]
def tr(A):return list(map(list,zip(*A)))
def ident(n):return [[Q(int(i==j)) for j in range(n)] for i in range(n)]

def diagonalize(A,tau):
    assert tau>0
    n=len(A)
    assert n and all(len(row)==n for row in A)
    A=[[Q(x) for x in row] for row in A]
    assert A==tr(A)
    original=[row[:] for row in A];U=ident(n);history=[];refines=0
    basebits=max(32,2*max(0,-floor_log2(tau))+3*(n+1).bit_length()+16)
    while off2(A)>tau*tau:
        pairs=[(abs(A[i][j]),i,j) for i in range(n) for j in range(i+1,n)]
        _,p,q=max(pairs);a,b,d=A[p][p],A[p][q],A[q][q]
        bits=basebits
        while True:
            t=proposed_circle_parameter(a,b,d,bits)
            c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
            newb=c*s*(a-d)+(c*c-s*s)*b
            if 2*newb*newb<=b*b:break
            bits*=2;refines+=1
        oldoff=off2(A)
        for i in range(n):
            if i not in (p,q):
                x,y=A[i][p],A[i][q]
                A[i][p]=A[p][i]=c*x-s*y
                A[i][q]=A[q][i]=s*x+c*y
        A[p][p]=c*c*a-2*c*s*b+s*s*d
        A[q][q]=s*s*a+2*c*s*b+c*c*d
        A[p][q]=A[q][p]=newb
        for i in range(n):
            x,y=U[i][p],U[i][q]
            U[i][p]=c*x-s*y;U[i][q]=s*x+c*y
        newoff=off2(A)
        assert newoff<=oldoff-b*b
        history.append({'pivot':str(b),'old_off2':str(oldoff),'new_off2':str(newoff),'rotation_bits':bits})
    assert mm(tr(U),U)==ident(n)
    assert mm(mm(tr(U),original),U)==A
    weights=[U[0][i]**2 for i in range(n)]
    assert all(x>=0 for x in weights) and sum(weights)==1
    return {'Q':U,'T':A,'weights':weights,'off2':off2(A),'rotations':len(history),'refinements':refines,'rotation_bits':basebits,'max_output_bitlength':max(max(x.numerator.bit_length(),x.denominator.bit_length()) for row in U+A for x in row)}

def serial(z):
    if isinstance(z,Q):return str(z)
    if isinstance(z,list):return [serial(x) for x in z]
    if isinstance(z,dict):return {k:serial(v) for k,v in z.items()}
    return z

if __name__=='__main__':
    fixtures=[
      ('positive2',[[Q(1,3),Q(1,10)],[Q(1,10),Q(2,3)]]),
      ('irreducible3',[[Q(1,2),Q(1,8),Q(0)],[Q(1,8),Q(1,2),Q(1,8)],[Q(0),Q(1,8),Q(1,2)]]),
      ('rank2_with_endpoint0',[[Q(1,6),Q(1,6),Q(0)],[Q(1,6),Q(1,3),Q(1,6)],[Q(0),Q(1,6),Q(1,6)]])]
    rows=[]
    for name,A in fixtures:
        start=time.monotonic();ans=diagonalize(A,Q(1,2**16));ans['name']=name;ans['seconds']=time.monotonic()-start
        assert all(0<=ans['T'][i][i]<=1 for i in range(len(A)))
        if name=='rank2_with_endpoint0':assert min(ans['T'][i][i] for i in range(len(A)))<=Q(1,2**16)
        rows.append(serial(ans))
        print(json.dumps({k:ans[k] for k in ['name','seconds','rotations','refinements','rotation_bits','max_output_bitlength']}),flush=True)
    Path(__file__).with_suffix('.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'finite exact rational rotation fixtures; analytic complexity proof supplies general bit bound','all_passed':True,'fixtures':rows},indent=2))
