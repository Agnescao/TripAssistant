# LLM 配置对比表

本文档详细列出了不同 LLM 提供商及其对应的 `quick_think_llm` 和 `deep_think_llm` 配置，帮助开发者更好地理解和选择合适的语言模型。

## 配置对比总览

| LLM 提供商 | 研究深度 | `quick_think_llm` | `deep_think_llm` | 特点 | `max_token` (近似值) |
|------------|----------|-------------------|------------------|------|---------------------|
| **dashscope (阿里百炼)** | 1级 - 快速分析 | `qwen-turbo` | `qwen-plus` | 最快响应，适合日常对话 | ~8192 |
| | 2级 - 基础分析 | `qwen-plus` | `qwen-plus` | 平衡性能和成本 | ~32768 |
| | 3级 - 标准分析 | `qwen-plus` | `qwen-max` | 默认配置，平衡性能 | ~32768 / ~8192 |
| | 4级 - 深度分析 | `qwen-plus` | `qwen-max` | 更强性能 | ~32768 / ~8192 |
| | 5级 - 全面分析 | `qwen-max` | `qwen-max` | 最强性能 | ~8192 |
| **deepseek** | 所有级别 | `deepseek-chat` | `deepseek-chat` | DeepSeek 只有一个模型 | ~8192 |
| **Google AI** | 1级 - 快速分析 | `gemini-2.0-flash` | `gemini-2.0-flash` | 快速模型 | ~8192 |
| | 2级 - 基础分析 | `gemini-2.0-flash` | `gemini-1.5-pro` | 快速思考用flash，深度思考用pro | ~8192 / ~8192 |
| | 3级 - 标准分析 | `gemini-1.5-pro` | `gemini-2.5-flash` | 平衡性能 | ~8192 / ~8192 |
| | 4级 - 深度分析 | `gemini-2.5-flash` | `gemini-2.5-pro` | 强大模型 | ~8192 / ~8192 |
| | 5级 - 全面分析 | `gemini-2.5-pro` | `gemini-2.5-pro` | 最强模型 | ~8192 |
| **openai** | 所有级别 | 根据选择的模型 | 根据选择的模型 | 使用统一模型配置 | 视具体模型而定 |
| **qianfan (百度千帆)** | 所有级别 | 根据选择的模型 | 根据选择的模型 | 使用统一模型配置 | 视具体模型而定 |
| **openrouter** | 所有级别 | 根据选择的模型 | 根据选择的模型 | 使用统一模型配置 | 视具体模型而定 |

## OpenAI 及其他提供商的模型选项

对于 `openai` 及其他支持自定义模型的提供商，具体的模型选择取决于用户在 `cli/utils.py` 文件中的选择。根据代码，可用的模型包括：

- `gpt-4o-mini` - 快速且高效的模型，适用于快速任务
- `gpt-4o` - 标准模型，具有可靠的综合能力
- `gpt-3.5-turbo` - 成本效益高的选项
- `claude-3-haiku-20240307` - Anthropic 的快速模型
- `meta-llama/llama-3.1-8b-instruct` - 开源模型
- `qwen/qwen-2.5-7b-instruct` - 针对中文优化的模型
- `custom` - 自定义模型名称

## extra model
 # Define shallow thinking llm engine options with their corresponding model names
    SHALLOW_AGENT_OPTIONS = {
        "openai": [
            ("GPT-4o-mini - Fast and efficient for quick tasks", "gpt-4o-mini"),
            ("GPT-4.1-nano - Ultra-lightweight model for basic operations", "gpt-4.1-nano"),
            ("GPT-4.1-mini - Compact model with good performance", "gpt-4.1-mini"),
            ("GPT-4o - Standard model with solid capabilities", "gpt-4o"),
        ],
        "anthropic": [
            ("Claude Haiku 3.5 - Fast inference and standard capabilities", "claude-3-5-haiku-latest"),
            ("Claude Sonnet 3.5 - Highly capable standard model", "claude-3-5-sonnet-latest"),
            ("Claude Sonnet 3.7 - Exceptional hybrid reasoning and agentic capabilities", "claude-3-7-sonnet-latest"),
            ("Claude Sonnet 4 - High performance and excellent reasoning", "claude-sonnet-4-0"),
        ],
        "google": [
            ("Gemini 2.5 Pro - 🚀 最新旗舰模型", "gemini-2.5-pro"),
            ("Gemini 2.5 Flash - ⚡ 最新快速模型", "gemini-2.5-flash"),
            ("Gemini 2.5 Flash Lite - 💡 轻量快速", "gemini-2.5-flash-lite"),
            ("Gemini 2.5 Pro-002 - 🔧 优化版本", "gemini-2.5-pro-002"),
            ("Gemini 2.5 Flash-002 - ⚡ 优化快速版", "gemini-2.5-flash-002"),
            ("Gemini 2.5 Flash - Adaptive thinking, cost efficiency", "gemini-2.5-flash-preview-05-20"),
            ("Gemini 2.5 Pro Preview - 预览版本", "gemini-2.5-pro-preview-06-05"),
            ("Gemini 2.0 Flash Lite - 轻量版本", "gemini-2.0-flash-lite"),
            ("Gemini 2.0 Flash - 推荐使用", "gemini-2.0-flash"),
            ("Gemini 1.5 Pro - 强大性能", "gemini-1.5-pro"),
            ("Gemini 1.5 Flash - 快速响应", "gemini-1.5-flash"),
        ],
        "openrouter": [
            ("Meta: Llama 4 Scout", "meta-llama/llama-4-scout:free"),
            ("Meta: Llama 3.3 8B Instruct - A lightweight and ultra-fast variant of Llama 3.3 70B", "meta-llama/llama-3.3-8b-instruct:free"),
            ("google/gemini-2.0-flash-exp:free - Gemini Flash 2.0 offers a significantly faster time to first token", "google/gemini-2.0-flash-exp:free"),
        ],
        "ollama": [
            ("llama3.1 local", "llama3.1"),
            ("llama3.2 local", "llama3.2"),
        ],
        "阿里百炼 (dashscope)": [
            ("通义千问 Turbo - 快速响应，适合日常对话", "qwen-turbo"),
            ("通义千问 Plus - 平衡性能和成本", "qwen-plus"),
            ("通义千问 Max - 最强性能", "qwen-max"),
        ],
        "deepseek v3": [
            ("DeepSeek Chat - 通用对话模型，适合股票投资分析", "deepseek-chat"),
        ],
        "🔧 自定义openai端点": [
            ("GPT-4o-mini - Fast and efficient for quick tasks", "gpt-4o-mini"),
            ("GPT-4o - Standard model with solid capabilities", "gpt-4o"),
            ("GPT-3.5-turbo - Cost-effective option", "gpt-3.5-turbo"),
            ("Claude-3-haiku - Fast Anthropic model", "claude-3-haiku-20240307"),
            ("Llama-3.1-8B - Open source model", "meta-llama/llama-3.1-8b-instruct"),
            ("Qwen2.5-7B - Chinese optimized model", "qwen/qwen-2.5-7b-instruct"),
            ("自定义模型 - 手动输入模型名称", "custom"),
        ]
    }
## 使用建议

1. **快速响应需求**：选择 `dashscope` 的 1 级配置或者 `Google AI` 的 flash 系列模型
2. **平衡性能与成本**：考虑使用 `dashscope` 的 2-3 级配置或 `deepseek`
3. **高性能需求**：选用 `dashscope` 的 4-5 级配置或 `Google AI` 的 pro 系列模型
4. **特定领域优化**：针对中文任务可以选择 `qwen` 系列模型

## 注意事项

- 不同提供商的模型在价格、速度和能力方面各有特点
- 应根据具体应用场景选择合适的模型配置
- 在生产环境中建议进行充分测试后再做最终选择
- 表格中的`max_token`值是基于公开资料的估计值，并非来自项目源码
- 对于`openai`、`qianfan`和`openrouter`提供商，其`max_token`值取决于用户选择的具体模型
- 项目代码中并未显式定义这些模型的最大token限制
- 实际应用中，这些值可能受到服务商API限制和项目配置的影响