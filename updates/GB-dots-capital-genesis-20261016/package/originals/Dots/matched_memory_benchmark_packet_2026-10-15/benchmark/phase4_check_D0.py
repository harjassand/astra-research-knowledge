from independent_audit import *
exe=str(ROOT/'simulator_readouts')
count=0

def recover(s,L):
    global count
    p=subprocess.run([exe,'decode',str(L)],input=' '.join(str(encode(e,L)) for e in sorted(s)),text=True,capture_output=True,check=True)
    lines=p.stdout.splitlines();flag=int(lines[0]);D={decode_id(int(i),L,2) for i in lines[1].split()} if len(lines)>1 else set()
    assert bd(D,L)==s,(L,'boundary',s,D)
    count+=1
    return flag,D

# Every basis face at L3,4 exercises fallback, including all seams; literal H comparison.
for L in (3,4):
    for f in cells(L,2):
        s=bd({f},L);flag,D=recover(s,L)
        assert flag and D==literal_H(s,L)
# All orientations, translated and seam-straddling local faces at L16 and L17.
local=0
for L in (16,17):
    for a in ORI:
        for x in it.product((0,1,L-2,L-1),repeat=4):
            E={(x,a)};s=bd(E,L);flag,D=recover(s,L)
            assert not flag and not hom(E^D)
            local+=1
# Multi-face disks across seams, cutoff strictness; winding pairs; arbitrary random boundaries.
for L in (16,24):
    for a in ORI:
        x=[L-1]*4;y=x.copy();y[a[0]]=0
        E={(tuple(x),a),(tuple(y),a)};s=bd(E,L);flag,D=recover(s,L)
        assert flag==(L==16)
        if not flag:assert not hom(E^D)
        strip=set()
        for q in range(L):
            z=[0]*4;z[a[0]]=q;strip.add((tuple(z),a))
        s=bd(strip,L);flag,D=recover(s,L)
        assert flag and D==literal_H(s,L)
        # Add disjoint small component: all-local-or-global contract requires H on entire union.
        z=[L//2]*4;E=strip^{(tuple(z),a)};s=bd(E,L);flag,D=recover(s,L)
        assert flag and D==literal_H(s,L)
    gen=random.Random(17001+L)
    for _ in range(5):
        E={(tuple(gen.randrange(L) for _ in range(4)),gen.choice(ORI)) for _ in range(100)}
        s=bd(E,L);flag,D=recover(s,L)
        assert (not flag) or D==literal_H(s,L)
        assert recover(s,L)==(flag,D)
res={'status':'PASS','external_decode_cases':count,'seam_and_translation_single_faces':local,'checks':['independent dD=s','small-L every basis face matches literal H','strict diameter cutoff','winding components combined','all-syndrome fallback including local components','repeat determinism']}
(ROOT/'phase4_D0_executable_results.json').write_text(json.dumps(res,indent=2));print(json.dumps(res))
