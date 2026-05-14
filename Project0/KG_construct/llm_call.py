from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from transformers import AutoModelForCausalLM, AutoTokenizer

from project_utils import get_model_device, get_model_path, get_visible_devices


def load_model(model_path=None):
    if model_path is None:
        model_path = get_model_path()
    visible_devices = get_visible_devices()
    if visible_devices:
        import os

        os.environ["CUDA_VISIBLE_DEVICES"] = visible_devices
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype="auto",
        device_map="auto",
    )
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    return tokenizer, model


# 模型交互。
def chat_qwen(device, tokenizer, model, prompt):
    if not device:
        device = get_model_device()
    messages = (
        {"role": "system", "content": "You are a helpful scientist."},
        {"role": "user", "content": prompt},
    )
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    model_inputs = tokenizer(text, return_tensors="pt").to(device)
    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=8000,
    )
    generated_ids = (
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    )
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response
