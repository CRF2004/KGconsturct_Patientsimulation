import pymupdf as fitz
from PIL import Image
import io
import read_and_write as rw
import re

content = ""
# 打开PDF文件
doc = fitz.open("./input/Case Reports in Infectious Diseases - 2015 - Ansari - Chromobacterium violaceum Isolated from a Wound Sepsis  A Case Study.pdf")
for page_number,page in enumerate(doc):
    text = page.get_text()
    
    content += text
    
    print(f"第 {page.number + 1} 页的内容:\n{text}")
    # 获取页面中的所有图片
    image_list = page.get_images(full=True)
    # 遍历所有图片
    for img_index, img in enumerate(image_list):
        # 图片的XREF
        xref = img[0]
        
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]

        # 将二进制数据转为PIL图像
        image = Image.open(io.BytesIO(image_bytes))
        
        # 获取图片的扩展名
        image_ext = base_image["ext"]
        
        # 保存图片
        # with open(f"page_{page_number + 1}_img_{img_index + 1}.{image_ext}", "wb") as image_file:
        #     image_file.write(image_bytes)
        image.save(f"page_{page_number + 1}_img_{img_index + 1}.{image_ext}")
        
        print(f"第 {page_number + 1} 页中提取的图片 {img_index + 1} 已保存。")
print("pdf提取完成")

################清洗###############
    
# 查找 "References\n[1]" 的位置，从后往前
index = content.rfind("References\n[1]")

# 如果找到了该字符串，就进行清理
if index != -1:
    content = content[:index]  # 截取到该字符串之前的内容

index = content.find("cited.")

# 如果找到了该字符串，就进行清理
if index != -1:
    content = content[index + len("cited."):] 

lines = content.splitlines()  # 将文本按行分割
lines = [line for line in lines if "Downloaded from https://" not in line]  # 过滤掉包含目标字符串的行

# 将过滤后的内容重新拼接成单一字符串
content = "\n".join(lines)

rw.pdf_write(content)

