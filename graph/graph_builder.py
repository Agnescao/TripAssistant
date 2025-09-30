from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import MessagesState, StateGraph
import os

from agents.agent_creation import create_agents
from graph.agent_nodes import supervisor_agent
from graph.supervisor_node import get_user_info


class State(MessagesState):
    pass


memory = MemorySaver()



graph=(
    StateGraph(State)
    .add_node('fetch_user_info', get_user_info)
    # add supervisor agent node to manage the workflow
    .add_node('supervisor_agent', supervisor_agent,
              destinations=("research_agent", 'flight_booking_agent', 'hotel_booking_agent', 'car_rental_booking_agent',
                            'excursion_booking_agent', 'train_booking_agent', END))
    .add_node('research_agent', research_agent, destinations=(END,))
    .add_node('flight_booking_agent', dummy_node, destinations=('recommendation_agent', END))  # 可以转向推荐
    .add_node('hotel_booking_agent', dummy_node, destinations=('recommendation_agent', END))   # 可以转向推荐
    .add_node('car_rental_booking_agent', dummy_node, destinations=(END,))
    .add_node('excursion_booking_agent', dummy_node, destinations=(END,))
    .add_node('train_booking_agent', dummy_node, destinations=(END,))
    .add_node('recommendation_agent', dummy_node, destinations=('flight_booking_agent', 'hotel_booking_agent', END))  # 推荐后可返回预订
    .add_edge(START, 'fetch_user_info')
    .add_edge('fetch_user_info', 'supervisor_agent')
    .compile(checkpointer=memory)
)

# 生成mermaid图表文本并保存到文件
try:
    mermaid_code = graph.get_graph().draw_mermaid()
    
    # 添加自定义紫色样式
    styled_mermaid_code = mermaid_code.replace(
        "classDef default fill:#f2f0ff,line-height:1.2",
        "classDef default fill:#f2f0ff,line-height:1.2,stroke:#5a3e9e,color:#5a3e9e"
    )
    
    # 确保graph目录存在
    os.makedirs("graph", exist_ok=True)
    
    # 保存mermaid文本到文件
    with open("graph/workflow_graph.mmd", "w", encoding="utf-8") as f:
        f.write(styled_mermaid_code)
    
    print("Mermaid图表代码已保存到 graph/workflow_graph.mmd")
    print("节点文字颜色已调整为紫色调")
    print("您可以使用mermaid-cli等工具将其转换为PNG图像:")
    print("npx mmdc -i graph/workflow_graph.mmd -o graph/workflow_graph.png")
    
except Exception as e:
    print(f"生成图表时出错: {e}")