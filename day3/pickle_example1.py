import pickle

data = {"id": 1, "name": "Christos", "scores": [95, 88, 92]}

# Serialize
serialized = pickle.dumps(data)
print(serialized[:40])  # binary data preview

# Deserialize
restored = pickle.loads(serialized)
print(restored)
