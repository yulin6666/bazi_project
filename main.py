"""
八字Bazi API Server
基于FastAPI的八字计算和分析API服务
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os
from typing import Dict, Any
from datetime import datetime

from app.lunar import calculate_bazi

# ===== 环境变量 =====
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-c62c4cde8fe747faa4d919780339295f")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1")

# ===== 初始化模型 =====
model = ChatOpenAI(
    model="deepseek-chat",
    temperature=0,
    max_tokens=2000,
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

# ===== 定义八字计算函数 =====
def calculate_bazi_result(
    year: int, month: int, day: int, hour: int = 0,
    minute: int = 0, gender: int = 1, options: str = "all"
) -> Dict[str, Any]:
    """
    计算并返回八字分析结果

    Args:
        year: 出生年 (1900-2030)
        month: 出生月 (1-12)
        day: 出生日 (1-31)
        hour: 出生小时 (0-23)
        minute: 出生分钟 (0-59)
        gender: 性别 (1=男, 0=女)
        options: 分析选项 ("all", "basic", "wuxing", "fortune")

    Returns:
        包含八字分析结果的字典
    """
    try:
        bazi_result = calculate_bazi(year, month, day, hour, minute, gender)

        if options == "basic":
            return {
                "user_info": bazi_result["user_info"],
                "bazi": bazi_result["bazi"],
                "day_master": bazi_result["day_master"]
            }
        elif options == "wuxing":
            return {
                "wuxing": bazi_result["wuxing"],
                "nayin": bazi_result["nayin"]
            }
        elif options == "fortune":
            return {
                "qi_yun": bazi_result["qi_yun"],
                "da_yun": bazi_result["da_yun"][:8],
                "liu_nian": bazi_result["liu_nian"][:10]
            }
        else:
            return bazi_result
    except Exception as e:
        raise Exception(f"八字计算错误: {str(e)}")

# ===== NLP解析链 =====
def create_bazi_chain():
    """创建能够解析自然语言的八字分析链"""
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """你是一个命理分析助手，需要帮助用户将出生日期信息转换为标准格式。
提取以下信息并返回JSON格式：
- year: 出生年份 (1900-2030)
- month: 出生月份 (1-12)
- day: 出生日 (1-31)
- hour: 出生小时 (0-23，24小时制)
- minute: 出生分钟 (0-59)
- gender: 性别 (1=男，0=女)
- options: 分析选项 (all|basic|wuxing|fortune)

返回JSON只，无额外文本。"""),
        ("human", "{user_input}")
    ])

    parser = JsonOutputParser()
    chain = prompt_template | model | parser
    return chain

# ===== 初始化FastAPI应用 =====
app = FastAPI(
    title="八字Bazi API",
    description="基于FastAPI和LangChain的八字计算和分析API服务",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# 添加CORS支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== API端点 =====

@app.post("/api/v1/calculate_bazi")
async def calculate_bazi_endpoint(request: Request):
    """
    直接式的八字计算API
    接收JSON格式的出生信息
    """
    try:
        data = await request.json()
        year = data.get("year")
        month = data.get("month")
        day = data.get("day")
        hour = data.get("hour", 0)
        minute = data.get("minute", 0)
        gender = data.get("gender")
        options = data.get("options", "all")

        # 参数检验
        if not all([year, month, day, gender is not None]):
            return {"error": "缺少必要参数: year, month, day, gender"}, 400

        if year not in range(1900, 2031):
            return {"error": "年份应在1900-2030之间"}, 400

        # 调用Bazi计算
        result = calculate_bazi_result(year, month, day, hour, minute, gender, options)

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": f"计算错误: {str(e)}"}, 500

@app.post("/api/v1/nlp/bazi")
async def nlp_calculate_bazi(request: Request):
    """
    NLP处理模式的八字计算API
    接收自然语言输入
    """
    try:
        data = await request.json()
        user_input = data.get("query")

        if not user_input:
            return {"error": "缺少query参数"}, 400

        # 使用NLP解析用户输入
        chain = create_bazi_chain()
        parsed_data = chain.invoke({"user_input": user_input})

        if not parsed_data:
            return {"error": "无法解析输入信息"}, 400

        # 提取参数
        year = parsed_data.get("year")
        month = parsed_data.get("month")
        day = parsed_data.get("day")
        hour = parsed_data.get("hour", 0)
        minute = parsed_data.get("minute", 0)
        gender = parsed_data.get("gender", 1)
        options = parsed_data.get("options", "all")

        # 校验参数
        if not all([year, month, day]):
            return {"error": f"缺少必要参数, 解析结果: {parsed_data}"}, 400

        # 调用Bazi计算
        result = calculate_bazi_result(year, month, day, hour, minute, gender, options)

        return {
            "status": "success",
            "parsed_input": parsed_data,
            "bazi_analysis": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": f"处理错误: {str(e)}"}, 500

@app.get("/api/v1/")
async def api_info():
    """API信息和使用指南"""
    return {
        "name": "八字Bazi API",
        "version": "1.0.0",
        "endpoints": {
            "/api/v1/calculate_bazi": "直接计算八字（JSON格式输入）",
            "/api/v1/nlp/bazi": "自然语言处理模式（解析用户输入）",
            "/health": "健康检查",
            "/docs": "API交互文档"
        },
        "example_direct": {
            "url": "POST /api/v1/calculate_bazi",
            "body": {
                "year": 1990, "month": 5, "day": 15,
                "hour": 14, "minute": 30, "gender": 1, "options": "all"
            }
        },
        "example_nlp": {
            "url": "POST /api/v1/nlp/bazi",
            "body": {"query": "我出生于1987年3月28日11点，男"}
        }
    }

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "Bazi API",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/")
async def root():
    """根路由"""
    return {
        "message": "欢迎使用八字Bazi API",
        "docs": "/docs",
        "api_info": "/api/v1/"
    }

# 启动命令：uvicorn main:app --host 0.0.0.0 --port 8000 --reload
