from configs.firebase import get_database

class Model():
    
    @classmethod
    def get_all(cls):
        db = get_database()
        data = db.collection(cls.__name__.lower()).stream()
        # print(data)
        temp_data=[]
        for doc in data:
            # print(f'{doc.to_dict()}')
            temp_data.append(doc.to_dict())
        
        return temp_data

    @classmethod
    def get_by_id(cls, id):
        db = get_database()
        data = db.collection(cls.__name__.lower()).document(id)
        if data.get().to_dict() == None:
            return {'message': 'Data not found'}, 404
        return data.get().to_dict()

    @classmethod
    def insert(cls, data):
        db = get_database()
        return db.collection(cls.__name__.lower()).add(data)
    
    @classmethod
    def update(cls, id, data):
        db = get_database()
        checkId = db.collection(cls.__name__.lower()).document(id)
        if checkId.get().to_dict() == None:
            return {'message': 'Data not found'}, 404
        
        db.collection(cls.__name__.lower()).document(id).update(data)
        return {'message': 'Success Update User'}

    @classmethod
    def delete(cls, id):
        db = get_database()
        checkId = db.collection(cls.__name__.lower()).document(id)
        if checkId.get().to_dict() == None:
            return {'message': 'Data not found'}, 404

        db.collection(cls.__name__.lower()).document(id).delete()
        return {'message': 'Success Delete User'}



    def convert_to_dict(data):
        arr = []
        for d in data:
            arr.append({
                'key':d.id,
                'data' : d.to_dict()
            })
        return arr