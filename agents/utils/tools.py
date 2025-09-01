from langchain_core.tools import tool
from typing import Literal
import random


@tool
def calculator(operation: str, a: float, b: float) -> str:
    """
    执行基本数学运算
    
    Args:
        operation: 运算类型 (add, subtract, multiply, divide)
        a: 第一个数字
        b: 第二个数字
    
    Returns:
        计算结果的字符串
    """
    try:
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b == 0:
                return "错误：除数不能为零"
            result = a / b
        else:
            return f"错误：不支持的运算类型 '{operation}'"
        
        return f"{a} {operation} {b} = {result}"
    except Exception as e:
        return f"计算错误：{str(e)}"


@tool
def get_weather(city: Literal["beijing", "shanghai", "guangzhou", "shenzhen"]) -> str:
    """
    获取指定城市的天气信息（模拟）
    
    Args:
        city: 城市名称
    
    Returns:
        天气信息字符串
    """
    weather_conditions = ["晴天", "多云", "小雨", "阴天"]
    temp = random.randint(15, 30)
    condition = random.choice(weather_conditions)
    
    city_names = {
        "beijing": "北京",
        "shanghai": "上海", 
        "guangzhou": "广州",
        "shenzhen": "深圳"
    }
    
    return f"{city_names[city]}今天{condition}，温度{temp}°C"


@tool
def search_information(query: str) -> str:
    """
    搜索信息（模拟）
    
    Args:
        query: 搜索查询
    
    Returns:
        搜索结果
    """
    return f"关于'{query}'的搜索结果：这是一个模拟的搜索结果，实际应用中可以集成真实的搜索API。"


# 导出所有工具
ALL_TOOLS = [calculator, get_weather, search_information]