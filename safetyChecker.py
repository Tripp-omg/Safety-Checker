import requests
import re
import json
import os

def get_user_id(username):
    """Fetch the Roblox user ID for a given username using the current API."""
    url = "https://users.roblox.com/v1/usernames/users"
    payload = {"usernames": [username]}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data['data']:
            return data['data'][0]['id']
    return None

def get_friends(user_id):
    """Fetch the friends list of a Roblox user by user ID using the current API."""
    url = f"https://friends.roblox.com/v1/users/{user_id}/friends"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return [friend['id'] for friend in data.get('data', [])]
    return []

def extract_user_ids(file_path):
    """Extract user IDs from URLs in the given file."""
    ids = set()
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'users/(\d+)', line)
            if match:
                ids.add(match.group(1))
    return ids

def check_for_matches(username):
    user_id = get_user_id(username)
    if user_id is None:
        print("Username not found.")
        return

    print(f"Checking friends for user: {username} (ID: {user_id})")
    
    friends = get_friends(user_id)
    
    if not friends:
        print("No friends found for this user.")
        return

    # Use absolute paths for the files
    base_directory = os.path.dirname(os.path.abspath(__file__))
    unsafe_profiles_file = os.path.join(base_directory, '404accounts.txt')
    unsafe_friends_file = os.path.join(base_directory, 'friends.txt')

    unsafe_profiles_ids = extract_user_ids(unsafe_profiles_file)
    unsafe_friends_ids = extract_user_ids(unsafe_friends_file)

    # Check for matches
    profile_matches = [f"https://www.roblox.com/users/{friend_id}/profile" for friend_id in friends if str(friend_id) in unsafe_profiles_ids]
    friend_matches = [f"https://www.roblox.com/users/{friend_id}/profile" for friend_id in friends if str(friend_id) in unsafe_friends_ids]

    if profile_matches:
        print("Known ERP account(s) found in friends:")
        for match in profile_matches:
            print(match)
    
    if friend_matches:
        print("Friends of known ERP account(s) found in friends:")
        for match in friend_matches:
            print(match)

    if not profile_matches and not friend_matches:
        print("No matches found.")

if __name__ == "__main__":
    username = input("Enter a Roblox username: ")
    check_for_matches(username)
