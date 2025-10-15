import pickle

data = {"id": 1, "name": "Christos", "scores": [95, 88, 92]}

# Serialize
with open("data.pkl", "wb") as f:
    pickle.dump(data, f)

# Deserialize
with open("data.pkl", "rb") as f:
    loaded = pickle.load(f)

print(loaded)  # {'id': 1, 'name': 'Christos', 'scores': [95, 88, 92]}
