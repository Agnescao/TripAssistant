# 向量检索模块设计文档

## 模块概述

向量检索模块负责将文本内容转换为向量表示，并支持基于语义的相似度检索。该模块基于 ChromaDB 向量数据库实现，结合了 OpenAI 和 DashScope 的嵌入模型，提供了企业内部政策等文本的向量存储和检索功能。

## 核心组件

### 1. ChromaDBManager (单例管理器)

`ChromaDBManager` 是一个单例类，用于管理 ChromaDB 向量存储实例，避免创建多个实例导致冲突。

主要功能：
- 初始化 ChromaDB 客户端
- 线程安全的集合管理
- 自动持久化数据到本地

```python
class ChromaDBManager:
    _instance = None
    _lock = threading.Lock()
    _collections: Dict[str, any] = {}
```

### 2. EnterpriseInnerPolicyVectorStore (企业内部政策向量存储)

该类实现了企业内部政策文本的向量处理和存储功能。

#### 主要特性：

- **智能文本截断**：支持超长文本的智能截断处理
- **双模型支持**：同时支持 OpenAI 和 DashScope 嵌入模型
- **错误处理机制**：完善的异常处理和重试机制

#### 配置参数：

- `max_embedding_size`：最大嵌入文本长度（默认50000）
- `enable_max_embedding_length`：是否启用最大长度检查

## 工作流程

### 1. 初始化阶段

1. 读取企业政策文档内容
2. 使用正则表达式按标题分割文档
3. 初始化嵌入模型（OpenAI `text-embedding-ada-002`）
4. 创建 ChromaDB 管理器实例

### 2. 文本嵌入处理

```python
def get_embedding(self, search_text):
    # 输入验证
    # 文本长度检查和截断
    # 调用 DashScope API 获取嵌入向量
    # 错误处理和重试机制
```

### 3. 向量存储

```python
def add_to_embedding(self, policies):
    # 批量处理政策文本
    # 生成唯一ID
    # 获取文本嵌入向量
    # 存储到 ChromaDB 集合中
```

## 技术特点

### 1. 多模型支持
- 主要使用 DashScope `text-embedding-v1` 模型
- 备用 OpenAI `text-embedding-ada-002` 模型配置

### 2. 智能错误处理
- 自动检测文本长度超限错误
- 动态启用文本截断机制
- 详细的日志记录和错误追踪

### 3. 线程安全
- 使用线程锁保证并发安全
- 单例模式避免重复初始化
- 集合缓存提高访问效率

## 配置说明

环境变量配置：
- `max_embedding_size`：设置最大文本长度限制
- `enable_max_embedding_length`：控制是否启用长度检查

## 使用场景

1. **企业政策检索**：快速检索相关政策条款
2. **智能问答系统**：基于语义相似度的问答匹配
3. **文档内容分析**：分析文档间的语义关联性

该模块为 TripAssistant 项目提供了强大的语义检索能力，能够有效处理企业内部复杂政策文档的向量化存储和检索需求。