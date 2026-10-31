"""Pending single-logical-token comparison; accepted protected sources untouched."""
import sys,json,hashlib
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'stochastic_protected_boundary_20261031'))
import protected_boundary as p

def single_clock(rec,max_clock_states=2000):
    I=rec['inactive'];n=1+len(I);index={i:k+1 for k,i in enumerate(I)}
    if n>max_clock_states:return {'accepted':False,'reason':'single-token clock budget exceeded','required_clock_states':n,'budget':max_clock_states}
    A=[[F(0)]*n for _ in range(n)]
    A[0][0]=sum(rec['immigration'])
    for i in I:A[0][index[i]]-=rec['immigration'][i]
    for i in I:
        a=index[i];A[a][a]=rec['death'][i]+sum(rec['conversion'][i]);A[a][0]-=rec['death'][i]
        for j in I:
            if j!=i:A[a][index[j]]-=rec['conversion'][i][j]
    t=p.solve(A,[F(1)]*n);assert min(t)>0
    return {'accepted':True,'method':'single-logical-protected-token','clock_states':['absent']+list(I),'clock_matrix':A,
      'clock_hitting_means':t,'uniform_activation_mean_upper':t[0],'clock_linear_system_dimension':n,
      'largest_clock_fraction_bits':max(max(z.numerator.bit_length(),z.denominator.bit_length()) for z in t)}

def main():
    binary=p.activation_clock;out=[]
    sp,rs=p.demo_network()
    for name,sp,rs in [('frozen_demo',sp,rs),('parallel_arrivals',['A','E','B','C'],[
        ((0,0,0,0),(1,0,0,0),1),((0,0,0,0),(0,1,0,0),1),
        ((1,0,0,0),(0,0,1,0),1),((0,1,0,0),(0,0,1,0),1),((0,0,1,0),(0,0,0,0),1),
        ((0,0,2,0),(0,0,1,1),1),((0,0,1,1),(0,0,2,0),1)])]:
        rec=p.recognize(sp,rs);assert rec['accepted']
        p.activation_clock=binary;cb=p.construct(rec)
        p.activation_clock=single_clock;cs=p.construct(rec)
        assert cb['accepted'] and cs['accepted']
        ignored={'activation_clock','termination_witness','work'}
        assert {k:v for k,v in cb.items() if k not in ignored}=={k:v for k,v in cs.items() if k not in ignored}
        out.append({'case':name,'raw_species':sp,'raw_reactions':rs,'binary_clock':cb['activation_clock'],
          'single_clock':cs['activation_clock'],'actual_patch_and_foster_data_identical':True,'R':cb['R'],
          'head_states':len(cb['head_states']),'search_trials':cb['search_trials'],
          'binary_scalar_radius':cb['termination_witness']['guaranteed_scalar_radius'],
          'single_scalar_radius':cs['termination_witness']['guaranteed_scalar_radius']})
    p.activation_clock=binary
    print(json.dumps(out,default=p.encode,indent=2,sort_keys=True))
if __name__=='__main__':main()
