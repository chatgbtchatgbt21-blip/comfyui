import runpod


def handler(job):
    job_input = job.get("input", {})
    return {
        "status": "ready",
        "message": "Larix ComfyUI Serverless worker is running",
        "received_input": job_input
    }


runpod.serverless.start({"handler": handler})