exec(open('/workspace/shared/interchange_local_saturation/pair_profile_check.py').read().split('rows=[]')[0])
n=6;edges=[(i,i+1) for i in range(5)];rs=np.array([1,10,100,1000,10000.])
for start in [1,2,3,4]:
    for W in [1e5,1e6,1e7]:
        boost=rs.copy();boost[start:]=W
        b,per,mn=profile_certificate(n,edges,boost,rs)
        # finite cap tail by general local theorem, mfast edges simultaneously reduced from infinity.
        s=n-start;c=s*(s-1)/4;boundary=rs[start-1];mfast=n-1-start
        tail=mfast*c*c/W*(boundary*boundary+2*(1+boundary)*(2+math.log(W/c)))
        print(start,W,b,tail,b+tail,per,flush=True)
