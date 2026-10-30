# Physical-site repair required for the native warm handoff
30 October 2026. Independent audit finding; finite correction, not an obstruction theorem.

The actual physical convention in producer-workspace/REPAIRED_GENERATOR.md, section Physical sites and fixed parameters, puts payload DATA and lock in the SAME resource qudit. The monitor construction subsequently adds a local monitor. Therefore a delivered DATA qubit and its lock/monitor initialization cannot be counted as two disjoint physical output regions with respective strengths p_dec,p_app and a maximum bound. One actual resource-site perturbation can affect both subregisters.

Use one region per physical resource, containing its DATA and lock/monitor. It receives both the output decoder and the local auxiliary reset/idle module. Keep hub-only regions separate. Serialize operations that share that physical site in the final fixed-duration window, or explicitly combine them into one bounded-body target gate and use its actual cavity bound. The sequential option is simplest and costs only a fixed constant.

Define a resource region bad when either its output decoder or its local boot module is bad. Their location sets are now genuinely disjoint by schedule. Exact inclusive OR sieving gives

    p_resource <= (1+p_dec)(1+p_app)-1.

Use p=max(p_resource,p_hub), rather than max(p_dec,p_app), in the region-cardinality bound. All sites belong to one region, so the bounded-body shared-bath law applies with its actual site convention. This change preserves p=O(x0), all exponential density tails and the finite footprint conversion.

Finally the resource boot reset must be Id_DATA tensor replacement_(lock,monitor), not a replacement of the whole resource qudit. The latter would erase already delivered quantum DATA. The accepted finite native activation source explicitly resets only clock/workspace/tag factors and acts as DATA identity. Resetting the optional monitor factor too is allowed only with the declared local replacement primitive. Finite-time residual errors remain charged; no exact physical reset is claimed.
