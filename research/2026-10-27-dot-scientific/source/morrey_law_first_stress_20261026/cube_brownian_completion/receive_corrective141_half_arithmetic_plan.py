from pathlib import Path
from fractions import Fraction as Q
import json,hashlib
P=Path(__file__).resolve().parent;O=P/'fully_corrective141_half_K48';u=Q(1,2**53);r=Q(1,2**37);w=Q(1,2**39);gamma=lambda n:n*u/(1-n*u)
factor=(1+gamma(256))*(1+gamma(2048))*(1+gamma(16))*(1+gamma(6))-1
diff=(2+w)*((1+r)**3-1)+w+(2+w)*(1+r)**3*factor
moment=Q(1,2**33)+diff+gamma(2)*(4+diff);assert moment<Q(1,2**30)
eff=(2+Q(1,2**30))*(1+Q(1,2**36))*(1+Q(1,2**40))**2*(1+r)**3*(1+gamma(32768))-2;assert eff<Q(1,2**29)
A=Q(json.loads((P/'epsilon_half_discriminator/half_epsilon_budget_receipt.json').read_text())['amplification']);numeric=A*Q(1,2**29)+Q(1,10**6);assert numeric<Q(1,5000)
out={'status':'CONDITIONAL_CORRECTIVE25_SOURCE_REUSE_ARITHMETIC_PLAN','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'basis_radius':str(r),'signed_weight_L1_error_max':str(w),'signed_mass_TV_max':'2','block_size_max':256,'block_count_max':2048,'saved_original_moment_error':'1/8589934592','new_difference_moment_error_upper':str(diff),'new_source_signed_moment_error_upper':str(moment),'declared_moment_guard':'1/1073741824','effective_field_guard':'1/536870912','actual_contraction_operation_count':32768,'functional_amplification':str(A),'calculated_numerical_payment':str(numeric),'declared_numerical_payment':'1/5000','scope':'New exact candidate proxy minus original computational endpoint proxy, plus saved original signed-source tensor. Original source384 quadrature unchanged. Every weight/count/basis/H/b bound must be checked by execution; exact source/actual proxy transfer separate. Gamma32768 covers actual9216-term edge einsum.'};(O/'arithmetic_plan_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(float(diff),float(moment),float(eff),float(numeric))
