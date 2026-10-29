"""Deterministic exact value-polynomial identity certificate, not probabilistic CRT."""
from pathlib import Path
src=(Path(__file__).parent/'modular_value.py').read_text().split('mod=1;res=')[0]
src=src.replace('return [A[i][-1] for i in range(n)]+[1]','result=[A[i][-1] for i in range(n)]+[1]\n assert all(sum(result[k]*cols[k][i] for k in range(n+1))%pr==0 for i in range(n))\n return result')
exec(compile(src,'modular_value_library','exec'))
start=time.time();candidate=json.loads((PTH/'candidate_value_polynomial.json').read_text());coeff=[Fraction(c) for c in candidate['monic_coefficients_low_to_high']];ints=[int(c) for c in candidate['integer_coefficients_low_to_high']];height=json.loads((PTH/'value_polynomial_height_bound.json').read_text());H=int(height['primitive_coefficient_height_bound']);threshold=2*H*H
assert all(abs(c)<=H for c in ints) and math.gcd(*ints)==1 and len(coeff)==41 and coeff[-1]==1
assert all(Fraction(c,ints[-1])==r for c,r in zip(ints,coeff))
mod=1;pr=1000000007;primes=[];failures=[]
for attempt in range(512):
 try:got=charpoly(pr)
 except ValueError as e:failures.append([pr,str(e)]);pr=int(s.nextprime(pr));continue
 assert all(c.denominator%pr and c.numerator*pow(c.denominator%pr,-1,pr)%pr==a for c,a in zip(coeff,got))
 mod*=pr;primes.append(pr)
 if len(primes)%32==0:print(len(primes),mod.bit_length(),time.time()-start,flush=True)
 if mod>threshold:break
 pr=int(s.nextprime(pr))
else:raise RuntimeError('512prime exactverification budget exhausted')
out={'status':'EXACT_CHARPOLY_AND_P_LAMBDA_IDENTITY_BY_HEIGHT_BOUND','degree':40,'prime_count':len(primes),'primes':primes,'skipped_primes':failures,'product_modulus':str(mod),'modulus_bits':mod.bit_length(),'required_bound':str(threshold),'strict_modulus_threshold_verified':True,'candidate_primitive_integer_coefficient_bits':max(abs(a).bit_length() for a in ints),'proven_actual_primitive_coefficient_height_bits':H.bit_length(),'every_modular_krylov_rank':40,'every_modular_p_lambda_identity_verified':True,'seconds':time.time()-start,'input_sha256':hashlib.sha256((PTH/'quotient_input.json').read_bytes()).hexdigest(),'candidate_sha256':hashlib.sha256((PTH/'candidate_value_polynomial.json').read_bytes()).hexdigest(),'height_bound_sha256':hashlib.sha256((PTH/'value_polynomial_height_bound.json').read_bytes()).hexdigest(),'proof':'The true primitive value polynomial has coefficient height≤H by the exact Macaulay/Hadamard/Mahler bound. Modular full-rank multiplication-algebra checks identify its monic characteristic coefficients modulo each admissible prime. Candidate primitive coefficients≤H. Cross-multiplied rational coefficient differences are integers of magnitude≤2H² divisible by their product M>2H²; hence every difference is zero. Thus p is exactly the multiplication characteristic polynomial and p(lambda)=0 in Q[z]/U, without probabilistic reconstruction assumptions.'}
(PTH/'deterministic_exact_verification.json').write_text(json.dumps(out,indent=2)+'\n');print('EXACT_VERIFIED',len(primes),mod.bit_length(),out['seconds'],flush=True)
