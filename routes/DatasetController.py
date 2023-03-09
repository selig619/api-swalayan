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
    def insertArm():
        errors = insertDsSchema().validate(request.json)
        if errors:
            return errors, 400

        # insert datasets
    # try:
        db = get_database()
        #insert datasets baru =============================================
        # add_time, ds_ref = db.collection('dataset').add(
        #     {
        #         "ds_name": request.json["name"],
        #         # "user_id": request.user['uid'],
        #         "user_id": 'seseorang',
        #         "created_at": datetime.now(timezone.utc),
        #         "updated_at": datetime.now(timezone.utc)
        #     }
        # )

        # #insert transaction baru ========================================
        # insertTrans(db)
        # insertTransBaru(db)

        # cobaGetTransItem(db)
            
        #cari transaction yg dari dataset tadi
        # docs = db.collection('transaction').where('dataset_id', '==', ds_ref.id).stream()

            
        # ctr=0  
        # for i in tempItems:
        #     for j in i:
        #         if kata in j:
        #             ctr+=1
        # print(ctr)

        # for i in tempItems:
        #     if 'Bawang' in i:
        #         ctr+=1
        # print(ctr)

        # ===============================

        # GET DATA MODEL LAMA SG TIAP DOCUMENT / 1 DATA ITU 1 TRANS
        # docs = db.collection('transaction').where('dataset_id', '==', 'hxVtUCXV3IU0spqYgnqX').stream()
        # temp=[]
        # for doc in docs:
        #     # temp.append(doc.get("items"))
        #     print(doc.get("items"))

        # #dibikin kyk dataset bwt diproses generate freq_itemsets
        # temp=[]
        # for doc in docs:
        #     temp.append(doc.get("items"))
        #     # URUS INI======================
        #     # Jadinya
        #     # [
        #     #     ['Milk', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
        #     #     ['Dill', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt']
        #     # ]
        # print(temp)
        # if temp == []:
        #     return {'message': 'No dataset found'}, 404

        # #GENERATE FREQUENT ITEMSET
        # genFIset(db)
        # rencana save e bentuk 1 data kabeh array
        # bingung data di firestore dbkin satu2 kek di db?? TTEP ada items=[aa,bb]

        #GENERATE RULES
        # genRules(db)
        
        # return {'message': 'Insert Success'}
        return tempItems
    # except:
    #     return {'message': 'Insert Failed'}

    def insertTrans(db):
        for x in range(len(request.json['transactions'])):
            trans_ref = db.collection('transaction').add(
                {
                    "dataset_id": ds_ref.id,
                    "trans_id": request.json["transactions"][x]['trans_id'],
                    "items" : request.json["transactions"][x]['items']
                }
            )
        print('msk funccc')


    def insertTransBaru(db):
        print('msk insert trans baru')
        add_time, trans_ref = db.collection('transaction').add(
            {
                "dataset_id": 'hXNQ96ZpIzoJhE89asD7',
                "data" : request.json["transactions"]
            }
        )
        
    def cobaGetTransItem(db):
        # print(f"msk cobagettransitem")
        docs = db.collection("transaction").get()
        # where("data", "in", ["Susu"])

        # docs = docs
        # print(docs.get('items'))
        
        for doc in docs:
            print(f"{doc.get('data')}")
            # temp.append(doc.to_dict())

    def genFIset(db):
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

    def genRules(db):
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
            
#==================================================================================

    @app.route(USER_BASE_URL, methods = ['GET'])
    # @check_token
    def getDsByUser():
        db = get_database()
        docs = db.collection('dataset').where('user_id', '==', request.user['uid']).stream()
        return docs
    
    @app.route(USER_BASE_URL + '/<id>', methods = ['DELETE'])
    # @check_token
    def delDs(id):
        db = get_database()
        try:
            doc_ref = db.collection("dataset").document(id)
            doc_ref.delete()

            return {'message': 'Delete Success'}, 200
        except:
            return {'message': 'Delete Failed'}, 400
        
    @app.route(USER_BASE_URL + '/<id>/transactions', methods = ['GET'])
    # @check_token
    def getTransByDs(id):
        db = get_database()
        docs = db.collection('transaction').where('dataset_id', '==', id).stream()
        return docs
    
        
    @app.route(USER_BASE_URL + '/<id>/frequentItems', methods = ['GET'])
    # @check_token
    def getFIsetByDs(id):
        db = get_database()

        # BISA DPT ARR ITEMS TOK=========
        docs = db.collection('transaction').where('dataset_id', '==', 'hXNQ96ZpIzoJhE89asD7').stream()
        # # print(docs)
        # temp=[]
        for doc in docs:
            # print(f"{doc.get('data')}")
            temp = (doc.get('data'))
        # print(temp)

        #NYOBA PAKE ITERATE LGSG KE items
        ctr=0
        tempItems=[]
        for i in temp:
            print(i) 
            #{'items': ['Susu', 'Bawang', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'], 'trans_id': '202101040001'}
            # print(i['items']) 
            # ['Susu', 'Bawang', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt']
            for j in i['items']: #Susu Bawang Nutmeg Kidney Beans
                # print(j)
                # tempItems.append(t['items'])
                if 'Susu' in j:
                    tempItems.append(i)
                
        # print(ctr)


        # docs = db.collection('freqItemset').where('dataset_id', '==', id).stream()
        return tempItems
    #bandingno data dimasukno kabeh / 1 ae trs di dlm dbkin arr
    #masukno func