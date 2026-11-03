#!/usr/bin/env python3
"""Launcher: pinned orchestration metadata + isolated Python; no comparison logic."""
import argparse
import base64
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import selectors
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

DOCKER = "/usr/local/bin/docker"
CONTEXT = "desktop-linux"
PLATFORM = "linux/amd64"
IMAGE_INDEX = "sha256:4766d8b510c428e595d74b9cc5bbb2fae8e26316fffb4adc89908d79aacd58a2"
IMAGE = "python@" + IMAGE_INDEX
IMAGE_CHILD = "sha256:6e13e65c55e33adf203d77ee371cf8bf5d81bd4902ef07565721f46bf44917af"
IMAGE_CONFIG = "sha256:64d91f7b885eed272bba87909446b12ff408d4aaa5f1a0e9ca787bbea1a020b9"
TIMEOUT = 30
MAX_OUTPUT = 262144
MAX_INPUT = 4194304
BOOTSTRAP = (
    "import runpy,sys; module=sys.argv[1]; "
    "sys.path.insert(0,'/app'); sys.argv=[module]+sys.argv[2:]; "
    "runpy.run_module(module,run_name='__main__',alter_sys=True)"
)
INSPECT_FORMAT = '''{"Id":{{json .Id}},"Image":{{json .Image}},"Name":{{json .Name}},"State":{{json .State}},"Config":{"Image":{{json .Config.Image}},"User":{{json .Config.User}},"WorkingDir":{{json .Config.WorkingDir}},"Entrypoint":{{json .Config.Entrypoint}},"Cmd":{{json .Config.Cmd}}},"HostConfig":{"NetworkMode":{{json .HostConfig.NetworkMode}},"ReadonlyRootfs":{{json .HostConfig.ReadonlyRootfs}},"CapDrop":{{json .HostConfig.CapDrop}},"CapAdd":{{json .HostConfig.CapAdd}},"Privileged":{{json .HostConfig.Privileged}},"SecurityOpt":{{json .HostConfig.SecurityOpt}},"PidsLimit":{{json .HostConfig.PidsLimit}},"Memory":{{json .HostConfig.Memory}},"NanoCpus":{{json .HostConfig.NanoCpus}}},"NetworkSettings":{"Networks":{{json .NetworkSettings.Networks}}},"Mounts":{{json .Mounts}}}'''


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def strict_json(raw):
    def invalid_constant(value):
        raise ValueError("non-finite JSON constant")
    return json.loads(raw, object_pairs_hook=unique, parse_constant=invalid_constant)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def docker(args, timeout=8):
    result = subprocess.run([DOCKER, "--context", CONTEXT, *args],
                            capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError("Docker metadata/control command failed: " +
                           result.stderr[:4096].decode("utf-8", "replace"))
    return result.stdout


def checked_bytes(path, digest, maximum):
    require(isinstance(digest, str) and re.fullmatch(r"[a-f0-9]{64}", digest),
            "invalid expected SHA256")
    path = Path(path)
    require(path.is_absolute() and not path.is_symlink() and path.is_file(),
            "source must be an absolute regular non-symlink file")
    require(path.stat().st_size <= maximum, "source exceeds size limit")
    raw = path.read_bytes()
    require(len(raw) <= maximum and sha(raw) == digest, "source bytes changed")
    return raw


def orchestration_record(spec):
    """Validate preassigned identifiers and plan pin before any child execution."""
    require(isinstance(spec, dict) and
            set(spec) == {"schema_version", "module", "program_root", "files", "input",
                          "orchestration"}, "unexpected spec keys")
    require(type(spec["schema_version"]) is int and spec["schema_version"] == 2,
            "unsupported orchestration spec")
    value = spec["orchestration"]
    require(isinstance(value, dict) and
            set(value) == {"run_id", "component_run_id", "plan"},
            "unexpected orchestration keys")
    for field in ("run_id", "component_run_id"):
        require(isinstance(value[field], str) and
                re.fullmatch(r"[a-f0-9]{32}", value[field]),
                "invalid preassigned " + field)
    require(value["run_id"] != value["component_run_id"],
            "orchestration and component IDs must differ")
    plan = value["plan"]
    require(isinstance(plan, dict) and set(plan) == {"bytes", "sha256"},
            "unexpected orchestration plan pin")
    require(type(plan["bytes"]) is int and 0 < plan["bytes"] <= MAX_INPUT,
            "invalid orchestration plan byte count")
    require(isinstance(plan["sha256"], str) and
            re.fullmatch(r"[a-f0-9]{64}", plan["sha256"]),
            "invalid orchestration plan SHA256")
    return {"run_id": value["run_id"], "plan": dict(plan)}


def prepare(spec, stage):
    orchestration_record(spec)
    module = spec["module"]
    require(isinstance(module, str) and
            re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*", module),
            "invalid module")
    root = Path(spec["program_root"])
    require(root.is_absolute() and root.is_dir() and not root.is_symlink(),
            "program root must be an absolute non-symlink directory")
    require(isinstance(spec["files"], list) and 1 <= len(spec["files"]) <= 32,
            "invalid program allowlist")
    code = stage / "app"
    code.mkdir(mode=0o755)
    seen, file_records = set(), []
    for item in spec["files"]:
        require(set(item) == {"path", "sha256"}, "unexpected program item keys")
        relative = item["path"]
        require(isinstance(relative, str) and
                re.fullmatch(r"[A-Za-z0-9_./-]+", relative), "invalid program path")
        pure = PurePosixPath(relative)
        require(not pure.is_absolute() and str(pure) == relative and
                all(part not in {".", "..", ".git", "__pycache__"} for part in pure.parts)
                and pure.suffix == ".py", "unsafe program path")
        require(relative.casefold() not in seen, "duplicate program path")
        seen.add(relative.casefold())
        source = root / relative
        require(source.resolve().is_relative_to(root.resolve()), "program escapes root")
        for parent in [source, *source.parents]:
            if parent == root.parent:
                break
            require(not parent.is_symlink(), "program symlink rejected")
        raw = checked_bytes(source, item["sha256"], 1048576)
        destination = code / relative
        destination.parent.mkdir(parents=True, exist_ok=True, mode=0o755)
        with destination.open("xb") as handle:
            handle.write(raw)
        destination.chmod(0o444)
        file_records.append({"path": relative, "bytes": len(raw), "sha256": sha(raw)})
    require(module.replace(".", "/") + ".py" in {x["path"] for x in spec["files"]},
            "entry module is not in allowlist")
    require(set(spec["input"]) == {"path", "sha256"}, "unexpected input keys")
    raw = checked_bytes(spec["input"]["path"], spec["input"]["sha256"], MAX_INPUT)
    strict_json(raw)
    inp = stage / "assessor-input.json"
    with inp.open("xb") as handle:
        handle.write(raw)
    inp.chmod(0o444)
    return code, inp, file_records, {"bytes": len(raw), "sha256": sha(raw)}


def create_args(name, code, inp, module):
    require("," not in str(code) and "," not in str(inp), "mount path contains comma")
    return ["create", "--pull=never", "--platform=" + PLATFORM, "--name", name,
            "--network=none", "--read-only", "--user=65532:65532", "--cap-drop=ALL",
            "--security-opt=no-new-privileges:true", "--pids-limit=64", "--memory=256m",
            "--cpus=1", "--ulimit=nofile=64:64", "--workdir=/app",
            "--mount", "type=bind,src=" + str(code) + ",dst=/app,readonly",
            "--mount", "type=bind,src=" + str(inp) + ",dst=/input/assessor-input.json,readonly",
            "--entrypoint=/usr/local/bin/python3", IMAGE,
            "-I", "-B", "-S", "-c", BOOTSTRAP, module,
            "--input", "/input/assessor-input.json"]


def inspect_container(identifier):
    return strict_json(docker(["inspect", identifier, "--format", INSPECT_FORMAT]))


def validate_container(actual, code, inp, module):
    h, c = actual["HostConfig"], actual["Config"]
    require(c["Image"] == IMAGE and c["User"] == "65532:65532" and
            c["WorkingDir"] == "/app", "unexpected container identity/settings")
    require(c["Entrypoint"] == ["/usr/local/bin/python3"] and
            c["Cmd"] == ["-I", "-B", "-S", "-c", BOOTSTRAP, module,
                          "--input", "/input/assessor-input.json"], "unexpected command")
    require(h["NetworkMode"] == "none" and h["ReadonlyRootfs"] and
            not h["Privileged"] and not h["CapAdd"] and
            {x.upper() for x in h["CapDrop"]} == {"ALL"}, "unexpected isolation config")
    require(any(x in {"no-new-privileges", "no-new-privileges:true"}
                for x in h["SecurityOpt"]), "no-new-privileges missing")
    require(h["PidsLimit"] == 64 and h["Memory"] == 268435456 and
            h["NanoCpus"] == 1000000000, "resource limit mismatch")
    require(set(actual["NetworkSettings"]["Networks"]) == {"none"},
            "extra or unexpected attached network")
    mounts = actual["Mounts"]
    expected = {"/app": str(code), "/input/assessor-input.json": str(inp)}
    require(len(mounts) == 2 and {m["Destination"] for m in mounts} == set(expected),
            "unexpected mounts")
    require(all(m["Type"] == "bind" and not m["RW"] and
                m["Source"] == expected[m["Destination"]] for m in mounts),
            "mount source or access mismatch")


def capture(identifier):
    proc = subprocess.Popen([DOCKER, "--context", CONTEXT, "start", "--attach", identifier],
                            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    selector = selectors.DefaultSelector()
    for name, stream in [("stdout", proc.stdout), ("stderr", proc.stderr)]:
        os.set_blocking(stream.fileno(), False)
        selector.register(stream, selectors.EVENT_READ, name)
    deadline, failure = time.monotonic() + TIMEOUT, None
    try:
        while selector.get_map():
            if time.monotonic() >= deadline:
                failure = "timeout"
                break
            for key, _ in selector.select(timeout=min(0.2, max(0, deadline-time.monotonic()))):
                raw = os.read(key.fileobj.fileno(), 65536)
                if not raw:
                    selector.unregister(key.fileobj)
                    continue
                buffer = buffers[key.data]
                available = MAX_OUTPUT - len(buffer)
                buffer.extend(raw[:available])
                if len(raw) > available:
                    failure = key.data + "_limit"
                    break
            if failure:
                break
        if failure:
            proc.kill()
        proc.wait(timeout=3)
    finally:
        selector.close()
        if proc.poll() is None:
            proc.kill()
            proc.wait(timeout=3)
        proc.stdout.close()
        proc.stderr.close()
    return proc.returncode, {k: bytes(v) for k, v in buffers.items()}, failure


def run(spec_raw, staging_parent):
    # Exact spec bytes and preassigned metadata are fixed before staging or Docker.
    spec = strict_json(spec_raw)
    orchestration = orchestration_record(spec)
    run_id = spec["orchestration"]["component_run_id"]
    # Keep cleanup isolated even if a caller accidentally reuses a component ID.
    container_nonce = uuid.uuid4().hex
    launcher_raw = Path(__file__).read_bytes()
    report = {"schema_version": 1, "profile": "s3-bjorn-isolated-python-v1",
              "run_id": run_id, "orchestration": orchestration,
              "spec": {"bytes": len(spec_raw), "sha256": sha(spec_raw)},
              "recorded_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "launcher": {"bytes": len(launcher_raw), "sha256": sha(launcher_raw)},
              "image_index": IMAGE_INDEX, "image_child_manifest": IMAGE_CHILD,
              "image_config_digest": IMAGE_CONFIG, "image_config_digest_basis":
              "Local platform-filtered image save manifest/config SHA256, observed 2026-10-30",
              "platform": PLATFORM, "docker_context": CONTEXT, "start_attempts": 0}
    name, identifier, created = "s3-bjorn-" + container_nonce, None, False
    with tempfile.TemporaryDirectory(prefix="isolated-", dir=staging_parent) as temp:
        stage = Path(temp)
        stage.chmod(0o755)
        try:
            code, inp, files, input_record = prepare(spec, stage)
            report.update(program_files=files, input=input_record, module=spec["module"])
            image = strict_json(docker(["image", "inspect", "--platform", PLATFORM, IMAGE,
                "--format", '{"id":{{json .Id}},"descriptor":{{json .Descriptor}}}']))
            require(image["id"] == IMAGE_CHILD and image["descriptor"]["digest"] == IMAGE_CHILD
                    and image["descriptor"]["platform"] == {"architecture": "amd64", "os": "linux"},
                    "local image/platform mismatch")
            report["image_inspection"] = image
            args = create_args(name, code, inp, spec["module"])
            report["create_argv"] = [DOCKER, "--context", CONTEXT, *args]
            identifier = docker(args).decode().strip()
            require(re.fullmatch(r"[a-f0-9]{64}", identifier), "invalid created container id")
            created = True
            report["container_id"] = identifier
            before = inspect_container(identifier)
            report["container_before_start"] = before
            validate_container(before, code, inp, spec["module"])
            report["start_attempts"] = 1
            code_returned, streams, failure = capture(identifier)
            report.update(attach_exit_code=code_returned, capture_failure=failure)
            for label, raw in streams.items():
                report[label] = {"bytes": len(raw), "sha256": sha(raw),
                                 "base64": base64.b64encode(raw).decode("ascii"),
                                 "text": raw.decode("utf-8", "replace")}
            report["container_after_capture"] = inspect_container(identifier)
            state = report["container_after_capture"]["State"]
            if failure:
                report["status"] = "capture_failed"
            elif code_returned != 0 or state["Running"] or state["ExitCode"] != 0:
                report["status"] = "program_failed"
            else:
                try:
                    value = strict_json(streams["stdout"].decode("utf-8", "strict"))
                    require(isinstance(value, dict), "stdout JSON must be one object")
                    report["result"] = value
                    report["status"] = "completed"
                except UnicodeError as exc:
                    report["status"] = "invalid_stdout_utf8"
                    report["stdout_validation_error"] = str(exc)[:1024]
                except ValueError as exc:
                    report["status"] = "invalid_stdout_json"
                    report["stdout_validation_error"] = str(exc)[:1024]
        except Exception as exc:
            report.update(status="launcher_failed", error_type=type(exc).__name__,
                          error=str(exc)[:4096])
        finally:
            # Only our unique name/created ID; never retry starting the container.
            try:
                target = identifier if created else name
                cleanup = subprocess.run([DOCKER, "--context", CONTEXT, "rm", "--force", target],
                                         capture_output=True, timeout=8)
                report["cleanup"] = {"exit_code": cleanup.returncode,
                                     "stderr": cleanup.stderr[:4096].decode("utf-8", "replace")}
                if created and cleanup.returncode:
                    report["status"] = "cleanup_failed"
            except Exception as exc:
                report["cleanup"] = {"error_type": type(exc).__name__, "error": str(exc)[:1024]}
                report["status"] = "cleanup_failed"
    report["semantic_comparison_performed"] = False
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    require(args.output.is_absolute() and not args.output.exists() and
            not args.output.is_symlink(), "output must be a fresh absolute path")
    spec_raw = args.spec.read_bytes()
    report = run(spec_raw, args.output.parent)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(json.dumps({"status": report["status"], "receipt": str(args.output),
                      "sha256": sha(args.output.read_bytes())}))
    return 0 if report["status"] == "completed" else 1


if __name__ == "__main__":
    sys.exit(main())
