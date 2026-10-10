# Explicit qubit-concurrence gap from a Gaussian ensemble

2026-10-09 22:06 UTC. New internal derivation; no priority or external verification claim.

Let rho be a normalized PPT state on C^2 tensor C^d. Write S_a=sigma_a tensor I, R=rho, B_a=sqrt(rho) S_a sqrt(rho). For a standard circular complex Gaussian vector g, define v=sqrt(rho)g, w=v*v, b_a=v*S_a v. The homogeneous pure qubit concurrence is sqrt(w^2-|b|^2), so the deficit obeys

w-c(v) = |b|^2/[w+sqrt(w^2-|b|^2)] >= |b|^2/(2w).

The zero-weight set contributes zero. E vv*=rho and E w=1.

Put a=sum_a (tr B_a)^2, b=sum_a tr B_a^2, c=sum_a tr(rho B_a^2). All three are nonnegative; c<=b because 0<=rho<=I. Gaussian second moments give A=E|b_vector|^2=a+b. Third moments give

E[w |b_vector|^2] = A + 2 sum_a tr(rho B_a)tr B_a + 2c.

The weighted Cauchy inequality gives sum_a [tr(rho B_a)]^2 <= c, hence the middle sum is <=sqrt(ac). Consequently

E[w |b_vector|^2] <= a+b+2sqrt(ac)+2c <=2a+4b <=4A.

Cauchy applied to sqrt(|b_vector|^2/w) and sqrt(w |b_vector|^2) yields

E[|b_vector|^2/w] >= A^2/E[w |b_vector|^2] >= A/4.

The Pauli identity gives b=2 tr(rho_B^2)-tr(rho^2). PPT on the qubit implies the reduction inequality rho <= I_2 tensor rho_B, because the qubit reduction map is transpose followed by conjugation by sigma_y. Therefore tr(rho^2)<=tr(rho_B^2), and A>=b>=tr(rho_B^2)>=1/d.

It follows that this Gaussian ensemble has expected concurrence deficit at least1/(8d). The probability measure weighted by w has total mass1 and lies on the compact graph of pure-state concurrence. Its barycenter (rho,E c(v)) is in the finite convex hull of that graph, by finite-dimensional compact convexity/Caratheodory. Thus a finite ensemble attains the same pair and

C(rho) <= 1-1/(8d).

This does not assert a sharp bound. Together with exact qubit-filter covariance it supplies a uniform explicit concurrence contraction for any CP trace-preserving 2-copositive channel on M_d. The Gaussian ensemble is an existence proof, not a required random algorithm or external computation.
