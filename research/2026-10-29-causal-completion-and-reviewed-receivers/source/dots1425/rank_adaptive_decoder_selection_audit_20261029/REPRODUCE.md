# Reproduction

```sh
python independent_checks.py
mkdir -p author_replay
cp source_snapshot/check_selection.py author_replay/
python author_replay/check_selection.py
```

Python3 standard library suffices. The independent file writes `INDEPENDENT_CHECKS.json`; author replay writes only `author_replay/check_selection.json`. The latter reproduced the frozen JSON exactly. All source snapshots remain unchanged. The receipt binds the required least-integer schedule clarification separately from the original governing theorem.
