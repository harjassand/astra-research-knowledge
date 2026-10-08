"""Integer coefficient trace for F_e=aI+cC+dD.
C=2|psi+><psi+|, D=(X tensor X) SWAP, LSB vertex indexing.
No external libraries.
"""
def trace_word(n,edges,types):
    out=0
    for start in range(1<<n):
        vec={start:1}
        for (i,j),t in zip(edges,types):
            if t=='a':continue
            nxt={};mask=(1<<i)|(1<<j)
            for x,w in vec.items():
                bi=(x>>i)&1;bj=(x>>j)&1
                if t=='c':
                    if bi==bj:continue
                    ys=(x,x^mask)
                elif t=='d':ys=(x if bi!=bj else x^mask,)
                else:raise ValueError(t)
                for y in ys:nxt[y]=nxt.get(y,0)+w
            vec=nxt
        out+=vec.get(start,0)
    return out
