# 使用 python:3.11-slim，并优化安装
FROM python:3.11-slim

# 更新apt包管理器并安装编译器，用于编译某些python包
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制requirements文件（这样可以充分利用Docker的缓存）
COPY requirements.txt .

# 先安装python依赖，这样修改代码时不必要重新安装依赖
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip cache purge

# 复制应用代码（此操作会Invalidate Docker cache）
COPY . .

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 暴露端口
EXPOSE 8000

# 健康检查 - 在Uvicorn开始运行后 exec-ed
HEALTHCHECK --interval=30s --timeout=10s --start-period=5m --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=1)" || exit 1

# 启动命令，使用 exec 格式
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]