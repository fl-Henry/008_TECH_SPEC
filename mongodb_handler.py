import pymongo
import pandas as pd


class MongodbHandler:

    def __init__(self, host=None, db_name="mongo_db", collection_name="mongo_collection"):

        if host is None:
            host = "mongodb://localhost:27017/"

        self.db_client = pymongo.MongoClient(host)
        self.db = self.db_client[db_name]
        self.collection = self.db[collection_name]

    @staticmethod
    def collection_data_to_json(collection):
        json_to_return = []
        for record in collection:
            json_to_return.append({key: value for key, value in zip([*record.keys()][1:], [*record.values()][1:])})

    def delete_duplicates(self, fields):
        """

        :param fields: list of fields   | ["name", "count", "sum", "article"]
        :return:
        """
        collection_json = [record for record in self.collection.find()]
        collection_df = pd.DataFrame(collection_json)
        duplicated_df = collection_df[collection_df.duplicated(subset=fields)]
        for index, row in duplicated_df.iterrows():
            self.collection.delete_one({"_id": row["_id"]})
