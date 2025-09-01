from langgraph.graph import START, END
from langgraph.graph.state import StateGraph, CompiledStateGraph
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from .utils.state import AgentState
from .utils.nodes import call_model, should_continue, tool_node


def create_agent() -> CompiledStateGraph:
    """
    创建并返回LangGraph智能体
    """
    # 创建状态图
    workflow = StateGraph(AgentState)
    
    # 添加节点
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)
    
    # 设置入口点
    workflow.add_edge(START, "agent")
    
    # 添加条件边
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )
    
    # 工具执行后返回agent
    workflow.add_edge("tools", "agent")
    
    # 编译图
    return workflow.compile()


def run_agent(query: str) -> dict:
    """
    运行智能体处理查询
    
    Args:
        query: 用户查询
        
    Returns:
        智能体响应结果
    """
    app = create_agent()
    
    # 准备初始状态
    initial_state = {
        "messages": [HumanMessage(content=query)],
        "current_step": "start",
        "intermediate_results": [],
        "final_answer": ""
    }
    
    # 运行智能体
    result = app.invoke(initial_state)
    
    return result


if __name__ == "__main__":
    # 测试示例
    test_query = "请帮我计算 15 + 27 的结果"
    print("测试查询:", test_query)
    
    try:
        result = run_agent(test_query)
        print("智能体响应:", result["messages"][-1].content)
    except Exception as e:
        print(f"运行错误: {e}")
        print("请确保已正确配置 .env 文件中的 API 密钥")