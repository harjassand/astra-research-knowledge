"""Finite exact checks of the dyadic completion compiler's arithmetic.

These do not certify the source factoring theorem or an acquired mass decoder.
"""
from fractions import Fraction as F
import json
from pathlib import Path


def filters(width, denominator_bits, numerator):
    B = denominator_bits
    E = width+3
    assert 2**(B-1) <= numerator <= 2**B
    K = 2**(E-1+B)//numerator
    D = 2**(B+E-1)-numerator*K
    assert 0 <= K <= 2**E
    assert 0 <= D < numerator
    p = F(numerator,2**B)
    C = F(K,2**E)
    q = F(D,2**(B+3))
    assert 0 <= C <= 1
    assert 0 <= q <= F(1,8)
    assert p*C/2 + q/F(2**(width+1)) == F(1,4)
    return K,D,C,q


def main():
    count = 0
    for W in range(1,9):
        for B in range(1,11):
            for P in range(2**(B-1),2**B+1):
                filters(W,B,P)
                count += 1

    # Actual finite toy preparation: a branch bit and six Hadamard bits.
    # Ordinary output is AND(r1,r2), hence the unique valid output zero
    # has p=3/4. The decoder supplies P=3,B=2 on that verified output.
    # Guess output is r1; its independent five-bit coin has threshold D.
    W,B,P = 1,2,3
    K,D,C,q = filters(W,B,P)
    signs = []
    accepted = 0
    ordinary_accepted = 0
    guess_accepted = 0
    for branch in range(2):
        for r in range(64):
            r1,r2 = (r>>5)&1,(r>>4)&1
            if branch == 0:
                output = r1*r2
                flag = output == 0 and (r & 15) < K
                ordinary_accepted += int(flag)
            else:
                output = r1
                flag = output == 0 and (r & 31) < D
                guess_accepted += int(flag)
            if flag: assert output == 0
            accepted += int(flag)
            signs.append(-1 if flag else 1)
    assert accepted == 32
    overlap = F(sum(signs),len(signs))
    assert overlap == F(1,2)
    # R_psi after the success sign gives 2 on good coordinates,0 elsewhere,
    # with a common original amplitude1/sqrt(128). No floating point needed.
    reflected_coefficients = [2*overlap-sign for sign in signs]
    assert all(v == (2 if sign == -1 else 0) for v,sign in zip(reflected_coefficients,signs))
    assert sum(v*v for v in reflected_coefficients)/len(signs) == 1
    result = {
        "status":"finite exact arithmetic and a reversible toy history preparation; general proof is in the report",
        "rational_filter_cases":count,
        "widths_checked":[1,8],
        "denominator_bits_checked":[1,10],
        "toy":{"P":P,"B":B,"W":W,"K":K,"D":D,"ordinary_retention":str(C),"guess_retention":str(q),"history_count":128,"ordinary_accepted":ordinary_accepted,"guess_accepted":guess_accepted,"total_accepted":accepted,"success_probability":"1/4","reflected_good_probability":"1","postselection_used":False},
        "unproved_or_unacquired":["global source factoring theorem","general exact mass decoder acquisition","historical novelty"]
    }
    Path(__file__).with_name('exactification_check_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
