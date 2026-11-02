import mpmath as mp
mp.mp.dps=100

def gap(K): return 2*(1-mp.cos(mp.pi/K))
def thermal(K,x):
    # Bessel representation resolves exponentially small flux contrast.
    if x/K**2>0.1:
        lp=mp.log(sum(mp.exp(2*x*(mp.cos(2*mp.pi*m/K)-1)) for m in range(K)))+2*x
        lm=mp.log(sum(mp.exp(2*x*(mp.cos((2*m+1)*mp.pi/K)-1)) for m in range(K)))+2*x
        return (lp-lm)/x, None
    b0=mp.besseli(0,2*x)
    even=b0; odd=mp.mpf('0')
    for ell in range(1,10000):
        b=2*mp.besseli(ell*K,2*x)
        if ell%2: odd+=b
        else: even+=b
        if b/b0<mp.mpf('1e-110'): break
    r=odd/even
    return 2*mp.atanh(r)/x, r
if __name__=='__main__':
    print('K,beta_t,DeltaF_over_t,zero_T_gap_over_t')
    for K in [4,8,16,180]:
        for x in [1,10,100,1000,10000]:
            F,r=thermal(K,x)
            print(K,x,mp.nstr(F,12),mp.nstr(gap(K),12),sep=',')
