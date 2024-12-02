from llm.qwen import Qwen


def test_qwen_chat():
    # 初始化 Qwen 实例
    qwen = Qwen(version="qwen-plus")

    # 测试基本对话
    prompt = "你好，请介绍一下你自己"
    history = []
    response = qwen.chat(prompt, history)

    # 验证响应
    assert response is not None
    print("Chat response:", response)


def test_qwen_stream_chat():
    # 初始化 Qwen 实例
    qwen = Qwen(version="qwen-plus")

    # 测试流式对话
    prompt = "计算 123 + 456 等于多少?"
    history = []

    # 获取流式响应
    for response in qwen.stream_chat(prompt, history):
        # 验证每个响应块
        assert response is not None
        print("Stream response chunk:", response)


if __name__ == "__main__":
    # 运行测试
    print("Testing chat...")
    test_qwen_chat()

    print("\nTesting stream chat...")
    test_qwen_stream_chat()
