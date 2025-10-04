from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import MessagesState, StateGraph
import os
import re
from langgraph.types import Command

from graph.agent_nodes import supervisor_agent, research_agent, flight_booking_agent, hotel_booking_agent, \
    car_rental_booking_agent, excursion_booking_agent, train_booking_agent, recommendation_agent
from graph.pretty_print import pretty_print_messages
from graph.supervisor_node import get_user_info
from tools.retriever_vector import EnterpriseInnerPolicyVectorStore


class State(MessagesState):
    pass


memory = MemorySaver()
# create a singleton instance of enterprise inner policy vector store
enterprise_vector_store = None


def _init_vector_store(config):
    """初始化向量存储"""
    global enterprise_vector_store
    if enterprise_vector_store is not None:
        return enterprise_vector_store
        
    try:

        # 获取当前文件所在目录，然后构建正确的文件路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        doc_path = os.path.join(current_dir, "..", "doc", "order_faq.md")

        # read invoice rules and cancelation policy
        with open(doc_path, "r", encoding="utf-8") as f:
            order_text = f.read()

        # create document from  text and split it into chunks by title like "##
        doc = [{"page_content": txt} for txt in re.split(r"(?=\n##)", order_text)]
        # use EnterpriseInnerPolicyVectorStore to store doc

        enterprise_vector_store = EnterpriseInnerPolicyVectorStore("enterprise_policy", config)
        # 注意：根据实际API可能需要调整以下方法调用
        enterprise_vector_store.add_to_embedding(doc)
        # enterprise_vector_store.persist()
        print("Enterprise vector store initialized successfully")
        return enterprise_vector_store
    except Exception as e:
        print(f"Failed to initialize enterprise vector store: {e}")
        return None


class TripGraph:
    """封装旅行规划工作流图的类"""
    def __init__(self,config:dict):
        self.config = config


graph=(
    StateGraph(MessagesState)
    .add_node('fetch_user_info', get_user_info)
    # add supervisor agent node to manage the workflow
    .add_node('supervisor_agent', supervisor_agent,
              destinations=("research_agent", 'flight_booking_agent', 'hotel_booking_agent', 'car_rental_booking_agent',
                            'excursion_booking_agent', 'train_booking_agent','recommendation_agent', END))
    .add_node('research_agent', research_agent, destinations=(END,))
    .add_node('flight_booking_agent', flight_booking_agent, destinations=('recommendation_agent', END))  # 可以转向推荐
    .add_node('hotel_booking_agent', hotel_booking_agent, destinations=('recommendation_agent', END))   # 可以转向推荐
    .add_node('car_rental_booking_agent', car_rental_booking_agent, destinations=(END,))
    .add_node('excursion_booking_agent', excursion_booking_agent, destinations=(END,))
    .add_node('train_booking_agent', train_booking_agent, destinations=(END,))
    .add_node('recommendation_agent', recommendation_agent, destinations=('flight_booking_agent', 'hotel_booking_agent', END))  # 推荐后可返回预订
    .add_edge(START, 'fetch_user_info')
    .add_edge('fetch_user_info', 'supervisor_agent')
    .compile(checkpointer=memory)
)

# 生成mermaid图表文本并保存到文件
# try:
#     mermaid_code = graph.get_graph().draw_mermaid()
#
#     # 添加自定义紫色样式
#     styled_mermaid_code = mermaid_code.replace(
#         "classDef default fill:#f2f0ff,line-height:1.2",
#         "classDef default fill:#f2f0ff,line-height:1.2,stroke:#5a3e9e,color:#5a3e9e"
#     )
#
#     # 确保graph目录存在
#     os.makedirs("graph", exist_ok=True)
#
#     # 保存mermaid文本到文件
#     with open("graph/workflow_graph.mmd", "w", encoding="utf-8") as f:
#         f.write(styled_mermaid_code)
#
#     print("Mermaid图表代码已保存到 graph/workflow_graph.mmd")
#     print("节点文字颜色已调整为紫色调")
#     print("您可以使用mermaid-cli等工具将其转换为PNG图像:")
#     print("npx mmdc -i graph/workflow_graph.mmd -o graph/workflow_graph.png")
#
# except Exception as e:
#     print(f"生成图表时出错: {e}")


    # 生成一个唯一的会话ID testing on localhost
import uuid
session_id = str(uuid.uuid4())
# 配置参数，包含乘客ID和线程ID
config = {
    "configurable": {
        # passenger_id用于我们的航班工具，以获取用户的航班信息
        "passenger_id": "3442 587242",
        # 检查点由session_id访问
        "thread_id": session_id,
    }
}



def execute_graph(user_input:str):
    """执行工作 流"""
    # 初始化企业内部政策向量存储
    global enterprise_vector_store
    if enterprise_vector_store is None:
        enterprise_vector_store = _init_vector_store(config)
    else:
        print(" enterprise_vector_store is initialized")

    result = ''  # AI助手的最后一条消息
    current_state = graph.get_state(config)
    if current_state.next:  # 出现了工作流的中断
        human_command = Command(resume={'answer': user_input})
        for chunk in graph.stream(human_command, config, stream_mode='values'):
            pretty_print_messages(chunk, last_message=True)
        return result
    else:
        for chunk in graph.stream({'messages': ('user', user_input)}, config):
            pretty_print_messages(chunk, last_message=True)

    current_state = graph.get_state(config)
    if current_state.next:  # 出现了工作流的中断
        result = current_state.interrupts[0].value

    return result


#执行工作流
while True:
    user_input = input('用户：')
    res = execute_graph(user_input)
    if res:
        print('AI: ', res)