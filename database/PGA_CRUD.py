from pymongo import MongoClient

class PGA_CRUD:
    def __init__(self):
        self.client = MongoClient('localhost',27017)
        self.db = self.client.PGA

    def create(self, collection, document):
        insertID = []
        if(len(document)>1):
            insertID = self.db[collection].insert_many(document)
        else:
            insertID = self.db[collection].insert_one(document)
        return insertID

    def read(self, collection, query, projection):
        result = self.db[collection].find(query, projection)
        return result

    def update(self, collection, item, document):
        updated = self.db[collection].update(item,document,upsert = True)
        return updated

    def delete(self, collection, options):
        deleted = self.db[collection].delete_many(options)
        return deleted

    def aggregate(self, collection, query):
        # EXAMPLE TO QUERY SUBDOCUMENT
        # results = self.database.aggregate('tournaments', [{'$unwind': '$players'},{'$match':{'players.position':'CUT'}},{'$project': {'_id':0, 'players.name':1}}])
        result = self.db[collection].aggregate(query)
        return result



