"""Read saved synthetic calibration; audit actual word/selector interface only.
Uses no parameter knowledge in the reconstruction of the deployment selector.
"""
from pathlib import Path
from fractions import Fraction as F
import ast, hashlib, json, struct, zipfile
R=Path(__file__).resolve().parent.parent
report=json.loads((R/'ROBUST_PROGRAM_CHECKS.json').read_text())
N=report['trials_per_site_per_mode'];BITS=report['selector_bits']
counts={};post=list(report['initial_visible_state']);readouts=[]
with zipfile.ZipFile(R/'SYNTHETIC_CALIBRATION_READOUTS.npz') as z:
    for row in report['calibration']:
        key=f"site_{row['site']}_mode_{row['mode']}"
        data=z.read(key+'.npy')
        assert data[:6]==b'\x93NUMPY'
        version=tuple(data[6:8]);nhead=2 if version==(1,0) else 4
        size=int.from_bytes(data[8:8+nhead],'little')
        header=ast.literal_eval(data[8+nhead:8+nhead+size].decode('latin1').strip())
        assert header['descr']=='|u1' and not header['fortran_order']
        packed=data[8+nhead+size:]
        assert len(packed)==(N+7)//8 and N%8==0
        assert hashlib.sha256(packed).hexdigest()==row['packed_sha256']
        count=sum(x.bit_count() for x in packed)
        assert count==row['flips']
        counts[row['site'],row['mode']]=count
        post[row['site']]^=count%2
        readouts.append({'site':row['site'],'mode':row['mode'],'verified_count':count})
assert post==report['post_calibration_visible_state']

def clip(x,lo,hi):return min(hi,max(lo,x))
row_errors=[];round_errors=[]
H=(F(-1),F(-1,3),F(1,3),F(1))
for row in report['native_implementation_table']:
    i=row['site'];target=F(row['target_flip'])
    p0hat=clip(F(counts[i,0],N),F(1,20),F(3,20))
    p3hat=clip(F(counts[i,3],N),F(1,4),F(9,20))
    rhat=2*p3hat*(1-p3hat)
    w=(rhat-target)/(rhat-p0hat)
    assert 0<=w<=1 and rhat-p0hat>=F(9,40)
    shifted=w*(2**BITS)+F(1,2)
    numerator=shifted.numerator//shifted.denominator
    assert numerator==row['low_word_dyadic_numerator']
    assert 0<=numerator<=2**BITS
    wd=F(numerator,2**BITS)
    round_errors.append(abs(wd-w))
    # Truth is used only after the selector is reconstructed from counts.
    p0=F(1,10)+H[i]/20;p3=F(7,20)+H[i]/10
    actual=wd*p0+(1-wd)*2*p3*(1-p3)
    assert actual==F(row['actual_flip'])
    row_errors.append(abs(actual-target))
assert max(round_errors)<=F(1,2**(BITS+1))
assert max(row_errors)==F(report['max_true_macro_row_error'])
assert 2*len(H)*N==report['native_calibration_calls']==800000
out={'scope':'Audit of saved synthetic observations and finite-count implementation table; not physical data or a rerun of receiver proof',
     'saved_native_bits_verified':800000,'packed_arrays_verified':len(readouts),
     'post_calibration_state_verified':post,'dyadic_rows_verified':len(row_errors),
     'selector_bits':BITS,'row_selector_uses_hidden_parameter':False,
     'maximum_rounding_error':str(max(round_errors)),
     'maximum_true_row_error':str(max(row_errors)),
     'native_words':['T0','T3 T3'],'native_call_range':[1,2],
     'identity_branch_used':False,
     'max_magnetization_error_through_1000':report['transient_max_through_1000']['magnetization'],
     'error_at_step_1000':next(r['magnetization_error'] for r in report['transient_samples'] if r['macrostep']==1000),
     'readout_counts':readouts}
p=Path(__file__).with_name('ROBUST_PHYSICAL_INTERFACE_CHECKS.json')
p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='readout_counts'},indent=2))
