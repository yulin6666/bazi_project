#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
八字Bazi API 使用示例
展示了如何使用FastAPI八字计算API的各种方式
"""

import requests
import json

# API 基础URL（根据实际部署地址修改）
BASE_URL = "https://yulin15.zeabur.app"

# ===== API调用函数 =====

def health_check():
    """健康检查"""
    response = requests.get(f"{BASE_URL}/health")
    return response.json()

def api_info():
    """获取API信息"""
    response = requests.get(f"{BASE_URL}/api/v1/")
    return response.json()

def calculate_bazi_direct(data):
    """直接计算八字"""
    response = requests.post(
        f"{BASE_URL}/api/v1/calculate_bazi",
        json=data
    )
    return response.json()

def calculate_bazi_nlp(query):
    """通过NLP计算八字"""
    response = requests.post(
        f"{BASE_URL}/api/v1/nlp/bazi",
        json={"query": query}
    )
    return response.json()

def print_response(title, response):
    """格式化打印响应"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print({'='*60}")
    print(json.dumps(response, indent=2, ensure_ascii=False))

# ===== 示例1: 健康检查 =====
print("示例1: 健康检查")
print(health_check())

# ===== 示例2: 基础八字计算 =====
print("\n示例2: 基础八字计算 - 基础信息")
result = calculate_bazi_direct({
    "year": 1990,
    "month": 5,
    "day": 15,
    "hour": 14,
    "minute": 30,
    "gender": 1,
    "options": "basic"
})

# 如果成功，只显示基础信息
if result["status"] == "success":
    data = result["data"]
    print(f"\n基本信息:")
    print(f"  阳历: {data['user_info']['阳历']}")
    print(f"  农历: {data['user_info']['农历']}")
    print(f"  生肖: {data['user_info']['生肖']}")
    print(f"  性别: {data['user_info']['性别']}")
    print(f"\n四柱八字:")
    print(f"  年柱: {data['bazi']['年柱']}")
    print(f"  月柱: {data['bazi']['月柱']}")
    print(f"  日柱: {data['bazi']['日柱']}")
    print(f"  时柱: {data['bazi']['时柱']}")
    print(f"  日主: {data['day_master']}")

# ===== 示例3: 五行分析 =====
print("\n示例3: 五行分析")
result = calculate_bazi_direct({
    "year": 1987,
    "month": 3,
    "day": 28,
    "hour": 11,
    "minute": 0,
    "gender": 1,
    "options": "wuxing"
})

if result["status"] == "success":
    data = result["data"]
    print(f"\n五行统计:")
    print(f"  {data['wuxing']['counts']}")
    print(f"\n纳音:")
    for key, value in data['nayin'].items():
        print(f"  {value}", end=" ")
    print()

# ===== 示例4: 运势分析 =====
print("\n示例4: 运势分析")
result = calculate_bazi_direct({
    "year": 1988,
    "month": 12,
    "day": 25,
    "hour": 8,
    "minute": 20,
    "gender": 0,
    "options": "fortune"
})

if result["status"] == "success":
    data = result["data"]
    print(f"\n起运描述: {data['qi_yun']['起运描述']}")
    print(f"\n大运（前3步）:")
    for dy in data['da_yun'][:3]:
        print(f"  {dy['大运干支']}: {dy['起运年龄']}-{dy['结束年龄']}岁 | {dy['起运年份']}年")

# ===== 示例5: 完整分析 =====
print("\n示例5: 完整分析")
result = calculate_bazi_direct({
    "year": 1990,
    "month": 5,
    "day": 15,
    "hour": 14,
    "minute": 30,
    "gender": 1,
    "options": "all"
})

print_response("完整分析结果", result)

# ===== 示例6: 中文NLP输入 =====
print("\n示例6: 中文NLP输入")
nlp_queries = [
    "我出生于1987年3月28日11点，性别男",
    "1990年5月15下午3点半出生的男性",
    "1988年12月25日早上8点20分，女性"
]

for query in nlp_queries:
    print(f"\n输入: {query}")
    result = calculate_bazi_nlp(query)

    if result["status"] == "success":
        print(f"解析参数: {result['parsed_input']}")
        print(f"四柱: {result['bazi_analysis']['bazi']}")
    else:
        print(f"错误: {result.get('error')}")

# ===== 示例7: 英文NLP输入 =====
print("\n示例7: 英文NLP输入")
nlp_queries_en = [
    "Male, born on July 15, 1991 at 22:30",
    "Female, December 25, 1988 at 8:20 AM"
]

for query in nlp_queries_en:
    print(f"\nInput: {query}")
    result = calculate_bazi_nlp(query)

    if result["status"] == "success":
        print(f"Parsed: {result['parsed_input']}")
        print(f"Bazi: {result['bazi_analysis']['bazi']}")
    else:
        print(f"Error: {result.get('error')}")

# ===== 示例8: 错误处理 =====
print("\n示例8: 错误处理测试")

# 测试1: 缺少必要参数
test_cases = [
    ({"month": 5, "day": 15, "gender": 1}, "缺少年份"),
    ({"year": 1990, "day": 15, "gender": 1}, "缺少月份"),
    ({"year": 1990, "month": 5, "gender": 1}, "缺少日期"),
    ({"year": 1990, "month": 5, "day": 15}, "缺少性别"),
    ({"year": 1800, "month": 5, "day": 15, "gender": 1}, "无效年份")
]

for data, desc in test_cases:
    print(f"\n测试: {desc}")
    result = calculate_bazi_direct(data)
    if "error" in result:
        print(f"捕获到错误: {result['error']}")
    else:
        print("意外成功")

# ===== 示例结束 =====
print(f"\n{'='*60}")
print("所有示例完成！")
print(f"\n使用提示:")
print("1. 根据需求选择合适的分析选项")
print("2. NLP模式支持多种输入格式")
print("3. 生产环境请设置正确的API服务地址")
print("4. 合理控制请求频率")

"""
# 单独运行某个示例的快捷方式:

# 五行分析示例
python -c "import examples; r=examples.calculate_bazi_direct({'year':1990,'month':5,'day':15,'hour':14,'minute':30,'gender':1,'options':'wuxing'}); print(r['data']['wuxing']['counts']) if r['status']=='success' else print(r)"

# NLP模式示例
python -c "import examples; r=examples.calculate_bazi_nlp('我出生于1987年3月28日11点，男'); print(r['bazi_analysis']['bazi']) if r['status']=='success' else print(r)"
""""file_path"="/Users/linofficemac/Documents/AI/LIN_AI_resource/code/BAZI_project/examples.py"}