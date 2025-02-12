import read_and_write as rw

def chunk(text, chunk_size, overlap_size):
    """
    将文本按照指定长度分块，确保分块之间有一定重叠。
    参数:
        text (str): 需要分块的文本
        chunk_size (int): 每个分块的长度
        overlap_size (int): 分块之间的重叠字符数

    返回:
        list: 分块后的文本列表
    """

    chunks = []
    current_index = 0
    text_length = len(text)
    print(text_length)
    while current_index < text_length:
        # 取当前块的结束索引
        end_index = current_index + chunk_size

        # 确保结束索引不超过文本长度
        if end_index > text_length:
            end_index = text_length

        # 提取当前块
        chunk = text[current_index:end_index]
        chunks.append(chunk)

        if end_index == text_length:
            current_index = text_length
        else:
            # 移动索引到下一个块的开始位置（当前块结束位置 - 重叠大小）
            current_index = end_index - overlap_size


    return chunks

text = rw.read_text()
# 设置分块参数
chunk_size = 5000  # 每个分块的长度（字符数）
overlap_size = 1000  # 分块之间的重叠字符数

# 分块处理
chunks = chunk(text, chunk_size, overlap_size)

# 打印结果
for i, chunk0 in enumerate(chunks):
    print(f"Chunk {i+1}: {chunk0[:50]}...")  # 只显示前50个字符