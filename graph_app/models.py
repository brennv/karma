from py2neo import Graph, Node, Relationship, authenticate
from passlib.hash import bcrypt
from datetime import datetime
import os
import uuid

url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
username = os.environ.get('NEO4J_USERNAME')
password = os.environ.get('NEO4J_PASSWORD')

if username and password:
    authenticate(url.strip('http://'), username, password)

graph = Graph(url + '/db/data/')

class User:
    def __init__(self, username):
        self.username = username

    def find(self):
        user = graph.find_one("User", "username", self.username)
        return user

    def register(self, password):
        if not self.find():
            user = Node("User", username=self.username, password=bcrypt.encrypt(password))
            graph.create(user)
            return True
        else:
            return False

    def verify_password(self, password):
        user = self.find()
        if user:
            return bcrypt.verify(password, user['password'])
        else:
            return False

    def add_offer(self, title, tags, text):
        user = self.find()
        offer = Node(
            "Offer",
            id=str(uuid.uuid4()),
            title=title,
            text=text,
            timestamp=timestamp(),
            date=date()
        )
        rel = Relationship(user, "OFFERED", offer)
        graph.create(rel)

        tags = [x.strip() for x in tags.lower().split(',')]
        for t in set(tags):
            tag = graph.merge_one("Tag", "name", t)
            rel = Relationship(tag, "TAGGED", offer)
            graph.create(rel)

    def like_offer(self, offer_id):
        user = self.find()
        offer = graph.find_one("Offer", "id", offer_id)
        graph.create_unique(Relationship(user, "LIKED", offer))

    def get_recent_offers(self):
        query = """
        MATCH (user:User)-[:OFFERED]->(offer:Offer)<-[:TAGGED]-(tag:Tag)
        WHERE user.username = {username}
        RETURN offer, COLLECT(tag.name) AS tags
        ORDER BY offer.timestamp DESC LIMIT 5
        """

        return graph.cypher.execute(query, username=self.username)

    def get_similar_users(self):
        # Find three users who are most similar to the logged-in user
        # based on tags they've both blogged about.
        query = """
        MATCH (you:User)-[:OFFERED]->(:Offer)<-[:TAGGED]-(tag:Tag),
              (they:User)-[:OFFERED]->(:Offer)<-[:TAGGED]-(tag)
        WHERE you.username = {username} AND you <> they
        WITH they, COLLECT(DISTINCT tag.name) AS tags, COUNT(DISTINCT tag) AS len
        ORDER BY len DESC LIMIT 3
        RETURN they.username AS similar_user, tags
        """

        return graph.cypher.execute(query, username=self.username)

    def get_commonality_of_user(self, other):
        # Find how many of the logged-in user's offers the other user
        # has liked and which tags they've both blogged about.
        query = """
        MATCH (they:User {username: {they} })
        MATCH (you:User {username: {you} })
        OPTIONAL MATCH (they)-[:LIKED]->(offer:Offer)<-[:OFFERED]-(you)
        OPTIONAL MATCH (they)-[:OFFERED]->(:Offer)<-[:TAGGED]-(tag:Tag),
                       (you)-[:OFFERED]->(:Offer)<-[:TAGGED]-(tag)
        RETURN COUNT(DISTINCT offer) AS likes, COLLECT(DISTINCT tag.name) AS tags
        """

        return graph.cypher.execute(query, they=other.username, you=self.username)[0]

def get_todays_recent_offers():
    query = """
    MATCH (user:User)-[:OFFERED]->(offer:Offer)<-[:TAGGED]-(tag:Tag)
    WHERE offer.date = {today}
    RETURN user.username AS username, offer, COLLECT(tag.name) AS tags
    ORDER BY offer.timestamp DESC LIMIT 5
    """

    return graph.cypher.execute(query, today=date())

def timestamp():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()

def date():
    return datetime.now().strftime('%F')
