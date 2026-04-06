# 🌤️ LangChain Weather Agent 教程

使用 **LangGraph + Ollama + llama3.2** 构建一个本地运行的 AI Weather Agent，无需任何 API Key。

---

## 📋 目录

- [环境要求](#环境要求)
- [第一步：安装 Ollama](#第一步安装-ollama)
- [第二步：安装 Python 依赖](#第二步安装-python-依赖)
- [第三步：创建 Weather Agent](#第三步创建-weather-agent)
- [第四步：启动与运行](#第四步启动与运行)
- [常见问题](#常见问题)
- [进阶：切换为 Claude](#进阶切换为-claude)

---

## 环境要求

| 工具 | 版本要求 |
|------|---------|
| Python | 3.10+ 推荐（3.9 可用） |
| macOS | Homebrew 已安装 |
| 磁盘空间 | llama3.2 约 2GB |

---

## 第一步：安装 Ollama

Ollama 是本地运行大模型的工具，类似于 Docker，但专门用于 LLM。

### 1.1 安装

```bash
brew install ollama
```

### 1.2 启动服务

```bash
ollama serve
```

> ⚠️ **保持此终端窗口开启**，Ollama 服务需要持续运行。

你应该看到类似输出：

```
Ollama is running on http://127.0.0.1:11434
```

### 1.3 拉取模型（新开一个终端）

```bash
ollama pull llama3.2
```

> 📦 llama3.2 约 2GB，首次下载需要等待几分钟。

### 1.4 验证模型安装成功

```bash
ollama list
```

预期输出：

```
NAME            ID              SIZE    MODIFIED
llama3.2:latest ...             2.0 GB  ...
```

---

## 第二步：安装 Python 依赖

```bash
pip install langgraph langchain-ollama langchain-core
```

### 依赖说明

| 包 | 作用 |
|----|------|
| `langgraph` | 提供 `create_react_agent`，构建 Agent 核心逻辑 |
| `langchain-ollama` | LangChain 对 Ollama 模型的封装 |
| `langchain-core` | `@tool` 装饰器、消息类型等基础组件 |

> 💡 如果看到 `NotOpenSSLWarning` 警告，可以用 `pip install "urllib3<2"` 消除，不影响运行。

---

## 第三步：创建 Weather Agent

新建文件 `weather_agent.py`，写入以下代码：

```python
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
```

---

## 第四步：启动与运行

### 完整启动顺序

```bash
# 终端 1：启动 Ollama 服务（保持运行）
ollama serve

# 终端 2：运行 Agent
python weather_agent.py
```

### 预期输出

```
Why did the fog in San Francisco bring a sweater?

Because it heard the Golden Gate Bridge was feeling a little "sus-pended" 
in the cold! 🌁😄

(In reality, SF is famously cool and foggy, especially in summer — locals 
call it "Karl the Fog"!)
```

### 运行流程图

```
用户输入
   │
   ▼
Agent 分析问题
   │
   ▼
调用 get_weather("sf") 工具
   │
   ▼
llama3.2 生成回答
   │
   ▼
输出最终结果
```

---

## 常见问题

### ❌ `Connection refused`

```
httpx.ConnectError: [Errno 61] Connection refused
```

**原因**：Ollama 服务未启动。

**解决**：

```bash
ollama serve
```

---

### ❌ `does not support tools`

```
ollama._types.ResponseError: registry.ollama.ai/library/llama3:latest does not support tools
```

**原因**：`llama3`（旧版）不支持 tool call。

**解决**：换成支持 tools 的模型：

```bash
ollama pull llama3.2
```

```python
# 修改代码中的模型名
model = ChatOllama(model="llama3.2")  # ✅
```

---

### ❌ `cannot import name 'create_agent'`

```
ImportError: cannot import name 'create_agent' from 'langchain.agents'
```

**原因**：`create_agent` 不存在，是错误的 API 名称。

**解决**：使用正确的导入：

```python
# ❌ 错误
from langchain.agents import create_agent

# ✅ 正确
from langgraph.prebuilt import create_react_agent
```

---

## 进阶：切换为 Claude

如果你有 Anthropic API Key，可以将模型替换为 Claude，效果更好：

```bash
pip install langchain-anthropic
```

```python
# 替换这两行即可，其余代码不变
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-sonnet-4-20250514")
```

在终端中设置 API Key：

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

> 📌 Claude.ai 的付费订阅和 API Key 是独立的，需要在 [console.anthropic.com](https://console.anthropic.com) 单独注册并充值。

---

## 项目结构

```
weather-agent/
├── weather_agent.py   # Agent 主程序
└── README.md          # 本教程
```

---

## 参考链接

- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [Ollama 官网](https://ollama.com)
- [支持 Tools 的 Ollama 模型列表](https://ollama.com/search?c=tools)
- [Anthropic Console](https://console.anthropic.com)
