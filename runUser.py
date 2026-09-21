import json

with open("user.json", "r") as file:
    config = json.load(file)

# If user.json is directly a dictionary with a "users" list:
users = config.get("users", config)  # Handles both dict and list structures
print(f"Loaded {len(users)} users successfully.")

for user in users[:20]:
    print(
        f"User ID: {user.get('user_id')} | Username: {user.get('username')} | Role: {user.get('role')}"
    )