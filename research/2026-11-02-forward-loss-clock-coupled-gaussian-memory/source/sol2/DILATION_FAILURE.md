# Why individually exact free Gaussian channels are insufficient

A one-mode damping channel can be implemented at any fixed t by one fresh vacuum oscillator. That does not supply a coherently timed physical dilation.

Take decay rate gamma=1 and one initial photon. In a common output-field coordinate s, the physical loss wavepacket after duration t is

    phi_t(s)=exp(-s/2) 1_[0,t](s).

The common-field loss overlap is

    <phi_t1,phi_t2>=1-exp[-min(t1,t2)].

If every duration's loss wavepacket is instead compressed to the SAME auxiliary photon basis state, an individually exact amplitude-damping dilation gives the cross-duration loss overlap

    sqrt[(1-exp(-t1))(1-exp(-t2))].

At t1=log2, t2=log4 these are0.5 and sqrt(3/8)=0.6123724357. Including the remaining-photon branch, the full overlaps are0.8535533906 and0.9659258263. A coherent control register distinguishes these dilations. Thus a controlled interval channel, or a different Gram basis chosen for every history, cannot be inserted as a common emitted field without earning the cross-history overlaps.

The new compiler avoids that operation. Every INNER free block is the no-jump contraction Gamma(F), whose good output field is vacuum under every time partition. That common vacuum has no duration-dependent compressed-photon basis to align. Actual OUTER losses are represented by their common physical time/color Kraus amplitudes and retained through complete-isometry amplification. Only after amplification can the private orthogonal record be read. This is why the source construction does not hide lost-field memory in an assumed free-channel oracle.
