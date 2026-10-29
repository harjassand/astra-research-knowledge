# Reviewer-originated separate improvement: symmetric input transducer

2026-10-29. New construction by `producer-workspace/review_finite_quantum_sampler`; **not independently accepted by this reviewer** and not imported into the receiving acceptance of author v1.

Let A be the frozen author 16×81 rational transducer and Π+=(I+SWAP)/2 on its two 9-dimensional inputs. Define B=2AΠ+. Entrywise B[:,9j+k]=A[:,9j+k]+A[:,9k+j]. Since the physical inputs are c⊗c, Π+ acts identically and B(c⊗c)=2A(c⊗c)=(2/3)q⊗q.

Exact rational calculation gives AAᵀ spectrum {0 (six),1/4 (one),1/2 (nine)}, while (AΠ+)(AΠ+)ᵀ has eigenvalues {0 (six),1/4 (ten)}. More directly, BBᵀ is symmetric and idempotent, with exact trace10. It is therefore an orthogonal projector, so B is a contraction and a valid heralded Kraus operator. This proves success4/9 for two normalized rotation programs. One identity-Bell gate attempt gives conditional combined success1/9, and two successful attempts give1/36. Acquisition yield remains unchanged and may vanish.

`independent_checks.py` verifies exact projector identities and the full symbolic quaternion polynomial identity. `SYMMETRIZED_TRANSDUCER_CANDIDATE.json` retains the rational matrix. Another agent should independently check these new load-bearing claims before Astra acceptance. No optimum or novelty is claimed.
