from dao.graph import GraphDAO
from dao.config import GraphConfig
from KGQA.chatgpt import ChatGPT, ChatGPTConstant
from KGQA.chatbot_graph import KGQA_Chatbot


# web服务层
class GraphService:
    def __init__(self):
        self.graphDAO = GraphDAO(GraphConfig.HOST, GraphConfig.USER, GraphConfig.PASSWORD)
        self.chatbot = ChatGPT()
        self.KGQA_Chatbot = KGQA_Chatbot()

    # 查询对应实体
    def query_entity(self, name: str) -> dict:
        return self.graphDAO.match_node_with_relationship(name)

    # 查询所有实体及其关系
    def query_all_entity(self) -> dict:
        return self.graphDAO.query_all_entities()

    # 查询实体模型
    def query_entity_model(self) -> dict:
        return self.graphDAO.query_entity_model()

    # 智能问答机器人
    def question_chatbot(self, question: str) -> dict:
        answer = self.chatbot.question(question)
        return {"message": answer}

    # 知识图谱智能问答机器人
    def question_KGQA_chatbot(self, question: str) -> dict:
        answer = self.KGQA_Chatbot.receive(question)
        return {"message": answer}


if __name__ == "__main__":
    graphService = GraphService()
    data = graphService.question_chatbot("你好呀")
    print(data)
