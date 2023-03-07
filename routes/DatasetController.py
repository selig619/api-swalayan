from models.Dataset import Dataset
from configs.firebase import get_auth, get_database
from utils.middleware import check_token


from firebase_admin import firestore
from flask import request
from datetime import datetime, timezone, timezone
from marshmallow import Schema, fields, ValidationError, validate
from marshmallow.validate import Length, Range


USER_BASE_URL = '/datasets'

def routes_dataset(app):
    @app.route(USER_BASE_URL + '/all', methods = ['GET'])
    # @check_token
    def getAllDs():
        ds = Dataset.get_all()
        return ds

    #VALIDATION INPUT JSON
    class DsTransactiondsSchema(Schema):
        trans_id = fields.Str()
        items = fields.List(fields.Str())
        
    class insertDsSchema(Schema):
        name = fields.Str(required=True)
        method = fields.Str(required=True, validate=validate.OneOf(["apriori","fpgrowth"])) #hrs apriori/fpgrowth
        minSupp = fields.Float(required=True)
        # transactions = fields.List(fields.Dict(required=True), required=True)
        transactions = fields.List(fields.Nested(DsTransactiondsSchema))
        # a = fields.n

    @app.route(USER_BASE_URL, methods = ['POST'])
    # @check_token
    def insertDs():
        errors = insertDsSchema().validate(request.json)
        if errors:
            return errors, 400

        # insert datasets
        try:
            db = get_database()
            #insert datasets baru =============================================
            add_time, ds_ref = db.collection('dataset').add(
                {
                    "ds_name": request.json["name"],
                    # "user_id": request.user['uid'],
                    "user_id": 'seseorang',
                    "created_at": datetime.now(timezone.utc),
                    "updated_at": datetime.now(timezone.utc)
                }
            )

            # #insert transacation baru ========================================
            for x in range(len(request.json['transactions'])):
                trans_ref = db.collection('transaction').add(
                    {
                        "dataset_id": ds_ref.id,
                        "trans_id": request.json["transactions"][x]['trans_id'],
                        "items" : request.json["transactions"][x]['items']
                    }
                )
                
            #cari transaction yg dari dataset tadi
            docs = db.collection('transaction').where('dataset_id', '==', ds_ref.id).stream()

            # #dibikin kyk dataset bwt diproses generate freq_itemsets
            temp=[]
            for doc in docs:
                temp.append(doc.get("items"))
            #     # URUS INI======================
            #     # Jadinya
            #     # [
            #     #     ['Milk', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
            #     #     ['Dill', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt']
            #     # ]
            # print(temp)
            if temp == []:
                return {'message': 'No dataset found'}, 404

            # #GENERATE FREQUENT ITEMSET
            import pandas as pd
            import json
            from mlxtend.preprocessing import TransactionEncoder
            from mlxtend.frequent_patterns import apriori, fpgrowth

            te = TransactionEncoder()
            te_ary = te.fit(temp).transform(temp)
            df = pd.DataFrame(te_ary, columns=te.columns_)
            
            # frequent_itemsets=''
            minSupp = request.json["minSupp"]
            if request.json["method"] == "apriori":
                fIset_df = fpgrowth(df, min_support=minSupp, use_colnames=True)
            elif request.json["method"] == "fpgrowth":
                fIset_df = apriori(df, min_support=minSupp, use_colnames=True)

            fIset_jstring = fIset_df.to_json(orient="records")
            # print(type(fIset_jstring))
            fIset_jobj = json.loads(fIset_jstring)
            print(type(fIset_jobj))
        # UNCOMMENT SINI
        #COBA INSERT DATA kyk di docs mlxtend

            #insert table fIset =============================================
            # add_time, fIsets_ref = db.collection('freqItemset').add(
            #     {
            #         "dataset_id": 'pYpTcMY6Da5nQNOacuiK',
            #         "dataset_id": 'pYpTcMY6Da5nQNOacuiK',
            #         "data" : fIset_jobj
            #     }
            # )
            # print(fIsets_ref.id)
            # rencana save e bentuk 1 data kabeh array

            # bingung data di firestore dbkin satu2 kek di db?? TTEP ada items=[aa,bb]

            #GENERATE RULES
            from mlxtend.frequent_patterns import association_rules

            # rules_df = association_rules(fIset_df, metric="confidence", min_threshold=0.2)
            # print(rules_df.info())
            # rules_df = rules_df.drop(columns=['antecedent support','consequent support', 'leverage','conviction'])
            # print(rules_df.info())
            # print(rules_df)

            # rules_jstring = rules_df.to_json(orient="records")
            # # print(type(result))
            # rules_jobj = json.loads(rules_jstring)
            # # print(rules_jobj)
            # add_time, rules_ref = db.collection('rules').add(
            #     {
            #         "dataset_id": 'pYpTcMY6Da5nQNOacuiK',
            #         "data" : rules_jobj
            #     }
            # )
            # print(rules_ref.id)
            
            # return {'message': 'Insert Success'}
            return 'rules_ref.id'
        except:
            return {'message': 'Insert Failed'}
            