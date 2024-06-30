from src.main.python.service.KGQA.question_classifier import *
from src.main.python.service.KGQA.question_parser import *
from src.main.python.service.KGQA.answer_search import *

'''问答类'''


class KGQA_Chatbot:
    def __init__(self):
        self.classifier = QuestionClassifier()  # 问题分类器
        self.parser = QuestionPaser()  # 问题解析器
        self.searcher = AnswerSearcher()  # 答案搜寻器

    # 接收问题
    def receive(self, question):
        return self.do_handle(question)

    # 核心处理方法
    def do_handle(self, sent):
        answer = '您好，我是医药智能助理，希望可以帮到您。祝您身体健康！'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return self.response(answer)
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return self.response(answer)
        else:
            return self.response('\n'.join(final_answers))

    # 后置处理方法
    def response(self, result):
        return result


if __name__ == '__main__':
    handler = KGQA_Chatbot()
    while 1:
        question = input('用户:')
        answer = handler.receive(question)
        print('智能AI医疗小助手:', answer)
