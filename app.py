from flask import Flask, request, jsonify
from service.graph_service import GraphService


# webController层
class GraphController:
    def __init__(self):
        self.graphService = GraphService()
        print("初始化完毕, 一起开启愉快的知识之旅吧!!!")


graphController = GraphController()

app = Flask(__name__)


# 根据指定的name查询实体及其所有关系
@app.route('/searchEntity', methods=['GET', 'POST'])
def search_entity():
    entityName = request.args.get('entityName')
    json_data = graphController.graphService.query_entity(str(entityName))
    return jsonify(json_data)


# 查询所有的实体及其关系
@app.route('/getAllEntities', methods=['GET', 'POST'])
def get_all_entities():
    json_data = graphController.graphService.query_all_entity()
    return json_data


# 查询实体模型
@app.route('/getEntityModel', methods=['GET', 'POST'])
def get_entity_model():
    json_data = graphController.graphService.query_entity_model()
    return json_data


# 智能机器人问答
@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    question = data.get('message', "你好")
    print(question)
    json_data = graphController.graphService.question_chatbot(question)
    return json_data


# 知识图谱机器人问答
@app.route('/KGQA_chatbot', methods=['POST'])
def KGQA_chatbot():
    data = request.get_json()
    question = data.get('message', "你好")
    print(question)
    json_data = graphController.graphService.question_KGQA_chatbot(question)
    return json_data


if __name__ == '__main__':
    app.debug = True
    app.run(port=8888)
