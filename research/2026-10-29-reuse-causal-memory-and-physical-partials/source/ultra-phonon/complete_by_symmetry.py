"""Complete the first attempt by exact point-group reuse, not another fixture."""
from pathlib import Path
from fractions import Fraction as F
import gzip,hashlib,itertools,json,time
import numpy as np
from polynomial_charts import load_laurent,charts,split,approximate_whitener,exact_margin
BASE=Path(__file__).parent

def main():
    start=time.perf_counter();coeff,_,_=load_laurent();zero=np.zeros((6,6),dtype=object)
    for perm in itertools.permutations(range(3)):
        Q=np.eye(3,dtype=int)[list(perm)].astype(object);U=np.block([[Q,np.zeros((3,3),dtype=object)],[np.zeros((3,3),dtype=object),Q]])
        for R,A in coeff.items():
            assert np.array_equal(coeff.get(tuple(R[j] for j in perm),zero),U@A@U.T)
    saved=json.loads(gzip.open(BASE/'LEAVES_first.json.gz','rt').read());first=json.loads((BASE/'GLOBAL_CERTIFICATE_first.json').read_text())
    targets={'acoustic0+1','regular001','regular011','regular111'}
    known={name:{v['path']:v for v in saved if v['chart']==name} for name in targets}
    result=[];stats=[];newnodes=0;eta=None;success=True
    for name,re,im,den in charts():
        if name not in targets:continue
        begin=time.perf_counter();old=known[name];prefix={k[:i] for k in old for i in range(len(k))}
        pending=[('',re,im,den)];accepted=0;count=0;reused=0;depthmax=0
        while pending:
            path,re,im,den=pending.pop();count+=1;depthmax=max(depthmax,len(path))
            if path in old:
                leaf=old[path];reused+=1
                assert str(den)==leaf['coefficient_denominator']
                lower=F(leaf['matrix_lower_numerator'])/F(leaf['matrix_lower_denominator'])
                result.append(leaf);eta=lower if eta is None else min(eta,lower);accepted+=1;continue
            if path not in prefix:
                newnodes+=1;S,preview=approximate_whitener(re,im,den)
                if S is not None and preview>.03:
                    margin,lower,sr,si,bits=exact_margin(re,im,den,S)
                    if margin>0:
                        leaf=dict(chart=name,path=path,whitener_real=[[int(x) for x in row] for row in sr],whitener_imag=[[int(x) for x in row] for row in si],whitener_bits=bits,integer_margin=str(margin),coefficient_denominator=str(den),matrix_lower_numerator=str(lower.numerator),matrix_lower_denominator=str(lower.denominator))
                        result.append(leaf);eta=lower if eta is None else min(eta,lower);accepted+=1;continue
                if newnodes>=20000 or len(path)>=30:success=False;break
            axis=[1,2,0][len(path)%3];left,right,factor=split(re,im,axis)
            pending.append((path+'1',right[0],right[1],den*factor));pending.append((path+'0',left[0],left[1],den*factor))
        st=dict(chart=name,traversed_nodes=count,new_nodes=newnodes-sum(x['new_nodes'] for x in stats),leaves=accepted,reused_leaves=reused,max_depth=depthmax,seconds=time.perf_counter()-begin,complete=not pending and success)
        stats.append(st);print(json.dumps(st),flush=True)
        if not success:break
    if success:
      for name in targets:
        paths=[v['path'] for v in result if v['chart']==name]
        assert sum((F(1,2**len(k)) for k in paths),F(0))==1
        assert not any(k[:i] in set(paths) for k in paths for i in range(len(k)))
    out=dict(status='EXACT_ALL_TORUS_ACOUSTIC_BLOWUP_CERTIFICATE_WITH_VERIFIED_SYMMETRY' if success else 'CONTINUATION_INCOMPLETE',model_sha256=hashlib.sha256((BASE/'MODEL.json').read_bytes()).hexdigest(),charts=stats,leaves=len(result),new_nodes=newnodes,exact_primitive_axis_permutation_covariance=True,negative_q_by_complex_conjugation=True,common_chart_matrix_lower_bound=str(eta) if eta else None,seconds=time.perf_counter()-start,first_attempt_seconds=first['seconds'],total_attempt_seconds=first['seconds']+time.perf_counter()-start,all_accepted_congruence_checks_exact=True,ordinary_comparator_gets_same_symmetry=True,physical_specimen_stability='NOT_ACQUIRED')
    with gzip.open(BASE/'LEAVES.json.gz','wt') as f:json.dump(result,f,separators=(',',':'))
    (BASE/'GLOBAL_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)

if __name__=='__main__':main()
