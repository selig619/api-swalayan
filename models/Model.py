from configs.firebase import get_database

class Model():
    @classmethod
    def get_all(cls, limit = None, asc = False):
        db = get_database()
        data = db.collection(cls).get()
        # panggil convert to dict mbe ksh limit
        if limit is None:
            return data.to_dict()
            return db.child(cls.__name__.lower() + 's').get(token).val()
        if asc:
            return db.child(cls.__name__.lower() + 's').order_by_key().limit_to_first(limit).get(token).val()
        return db.child(cls.__name__.lower() + 's').order_by_key().limit_to_last(limit).get(token).val()
    
    
    def convert_to_dict(data):
        arr = []
        for d in data:
            arr.append({
                'key':d.id
            })
        return arr