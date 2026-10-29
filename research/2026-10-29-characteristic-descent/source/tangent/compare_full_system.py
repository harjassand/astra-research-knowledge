"""Matched ordinary full-Jacobian controls for the proposed quotient compiler.

These are correctness and implementation-cost controls, not a claim to beat
optimized existing C++/M4RI flip-graph or Hensel implementations.
"""
from pathlib import Path
import itertools, json, time
import numpy as np
import tangent_repair as p

HERE=Path(__file__).resolve().parent


def row_consistent(cols,rhs,nrows):
    """Independent equation-row elimination, with no Image method calls."""
    ncols=len(cols)
    rows=[0]*nrows
    for j,col in enumerate(cols):
        while col:
            low=col&-col
            i=low.bit_length()-1
            rows[i] |= 1<<j
            col ^= low
    for i in range(nrows):
        rows[i] |= ((rhs>>i)&1)<<ncols
    pivots={}
    bad=0
    mask=(1<<ncols)-1
    for row in rows:
        while row&mask:
            pivot=(row&mask).bit_length()-1
            if pivot not in pivots:
                pivots[pivot]=row
                break
            row ^= pivots[pivot]
        else:
            bad += bool(row>>ncols)
    return {'consistent':bad==0,'rank':len(pivots),'inconsistent_rows':bad}


def main():
    allstart=time.perf_counter()
    f,t=p.load()
    basecols=p.jacobian(f)
    residual=p.defect(f,t)
    independent_start=time.perf_counter()
    independent=row_consistent(basecols,residual,t.size)
    independent_seconds=time.perf_counter()-independent_start
    assert not independent['consistent'] and independent['rank']==2117
    init=time.perf_counter()
    base=p.Image(basecols)
    rr=base.reduce(residual)
    init_seconds=time.perf_counter()-init
    # First 64 ordered moves in the published enumeration: same native inputs,
    # same candidates and same exact mod4 question in each arm.
    paths=list(itertools.islice(((perm,i,j) for perm in itertools.permutations(range(3))
                               for i in range(47) for j in range(47) if i!=j),64))
    begin=time.perf_counter()
    candidates=[p.expand(f,i,j,perm) for perm,i,j in paths]
    materialize_seconds=time.perf_counter()-begin
    begin=time.perf_counter()
    ordinary=[]
    for cand in candidates:
        cols=p.jacobian(cand)
        full=p.Image(cols)
        result=full.reduce(p.defect(cand,t))==0
        ordinary.append((result,len(full.basis)))
    ordinary_seconds=time.perf_counter()-begin
    begin=time.perf_counter()
    compiler=[]
    for perm,i,j in paths:
        ff=f[list(perm)]
        a,b,c=ff[:,:,i]
        d,e,g=ff[:,:,j]
        central=np.stack((a,e,(g+c)%2))[np.argsort(perm)]
        extra=p.Image([base.reduce(x) for x in p.columns(*central)])
        compiler.append((extra.reduce(rr)==0,2117+len(extra.basis)))
    compiler_seconds=time.perf_counter()-begin
    assert ordinary==compiler
    # Check BOTH claims of the update lemma against raw coefficients:
    # the whole Jacobian image equality and transport of the residual class.
    lemma_start=time.perf_counter()
    image_checks=0
    residual_checks=0
    flip_checks=0
    for cand,(perm,i,j) in zip(candidates[:8],paths[:8]):
        ff=f[list(perm)]
        central=np.stack((ff[0,:,i],ff[1,:,j],(ff[2,:,i]+ff[2,:,j])%2))[np.argsort(perm)]
        extended=p.Image(basecols+p.columns(*central))
        actualcols=p.jacobian(cand)
        actual=p.Image(actualcols)
        assert len(extended.basis)==len(actual.basis)
        assert all(extended.reduce(x)==0 for x in actualcols)
        assert all(actual.reduce(x)==0 for x in basecols+p.columns(*central))
        image_checks+=1
        assert actual.reduce(p.defect(cand,t)^residual)==0
        residual_checks+=1
        # All flips of these first eight expansions, not selected by outcome.
        for mode,fp,k,l in p.flips(cand):
            after=p.do_flip(cand,fp,k,l)
            aftercols=p.jacobian(after)
            cross=cand[:,:,k].copy()
            cross[fp[1]]=cand[fp[1],:,l]
            crosscols=p.columns(*cross)[mode*16:(mode+1)*16]
            union=p.Image(actualcols+crosscols)
            assert all(union.reduce(x)==0 for x in aftercols)
            assert union.reduce(p.defect(cand,t)^p.defect(after,t))==0
            full=p.Image(aftercols)
            assert full.reduce(p.defect(after,t))
            flip_checks+=1
    lemma_seconds=time.perf_counter()-lemma_start
    # A supplied exact ordinary positive control: Strassen's F2 scheme must
    # pass the same unrestricted mod4 test. This avoids a reject-everything
    # implementation masquerading as a useful obstruction compiler.
    s,ts=p.load('2,2,2')
    positive=row_consistent(p.jacobian(s),p.defect(s,ts),ts.size)
    assert positive['consistent']
    out={'independent_row_equation_check':independent,
         'independent_row_seconds':independent_seconds,
         'positive_native_Strassen_mod4':positive,
         'matched_candidates':len(paths),
         'all_full_and_compiler_answers_equal':True,
         'all_full_and_compiler_ranks_equal':True,
         'ordinary_full_system_seconds':ordinary_seconds,
         'compiler_batch_seconds_excluding_base':compiler_seconds,
         'shared_base_image_seconds':init_seconds,
         'ordinary_candidate_materialization_seconds':materialize_seconds,
         'raw_image_lemma_checks':image_checks,
         'raw_residual_transport_checks':residual_checks,
         'raw_post_flip_system_checks':flip_checks,
         'lemma_checks_seconds':lemma_seconds,
         'total_seconds':time.perf_counter()-allstart,
         'cost_scope':'Python implementations only; no advantage over optimized incumbent claimed.'}
    (HERE/'COMPARISON.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
