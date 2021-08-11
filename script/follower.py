import requests

from neo4j import GraphDatabase


class JueJin(object):
    followers_url = "https://api.juejin.cn/user_api/v1/follow/followers"
    followees_url = "https://api.juejin.cn/user_api/v1/follow/followees"

    def __init__(self):
        self.session = requests.session()

    def get_followers(self, user_id, cursor, limit):
        params = {
            "user_id": user_id,
            "cursor": cursor,
            "limit": limit
        }
        return self.session.request("get", self.followers_url, params=params).json()

    def get_followees(self, user_id, cursor, limit):
        params = {
            "user_id": user_id,
            "cursor": cursor,
            "limit": limit
        }
        return self.session.request("get", self.followees_url, params=params).json()


class App(object):

    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        self.driver.close()

    @classmethod
    def create_person(cls, tx, name):
        tx.run("CREATE (:Person {name: $name})", name=name)

    @classmethod
    def create_friendship(cls, tx, name_a, name_b):
        tx.run("MATCH (a:Person {name: $name_a}) "
               "MATCH (b:Person {name: $name_b}) "
               "MERGE (a)-[:Follower]->(b)",
               name_a=name_a, name_b=name_b)

    @classmethod
    def delete_person(cls, tx):
        tx.run("MATCH(p:Person) DETACH DELETE p;", )

    @staticmethod
    def _find_and_return_person(tx, name):
        query = (
            "MATCH (p:Person) "
            "WHERE p.name = name "
            "RETURN p.name AS name"
        )
        result = tx.run(query, name=name)
        return [record["name"] for record in result]


def main():
    # Connecting to Aura, use the "neo4j+s" URI scheme
    scheme = "neo4j"
    host_name = "deepin"
    port = 7687
    url = "{scheme}://{host_name}:{port}".format(scheme=scheme, host_name=host_name, port=port)
    user = "neo4j"
    password = "admin"
    app = App(url, user, password)

    juejin = JueJin()
    user_id, user_name = "993614678985085", "西红柿蛋炒饭"
    cursor, limit = 0, 20
    followees, followers = [], []

    has_more = True
    while has_more:
        result = juejin.get_followees(user_id, cursor, limit)
        data = result['data']['data']
        followees += data
        has_more = result['data']['hasMore']
        cursor = result['data']['cursor']

    cursor, limit = 0, 20
    has_more = True
    while has_more:
        result = juejin.get_followers(user_id, cursor, limit)
        data = result['data']['data']
        followers += data
        has_more = result['data']['hasMore']
        cursor = result['data']['cursor']

    names = {f["user_name"] for f in followees + followers}

    "MATCH(p1:Person) - [:Follower]->(p2:Person) - [:Follower]->(p1:Person)  return p1,p2;"

    with app.driver.session() as session:

        session.write_transaction(app.delete_person)

        session.write_transaction(
            app.create_person, user_name)

        for name in names:
            session.write_transaction(
                app.create_person, name)

        for person in followees:
            session.write_transaction(
                app.create_friendship, user_name, person['user_name'])

        for person in followers:
            session.write_transaction(
                app.create_friendship, person['user_name'], user_name)

    names1 = {f["user_name"] for f in followees}
    names2 = {f["user_name"] for f in followers}

    # 查看我关注却没有关注我的人
    print(names1 - names2)
    app.close()


if __name__ == '__main__':
    main()
