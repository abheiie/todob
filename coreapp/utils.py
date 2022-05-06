def create_new_sequential_id(collection):
    id = 1
    data_dict = collection.find_one(sort=[("id", -1)])
    if data_dict and data_dict.get("id"):
        id = data_dict.get("id") + 1
    return id



