from models.Transaction import Transaction
from configs.firebase import get_auth, get_database

from datetime import datetime, timezone
from flask import request
from marshmallow import Schema, fields, ValidationError, validate
from marshmallow.validate import Length, Range



USER_BASE_URL = '/transactions'

def routes_transaction(app):
    @app.route(USER_BASE_URL, methods = ['POST'])
    def insertTrans():
        # Dataset.insert(request.json)

        # insert datasets
        return {'message': 'Success Insert User'}
    
    @app.route(USER_BASE_URL + '/all', methods = ['GET'])
    # @check_token
    def getAllTrans():
        # trans = Transaction.get_all()
        # print(trans)
        db = get_database()
        docs = db.collection('transaction').where('dataset_id', '==', 'pYpTcMY6Da5nQNOacuiK').stream()

        # temp=[]
        # for doc in docs:
        #     for x in range(len(doc.get("items"))):
        #         temp.append({
        #             "trans_id":doc.get("trans_id"),
        #             "items":doc.get("items")[x]
        #         })
                # Jadinya
                # [
                #     {
                #         "items": "COKLAT",
                #         "trans_id": "202101020001"
                #     },
                #     {
                #         "items": "TIP EX",
                #         "trans_id": "202101020001"
                #     },
                # ]
            # print(f'{doc.id} => {doc.to_dict()} => {doc.get("items")}')
        
        temp=[]
        for doc in docs:
            temp.append(doc.get("items"))
            # Jadinya
            # [
            #     ['Milk', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
            #     ['Dill', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt']
            # ]

        import pandas as pd
        from mlxtend.preprocessing import TransactionEncoder
        from mlxtend.frequent_patterns import apriori, fpmax, fpgrowth

        te = TransactionEncoder()
        te_ary = te.fit(temp).transform(temp)
        df = pd.DataFrame(te_ary, columns=te.columns_)

        frequent_itemsets = fpgrowth(df, min_support=0.2, use_colnames=True)
        # print(frequent_itemsets)
        # print(type(frequent_itemsets)) #formatnya dataframe

        from mlxtend.frequent_patterns import association_rules
        print(association_rules(frequent_itemsets, metric="confidence", min_threshold=0.3))

        return 'frequent_itemsets' # responsenya gabisa dataframe, kyknya hrs balik ke json lg