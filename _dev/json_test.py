import json

# Sample dictionary
data = {'name': 'John', 'age': 30, 'city': 'New York'}

# Save to a JSON file
with open('data.json', 'w') as file:
    json.dump(data, file)

# Load from the JSON file
with open('data.json', 'r') as file:
    loaded_data = json.load(file)