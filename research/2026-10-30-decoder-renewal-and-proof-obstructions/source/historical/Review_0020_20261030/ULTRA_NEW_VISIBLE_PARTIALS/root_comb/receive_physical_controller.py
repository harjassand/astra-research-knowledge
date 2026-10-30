"""Independent literal-circuit composition, including the complete logical Choi.

No producer imports, source, solver, Haar draw or floating operation.  Enumerate
the FIVE equality patterns of three fresh junk labels.  Physical controlled
permutations are composed on sparse amplitudes before the actual saved known
decoder is applied.  Pattern counts give the entire exact all-r channel.
"""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import hashlib, json, time

P = list(permutations(range(3)))
AMPS = ((F(11,14),F(5,14)),(F(1,97),F(56,97)))
# Real matrices I,X,Z,J=-iY.  Relative phases are retained, not erased.
PAULI = (((1,0),(0,1)),((0,1),(1,0)),((1,0),(0,-1)),((0,-1),(1,0)))

def inv(p):
    return tuple(p.index(i) for i in range(3))

def move(registers,p):
    return tuple(registers[p.index(i)] for i in range(3))

def add(table,key,value):
    table[key]=table.get(key,F(0))+value

def pattern_state(junk):
    """Actual unweighted branch after two queries and coherent group channel."""
    # The two Bell pairs contribute amplitude1/2. Junk probability is external.
    v={}
    for t in range(2):
      for m in range(2):
        for e,op in enumerate(PAULI):
          ap=AMPS[0][0 if e==3 else 1]
          am=AMPS[1][0 if e==3 else 1]
          for a2 in range(2):
            if not op[a2][m]: continue
            b=((t,junk[0]),(m,junk[1]),(a2,junk[2]))
            add(v,(t,e,b),(ap+am)*op[a2][m]/4)
            add(v,(t,e,(b[1],b[0],b[2])),(ap-am)*op[a2][m]/4)
    # Uniform group preparation, controlled permutation, label inversion,
    # then tracing all physical carriers: a Gram matrix, manifestly positive.
    physical={}
    for (t,e,b),amp in v.items():
      if not amp: continue
      for g,p in enumerate(P):
        moved=move(b,inv(p))
        add(physical.setdefault(moved,{}),24*t+6*e+g,amp)
    out=[[F(0) for _ in range(48)] for _ in range(48)]
    for values in physical.values():
      for i,a in values.items():
        for j,b in values.items(): out[i][j]+=a*b/6
    assert sum(out[i][i] for i in range(48))==1
    return out

def strict_ldl(a):
    assert all(a[i][j]==a[j][i] for i in range(len(a)) for j in range(len(a)))
    n=len(a); lower=[[F(0) for _ in range(n)] for _ in range(n)]; pivots=[]
    for j in range(n):
      lower[j][j]=1
      pivot=a[j][j]-sum(lower[j][h]**2*pivots[h] for h in range(j))
      assert pivot>0
      pivots.append(pivot)
      for i in range(j+1,n):
        lower[i][j]=(a[i][j]-sum(lower[i][h]*lower[j][h]*pivots[h] for h in range(j)))/pivot
    return min(pivots)

def compose_decoder(state,c):
    return [[sum(state[24*t+i][24*u+j]*c[2*i+a][2*j+b]
                     for i in range(24) for j in range(24))
             for u in range(2) for b in range(2)]
            for t in range(2) for a in range(2)]

def bell_weights(j):
    # I,X,Z,Y Pauli probabilities after the physically supplied query twirl.
    return [(j[0][0]+j[3][3]+j[0][3]+j[3][0])/2,
            (j[1][1]+j[2][2]+j[1][2]+j[2][1])/2,
            (j[0][0]+j[3][3]-j[0][3]-j[3][0])/2,
            (j[1][1]+j[2][2]-j[1][2]-j[2][1])/2]

def main():
    start=time.perf_counter();base=Path(__file__).parent
    cpath=base.parent/'c_active_inverse'/'COHERENT_FEEDBACK_DECODER.json'
    raw=cpath.read_bytes();data=json.loads(raw)
    c=[[F(x) for x in row] for row in data['repaired_CPTP_Choi']]
    pivot=strict_ldl(c)
    assert all(c[2*i][2*j]+c[2*i+1][2*j+1]==int(i==j) for i in range(24) for j in range(24))
    # Exactly five set partitions. Counts are r, r(r-1) for each two-equal
    # pattern, and r(r-1)(r-2), divided by r^3.  No source-r sampling.
    patterns=[(0,0,0),(0,0,1),(0,1,0),(0,1,1),(0,1,2)]
    counts=[(0,0,1),(0,1,-1),(0,1,-1),(0,1,-1),(1,-3,2)]
    states=[pattern_state(p) for p in patterns]
    coeff=[[[sum(F(counts[h][power])*states[h][i][j] for h in range(5))
              for j in range(48)] for i in range(48)] for power in range(3)]
    for h,state in enumerate(coeff):
      for t in range(2):
        for u in range(2):
          assert sum(state[24*t+i][24*u+i] for i in range(24))==(F(int(t==u),2) if h==0 else 0)
    choi=[compose_decoder(state,c) for state in coeff]
    for h,j in enumerate(choi):
      for t in range(2):
        for u in range(2):
          assert sum(j[2*t+a][2*u+a] for a in range(2))==(F(int(t==u),2) if h==0 else 0)
    weights=[bell_weights(j) for j in choi]
    family=json.loads((base.parent/'c_active_inverse'/'ALL_R_FAMILY.json').read_text())
    assert [w[0] for w in weights]==list(map(F,family['exact_Bell_fidelity_coefficients_1_rinv_rinv2']))
    exact_r2=[sum(weights[h][i]/2**h for h in range(3)) for i in range(4)]
    assert all(w>=0 for w in exact_r2) and sum(exact_r2)==1
    parallel=json.loads((base/'PARALLEL_DUAL_CERTIFICATE.json').read_text())
    gap=exact_r2[0]-F(parallel['parallel_Bell_fidelity_upper'])
    assert gap>F(1,80)
    result={'scope':'independent full literal physical controller composition via five junk equality patterns; exact all-r normalized logical Choi; no producer imports',
      'decoder_sha256':hashlib.sha256(raw).hexdigest(),
      'minimum_exact_decoder_LDL_pivot':str(pivot),'all_576_decoder_TP_entries':True,
      'pattern_count_weights_in_1_rinv_rinv2':counts,
      'normalized_logical_Choi_coefficients':[[[str(v) for v in row] for row in j] for j in choi],
      'Pauli_twirl_weights_I_X_Z_Y_coefficients':[[str(v) for v in row] for row in weights],
      'r2_twirl_weights_I_X_Z_Y':list(map(str,exact_r2)),
      'r2_complete_halfdiamond':str(1-exact_r2[0]),
      'strict_exact_parallel_gap':str(gap),
      'source_solver_Haar_quantum_calls':0,
      'seconds_after_imports':time.perf_counter()-start}
    (base/'PHYSICAL_CONTROLLER_INTAKE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['scope','r2_twirl_weights_I_X_Z_Y','r2_complete_halfdiamond','strict_exact_parallel_gap','seconds_after_imports']},indent=2))

if __name__=='__main__': main()
