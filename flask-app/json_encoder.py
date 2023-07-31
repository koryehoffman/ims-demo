import json
from bson import ObjectId

# Custom JSON Encoder to serialize ObjectId to string
class JSONEncoder(json.JSONEncoder):
    # serialize ObjectId to string
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        # if not an ObjectId, use default serialization
        return json.JSONEncoder.default(self, o)