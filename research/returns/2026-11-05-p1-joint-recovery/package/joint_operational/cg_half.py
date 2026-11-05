"""Deterministic spin-J plus spin-half Clebsch-Gordan isometries.

Input order Q_J tensor E, magnetic bases descending.  Output path signs are
fixed by the explicit formulas below, so the relative phase is reproducible.
"""
import numpy as np

def cg_half(j,sign):
    """Return C: Q_(j+sign/2) -> Q_j tensor C^2, sign in {-1,+1}."""
    out_j=j+sign/2
    if out_j<0:return np.zeros((2*int(round(2*j+1)),0),float)
    d=int(round(2*j+1));D=int(round(2*out_j+1));c=np.zeros((2*d,D),float)
    for col in range(D):
        mag=out_j-col
        # Up component |j,mag-1/2>|up>; down |j,mag+1/2>|down>.
        m_up=mag-.5;m_down=mag+.5
        if sign==1:
            a=np.sqrt(max(0,(j+mag+.5)/(2*j+1)))
            b=np.sqrt(max(0,(j-mag+.5)/(2*j+1)))
        else:
            a=-np.sqrt(max(0,(j-mag+.5)/(2*j+1)))
            b=np.sqrt(max(0,(j+mag+.5)/(2*j+1)))
        if -j-1e-10<=m_up<=j+1e-10:c[2*int(round(j-m_up)),col]=a
        if -j-1e-10<=m_down<=j+1e-10:c[2*int(round(j-m_down))+1,col]=b
    return c


def payload_fusion_paths(j,total):
    """CG columns in R_half tensor Q_j tensor E_half for fixed total spin.

Returns (path_sign, isometry) pairs, path_sign denoting Q_j+E fusion.
Columns are magnetic m=total,...,-total.  At total=j, the two returned
isometries give a deterministic multiplicity basis for the 2x2 mixing.
"""
    result=[]
    for sign in [1,-1]:
        fused=j+sign/2
        if fused<0:continue
        total_sign=int(round(2*(total-fused)))
        if total_sign not in [-1,1] or total<0:continue
        inner=cg_half(j,sign)
        outer=cg_half(fused,total_sign) # fused tensor R_half
        if outer.shape[1]!=int(round(2*total+1)):continue
        # Reorder fused,R to R,fused before embedding fused into gauge,E.
        outer=outer.reshape(int(round(2*fused+1)),2,-1).transpose(1,0,2).reshape(2*int(round(2*fused+1)),-1)
        result.append((sign,np.kron(np.eye(2),inner)@outer))
    return result


if __name__=='__main__':
    from rep_control import spin_rep,tensor_rep
    for j in [0,.5,1.,1.5,3.]:
        c=np.concatenate([cg_half(j,1),cg_half(j,-1)],axis=1)
        assert np.linalg.norm(c.T@c-np.eye(len(c)))<1e-12
        rep=tensor_rep(tensor_rep(spin_rep(.5),spin_rep(j)),spin_rep(.5));plus,z=rep
        vectors=[]
        for total in [j+1,j,j-1]:
            if total<0:continue
            for sign,u in payload_fusion_paths(j,total):
                p2,z2=spin_rep(total)
                assert np.linalg.norm(plus@u-u@p2)<1e-12
                assert np.linalg.norm(z@u-u@z2)<1e-12
                vectors.append(u)
        u=np.concatenate(vectors,axis=1)
        assert np.linalg.norm(u.T@u-np.eye(len(u)))<1e-12
    print('CG phase convention, completeness, and generator intertwiners checked.')
