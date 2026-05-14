from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from transformers import AutoModelForCausalLM, AutoTokenizer

from llm_prompt import prompt
from query import query
from project_utils import get_model_device, get_model_path


def load_model(model_path):
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype="auto",
        device_map="auto",
    )
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    return tokenizer, model


# 模型交互

def chat_qwen(device, tokenizer, model, user_prompt, system_message, chat_history=None):
    if chat_history is None:
        chat_history = []
    if len(chat_history) == 4:
        chat_history.pop()

    if not device:
        device = get_model_device()

    user_message = {"role": "user", "content": user_prompt}
    chat_history.append(user_message)

    messages = [system_message] + chat_history
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
    return response, chat_history


if __name__ == "__main__":
    model_path = get_model_path()
    tokenizer, model = load_model(model_path)
    print("halo")
    print("Enter 'exit' to exit")
    prompt_triple, patient_description = query()
    content = prompt.role_prompt.format(description=patient_description + " The information of this patient also includes" + "\n".join(prompt_triple))
    system_message = {"role": "system", "content": content}

    chat_history = []
    while True:
        text = input("User: ")
        if text.lower() == 'exit':
            break

        response, chat_history = chat_qwen("cuda", tokenizer, model, text, system_message, chat_history)
        print(f"Patient: {response}")
