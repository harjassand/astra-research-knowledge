"""Disposable replay guard: no network or writes outside the execution tree."""
import os
from pathlib import Path
import sys

WRITE_ROOT = Path(os.environ["ASTRA_REPLAY_WRITE_ROOT"]).resolve()
ORIGINAL_R = Path(os.environ["ASTRA_REPLAY_ORIGINAL_R"]).resolve()
ORIGINAL_W = Path(os.environ["ASTRA_REPLAY_ORIGINAL_W"]).resolve()
AUDIT_ROOT = WRITE_ROOT.parent


def path(value):
    if isinstance(value, (str, bytes, os.PathLike)):
        return Path(os.fsdecode(value)).resolve()
    return None


def writable(value):
    target = path(value)
    if target is not None and not target.is_relative_to(WRITE_ROOT):
        raise PermissionError("Replay guard refused write outside disposable execution tree: " + str(target))


def audit(event, args):
    if event in {"socket.connect", "socket.connect_ex", "socket.getaddrinfo", "socket.bind"}:
        raise PermissionError("Replay guard refused network operation: " + event)
    if event == "open":
        target, mode, flags = args
        writing = (isinstance(mode, str) and any(c in mode for c in "wax+")) or bool(
            isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)
        )
        if writing:
            writable(target)
        else:
            target = path(target)
            if target is not None and target.is_relative_to(ORIGINAL_W):
                raise PermissionError("Replay guard refused original W data read: " + str(target))
            if target is not None and target.is_relative_to(ORIGINAL_R):
                if not target.is_relative_to(AUDIT_ROOT) and not target.is_relative_to(ORIGINAL_R / ".venv"):
                    raise PermissionError("Replay guard refused original R data read: " + str(target))
    elif event in {"os.remove", "os.rmdir", "os.mkdir", "os.chmod", "os.utime", "os.truncate"}:
        writable(args[0])
    elif event in {"os.rename", "os.link", "os.symlink"}:
        writable(args[0])
        writable(args[1])


sys.addaudithook(audit)
