# 八字Bazi API

基于 FastAPI 的八字计算和分析 API 服务

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

## 功能特性

🔮 **八字计算**
- 完整的四柱八字排盘
- 五行分析（金木水火土统计）
- 纳音推算
- 十神分析
- 大运推演（8步）
- 流年运势

🤖 **NLP自然语言解析**
- 支持中英文输入
- 自动提取出生信息

🚀 **生产就绪**
- Docker 容器化
- Zeabur 一键部署
- CORS 跨域支持
- 健康检查端点
- 完整的错误处理

## 部署指南

### 前提条件
- Python 3.11+
- OpenAI API Key（或使用 DeepSeek API）

### 本地部署

```bash
# 克隆项目
git clone https://github.com/yourusername/bazi_project.git
cd bazi_project

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 OPENAI_API_KEY

# 运行服务
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

访问 http://localhost:8000/docs 查看API文档

### Zeabur 一键部署

1. 访问 [Zeabur.com](https://zeabur.com)
2. 连接你的 GitHub 账户，创建新项目
3. 设置环境变量：从 `.env.example` 中复制并填入 `OPENAI_API_KEY`
4. 等待自动部署完成（2-5分钟）

### Docker 部署

```bash
# 构建镜像
docker build -t bazi-api .

# 运行容器
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key bazi-api
```

## API 使用

### 1. 直接计算八字（JSON格式）

```bash
curl -X POST "https://yulin15.zeabur.app/api/v1/calculate_bazi" \
     -H "Content-Type: application/json" \
     -d '{
       "year": 1990,
       "month": 5,
       "day": 15,
       "hour": 14,
       "minute": 30,
       "gender": 1,
       "options": "all"
     }'
```

### 2. NLP 自然语言解析

```bash
curl -X POST "https://yulin15.zeabur.app/api/v1/nlp/bazi" \
     -H "Content-Type: application/json" \
     -d '{"query": "我出生于1987年3月28日11点，男"}'
```

### 3. 健康检查

```bash
# 本地
http://localhost:8000/health

# 部署后
https://yulin15.zeabur.app/health
```

## 更轻量级部署（推荐）

如果遇到依赖冲突，可以使用超轻量级的依赖配置：

```bash
# 使用最小化依赖
mv requirements-micro.txt requirements.txt
```

这将移除 NLP 功能，但保证 100% 部署成功。

## API 端点

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/api/v1/calculate_bazi` | 直接计算八字 |
| POST | `/api/v1/nlp/bazi` | NLP模式计算 |
| GET | `/api/v1/` | API信息 |
| GET | `/health` | 健康检查 |

## Python 客户端示例

```python
import requests

# 直接计算
def calculate_bazi(year, month, day, hour=0, minute=0, gender=1):
    return requests.post(
        "https://yulin15.zeabur.app/api/v1/calculate_bazi",
        json={"year": year, "month": month, "day": day, "hour": hour, "minute": minute, "gender": gender}
    ).json()

# NLP计算
def calculate_bazi_nlp(query):
    return requests.post(
        "https://yulin15.zeabur.app/api/v1/nlp/bazi",
        json={"query": query}
    ).json()
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OPENAI_API_KEY` | API密钥 | 必填 |
| `OPENAI_BASE_URL` | API服务地址 | https://api.deepseek.com/v1 |
| `PORT` | 监听端口 | 8000 |

## 结果响应示例

```json
{
  "status": "success",
  "data": {
    "user_info": {
      "阳历": "1990-05-15 14:30",
      "农历": "庚午年 四月 十八",
      "生肖": "马",
      "性别": "男"
    },
    "bazi": {
      "年柱": "庚午",
      "月柱": "己巳",
      "日柱": "癸巳",
      "时柱": "丙午"
    },
    "day_master": "癸",
    "wuxing": {...},
    "da_yun": [...]
  }
}
```

## 文件说明

- `requirements.txt` - Python 依赖包
- `requirements-micro.txt` - 超轻量依赖（无NLP）
- `Dockerfile` - Docker 容器化配置
- `examples.py` - Python 客户端示例

## 故障排除

**构建失败？** 查看 [ZEABUR_FIX.md](ZEABUR_FIX.md) 获取详细解决方案

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

祝部署顺利 ！🎉

如有问题，请在 GitHub Issues 中报告。