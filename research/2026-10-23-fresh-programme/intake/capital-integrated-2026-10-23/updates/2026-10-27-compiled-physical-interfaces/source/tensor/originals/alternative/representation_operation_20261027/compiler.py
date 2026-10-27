"""Exact no-supplied-gauge generic planar contraction and normalized edge weights.

Local recognition uses one formal quadratic algebra per vertex. Evaluation uses
one common Fp2 at each prime; CRT uses ORIGINAL integer contraction heights.
UNKNOWN is not a hardness result. No publication/historical advantage is implied.
"""
import argparse,json,time
from fractions import Fraction as Q
from pathlib import Path
from fields import Degenerate,primes
from local_recognition import clear_input,recognize
from fisher import topology
from modular import stage


def crt_update(xs,M,rs,p):
    inv=pow(M%p,-1,p)
    return [x+M*(((r-x)%p)*inv%p) for x,r in zip(xs,rs)],M*p

def centered(x,M):return x if x<=M//2 else x-M


def compile_network(data,prime_budget=200,marginals=True):
    start=time.perf_counter();cpu=time.process_time();ts,Ds,ports,H=clear_input(data);n=len(ts);edges=data['edges']
    top=topology(n,edges);den=1
    for D in Ds:den*=D
    common={'operation':'exact-generic-planar-binary-contraction','vertices':n,'edges':len(edges),'denominator_product':str(den),'original_integer_height_bound':str(H),'requested_normalized_edge_weights':marginals,'input_nonnegative':all(x>=0 for t in ts for x in t)}
    if not H:return {**common,'status':'EXACT','partition':'0','normalized_edge_weights':None,'marginal_reason':'zero partition; normalized weights undefined','reason':'an original tensor is identically zero'}
    try:local,bad=recognize(ts,ports)
    except Degenerate as e:return {**common,'status':'UNKNOWN','reason':str(e),'outside_generic_promise':True}
    if not local['recognized']:return {**common,'status':'UNKNOWN','reason':'local exact generic-class balance fails; other tractability not excluded','local_witness':local}
    # The simple bit bound prices all primes dividing a nonzero chart/norm
    # obstruction, output-dividing primes and sufficient good CRT factors.
    theoretical_count=bad.bit_length()+2*H.bit_length()+4
    zres=[0];Mz=1;nres=[0]*(2*len(edges));Mn=1;known=None;receipts=[];rejected=[]
    def finish():
        out={**common,'status':'EXACT','partition':str(Q(known,den)),'cleared_integer_partition':str(known),'normalized_edge_weights':None,
             'local_recognition':local,'accepted_prime_certificates':receipts,'rejected_primes':rejected,'partition_modulus':str(Mz),'marginal_numerator_modulus':str(Mn),
             'bad_integer_bit_length':bad.bit_length(),'guaranteed_prime_count_upper_on_promise':theoretical_count,
             'wall_seconds_including_recognition':time.perf_counter()-start,'cpu_seconds_including_recognition':time.process_time()-cpu}
        if marginals and known:
            nums=[centered(x,Mn) for x in nres]
            if any(abs(x)>H for x in nums) or any(nums[2*i]+nums[2*i+1]!=known for i in range(len(edges))):raise ArithmeticError('CRT pin height/sum identity failed')
            rows=[[Q(nums[2*i],known),Q(nums[2*i+1],known)] for i in range(len(edges))]
            if common['input_nonnegative'] and (known<0 or any(not 0<=x<=1 for row in rows for x in row)):raise ArithmeticError('nonnegative input produced invalid probabilities')
            out['cleared_integer_pin_weights']=nums;out['normalized_edge_weights']=[[str(x) for x in row] for row in rows]
            out['normalized_weights_are_probabilities']=common['input_nonnegative']
        elif marginals:out['marginal_reason']='exact partition zero; normalized weights undefined; pin numerators are NOT asserted zero'
        return out
    for count,p in enumerate(primes(),1):
        if prime_budget is not None and count>prime_budget:break
        try:r=stage(ts,edges,ports,top,p,marginals)
        except Degenerate as e:rejected.append({'prime':p,'reason':str(e)});continue
        receipts.append(r);zres,Mz=crt_update(zres,Mz,[r['residue']],p)
        if r['pin_residues'] is not None:nres,Mn=crt_update(nres,Mn,r['pin_residues'],p)
        if known is None and Mz>2*H:
            known=centered(zres[0],Mz)
            if abs(known)>H:raise ArithmeticError('CRT partition violates original-input height')
        if known is not None and (not marginals or not known or Mn>2*H):return finish()
    return {**common,'status':'UNKNOWN','reason':'declared prime budget exhausted; no false partial CRT answer','local_recognition':local,'accepted_prime_certificates':receipts,'rejected_primes':rejected,'partition_modulus':str(Mz),'marginal_numerator_modulus':str(Mn),'bad_integer_bit_length':bad.bit_length(),'guaranteed_prime_count_upper_on_promise':theoretical_count,'wall_seconds_including_recognition':time.perf_counter()-start,'cpu_seconds_including_recognition':time.process_time()-cpu}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('-o','--output');p.add_argument('--prime-budget',type=int,default=200);p.add_argument('--unbounded-prime-search',action='store_true');p.add_argument('--partition-only',action='store_true');a=p.parse_args()
    try:
        data=json.loads(Path(a.input).read_text());out=compile_network(data,None if a.unbounded_prime_search else a.prime_budget,not a.partition_only)
    except (ValueError,KeyError,ZeroDivisionError) as e:out={'status':'INVALID_OR_UNSUPPORTED_INPUT','reason':str(e)}
    text=json.dumps(out,indent=2)+'\n'
    if a.output:Path(a.output).write_text(text)
    else:print(text,end='')
if __name__=='__main__':main()
