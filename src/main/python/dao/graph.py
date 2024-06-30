import json

from py2neo import Graph, Node, Relationship
from py2neo.cypher import Cursor
from src.main.python.dao.config import GraphConfig
from src.main.python.dao.utils import *
from my_utils import Utils
import os


# webDAO层
class GraphDAO:
    def __init__(self, host: str, user: str, password: str):
        self.graph = Graph(
            host=host,
            user=user,
            password=password
        )

        print("GraphDAO->初始化成功...")

    # 测试连接
    def test_connection(self):
        try:
            self.graph.run("MATCH (n) RETURN count(n)")
            print("Neo4j database connected successfully!")
        except Exception as e:
            print(f"Failed to connect to Neo4j database: {str(e)}")

    # 插入节点
    def insert_node(self, label: str, properties: dict):
        try:
            node = Node(label, **properties)
            self.graph.create(node)
            print(f"Node inserted successfully: {label} - {properties}")
        except Exception as e:
            print(f"Failed to insert node into Neo4j database: {str(e)}")

    # 删除节点
    def delete_node(self, label: str, properties: dict):
        try:
            node = self.graph.nodes.match(label, **properties).first()
            if node:
                self.graph.delete(node)
                print(f"Node deleted successfully: {label} - {properties}")
            else:
                print(f"Node not found: {label} - {properties}")
        except Exception as e:
            print(f"Failed to delete node from Neo4j database: {str(e)}")

    # 更新节点属性
    def update_node(self, label: str, properties: dict, new_properties: dict):
        try:
            node = self.graph.nodes.match(label, **properties).first()
            if node:
                for key, value in new_properties.items():
                    node[key] = value
                self.graph.push(node)
                print(f"Node updated successfully: {label} - {properties} -> {new_properties}")
            else:
                print(f"Node not found: {label} - {properties}")
        except Exception as e:
            print(f"Failed to update node in Neo4j database: {str(e)}")

    # 查询对应的节点
    def match_node(self, label: str, properties: dict) -> Node:
        try:
            node = self.graph.nodes.match(label, **properties).first()
            return node
        except Exception as e:
            print(f"Failed to match node in Neo4j database: {str(e)}")

    # 返回指定的节点及其所有关联节点和它们之间的关系
    def match_node_with_relationship(self, name: str) -> dict:
        try:
            cypher = 'MATCH (p:Disease{name: "%s"})-[r]->(n) RETURN p.name, r.name, n.name, labels(p), labels(n) UNION ALL MATCH (p)-[r]->(n:Disease {name: "%s"}) RETURN p.name, r.name, n.name, labels(p), labels(n)' % (
                name, name)
            # cypher = 'MATCH (p)-[r]->(n) RETURN p.name, r.name, n.name, labels(p), labels(n)'
            results: Cursor = self.graph.run(cypher)
            records = []
            for result in results.data(*results.keys()):
                records.append(result)
            return get_json_data(records)
        except Exception as e:
            print(f"Failed to match node with relationships: {str(e)}")

    # 创建节点关系
    def create_relationship(self, start_node: Node, end_node: Node, relationship_type: str):
        try:
            relationship = Relationship(start_node, relationship_type, end_node)
            self.graph.create(relationship)
            print(f"Relationship created successfully: {start_node} -[{relationship_type}]-> {end_node}")
        except Exception as e:
            print(f"Failed to create relationship in Neo4j database: {str(e)}")

    # 返回出现次数最多的关系以及其出现次数
    def list_relationships(self, count) -> list:
        try:
            query = """
            MATCH ()-[r]->()
            RETURN type(r) AS relationship_type, COUNT(r) AS relationship_count
            ORDER BY relationship_count DESC
            LIMIT {}
            """.format(count)
            result = self.graph.run(query).data()
            if result:
                return result
            else:
                return []
        except Exception as e:
            print(f"Failed to retrieve relationship: {str(e)}")

    # 返回出现次数最多的关系以及其出现次数
    def list_nodes(self, count) -> list:
        try:
            query = """
            MATCH (n)-[r]->()
            WITH n, COUNT(r) AS relationship_count
            ORDER BY relationship_count DESC
            LIMIT {}
            RETURN n, relationship_count
            """.format(count)
            result = self.graph.run(query).data()
            if result:
                return result
            else:
                return []
        except Exception as e:
            print(f"Failed to retrieve node: {str(e)}")

    # 执行指定的cyper语句
    def do_cyper(self, cyper: str):
        try:
            return self.graph.run(cyper).data()
        except Exception as e:
            print(f"Failed run specific cyper: {str(e)}")

    # 返回所有的实体比例
    def get_entity_ratio(self):

        # 获取总实体数
        total_entities_query = """
        MATCH (n)
        RETURN count(n) AS count
        """
        total_entities_result = self.graph.run(total_entities_query).data()
        total_entities = total_entities_result[0]['count']

        # 获取每个实体类型的数量并计算比例
        entity_ratio_query = """
        MATCH (n)
        RETURN labels(n)[0] AS label, count(n) AS count
        """
        entity_ratio_results = self.graph.run(entity_ratio_query).data()

        entity_ratios = []
        for result in entity_ratio_results:
            label = result['label']
            count = result['count']
            percentage = round((count / total_entities) * 100)
            entity_ratios.append({"value": percentage, "name": label})

        return entity_ratios

    # 返回所有的关系比例
    def get_relationship_ratio(self):

        # 获取总关系数
        total_relationships_query = """
        MATCH ()-[r]->()
        RETURN count(r) AS count
        """
        total_relationships_result = self.graph.run(total_relationships_query).data()
        total_relationships = total_relationships_result[0]['count']

        # 获取每种关系类型的数量并计算比例
        relationship_ratio_query = """
        MATCH ()-[r]->()
        RETURN type(r) AS type, count(r) AS count
        """
        relationship_ratio_results = self.graph.run(relationship_ratio_query).data()

        relationship_ratios = []
        for result in relationship_ratio_results:
            rel_type = result['type']
            count = result['count']
            percentage = round((count / total_relationships) * 100)
            relationship_ratios.append({"value": percentage, "name": rel_type})

        return relationship_ratios

    # 返回所有的节点及其关系
    @staticmethod
    def query_all_entities():
        path = os.path.join(Utils.RESOURCES_PATH, 'static/all_entities.json')
        with open(path, encoding='utf-8') as f:
            return json.loads(f.read())

    # 获取实体模型
    @staticmethod
    def query_entity_model():
        path = os.path.join(Utils.RESOURCES_PATH, 'static/entity_model.json')
        with open(path, encoding='utf-8') as f:
            return json.loads(f.read())


if __name__ == "__main__":
    graphDAO = GraphDAO(GraphConfig.HOST, GraphConfig.USER, GraphConfig.PASSWORD)
    graphDAO.test_connection()
    data = graphDAO.query_entity_model()
    print(data)
