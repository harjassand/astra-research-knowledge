# Isolated replay layout correction

The first root replay copied each worker into root/replay/<name>, while several scripts locate originals/root/other workers two parent directories above themselves. Four of eight invocations failed with FileNotFoundError at that wrong scratch path. Their algorithms had not failed a mathematical assertion. The initial ROOT_REPLAY_RECEIPT.json is retained without changing its failures; detailed original logs remain in the research workspace root/replay.

The corrected replay_public_evidence.py explicitly rehydrates exact original and derived artifacts into originals/, root/, and workers/<name> in a new scratch directory. All nine selected exact replays then passed. PUBLIC_REPLAY_RECEIPT.v0002.json records that separate execution. Sources and worker proofs were not changed to make the checks pass.

For a published checkout, run:

    python3 updates/GA-conformal-causal-genesis-20261016/package/derived/root/replay_public_evidence.py --package updates/GA-conformal-causal-genesis-20261016/package --output /tmp/astra-ga-replay-new

The output must not already exist. Python3 and SymPy are needed for the scripts that use symbolic algebra; the independent stress audit uses Python standard-library Fraction arithmetic. This wrapper does not execute optimizers or acquire external fulltexts/data. Producer verifiers were separately replayed from original nested ZIPs, and their original logs/receipts are retained in ga_source_replay/replay. No replay formalizes the analytic density/interpolation arguments, clears historical priority, or establishes a physical operation.

The subsequent PUBLIC_REPLAY_RECEIPT.v0003.json records twelve passing checks after adding the exact all-r constructor, independent all-r Fraction audit, and independent mixed-source falsifier. This is a separately preserved expansion of the replay scope, not a replacement of the earlier failure or corrected nine-check receipt.
