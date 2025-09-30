from typing import Type

from langgraph.types import interrupt
from pydantic import BaseModel, Field

from llm.llm_provider import get_llm_by_type


class SearchArgs(BaseModel):
    """Input for search tool."""
    query: str = Field(description="The query to web search for.")

class WebSearchTool(BaseModel):
    # tool name
    name : str = "web_search"
    # tool description
    description : str = "A tool for searching the web. Useful for when you need to answer questions about current events. Input should be a search query."
    return_direct: bool = False
    args_schema: Type[BaseModel] = SearchArgs


    def run(self, query: str) -> str:
        """Run the web search tool."""


        print('AI大模型尝试调用工具 `search_tool`来完成数据搜索')
        response = interrupt(
            f"AI大模型尝试调用工具 `search_tool`来完成数据搜索，\n"
            "请审核并选择：批准（y）或直接给我工具执行的答案。"
        )
        # response(字典): 由人工输入的：批准(y),工具执行的答案或者拒绝执行工具的理由
        # 根据人工响应类型处理
        if response["answer"] == "y":
            pass  # 直接使用原参数继续执行
        else:
            return f"人工终止了该工具的调用，给出的理由或者答案是:{response['answer']}",

        # call web search  model

        response = get_llm_by_type("websearch").web_search(query)

        if response.status_code == 200:
            return response.json()["data"]["results"][0]["snippet"]
        else:
            return "Error: " + response.text




