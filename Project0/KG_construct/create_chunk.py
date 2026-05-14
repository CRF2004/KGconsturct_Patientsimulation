def chunk(text, chunk_size, overlap_size):
    """将文本按固定长度分块，并保留重叠区间。"""
    chunks = []
    current_index = 0
    text_length = len(text)

    while current_index < text_length:
        end_index = min(current_index + chunk_size, text_length)
        chunks.append(text[current_index:end_index])

        if end_index == text_length:
            break
        current_index = end_index - overlap_size

    return chunks
