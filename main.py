from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent


# 1. 定义工具
#    @tool 装饰器会将函数注册为 Agent 可调用的工具
#    docstring 会作为工具描述传给模型，写清楚很重要
@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"Return the weather in {city} in a joke."


# 2. 初始化模型
#    llama3.2 支持 tool call，llama3 不支持
model = ChatOllama(model="llama3.2")

# 3. 创建 Agent
agent = create_react_agent(
    model=model,
    tools=[get_weather],
    prompt="You are a helpful assistant",
)

if __name__ == "__main__":
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
    )
    print(result["messages"][-1].content)
