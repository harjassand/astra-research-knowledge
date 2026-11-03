exec(open('producer-workspace/wilson_endpoint.py').read().split('out=[]')[0])
L=3;h=slab(L);M=2;lam=.4;Hs=[full(h,L,p,M,lam) for p in [pa,pb]]
ees=[la.eigvalsh(H) for H in Hs];delta=la.norm(Hs[1]-Hs[0],2)
np.savez(D+'complete_endpoint_spectra.npz',e_a=ees[0],e_b=ees[1],delta_operator_norm=delta,phi_a=pa,phi_b=pb)
print('representative perturbation norm',delta,'minabs',min(abs(ees[0])))
# Translation-invariant check of boundary relocation retains ALL normal-direction orbitals.
L=12;k=np.pi/24
for M in [0,2,8,64]:
 h=np.zeros((4*L,4*L),complex)
 for w in range(L):
  h[4*w:4*w+4,4*w:4*w+4]=np.sin(k)*G[0]+(-1+1-np.cos(k)+1)*G[4]
  if w<L-1:
   t=-.5*G[4]+G[3]/(2j);h[4*w:4*w+4,4*w+4:4*w+8]=t;h[4*w+4:4*w+8,4*w:4*w+4]=t.conj().T
 P=np.zeros_like(h);P[:4,:4]=np.eye(4);H=np.block([[h,M*P],[M*P,-h]])
 e,v=la.eigh(H);ids=np.argsort(abs(e))[:8]
 # Sum all near-low-energy eigenspace weights to remove accidental eigenvector basis choices.
 weight=np.sum(abs(v[:,ids].reshape(2,L,4,8))**2,axis=(0,2,3))/8
 print('M',M,'lowabs',abs(e[ids]),'layerweight',weight)
