"""Exact GF(2) column-span membership; integer-bitset implementation."""
def pivots(columns):
    out={}
    for v in columns:
        while v:
            p=v.bit_length()-1
            if p in out: v ^= out[p]
            else:
                out[p]=v
                break
    return out

def member(v,P):
    while v:
        p=v.bit_length()-1
        if p not in P: return False
        v ^= P[p]
    return True
