from transformers import AutoModelForCausalLM, AutoTokenizer
from llm_prompt import prompt
from query import query
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

# 模型交互
def chat_qwen(device, tokenizer, model, user_prompt, system_message, chat_history=None):
    # 如果没有历史记录，初始化为空列表
    if chat_history is None:
        chat_history = []
    if len(chat_history) == 4:
        chat_history.pop()
    
    user_message = {"role": "user", "content": user_prompt}
    chat_history.append(user_message)
    
    messages = [system_message] + chat_history

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
    return response, chat_history


model_path = '/mnt/diskb5/LLM/Qwen/qwen/Qwen2.5_7B-instruct'
tokenizer, model = load_model(model_path) 
print("halo")
print("Enter 'exit' to exit")
prompt_triple, patient_description = query()
content = prompt.role_prompt.format(description=patient_description+
                                    " The information of this patient also includes"+"\n".join(prompt_triple))
system_message = {"role": "system",
                  "content": content}

chat_history = []
while True:
    text = input("User: ")
    if text.lower() == 'exit':
        break
    
    
    # 生成对话回应
    response, chat_history = chat_qwen("cuda", tokenizer, model, text, system_message, chat_history)
    
    # 打印模型的回应
    print(f"Patient: {response}")
    
