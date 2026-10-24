# Correction — finite-exchange condition in the P2 return summary

This note corrects the condition attached to the 1 s^-1 finite charge-exchange comparison in the preceding [overview](README.md) and [source manifest](source_manifest.json). Their exact original bytes remain preserved and pinned by the earlier checkpoint.

The completed P2 rendered return, [source-05](source/dispatch/P2_charge_exchange_mobility_completed_1421_20261024.json), separates two conditions:

- Its Section 3 mobility-maximizing baseline at 1,200 K is near E_F − E_V ≃ 1.16 eV, with π_+ ≃ 0.664.
- Its Section 4 finite-exchange percentages are reported at 1,200 K with equal +1/0 formation energies. At that condition, 0.01 s^-1, 1 s^-1 and 100 s^-1 give about 4.6%, 70% and 99.6% of the fast-exchange diffusivity, respectively.

The 70% value must not be applied as a finite-rate correction to the 1.16 eV mobility-maximizing diffusivity. The source places the +1/0 formation-energy crossing near 1.23 eV; the two charge distributions are distinct.

This correction changes only the attribution of that reported comparison. It does not recalculate the model, recheck its literature inputs, or alter the return’s experimental, novelty, or advantage status.
