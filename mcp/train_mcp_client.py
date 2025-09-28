from langchain_mcp_adapters.client import MultiServerMCPClient

ticket_mcp_server_config = {  # 12306  免费的mcp server
    "transport": "sse",
    "url": "https://mcp.api-inference.modelscope.net/fe27f100425941/sse"
}

# mcp client
internal_mcp_client = MultiServerMCPClient({
    'ticket_mcp': ticket_mcp_server_config,
})
