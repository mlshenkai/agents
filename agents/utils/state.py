from typing import Annotated, List, TypedDict
import operator
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """
    智能体状态定义
    包含消息历史、当前步骤和任何中间结果
    """
    messages: Annotated[List[BaseMessage], operator.add]
    current_step: str
    intermediate_results: List[str]
    final_answer: str