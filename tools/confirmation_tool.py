from typing import Type, Any, Dict
from pydantic import BaseModel, Field
from langgraph.types import interrupt
from langchain_core.tools import tool


class ConfirmationArgs(BaseModel):
    """Input for confirmation tool."""
    message: str = Field(description="The message to show for confirmation.")
    operation_details: Dict[str, Any] = Field(description="Details of the operation to be confirmed.")


class ConfirmationTool:
    """通用确认工具类，用于在执行关键操作前请求用户确认"""
    
    def __init__(self, name: str = "confirmation_tool"):
        self.name = name
        self.description = "A tool for requesting user confirmation before critical operations."
        self.args_schema: Type[BaseModel] = ConfirmationArgs

    def run(self, message: str, operation_details: Dict[str, Any]) -> bool:
        """运行确认工具，请求用户确认"""
        print(f"请求用户确认: {message}")
        
        # 使用interrupt请求用户确认
        response = interrupt(
            f"{message}\n"
            "请审核并确认：批准（y）或拒绝（n）。"
        )
        
        # 根据用户响应处理
        if response.get("answer", "").lower() in ["y", "yes", "是"]:
            return True
        else:
            return False


# 创建航班确认工具实例
flight_confirmation_tool = ConfirmationTool("flight_confirmation_tool")

# 创建酒店确认工具实例
hotel_confirmation_tool = ConfirmationTool("hotel_confirmation_tool")


@tool("generic_confirmation")
def generic_confirmation(message: str, operation_details: Dict[str, Any]) -> str:
    """
    通用确认工具，用于请求用户确认关键操作
    
    Args:
        message: 显示给用户的确认消息
        operation_details: 操作的详细信息
        
    Returns:
        str: 用户的确认结果
    """
    print(f"请求确认: {message}")
    
    # 使用interrupt请求用户确认
    response = interrupt(
        f"{message}\n"
        f"操作详情: {operation_details}\n"
        "请确认：批准（y）或拒绝（n）或其他说明。"
    )
    
    # 返回用户响应
    return response.get("answer", "未收到确认")