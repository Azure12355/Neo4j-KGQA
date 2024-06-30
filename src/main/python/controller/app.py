from flask import Flask, request, jsonify
from src.main.python.service.graph_service import GraphService


# webController层
class GraphController:

    def __init__(self, debug=True, port=5050):
        self.graphService = GraphService()
        self.app = Flask(__name__)
        self.setup_routes()
        self.app.debug = debug
        self.app.run(port=port)
        print("初始化完毕, 一起开启愉快的知识之旅吧!!!")

    # 设置flask路由路径
    def setup_routes(self):
        # 根据指定的name查询实体及其所有关系
        @self.app.route('/searchEntity', methods=['GET', 'POST'])
        def search_entity():
            entityName = request.args.get('entityName')
            json_data = self.graphService.query_entity(str(entityName))
            return jsonify(json_data)

        # 查询所有的实体及其关系
        @self.app.route('/getAllEntities', methods=['GET', 'POST'])
        def get_all_entities():
            json_data = self.graphService.query_all_entity()
            return json_data

        # 查询实体模型
        @self.app.route('/getEntityModel', methods=['GET', 'POST'])
        def get_entity_model():
            json_data = self.graphService.query_entity_model()
            return json_data

        # 智能机器人问答
        @self.app.route('/chatbot', methods=['POST'])
        def chatbot():
            data = request.get_json()
            question = data.get('message', "你好")
            print(question)
            json_data = self.graphService.question_chatbot(question)
            return json_data

        # 知识图谱机器人问答
        @self.app.route('/KGQA_chatbot', methods=['POST'])
        def KGQA_chatbot():
            data = request.get_json()
            question = data.get('message', "你好")
            print(question)
            json_data = self.graphService.question_KGQA_chatbot(question)
            return json_data


if __name__ == '__main__':
    controller: GraphController = GraphController()
    controller.app.debug = True
    controller.app.run(port=8888)
