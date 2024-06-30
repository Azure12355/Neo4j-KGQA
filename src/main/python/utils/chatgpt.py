import requests
from openai import OpenAI
import os

FREE_API_KEY = "sk-PtANUuG4EnktCbEpzrhOGiGF8fxnetLR9kpCXQDaQP3MRWEu"
PREMIUM_API_KEY = "sk-MjDZOW5dPHFb74D2NJGqRMQaNlTZJ3Y4Wdzn0LRcTdLT3UTw"


class ChatGPTConstant:
    """
    转发地址URL
    """
    BASE_URL_DIRECT1 = "https://api.chatanywhere.tech/v1"  # 国内直连1
    BASE_URL_DIRECT2 = "https://api.chatanywhere.com.cn/v1"  # 国内直连2
    BASE_URL_REDIRECT = "https://api.chatanywhere.cn/v1"  # 国外转发

    """
    ChatGPT问答模型
    """
    GPT35_TURBO = "gpt-3.5-turbo"  # 默认模型，等于gpt-3.5-turbo-0613
    GPT35_TURBO_1106 = "gpt-3.5-turbo-1106"  # 最新模型，数据最新，价格更低，速度更快。
    GPT35_TURBO_0125 = "gpt-3.5-turbo-0125"  # 最新模型，数据最新，价格更更低，速度更快，修复了一些1106的bug, 强烈推荐!!!
    GPT35_TURBO_0301 = "gpt-3.5-turbo-0301"  # 适合快速回答简单问题
    GPT35_TURBO_0613 = "gpt-3.5-turbo-0613"  # 适合快速回答简单问题，支持Function
    GPT35_TURBO_16K = "gpt-3.5-turbo-16k"  # 适合快速回答简单问题,字数更多
    GPT35_TURBO_16K_0613 = "gpt-3.5-turbo-16k-0613"  # 适合快速回答简单问题，字数更多，支持Function
    GPT4 = "gpt-4"  # 默认模型，等于gpt-4-0613
    GPT4_0613 = "gpt-4-0613	"  # 最强模型，功能更强大
    GPT4_TURBO_PREVIEW = "gpt-4-turbo-preview"  # 最新模型，输入128K，输出最大4K，知识库最新2023年4月, 此模型始终指向最新的4的preview模型
    GPT4_0125_PREVIEW = "gpt-4-0125-preview"  # 最新模型，输入128K，输出最大4K，知识库最新2023年4月, 修复了一些1106的bug
    GPT4_1106_PREVIEW = "gpt-4-1106-preview"  # 最新模型，输入128K，输出最大4K，知识库最新2023年4月
    GPT4_VISION_PREVIEW = "gpt-4-vision-preview"  # 最新模型，多模态（此模型官方有每日调用次数限制可能会不能用，次日上午8点刷新限制）
    GPT35_TURBO_INSTRUCT = "gpt-3.5-turbo-instruct"  # Completions模型 用于文本生成，提供准确的自然语言处理模型一般人用不上


class ChatGPT:
    def __init__(self,
                 base_url: str = os.environ.get("OPENAI_API_BASE"),
                 is_stream: bool = True,
                 is_premium: bool = False,
                 gpt_model: str = ChatGPTConstant.GPT35_TURBO_0125):

        self.is_stream = is_stream  # 是否以stream流的形式传输
        self.gpt_model = gpt_model  # 选择的gpt模型
        self.base_url = base_url  # 转发地址
        self.context = []  # 用于保存每次对话的上下文
        if is_premium:
            self.API_KEY = os.environ.get("OPENAI_API_KEY")
        else:
            self.API_KEY = os.environ.get("OPENAI_API_KEY")
        self.client = OpenAI(
            # defaults to os.environ.get("OPENAI_API_KEY")
            api_key=self.API_KEY,
            base_url=self.base_url
        )

        print("ChatGPT->初始化成功...")

    # 非流式响应
    def gpt_api(self, messages: list) -> str:
        """为提供的对话消息创建新的回答
        Args:
            messages (list): 完整的对话消息
        """
        completion = self.client.chat.completions.create(
            model=self.gpt_model,
            messages=messages)
        print("ChatGPT: " + completion.choices[0].message.content)
        return completion.choices[0].message.content

    # 流式响应

    def gpt_api_stream(self, messages: list) -> str:
        """为提供的对话消息创建新的回答 (流式传输)
        Args:
            messages (list): 完整的对话消息
        """
        stream = self.client.chat.completions.create(
            model=self.gpt_model,
            messages=messages,
            stream=True,
        )

        buffer_result = ''
        print("ChatGPT: ", end='')
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                buffer_result += chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, end='')
        print()  # 打印换行符
        return buffer_result

    # ChatGPT 问答
    def question(self, question: str):
        """向ChatGPT提出问题
        Args:
            question (str): 问题

        Returns:
            str: 回答
        """
        if len(self.context) == 0:
            self.context.append({
                'role': 'system',
                'content': '假设你现在是一位专业的医疗领域的智能问答机器人，你可以根据用户提出的问题作出相应的医疗领域的回答并给出相应的解决方案，你只能回答医疗领域的相关问题，不能回答其他领域的问题！！！'
            })

        self.context.append({
            'role': 'user',
            'content': question
        })

        if self.is_stream:
            answer = self.gpt_api_stream(self.context)
            self.context.append({
                'role': 'assistant',
                'content': answer
            })
            return answer
        else:
            answer = self.gpt_api(self.context)
            self.context.append({
                'role': 'assistant',
                'content': answer
            })
            return answer

    # 罗列所有可用模型
    def list_models(self):
        url = "https://api.chatanywhere.com.cn/v1/models"

        payload = {}
        headers = {
            'Authorization': f'Bearer {self.API_KEY}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    # 语音转文字
    def speech_to_text(self, voice_file_path):
        url = "https://api.chatanywhere.com.cn/v1/audio/transcriptions"
        # 生成自定义的多部分边界字符串（不需要这一步）

        payload = {}
        files = [
            ('file', (voice_file_path, open(voice_file_path, 'rb'), 'application/octet-stream'))
        ]
        headers = {
            'Authorization': f'Bearer {self.API_KEY}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            # 'Content-Type': 'multipart/form-data'
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        return response.json()


if __name__ == '__main__':
    chat = ChatGPT(is_premium=True, gpt_model=ChatGPTConstant.GPT35_TURBO_0125)
    print("ChatGPT: How can I help you today?")
    while True:
        question = input("User: ")
        chat.question(question)
