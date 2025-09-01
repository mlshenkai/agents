from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv
import os

try:
    from .state import AgentState
    from .tools import ALL_TOOLS
except ImportError:
    # When running as script directly
    from state import AgentState
    from tools import ALL_TOOLS

load_dotenv()


def get_llm_model(model_name: str = "gpt-4o-mini") -> Any:
    """
    根据模型名称获取对应的LLM实例
    """
    if model_name.startswith("gpt"):
        return ChatOpenAI(
            model=model_name,
            temperature=0.1,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
    elif model_name.startswith("claude"):
        return ChatAnthropic(
            model=model_name,
            temperature=0.1,
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
        )
    else:
        # 默认使用OpenAI
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )


def should_continue(state: AgentState) -> str:
    """
    判断是否继续执行工具调用
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    if last_message.tool_calls:
        return "tools"
    else:
        return "end"


def call_model(state: AgentState) -> Dict[str, Any]:
    """
    调用LLM模型处理用户消息
    """
    messages = state["messages"]
    
    # 获取LLM实例
    model = get_llm_model()
    
    # 绑定工具
    model_with_tools = model.bind_tools(ALL_TOOLS)
    
    # 调用模型
    response = model_with_tools.invoke(messages)
    
    # 更新状态
    return {
        "messages": [response],
        "current_step": "model_call"
    }


# 创建工具节点
tool_node = ToolNode(ALL_TOOLS)