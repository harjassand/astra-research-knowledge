#!/usr/bin/env python3
"""Independent exhaustive GL oracle for the singular-pair construction.

This file deliberately enumerates field matrices and is exponential. The
counter in nilpotent_pair_counter.py never calls this oracle.
"""
from pathlib import Path
import json,time,random
import numpy as np
from matrix_kloosterman import Field,mmul,minverse,eye
from nilpotent_strings_probe import string_types
from nilpotent_pair_counter import NilpotentPairCounter,string_matrices,acquire_nilpotent_strings,canonical_strings

def all_GL_arrays(n,field_h):
    F=Field(field_h);q=F.q
    table=np.array([[F.mul(x,y) for y in range(q)] for x in range(q)],dtype=np.uint8)
    inv=np.array([0]+[F.inv(x) for x in range(1,q)],dtype=np.uint8)
    xs=[];ys=[];total=q**(n*n)
    for start in range(0,total,16384):
        indexes=np.arange(start,min(total,start+16384),dtype=np.uint64)
        X=np.array([(indexes>>(F.a*j))&(q-1) for j in range(n*n)],dtype=np.uint8).T.reshape(-1,n,n)
        M=X.copy();Y=np.broadcast_to(np.eye(n,dtype=np.uint8),X.shape).copy()
        valid=np.ones(len(X),dtype=bool)
        for j in range(n):
            for k in range(j+1,n):
                swap=valid&(M[:,j,j]==0)&(M[:,k,j]!=0)
                temp=M[swap,j].copy();M[swap,j]=M[swap,k];M[swap,k]=temp
                temp=Y[swap,j].copy();Y[swap,j]=Y[swap,k];Y[swap,k]=temp
            valid &= M[:,j,j]!=0
            scalars=inv[M[:,j,j]]
            M[:,j]=table[scalars[:,None],M[:,j]]
            Y[:,j]=table[scalars[:,None],Y[:,j]]
            for i in range(n):
                if i==j:continue
                coeff=M[:,i,j].copy()
                M[:,i]^=table[coeff[:,None],M[:,j]]
                Y[:,i]^=table[coeff[:,None],Y[:,j]]
        xs.append(X[valid]);ys.append(Y[valid])
    return np.concatenate(xs),np.concatenate(ys)

def oracle(A,B,X,Y,field_h):
    F=Field(field_h);n=len(A)
    trace=np.array([F.trace(x) for x in range(F.q)],dtype=np.uint8)
    phase=np.zeros(len(X),dtype=np.uint8)
    for i in range(n):
        for j in range(n):
            if A[i][j]:phase^=np.array([F.mul(A[i][j],x) for x in range(F.q)],dtype=np.uint8)[X[:,j,i]]
            if B[i][j]:phase^=np.array([F.mul(B[i][j],x) for x in range(F.q)],dtype=np.uint8)[Y[:,j,i]]
    return len(X)-2*int(trace[phase].sum())

def random_unit(n,F,rng):
    U=eye(n)
    for _ in range(4*n*n):
        i,j=rng.sample(range(n),2);c=rng.randrange(F.q)
        U[i]=[x^F.mul(c,y) for x,y in zip(U[i],U[j])]
    return U

def run():
    start=time.perf_counter();rows=[];rng=random.Random(1907)
    for n,h in [(3,7),(2,11),(2,19)]:
        F=Field(h);X,Y=all_GL_arrays(n,h);counter=NilpotentPairCounter(F.q)
        cases=[];disguised=0
        for parts in string_types(n):
            A,B=string_matrices(parts);value=counter.count(parts)
            expected=oracle(A,B,X,Y,h)
            assert value==expected,(n,h,parts,value,expected)
            L=random_unit(n,F,rng);R=random_unit(n,F,rng)
            AA=mmul(mmul(L,A,F),minverse(R,F),F)
            BB=mmul(mmul(R,B,F),minverse(L,F),F)
            acquired=acquire_nilpotent_strings(AA,BB,h)
            assert acquired==canonical_strings(parts),(parts,acquired)
            # Validate the independent oracle for an actual dense disguise too.
            if any(l>3 for l,c in parts):
                assert oracle(AA,BB,X,Y,h)==value
                disguised+=1
            cases.append(dict(strings=parts,value=value))
        rows.append(dict(n=n,q=F.q,field_h=h,types=len(cases),GL_oracle_matrices=len(X),
                         dense_disguise_oracles=disguised,**counter.metadata(),cases=cases))
    # Unbounded ranks with both products nonzero, beyond the zero-product base.
    large=[]
    for n,a,parts in [(16,1,[(4,0)]*4+[(4,1)]*4),
                       (24,4,[(6,0)]*4+[(6,1)]*4),
                       (32,8,[(8,0)]*4+[(8,1)]*4)]:
        t=time.perf_counter();counter=NilpotentPairCounter(1<<a)
        value=counter.count(parts)
        large.append(dict(n=n,a=a,original_cubic_bits=3*a*n*n,strings=parts,
                          value_hex=hex(value),answer_bits=abs(value).bit_length(),
                          seconds=time.perf_counter()-t,**counter.metadata()))
    result=dict(checks=rows,large=large,seconds=time.perf_counter()-start)
    Path(__file__).with_name('nilpotent_extension_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(dict(checks=[{k:v for k,v in row.items() if k!='cases'} for row in rows],
                         large=[{k:v for k,v in row.items() if k not in ('value_hex','strings')} for row in large],
                         seconds=result['seconds']),indent=2))

if __name__=='__main__':run()
