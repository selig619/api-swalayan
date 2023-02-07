from configs.firebase import get_database

class Model():
    
    @classmethod
    def get_all(cls):
        db = get_database()
        data = db.collection(cls.__name__.lower()).get()
        d_dict = Model.convert_to_dict(data)
        return d_dict

    @classmethod
    def get_by_id(cls, id):
        db = get_database()
        data = db.collection(cls.__name__.lower()).document(id)
        return data.get().to_dict()

    @classmethod
    def insert(cls, data ,token):
        db = get_database()
        return db.child(cls.__name__.lower() + 's').push(data, token)
    
    @classmethod
    def update(cls, id, data ,token):
        db = get_database()
        return db.child(cls.__name__.lower() + 's').child(id).update(data, token)

    @classmethod
    def delete(cls, id ,token):
        db = get_database()
        return db.child(cls.__name__.lower() + 's').child(id).remove(token)
    
    def convert_to_dict(data):
        arr = []
        for d in data:
            arr.append({
                'key':d.id,
                'data' : d.to_dict()
            })
        return arr