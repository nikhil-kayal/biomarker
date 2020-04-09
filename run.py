import pymongo
import pandas as pd
from nltk.corpus import stopwords
from configparser import ConfigParser

from src.identify_biomarkers import biomarker_object


def main():
    client = pymongo.MongoClient(url)
    db = client[db_name]
    db.authenticate(username, password, source='admin', mechanism='SCRAM-SHA-1')
    ctgov_collection = db[collection_name]

    ctgov = pd.DataFrame(ctgov_collection.find({}, {lookup_markers_in: 1}))
    ctgov = ctgov.where(pd.notnull(ctgov), None)

    stopwords_list = stopwords.words('english')
    for i, r in enumerate(ctgov[lookup_markers_in]):
        init_list = []
        for j in r:
            init_list.append(' '.join(w for w in j.split() if w not in stopwords_list))
        ctgov[lookup_markers_in].at[i] = init_list

    ctgov[lookup_markers_in + 'biomarkers'] = pd.Series(ctgov[lookup_markers_in].map(lambda x: biomarker_object(x)))


if __name__ == "__main__":
    config = ConfigParser()
    config.read("src/config.ini")
    url = config.get("mongo", "db_name")
    db_name = config.get("mongo", "db_name")
    collection_name = config.get("mongo", "collection_name")
    username = config.get("mongo", "username")
    password = config.get("mongo", "password")
    lookup_markers_in = config.get("default", "lookup")
    main()

