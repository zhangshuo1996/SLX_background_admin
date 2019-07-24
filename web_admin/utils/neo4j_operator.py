# -*- coding: UTF-8 -*-

from py2neo import Graph, Relationship, Node


class NeoOperator(object):

    def __init__(self, host, port, username, password):
        """
        创建连接
        :param host:
        :param port:
        :param username:
        :param password:
        :return:
        """
        self.neo = Graph(host=host, port=port, username=username, password=password)

    def create_agent(self, agent_id, name, agent_type):
        """
        插入商务信息到图数据库中
        :param agent_id: 商务id
        :param name: str 商务名
        :param agent_type: int 商务类型 0 -> 高校商务， 1 -> 企业商务
        :return: dict {success: True / False, message: xxx}
        """
        try:
            agent_node = Node("Agent", id=agent_id, name=name, type=agent_type)
            # create 函数无返回值 ==> 执行成功返回 None, 失败进入 except
            self.neo.create(agent_node)
            return {"success": True}
        except Exception as e:
            print(e)
            return {"success": False, "message": "用户 %d 已存在，请不要重复" % agent_id}

    def upsert_agent_relation(self, agent_id, teacher_id, is_visit=True):
        """
        创建/更新 商务与教师间的关系 => TODO：创建/更新商务与企业的关系 & 创建/更新教师与企业的关系
        :param agent_id: int 商务id
        :param teacher_id: int 教师id
        :param is_visit: bool 关系类型，True ==> 拜访（默认）， False ==> 参与活动
        :return: dict {success: True / False, message: xxx}
        """
        try:
            # 查找节点，若无，返回 None
            agent = self.neo.nodes.match("Agent", id=agent_id).first()
            if agent is None:
                return {"success": False, "message": "%d 商务不存在" % agent_id}

            teacher = self.neo.nodes.match("Teacher", id=teacher_id).first()
            if teacher is None:
                return {"success": False, "message": "%d 教师不存在" % teacher_id}

            # 查找现有关系，若无，返回 None
            match = self.neo.match(nodes=(agent, teacher), r_type="knows").first()
            # 在已有关系上修改
            if match:
                if is_visit == 1:
                    match['visited'] += 1
                else:
                    match["activity"] += 1
                # 更新数据，无返回值
                self.neo.push(match)
            else:
                if is_visit == 1:
                    match = Relationship(agent, "knows", teacher, visited=1, activity=0)
                else:
                    match = Relationship(agent, "knows", teacher, visited=0, activity=1)
                # 创建关系，无返回值
                self.neo.create(match)

            return {"success": True}
        except Exception as e:
            print(e)
            return {"success": False, "message": ""}


if __name__ == '__main__':
    from web_admin.config import NEO4J_CONFIG
    obj = NeoOperator(**NEO4J_CONFIG)
    # obj.create_agent(100000, "杨秀宁", 0)
    # # obj.upsert_agent_relation(100000, 99331)
    # obj.upsert_agent_relation(100000, 86791)
    # obj.upsert_agent_relation(100000, 86831)
    # obj.upsert_agent_relation(100000, 90147)

    # obj.get_school_relation_with_agent(100000, "南京大学")
    # obj.get_institution_relation_with_agent(100000, "中国科学技术大学", "管理学院")
    # obj.get_personal_relation_with_agent(100000, 90147)
    # obj.get_personal_relation_with_agent(100000, 90021)