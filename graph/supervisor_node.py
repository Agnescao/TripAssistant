from langchain_core.runnables import RunnableConfig
from langgraph.graph import MessagesState


def get_user_info(state: MessagesState, config: RunnableConfig):
    # 返回更新部分，MessagesState 会自动处理消息追加
    return {
        "messages": "dfsds",  # 新增 AIMessage
    }
