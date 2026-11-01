"""Exact ordinary code-weight baseline for a rare binary linear target.

No native 80-bit acquisition is claimed. All coefficients of the reference
weight enumerators and reference means below are exact Python integers/Fractions.
Only displayed decimals and the independent small killed solve use floats.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import math
import random
import numpy as np
from scipy.linalg import solve

HERE=Path(__file__).resolve().parent


def xor_selected(columns, mask):
    result=0
    while mask:
        low=mask & -mask
        result ^= columns[low.bit_length()-1]
        mask ^= low
    return result


def build(n,m,seed):
    rng=random.Random(seed)
    P=[rng.getrandbits(m) for _ in range(n-m)]
    columns=[1<<i for i in range(m)]+P
    A=[0]*(n+1)
    minimum=n+1
    minimum_words=[]
    previous=parity=0
    for counter in range(1<<(n-m)):
        z=counter^(counter>>1)
        if counter:
            changed=z^previous
            parity ^= P[changed.bit_length()-1]
        weight=parity.bit_count()+z.bit_count()
        A[weight]+=1
        word=parity|(z<<m)
        if weight and weight<minimum:
            minimum=weight;minimum_words=[word]
        elif weight and weight==minimum:
            minimum_words.append(word)
        previous=z
    B=dual_enumerator(A,n,n-m)
    b=1-F(1,1<<m)
    R0=sum((F(B[j],2*j) for j in range(1,n+1)),F(0))
    s=F(1,10)
    Rs=sum((F(B[j],1)/(s+2*j) for j in range(1,n+1)),F(0))
    p=1-b
    r=1/(p*(1/s+Rs))
    mu=(r-s)/n
    return {"n":n,"m":m,"kernel_dimension":n-m,"P_seed":seed,
            "P_columns_uint64":P,"H_columns_uint64":columns,
            "P_column_weights":[x.bit_count() for x in P],
            "all_H_columns_nonzero":all(columns),
            "all_H_columns_distinct":len(set(columns))==n,
            "A_weights":A,"B_dual_weights":B,
            "minimum_nonzero_kernel_weight":minimum,
            "number_of_minimum_kernel_words":A[minimum],
            "minimum_kernel_words_hex":[hex(w) for w in minimum_words],
            "minimum_nonzero_dual_weight":next(j for j in range(1,n+1) if B[j]),
            "p_exact":str(p),"b_exact":str(b),"R0_exact":str(R0),
            "M0_exact":str(R0/b),"M0_decimal":float(R0/b),
            "s_exact":str(s),"Rs_exact":str(Rs),"Rs_decimal":float(Rs),
            "r_s_exact":str(r),"r_s_decimal":float(r),
            "receiver_success_probability_exact":str(mu),
            "receiver_success_probability_decimal":float(mu),
            "enumerated_kernel_words":1<<(n-m),
            "dual_words_represented":1<<m,
            "exact_enumerator_checks":{"A_sum":sum(A),"B_sum":sum(B),"B0":B[0],
                                       "nonnegative_integer_B":all(isinstance(v,int) and v>=0 for v in B)}}


def dual_enumerator(A,n,k):
    # K_j(w) is the coefficient of z^j in (1-z)^w(1+z)^(n-w).
    # The three-term recurrence performs only exact integer arithmetic.
    totals=[0]*(n+1)
    for w,Aw in enumerate(A):
        if not Aw:
            continue
        K=[1,n-2*w]
        for j in range(1,n):
            numerator=(n-2*w)*K[j]-(n-j+1)*K[j-1]
            assert numerator%(j+1)==0
            K.append(numerator//(j+1))
        for j in range(n+1):
            totals[j]+=Aw*K[j]
    assert all(v%(1<<k)==0 for v in totals)
    B=[v//(1<<k) for v in totals]
    assert all(v>=0 for v in B)
    assert B[0]==1 and sum(B)==1<<(n-k)
    return B


def exact_solve(matrix,rhs):
    """Small rational Gaussian elimination; used only on the31-state check."""
    a=[list(map(F,row))+[F(y)] for row,y in zip(matrix,rhs)]
    n=len(a)
    for i in range(n):
        pivot=next(j for j in range(i,n) if a[j][i])
        a[i],a[pivot]=a[pivot],a[i]
        d=a[i][i]
        for k in range(i,n+1):
            a[i][k]/=d
        for j in range(n):
            if j!=i and a[j][i]:
                d=a[j][i]
                for k in range(i,n+1):
                    a[j][k]-=d*a[i][k]
    return [row[-1] for row in a]


def small_crosscheck():
    data=build(8,5,2026110203)
    n,m=8,5
    columns=data["H_columns_uint64"]
    N=1<<m
    Q=[[0]*N for _ in range(N)]
    for x in range(N):
        for col in columns:
            y=x^col
            if y!=x:
                Q[x][y]+=1;Q[x][x]-=1
    killed=[[-Q[x][y] for y in range(1,N)] for x in range(1,N)]
    h=exact_solve(killed,[1]*(N-1))
    exact_mean=sum(h,F(0))/(N-1)
    assert exact_mean==F(data["M0_exact"])
    # Direct enumeration of the dual independently checks the transform.
    B=[0]*(n+1)
    for u in range(N):
        weight=sum((u&col).bit_count()%2 for col in columns)
        B[weight]+=1
    assert B==data["B_dual_weights"]
    # The original256-state killed solve checks the quotient mapping too.
    fullQ=np.zeros((1<<n,1<<n))
    for x in range(1<<n):
        for i in range(n):
            fullQ[x,x^(1<<i)]+=1
        fullQ[x,x]-=n
    outside=[x for x in range(1<<n) if xor_selected(columns,x)]
    K=-fullQ[np.ix_(outside,outside)]
    fullh=solve(K,np.ones(len(outside)))
    fullmean=float(np.mean(fullh))
    assert abs(fullmean/float(exact_mean)-1)<1e-12
    return {"n":n,"m":m,"P_columns":data["P_columns_uint64"],
            "A_weights":data["A_weights"],"B_weights":B,
            "quotient_states":N,"original_states":1<<n,
            "rational_killed_mean":str(exact_mean),
            "weight_formula_mean":data["M0_exact"],
            "exact_rational_equality":True,
            "original_killed_mean_float":fullmean,
            "original_killed_max_residual":float(max(abs(K@fullh-1)))}


def main():
    data=build(80,64,2026110202)
    assert data["all_H_columns_nonzero"] and data["all_H_columns_distinct"]
    data["small_crosscheck"]=small_crosscheck()
    data["ordinary_method_credit"]="Binary characters, quotient random-walk Green functions, and the classical MacWilliams identity; not a new invention."
    data["native_calibration_claimed"]=False
    (HERE/"code_target_exact.json").write_text(json.dumps(data,indent=2)+"\n")
    # First line n m trials rng_seed, then one64-bit column per line.
    (HERE/"receiver_input.txt").write_text("80 64 40000 2026110204\n"+
        "\n".join(map(str,data["H_columns_uint64"]))+"\n")
    print(json.dumps({k:data[k] for k in ("n","m","P_seed","P_column_weights",
        "minimum_nonzero_kernel_weight","number_of_minimum_kernel_words",
        "minimum_kernel_words_hex","minimum_nonzero_dual_weight","M0_decimal",
        "r_s_decimal","receiver_success_probability_decimal","small_crosscheck")},indent=2))


if __name__=="__main__":
    main()
