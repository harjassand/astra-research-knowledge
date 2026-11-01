"""Exact GF(2) CSS TQO-2 defect, using integer-bitset generator columns.
Actual geometric support is essential: do not replace columns by a row-space basis.
No dependency on numerical rank packages. Does not instantiate the recursive code.
"""
def rank(columns):
    pivots = {}
    for col in columns:
        while col:
            p = col.bit_length() - 1
            if p not in pivots:
                pivots[p] = col
                break
            col ^= pivots[p]
    return len(pivots)

def patch_defect(columns, n_qubits, A, B):
    """A,B are integer qubit masks; returns nonnegative missing-constraint rank."""
    universe = (1 << n_qubits) - 1
    assert not (A & ~B) and not (B & ~universe)
    columns = list(columns)
    assert all(not (c & ~universe) for c in columns)
    outside_A = universe ^ A
    local = [c for c in columns if not c & ~B]
    global_supported_rank = rank(columns) - rank(c & outside_A for c in columns)
    local_supported_rank = rank(local) - rank(c & outside_A for c in local)
    defect = global_supported_rank - local_supported_rank
    assert defect >= 0
    return dict(defect=defect, global_supported_rank=global_supported_rank,
                local_supported_rank=local_supported_rank,
                local_generator_count=len(local))

def self_test():
    n=12
    A=1<<6
    B=sum(1<<i for i in (5,6,7))
    onsite=[1<<i for i in range(n)]
    anchored=[(1<<i)|(1<<(i+1)) for i in range(n-1)]+[1]
    assert rank(onsite)==rank(anchored)==n
    assert patch_defect(onsite,n,A,B)['defect']==0
    assert patch_defect(anchored,n,A,B)['defect']==1
    # Redundant actual local column restores patch equality without changing code.
    assert patch_defect(anchored+[A],n,A,B)['defect']==0
    assert patch_defect(anchored,n,A,(1<<n)-1)['defect']==0
    # Stabilizers can be local products even if no individual generator is in A.
    D=[0b011,0b110]
    assert patch_defect(D,3,0b101,0b111)['global_supported_rank']==1
    assert patch_defect(D,3,0b101,0b101)['defect']==1
    print('6 patch-rank assertions passed; anchored example detects presentation dependence.')

if __name__=='__main__': self_test()
