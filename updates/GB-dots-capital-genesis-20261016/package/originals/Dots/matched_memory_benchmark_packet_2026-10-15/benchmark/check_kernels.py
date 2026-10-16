from independent_audit import *
exe=str(ROOT/'audit_simulator');n=0
for L in (4,):
    for x in ((0,0,0,0),(L-1,)*4):
        vertex=encode((x,(0,)),L)
        for mask in range(256):
            s=set()
            for a in range(4):
                if mask&(1<<a):s.add((x,(a,)))
                if mask&(1<<(a+4)):
                    y=list(x);y[a]=(y[a]-1)%L;s.add((tuple(y),(a,)))
            p=subprocess.run([exe,'kernel',str(L),'sweep',str(vertex)],input=' '.join(str(encode(e,L)) for e in s),text=True,capture_output=True)
            outgoing=[a for a in range(4) if mask&(1<<a)]
            if not mask>>4 and len(outgoing)%2:assert p.returncode!=0
            else:
                expected=set() if mask>>4 else {(x,tuple(outgoing[i:i+2])) for i in range(0,len(outgoing),2)}
                assert p.returncode==0
                actual={decode_id(int(i),L,2) for i in p.stdout.split()};assert actual==expected
            n+=1
        for axes in ORI:
            i,j=axes;f=(x,axes);edges=sorted(bd({f},L))
            north=list(x);north[j]=(north[j]+1)%L;north=(tuple(north),(i,))
            east=list(x);east[i]=(east[i]+1)%L;east=(tuple(east),(j,))
            for mask in range(16):
                s={e for q,e in enumerate(edges) if mask&(1<<q)}
                p=subprocess.run([exe,'kernel',str(L),'toom',str(encode(f,L))],input=' '.join(str(encode(e,L)) for e in s),text=True,capture_output=True,check=True)
                actual={decode_id(int(i),L,2) for i in p.stdout.split()}
                assert actual==({f} if north in s and east in s else set());n+=1
res={'status':'PASS','kernel_cases':n,'checks':['all incoming/outgoing patterns at origin and seam','six pairs and fixed two-face four-outgoing jump','odd outgoing rejection','Toom north/east truth table each orientation']}
(ROOT/'independent_kernel_results.json').write_text(json.dumps(res,indent=2));print(json.dumps(res))
