import requests
from dotenv import load_dotenv
import os


def fetch_github_docs(repo_owner, repo_name):
    load_dotenv()
    base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"
    github_token = os.environ.get("GITHUB_TOKEN")
    headers = {"Authorization": f"token {github_token}"}

    def retrieve_files(url):
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch: {url}")
            return []
        items = response.json()
        docs = []

        for item in items:
            # if item["type"] == "dir":
            #     docs.extend(retrieve_files(item["url"]))
            # elif item["type"] == "file" and item["name"].endswith(".md") and item["name"] == "README.md":
            #     file_content = requests.get(item["download_url"], headers=headers).text
            #     docs.append({"path": item["path"], "content": file_content})

            if item["type"] == "dir":
                docs.extend(retrieve_files(item["url"]))
            elif item["type"] == "file" and item["name"].endswith(".md") and item["name"] == "README.md":
                file_content = requests.get(item["download_url"], headers=headers).text
                url = f"https://github.com/{repo_owner}/{repo_name}/tree/master/{item['path']}"
                docs.append({"metadata": {"url": url}, "document": file_content})

        return docs

    return retrieve_files(base_url)


# repo_owner = "V4Fire"
# repo_name = "Client" # "Core"
# docs = fetch_github_docs(repo_owner, repo_name)

# # print(docs[:5])
# for doc in docs[:5]:
#     print(doc['content'])
