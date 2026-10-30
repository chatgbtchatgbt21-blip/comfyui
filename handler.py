import json
import os
import subprocess
import sys
import time
import uuid
import urllib.request
import urllib.error

import runpod

COMFY_URL = "http://127.0.0.1:8188"


def api_request(path, payload=None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        COMFY_URL + path,
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read())


def start_comfyui():
    process = subprocess.Popen(
        [sys.executable, "main.py", "--listen", "127.0.0.1", "--port", "8188"],
        cwd="/app",
    )
    for _ in range(120):
        if process.poll() is not None:
            raise RuntimeError("ComfyUI exited during startup")
        try:
            api_request("/system_stats")
            return process
        except Exception:
            time.sleep(2)
    process.terminate()
    raise RuntimeError("ComfyUI startup timed out")


comfy_process = start_comfyui()


def handler(job):
    workflow = job.get("input", {}).get("workflow")
    if not isinstance(workflow, dict):
        return {"error": "Provide a ComfyUI API-format workflow in input.workflow"}

    client_id = str(uuid.uuid4())
    result = api_request("/prompt", {"prompt": workflow, "client_id": client_id})
    prompt_id = result.get("prompt_id")
    if not prompt_id:
        return {"error": "ComfyUI rejected workflow", "details": result}

    deadline = time.monotonic() + 540
    while time.monotonic() < deadline:
        history = api_request("/history/" + prompt_id).get(prompt_id)
        if history:
            status = history.get("status", {})
            if status.get("status_str") == "error":
                return {"error": "Workflow execution failed", "status": status}
            if status.get("completed"):
                return {
                    "prompt_id": prompt_id,
                    "status": "completed",
                    "outputs": history.get("outputs", {}),
                }
        time.sleep(2)

    return {"error": "Workflow timed out", "prompt_id": prompt_id}


runpod.serverless.start({"handler": handler})