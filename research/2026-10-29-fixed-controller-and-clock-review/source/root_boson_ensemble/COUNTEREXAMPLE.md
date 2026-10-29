# Stable native bosons: grand positivity need not survive total-number projection

Root construction29October2026, shared with the canonical researcher. This is
an ensemble-admission counterexample, not a sign-problem hardness claim. This
diagonal model already has a trivial positive occupation representation.

Two sites, two flavors, no hopping:
H=U sum_i(nb_i-nc_i)^2-mu(Nb+Nc), U>0,mu<0. The physical grand partition is
finite, with no occupation cutoff. The exact Gaussian identity
exp(-beta U q^2)=E exp(i theta q), theta~N(0,2beta U), gives independent fields
and B_b=r diag(exp(i theta1),exp(i theta2)), B_c=B_b*, r=exp(beta mu)<1.

For every field the grand weight det(I-zB_b)^-1 det(I-zB_c)^-1 is finite and
nonnegative at z=1. At theta1=pi/2,theta2=-pi/2 it is(1+r^2 z^2)^-2, whose
TOTAL-N=2 coefficient is -2r^2. Separately fixed(1,1) instead has coefficient
|h1(B_b)|^2=0. These are different ensembles.

Negativity has positive Gaussian measure. In the phase rectangle of halfwidth
epsilon around that point, |h1|<=2r epsilon and |h2+r^2|<=6r^2 epsilon.
Thus [z^2]W=2Re h2+|h1|^2<=r^2(-2+12epsilon+4epsilon^2)<-r^2 at epsilon=1/16.

Choose r=1/2,beta U=ln2/2. Exact physical occupation enumeration gives
Z2=r^2[2+4exp(-2beta U)+4exp(-4beta U)]=5/4;
Z11=r^2[2+2exp(-2beta U)]=3/4; Z20=Z02=1/4.
At the phase center the total-N field coefficient is-1/2 and grand weight16/25.
One HS slice is exact since all number operators commute. This refutes transfer
of configurationwise grand positivity, not existence of a physical canonical
law or all other positive canonical representations. No frustrated-phase,
simulation-advantage or historical-priority claim follows.
