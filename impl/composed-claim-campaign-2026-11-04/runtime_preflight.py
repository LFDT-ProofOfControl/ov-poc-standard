"""Pure path/file admission. Importing this module runs no campaign or primitives."""
import hashlib
import os
from pathlib import Path

EXCLUSIONS = ["__pycache__", "*.pyc"]

def overlap(left, right):
    left, right = Path(left).resolve(), Path(right).resolve()
    return left == right or left in right.parents or right in left.parents

def validate_disjoint(bundle, venv, output):
    paths = [Path(p).resolve() for p in (bundle, venv, output)]
    names = ["bundle", "venv", "output"]
    for i in range(3):
        for j in range(i + 1, 3):
            if overlap(paths[i], paths[j]):
                raise ValueError("Overlapping placement: "+names[i]+"/"+names[j])
    return tuple(paths)

def require_new_output(output):
    if os.path.lexists(output):
        raise ValueError("Output location already exists; no resume or replacement")

def validate_runtime_read_roots(bundle, output, readable_roots):
    for data in (bundle, output):
        for runtime in readable_roots:
            if overlap(data, runtime):
                raise ValueError("Data overlaps a sandbox-readable runtime root")

def verify_installed_inventory(site, expected, exclusions):
    if exclusions != EXCLUSIONS:
        raise ValueError("Unsupported dependency exclusion policy")
    site = Path(site).resolve(strict=True)
    if not site.is_dir():
        raise ValueError("Installed site is not a directory")
    actual = {}
    for directory, dirs, files in os.walk(site, followlinks=False):
        here = Path(directory)
        # Symlinks are rejected even at excluded names; no extra readable aliases.
        for name in dirs + files:
            if (here/name).is_symlink():
                raise ValueError("Symlink in installed site: "+str((here/name).relative_to(site)))
        excluded_directory = "__pycache__" in here.relative_to(site).parts
        for name in files:
            p = here/name
            if excluded_directory or p.suffix == ".pyc":
                continue
            if not p.is_file():
                raise ValueError("Non-regular installed file")
            actual[str(p.relative_to(site))] = hashlib.sha256(p.read_bytes()).hexdigest()
    if set(actual) != set(expected):
        raise ValueError("Installed inventory differs: missing="+repr(sorted(set(expected)-set(actual)))+
                         " extra="+repr(sorted(set(actual)-set(expected))))
    changed = sorted(name for name in actual if actual[name] != expected[name])
    if changed:
        raise ValueError("Installed dependency hash mismatch: "+repr(changed))
    return {"files":len(actual),"exact_file_set":True,"exclusions":EXCLUSIONS}
