# Finite confidence and moment scheduling for bounded projection

Root specification, pending integration into a complete online receiver. This makes explicit the finite schedule reused by the mathematical construction.

Input finite alphabet size k>=1, horizon H>=1, rational epsilon, rational statistical failure allowance delta_stat in(0,1). Let W=sum_(j=0)^H k^j and W1=sum_(j=0)^(H+1) k^j. Compute these integers by the recurrence W_(h+1)=1+k W_h, without enumerating words. Let E=1+ceil_log2(W), Jmax=(E+1)(W1+1)^2, and beta=delta_stat/(W+1)^64.

Each mean is a fresh binary-report average for one unordered descriptor pair Gamma(u,v), where both descriptors have length<=H+1. Index its cache by precision epoch b and that canonical unordered pair. Every cross/control/residual/prefix entry needed by the theorem belongs to this finite universe. Symmetry is imposed by using the SAME cached estimate for the transposed pair, not by giving inconsistent independently estimated Gram entries to the PSD guard.

At epoch b=nextpower2(m), alpha=lambda/[128(b+4)b²]. Use the common exact integer shot count

 n_b=ceil[8 alpha^-2 ceil_log2(2 Jmax/beta)].

The conditional Hoeffding bound for[-1,1] reports is at most 2exp(-n_b alpha²/2)<=beta/Jmax. An adaptive union bound over at most Jmax jobs gives a simultaneous entrywise event of probability>=1-beta. This holds even when the next descriptor is selected from all previous results. No union bound over future coefficient vectors, optimization iterates or accepted tasks is required: a fixed entrywise event controls all bounded coefficient forms.

Only request entries actually needed. Reuse them at unchanged b. Remeasure old entries only after b changes, and retain any completed data needed for the current epoch. Computing all W1² entries upfront is neither required nor permitted under the claimed good-event acquisition cost.

Source failures, nonbinary returns, PSD-guard failure, iteration-cap exhaustion, or a rejected task with no certified fresh prefix cause a permanent acquisition failure latch. Independently of data, never retain duplicate descriptors. On bad data, there are at most W successful descriptor additions and a final failed stage, ensuring finite worst acquisition work. No infinite remeasurement on later tasks is allowed after failure. Output evaluation for future accepted requests is separate deployment work.

The sample formula is a sufficient conservative calibration schedule. It is not an instruction to execute enormous budgets, and no physical reports are claimed by emulator diagnostics. If a user-specified finite episode budget is exhausted, stop before starting an unaffordable mean; do not label unsampled means as experimental data.
