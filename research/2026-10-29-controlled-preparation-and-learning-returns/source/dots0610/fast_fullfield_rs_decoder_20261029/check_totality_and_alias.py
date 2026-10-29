"""Total fallback and deliberate above-radius syndrome alias; exact field arithmetic."""
import numpy as np,json,random
from pathlib import Path
from fast_rs import CSSDecoder,Field
p=Path(__file__).parent;d=CSSDecoder(4,19,3);coef=np.zeros(16,np.uint16);coef[6]=1;e=np.array(d.c.apply(coef),np.uint16);f=np.zeros(16,np.uint16);read=d.actual_readout(e,f);eh,fh,ok,detail=d.decode_readout(*read)
assert np.count_nonzero(e)>3 and not np.any(read[0]) and not np.any(read[1]);assert ok and not np.any(eh) and not np.any(fh)
res=d.logical_correction_bits(e^eh,f^fh);assert np.any(res[0])
small=Field(3,11);cnt=0
for pos in range(8):
 for amp in range(1,8):
  a=np.zeros(8,np.uint16);a[pos]=amp;b,valid,_=small.decode(small.moments(a,2),1);assert valid and np.array_equal(a,b);cnt+=1
out={'all_GF8_weight_one_errors_checked':cnt,'above_radius_alias':{'h':4,'B':16,'t':3,'actual_X_error':e.tolist(),'actual_support':int(np.count_nonzero(e)),'syndrome_readout_Xlast':read[0].tolist(),'syndrome_readout_phasebits':read[1].tolist(),'decoder_valid_representative_flag':bool(ok),'decoded_correction_X':eh.tolist(),'remaining_logical_X':res[0].tolist(),'meaning':'Valid verified low-weight syndrome representative is not proof actual error was within radius. This above-radius nontrivial logical error aliases zero syndrome. Guard tail, not decoder flag alone, supplies accepted-operation soundness.'}};(p/'totality_and_alias.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
