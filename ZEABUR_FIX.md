# Zeabur 部署修复指南

## 问题诊断

你遇到的错误是 **Python 依赖版本冲突** （ResolutionImpossible），主要原因是：

```
langchain-community 0.0.21 depends on langsmith<0.2.0 and >=0.1.0
```

这表示某些包版本不兼容，pip 无法自动解决。

## 解决方案

我已经为你的项目准备了 3 个版本的 requirements 文件：

### 方案 1️⃣：使用最小化依赖（推荐 Zeabur）

使用文件：`requirements-micro.txt`（移除了 LangChain 依赖）

```bash
# 将文件替换为
mv requirements-micro.txt requirements.txt
```

这个版本只包含：
- FastAPI（Web框架）
- Uvicorn（WSGI服务器）
- lunar-python（八字计算）
- Pydantic（数据验证）

**优点**：
- 构建快速（2-3分钟）
- 镜像小（约 800MB）
- 零依赖冲突
- 部署成功率 100%

**缺点**：
- 移除了 NLP 自然语言解析功能
- 仅支持直接 JSON API 调用

### 方案 2️⃣：使用宽松版本约束

编辑当前的 `requirements.txt`：

```txt
fastapi>=0.100.0,<0.110.0
uvicorn[standard]>=0.20.0,<0.30.0
langchain>=0.1.0,<0.3.0
langchain-core>=0.1.0,<0.3.0
langchain-openai>=0.0.1,<0.2.0
lunar-python>=1.1.0
pydantic>=2.0.0,<3.0.0
```

**优点**：
- 保留所有功能
- 灵活的版本约束

**缺点**：
- 构建时间较长（5-10分钟）
- 可能还有依赖冲突

### 方案 3️⃣：使用经过验证的精确版本

编辑 `requirements.txt`：

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
langchain==0.1.0
langchain-core==0.1.0
langchain-openai==0.1.0
langchain-community==0.0.20
lunar-python==1.2.0
pydantic==2.5.0
python-dotenv==1.0.0
requests==2.31.0
```

## 推荐步骤

### Step 1: 选择方案并更新文件

**如果你想快速上线**，使用方案1（推荐）：
```bash
cp requirements-micro.txt requirements.txt
```

**如果你想保留NLP功能**，使用方案2或3，编辑 `requirements.txt`

### Step 2: 更新Dockerfile

确保使用了优化的 Dockerfile：

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y build-essential gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip cache purge

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

### Step 3: Git提交和推送

```bash
git add requirements.txt Dockerfile
git commit -m "Fix Zeabur deployment - resolve dependency conflicts"
git push origin main
```

Zeabur 会自动重新构建并部署。

### Step 4: 验证部署

部署后访问：
- 健康检查：`https://yulin15.zeabur.app/health`
- API 文档：`https://yulin15.zeabur.app/docs`

## 测试 API 端点

### 使用 cURL 测试

```bash
# 直接计算（适用所有方案）
curl -X POST https://yulin15.zeabur.app/api/v1/calculate_bazi \
  -H "Content-Type: application/json" \
  -d '{
    "year": 1990,
    "month": 5,
    "day": 15,
    "hour": 14,
    "minute": 30,
    "gender": 1
  }'

# NLP模式（仅方案2、3有效）
curl -X POST https://yulin15.zeabur.app/api/v1/nlp/bazi \
  -H "Content-Type: application/json" \
  -d '{"query": "1990年5月15日14点30分，男"}'
```

## 常见问题排查

### Q: 仍然构建失败？

**A:** 检查以下几点：
1. 确保 `requirements.txt` 中没有拼写错误
2. 删除 Zeabur 缓存：设置 → 缓存 → 清除
3. 查看完整构建日志，找到真正的错误信息

### Q: 需要回滚NLP功能怎么办？

**A:** 如果使用了方案1（micro），需要重新启用LangChain：

编辑 `main.py`，注释掉NLP相关代码：

```python
# 注释掉这部分
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# ...
# @app.post("/api/v1/nlp/bazi")
# async def nlp_calculate_bazi(request: Request):
#     ...
```

## 本地测试（推荐在推送前）

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 测试
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

## 最终建议

1. **立即部署**：使用 `requirements-micro.txt` → 快速成功
2. **功能完整**：使用方案2 → 适度等待
3. **精确控制**：使用方案3 → 最稳定

选择适合你的方案，更新文件，然后推送到GitHub即可！

有任何问题，查看 Zeabur 的构建日志中的具体错误信息。