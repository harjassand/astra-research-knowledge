"""Construct independent DNA identifiers for distinct pairwise junctions.
Combinatorial code, not a physical recognition guarantee. No frame-shift claim.
"""
from itertools import combinations
BASES='ACGT'
LENGTH=10
NEEDED=1023

def decode(x,L=LENGTH):
    seq=[]
    for _ in range(L):
        seq.append(BASES[x&3]);x>>=2
    return ''.join(seq[::-1])

def encode(seq):
    v=0
    for c in seq:v=(v<<2)|BASES.index(c)
    return v

def decent(seq):
    gc=sum(c in 'CG' for c in seq)
    return 4<=gc<=6 and all(seq[i:i+3] != seq[i]*3 for i in range(len(seq)-2))

def neighbor_codes(seq):
    digits=[BASES.index(c) for c in seq]
    for i in range(len(seq)):
        for a in range(4):
            if a!=digits[i]:
                d=digits.copy();d[i]=a
                x=0
                for z in d:x=(x<<2)|z
                yield x
    for i,j in combinations(range(len(seq)),2):
        for a in range(4):
            if a==digits[i]:continue
            for b in range(4):
                if b==digits[j]:continue
                d=digits.copy();d[i]=a;d[j]=b
                x=0
                for z in d:x=(x<<2)|z
                yield x

def build():
    forbidden=bytearray(4**LENGTH)
    words=[]
    for x in range(4**LENGTH):
        if forbidden[x]:continue
        s=decode(x)
        if not decent(s):continue
        words.append(s)
        forbidden[x]=1
        for n in neighbor_codes(s):forbidden[n]=1
        if len(words)==NEEDED:break
    return words

def verify(words):
    assert len(words)==NEEDED and len(set(words))==NEEDED
    assert all(decent(x) for x in words)
    # Independent string-Hamming verification over every distinct unordered pair.
    # Does not reuse the construction's neighbor enumeration or forbidden bitmap.
    for i,u in enumerate(words):
        for v in words[i+1:]:
            if sum(x!=y for x,y in zip(u,v))<3:
                raise AssertionError((u,v))
    return True

if __name__=='__main__':
    from pathlib import Path
    words=build()
    print('Selected',len(words),'of',NEEDED)
    if len(words)==NEEDED:
        print('Independent all-neighbors check:',verify(words))
        path=Path(__file__).with_name('astra_chemistry_position_code1023.txt')
        path.write_text('Candidate 10nt position identifiers, Hamming distance >=3; GC 4-6, no homopolymer triple.\n'+ '\n'.join(' '.join(words[i:i+16]) for i in range(0,len(words),16))+'\n')
        print('Wrote',path)
