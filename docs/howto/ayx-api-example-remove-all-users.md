**Overview**

This guide is for the use case of any workspace admin who needs to clear out a workspace except themselves. This is especially useful for universities using Alteryx Analytics Cloud when they have new classes of students in their workspace each semester.

**Guide**
---------

This guide assumes limited knowledge of Python, but some research and debugging may be required by the user to set up Python and Pip Steps:

1. Make sure you have Python installed by running both of the following in your terminal (whichever works, you'll use the same prefix for later commands):
   1. `python --version`
   2. `python3 --version`

2. Install the library to make API calls in Python "Requests" using one of the following commands depending on whether you have "python" or "python3" installed:
   1. `pip install requests`
   2. `python -m pip install requests`
   3. `python3 -m pip install requests`
   4. If none of these work, you may need to install pip

3. Edit "removeAllUsersExceptExcluded.py" to match your workspace and needs
   1. Edit the `bearer_token` variable to be your static bearer token from the "user preferences" then Static API access tokens pages (link). These tokens will be deprecated soon so eventually this script will need to be updated to use the oauth 2.0 tokens
   2. Edit the `excluded_emails` array to include all the emails of users you don't want to be removed. If it's just you, make sure there are no commas and just your email in the brackets: `[ ]`.
   3. Save your changes

4. Run the python script using one of the following commands depending on whether you have "Python" or "Python3" installed
   1. `python removeAllUsersExceptExcluded.py`
   2. `python3 removeAllUsersExceptExcluded.py`

**The Script**
---------

```python
import requests

# Variables to adjust based on the environment
base_url = "us1.alteryxcloud.com"
bearer_token = "YOUR_STATIC_BEARER_TOKEN_HERE"
excluded_emails = ["user1_to_exclude@example.com", "user2_to_exclude@example.com"]  # Comma-seperated list of emails of users who should not be removed

# Headers
headers = {
    "Authorization": f"Bearer {bearer_token}",
    "Accept": "application/json"
}

# Function to make a GET request
def make_get_request(endpoint):
    # Complete URL
    url = base_url + endpoint

    # Making the GET request
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Successful request, return JSON response
        return response.json()
    else:
        # Request failed, print error and return None
        print(f"Failed to get data from {endpoint}, status code: {response.status_code}")
        print(response.text)
        return None

# Function to make a DELETE request for removing a person
def remove_person(workspace_id, person_id):
    # Complete URL for removing a person
    url = f"{base_url}/v4/workspaces/{workspace_id}/people/{person_id}"

    # Making the DELETE request
    response = requests.delete(url, headers=headers)

    if response.status_code in [200, 204]:
        # Successful removal
        print(f"Successfully removed person with ID: {person_id}")
    else:
        # Request failed
        print(f"Failed to remove person with ID: {person_id}, status code: {response.status_code}")
        print(response.text)

# Get people data
people_response = make_get_request("/v4/people")

# Get current workspace ID
workspace_data = make_get_request("/v4/workspaces/current")
if workspace_data:
    workspace_id = workspace_data.get("id")
    print("Current Workspace ID:", workspace_id)

    # Ensure we have the people data and the workspace ID
    if people_response and 'data' in people_response and workspace_id:
        # Filter out the users with the excluded emails
        filtered_people = [person for person in people_response['data'] if person.get("email") not in excluded_emails]

        # Loop through filtered people and remove each
        for person in filtered_people:
            remove_person(workspace_id, person.get("id"))
```