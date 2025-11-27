# 部署指南

## 目录
- [本地开发](#本地开发)
- [Docker 部署](#docker-部署)
- [Zeabur 云部署](#zeabur-云部署)
- [常见问题](#常见问题)

---

## 本地开发

### 前置要求
- Python 3.11+
- pip 或 conda

### 步骤

1. **克隆仓库**
```bash
git clone https://github.com/yourusername/BAZI_project.git
cd BAZI_project
```

2. **创建虚拟环境**
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
# 复制示例文件
cp .env.example .env

# 编辑 .env 文件
vim .env
# 或使用编辑器打开
```

填入以下变量：
```
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.deepseek.com/v1
```

5. **启动服务**
```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

6. **访问API**
- 交互式文档：http://localhost:8080/docs
- 健康检查：http://localhost:8080/health
- API信息：http://localhost:8080/api/v1/

---

## Docker 部署

### 前置要求
- Docker 20.10+

### 本地构建和运行

1. **构建镜像**
```bash
docker build -t bazi-api:latest .
```

2. **创建 .env 文件**
```bash
cp .env.example .env
# 编辑 .env 文件填入 API Key
```

3. **运行容器**
```bash
# 方式一：使用 .env 文件
docker run -p 8080:8080 \
  --env-file .env \
  bazi-api:latest

# 方式二：直接传递环境变量
docker run -p 8080:8080 \
  -e OPENAI_API_KEY=your_api_key \
  -e OPENAI_BASE_URL=https://api.deepseek.com/v1 \
  bazi-api:latest
```

4. **验证服务**
```bash
curl http://localhost:8080/health
```

### Docker Compose（可选）

创建 `docker-compose.yml`：
```yaml
version: '3.8'

services:
  bazi-api:
    build: .
    container_name: bazi-api
    ports:
      - "8080:8080"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_BASE_URL=https://api.deepseek.com/v1
      - PORT=8080
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

运行：
```bash
docker-compose up -d
```

---

## Zeabur 云部署

Zeabur 是一个现代化的云部署平台，支持 Docker 应用一键部署。

### 方式一：GitHub 自动部署（推荐）

1. **推送代码到 GitHub**
```bash
git remote add origin https://github.com/yourusername/BAZI_project.git
git branch -M main
git push -u origin main
```

2. **连接 Zeabur**
   - 访问 https://zeabur.com
   - 注册/登录账户
   - 点击 "New Project"
   - 选择 "Deploy from GitHub"
   - 连接 GitHub 账户
   - 选择 BAZI_project 仓库

3. **配置环境变量**
   - 在 Zeabur 项目设置中，添加以下环境变量：
     - `OPENAI_API_KEY`: 你的 OpenAI API Key
     - `OPENAI_BASE_URL`: https://api.deepseek.com/v1（可选）

4. **自动部署**
   - 等待部署完成（约 2-5 分钟）
   - 获取生成的公开URL
   - 访问 `/docs` 查看API文档

### 方式二：使用 Zeabur CLI

1. **安装 Zeabur CLI**
```bash
npm install -g @zeabur/cli
```

2. **登录**
```bash
zeabur auth login
```

3. **部署**
```bash
zeabur deploy
```

4. **配置环境变量**
```bash
zeabur env set OPENAI_API_KEY your_api_key
zeabur env set OPENAI_BASE_URL https://api.deepseek.com/v1
```

### 方式三：手动 Docker 部署（不推荐）

如果使用容器注册表（如 Docker Hub）：

1. **构建并推送镜像**
```bash
docker build -t yourusername/bazi-api:latest .
docker push yourusername/bazi-api:latest
```

2. **在 Zeabur 中创建服务**
   - New Service → Custom Docker Image
   - 输入镜像地址：`yourusername/bazi-api:latest`
   - 配置端口：8000
   - 添加环境变量

---

## 部署检查清单

部署前请确保：

- [ ] 项目根目录有 `Dockerfile`
- [ ] 项目根目录有 `requirements.txt`
- [ ] 项目根目录有 `.env.example`
- [ ] 代码已上传到 GitHub
- [ ] 获取了有效的 OpenAI API Key
- [ ] 已配置所有必需的环境变量
- [ ] 本地测试通过（`http://localhost:8000/docs` 可访问）

---

## 部署验证

部署成功后，验证以下端点：

```bash
# 健康检查
curl https://yulin15.zeabur.app/health

# API信息
curl https://yulin15.zeabur.app/api/v1/

# 测试计算
curl -X POST https://yulin15.zeabur.app/api/v1/calculate_bazi \
  -H "Content-Type: application/json" \
  -d '{"year":1990,"month":5,"day":15,"hour":14,"minute":30,"gender":1}'

# 测试NLP
curl -X POST https://yulin15.zeabur.app/api/v1/nlp/bazi \
  -H "Content-Type: application/json" \
  -d '{"query":"1990年5月15日14点30分，男"}'
```

---

## 常见问题

### Q1: Zeabur 部署失败，日志显示 "No OPENAI_API_KEY"

**A:** 确保在 Zeabur 项目设置中正确配置了 `OPENAI_API_KEY` 环境变量。

### Q2: 访问 API 返回 500 错误

**A:** 检查：
- API Key 是否正确
- 网络连接是否正常
- DeepSeek API 是否可用

### Q3: Docker 镜像构建失败

**A:** 确保：
- Docker 已安装并运行
- requirements.txt 中的所有包都有效
- Python 版本为 3.11+

### Q4: 如何更新部署的服务？

**A:** 使用 GitHub 自动部署时，只需推送代码到 main 分支：
```bash
git push origin main
```
Zeabur 会自动重新构建和部署。

### Q5: 如何查看部署日志？

**A:** 在 Zeabur 项目中：
- 点击服务
- 选择 "Logs" 标签
- 查看实时日志

### Q6: 如何管理多个环境（开发、生产）？

**A:** 在 Zeabur 中创建多个项目或分支：
- `main` 分支 → 生产环境
- `develop` 分支 → 开发环境

---

## 支持的部署平台

| 平台 | 难度 | 推荐度 | 说明 |
|------|------|--------|------|
| Zeabur | ⭐ | ⭐⭐⭐⭐⭐ | 最简单，支持自动部署 |
| Render | ⭐⭐ | ⭐⭐⭐⭐ | 类似Heroku，支持免费套餐 |
| Railway | ⭐⭐ | ⭐⭐⭐⭐ | 现代化UI，支持GitHub集成 |
| Fly.io | ⭐⭐ | ⭐⭐⭐ | 全球分布，性能好 |
| AWS Lambda | ⭐⭐⭐ | ⭐⭐⭐ | 扩展性好，需要配置 |
| Docker Hub | ⭐ | ⭐⭐⭐ | 仅用于镜像存储 |

---

## 下一步

- 查看 [README.md](README.md) 了解API使用
- 查看 [examples.py](examples.py) 了解使用示例
- 配置自己的域名
- 设置监控和告警
