# MedicalGraphRAG

一个基于医疗病例文本的知识图谱构建与患者对话检索项目。

## 项目做什么

这个仓库包含两条主要流程：

1. **知识图谱构建**
   - 从病例 PDF / 文本中抽取实体和关系
   - 写入 Neo4j
   - 生成可复用的图谱数据

2. **患者对话 / 图谱检索**
   - 将用户提问拆解为实体/关系需求
   - 在知识图谱中做相似度匹配
   - 把检索结果注入 prompt，让本地大模型生成回答

## 目录结构

- `Project0/KG_construct/`：病例文本 → 实体/关系抽取 → Neo4j 建图
- `Project0/patient_simulation/`：基于图谱检索的患者对话
- `project_utils.py`：统一配置读取（模型路径、GPU、Neo4j）
- `.env.example`：环境变量示例

## 环境要求

- Python 3.10+
- Neo4j 5.x
- 本地可用的大模型目录（例如 Qwen2.5 Instruct）
- CUDA 环境（如需 GPU 推理）

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

先复制环境变量示例并按自己的环境修改：

```bash
cp .env.example .env
```

需要配置的内容：

- `MODEL_PATH`：本地模型目录
- `MODEL_DEVICE`：模型推理设备，默认 `cuda`
- `CUDA_VISIBLE_DEVICES`：指定 GPU
- `NEO4J_URI`：Neo4j 地址
- `NEO4J_USER`：Neo4j 用户名
- `NEO4J_PASSWORD`：Neo4j 密码

## 运行方式

### 1. 构建知识图谱

```bash
python Project0/KG_construct/main.py
```

### 2. 患者对话

```bash
python Project0/patient_simulation/main.py
```

输入 `exit` 退出。

## 说明

- 该项目依赖本地模型，不会自动下载模型权重。
- `Project0/KG_construct/input/` 中包含示例病例文件。
- `Project0/KG_construct/output/` 中的内容为运行生成结果，不建议手动维护。
- Neo4j 账号密码已经移出源码，改为读取环境变量。

## 当前状态

这是一个正在整理中的研究型项目，重点是让别人能够理解、配置和复现，而不是直接提供在线服务。
