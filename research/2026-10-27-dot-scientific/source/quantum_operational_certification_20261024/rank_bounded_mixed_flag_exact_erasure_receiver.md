# Rank-bounded mixed flags with orthogonal reset: source-unknown relative recovery

2026-10-27. New model-family theorem, independent receipt requested. This is not a theorem for all zero-deficit channels or for overlapping noisy mixed-success sources.

## Source promise and result

Let a fixed stationary memoryless channel be

 E(rho)=p V(rho tensor sigma)V*+q Tr(rho)tau,
 p+q=1, p>=p0>0,

where V:C3 tensor F ->B is an unknown isometry, sigma is an unknown density operator of rank at most a supplied r, and reset is orthogonal to the whole success code (tau V=0). Receiver dimension may be arbitrarily large and finite. No nonzero lower bound on the eigenvalues of sigma is supplied.

For every0<nu<=1 the construction below uses ordinary labelled mixed training to produce a COMPLETE accepted-qutrit/erasure instrument whose composition with E is within unhalved diamond error less than nu p of

 p identity+(1-p)erasure.

Its consumed training cost is O(r²/(p0² nu³)) times explicit logarithmic factors; at fixed relative accuracy it is quadratic in r/p0 and has no raw receiver-dimension sample factor. Gate width and memory remain dimension dependent. Fresh training is consumed for every datum.

## 1. Reset-cancelled contrast and exact sector structure

Let J be normalized Choi, omega=I_A/3 tensor E(I3/3), and T=(J+3omega)/4, available through the received ordinary labelled mixed-sample preparation. Use

 H=J-omega=4T-4omega.

The reset terms cancel exactly. If sigma=sum_k s_k|k><k| and V_k|a>=V|a,k>, H has eigenvalue8p s_k/9 on the Bell vector Phi_(V,k), eigenvalue-p s_k/9 on the other eight logical Bell directions in that flag sector, and zero outside success support.

The nine known Weyl rotations on A give orthogonal bands P_j, each of rank rank(sigma). Their union is the common success projector Q=I_A tensor V(I3 tensor supp(sigma))V*. Every T_j and omega commutes with Q and has code weight

 Tr(Q T_j)=Tr(Q omega)=p.

Known A-Weyl and ancillary gates preserve Q. The corrected physical Bell components are V_k*/3; summing all nine labels recovers rho exactly on the success branch and rejects reset exactly. The ideal complete target is therefore the displayed p-throughput erasure channel.

## 2. Low-weight transition modes are charged, not resolved

Set

 s*=nu/(8r), xi=nu/2.

Flag sectors with s_k<s* have total conditional success weight at most r s*=nu/8. Their original-source mass is at most nu p/8, so arbitrary behavior there costs at most nu p/4 in complete unhalved diamond distance.

On every remaining good flag sector the positive H_j eigenvalue is at least8p0s*/9. Classify at H-value4p0s*/9. All nonpositive directions, including reset and zero modes, lie below this threshold. The good-sector margin is at least4p0s*/9.

There may be eigenvalues arbitrarily close to the threshold. Every such positive transition mode has flag weight below s*, so it is already charged. No hard cutoff gap or unknown flag projection is assumed or implemented. The flag split is analytical and has weights independent of the logical input/reference.

## 3. Explicit finite protocol and cost

Choose

 L=max(1,ceil log_16[900/(p0 xi)]),
 eta=(xi/(100L))²,
 M=2^m the least power of two at least768/(p0s*),
 R=ceil log_2(1/eta),
 S=9LR pi(M-1).

For each label use L fresh nondestructive classifiers and accept that label only if all pass. At a label's first failure retain A,B and advance to the next label. Correct the first accepted label; erase only after all nine labels fail.

A classifier uses R coherent QPE runs for exp[i pi(H_j+I)/2] and phase acceptance interval

 [1/4+p0s*/9,3/4).

On good sectors and reset, the phase margin is at least p0s*/9. The stated grid more than meets the finite-QPE tail requirement. Copy the reversible majority decision and uncompute QPE work before measuring it, so the retained accepted/rejected states preserve the required good-sector coherences.

For each forward or reverse controlled time t, take

 N_t=ceil[10^6 |t| S/xi]

fresh signed rounds, with angles4t/N_t,-4t/N_t. A conservative controlled simulation bound256t²/N_t applies (the4,-4 pair actually permits a smaller constant). Thus total squared pair time Htot<=xi/10^6 and total simulator error<=0.000256xi.

The fixed training cap is

 n_train<=2*10^6 S²/xi+36LRm.                        (1)

Each round consumes two original labelled training calls or two full Choi copies. Negative-time uncomputation uses fresh mixed programs, not inverse preparation. Add one physical use for the datum when reporting total uses.

## 4. Good success sectors and low-weight sectors

Restricted to good success sectors, each ideal finite-QPE classifier differs from the exact retained-data Lueders band instrument by at most4sqrt(eta). Across9L classifiers this is0.36xi. Ideal intermediate operations preserve each flag sector, so this restricted telescope is valid with arbitrary external references.

Adding uniform simulation, the original good-success branch contributes less than0.361p xi. The low-weight success branch contributes at most nu p/4 as already charged. This does not ask the simulator for absolute error of order p.

## 5. Reset: complete first-import/no-import accounting

Reset begins outside Q. Since all fresh programs are Q-block diagonal, exact controlled partial-SWAPs preserve joint Q/complement block diagonality with every control and reference. Virtual sector measurements are therefore valid for the analysis only; no unknown support oracle is physically used.

An outside input imports code population in one controlled collision of angle a with probability at most p sin²a. First-import histories across both signed steps give

 Pr(any import)<=p sum[sin²(4delta)+sin²(-4delta)]
 <=32p Htot<=0.000032p xi.

Without import the state remains outside Q, where ideal H_j=0. Each classifier's outside acceptance is at most beta=eta+256h, with h<=Htot/(9L), so beta<1/16. The no-import accepted histories are positive CP submaps, and the bound holds for arbitrary conditional joint states. Fresh programs allow multiplication through all L passes; union over labels gives

 Pr(reset accepted without import)<=9beta^L
 <=p0xi/100<=p xi/100.

The complete accepted-plus-erased reset error is twice its accepted mass, less than0.020064p xi. Earlier rejected labels retain the outside state on no-import histories, so every failure branch is included.

## Complete guarantee and scope

Combining all original-source branches,

 complete error <0.361p xi+0.020064p xi+nu p/4
                <0.441nu p<nu p.

The consumed sample cap(1) has fixed-accuracy scaling r²/p0² up to logarithms. The flat Haar subclass p=r/D has the independently received Omega(r²/p²) lower bound in FULL-CHOI-PROGRAM access, so those rank/signal exponents cannot be improved uniformly in that model. No matching quadratic lower for arbitrary adaptive physical queries is asserted.

This theorem requires the explicit mixed-flag isometry and orthogonal-reset model. It does not follow solely from zero entropy deficit, does not cover arbitrary reset overlap, and supplies no reusable learned decoder or free multi-data amortization. The p=1 case gives rank-controlled inversion of arbitrary reversible mixed flags without a minimum flag eigenvalue or ambient-dimension sample penalty.
