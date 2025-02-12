from transformers import AutoModelForCausalLM, AutoTokenizer

def load_model(model_path):
    #device = "cuda:0"  # 将模型加载到指定GPU 上
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype="auto",
        device_map="auto",
        #device_map={"": "cuda:5"} # 指定模型加载到 GPU 上
    )
    tokenizer = AutoTokenizer.from_pretrained(model_path)#加载分词器
    return tokenizer, model

# 模型交互。
def chat_qwen(device, tokenizer, model, prompt):
    messages = (
        {"role": "system", "content": "You are a helpful scientist."},
        {"role": "user", "content": prompt}
    )
    # 使用分词器的 apply_chat_template 方法将消息格式化为模型可理解的输入格式
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    model_inputs = tokenizer((text), return_tensors="pt").to(device)    #pt为pytorch张量格式
    #生成模型输出
    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=8000
    )
    # 由于模型输出包括输入模型，这里切去输入部分
    generated_ids = (output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids))
    # 将模型输出解码为文本
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response
