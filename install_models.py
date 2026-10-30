
import argparse
import os
from pathlib import Path

from huggingface_hub import hf_hub_download

MODEL_ROOT = Path(os.environ.get("COMFY_MODELS_DIR", "/app/models"))

MODELS = {
    "wan22": {
        "repo": "Comfy-Org/Wan_2.2_ComfyUI_Repackaged",
        "files": [
            (
                "split_files/diffusion_models/wan2.2_ti2v_5B_fp16.safetensors",
                "diffusion_models",
            ),
            (
                "split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors",
                "text_encoders",
            ),
            (
                "split_files/vae/wan2.2_vae.safetensors",
                "vae",
            ),
        ],
    },
}


def install_model(name):
    model = MODELS[name]

    for source_path, folder in model["files"]:
        destination = MODEL_ROOT / folder
        destination.mkdir(parents=True, exist_ok=True)

        print(f"Downloading {source_path}", flush=True)

        hf_hub_download(
            repo_id=model["repo"],
            filename=source_path,
            local_dir=str(destination),
        )

        downloaded = destination / source_path
        final_path = destination / Path(source_path).name
        downloaded.replace(final_path)

    print(f"{name} installation complete", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model", choices=MODELS.keys())
    args = parser.parse_args()

    install_model(args.model)
