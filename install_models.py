
from pathlib import Path
import argparse
import os
import sys

from huggingface_hub import hf_hub_download

MODELS = {
    "wan22": {
        "repo": "Comfy-Org/Wan_2.2_ComfyUI_Repackaged",
        "files": [
            ("split_files/diffusion_models/wan2.2_ti2v_5B_fp16.safetensors", "diffusion_models"),
            ("split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors", "text_encoders"),
            ("split_files/vae/wan2.2_vae.safetensors", "vae"),
        ],
    },
}

def install(name):
    if name not in MODELS:
        raise ValueError(f"Unknown model: {name}")

    root = Path(os.environ.get("COMFY_MODELS_DIR", "/app/models"))
    spec = MODELS[name]

    for filename, folder in spec["files"]:
        destination = root / folder
        destination.mkdir(parents=True, exist_ok=True)

        print(f"Downloading {filename}", flush=True)
        hf_hub_download(
            repo_id=spec["repo"],
            filename=filename,
            local_dir=str(root),
        )

    print(f"Finished downloading {name}", flush=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model", choices=list(MODELS))
    args = parser.parse_args()
    install(args.model)
