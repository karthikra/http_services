import requests


def get_repo_info():
    user = input("What is the username? ")
    repo = input("What is the repo name? ")

    return user, repo


def main():
    # mikeckennedy
    # consuming_services_python_demos

    user, repo = get_repo_info()
    url = f"https://api.github.com/repos/{user}/{repo}"
    resp = requests.get(url)

    if resp.status_code != 200:
        print(f'Could not access the repo {resp.status_code}')
        return
    repo_data = resp.json()
    clone = repo_data.get("clone_url", "ERROR:COULD NOT GET THE URL")
    print(f'To clone the repo {repo} use the following command')
    print(f'git clone {clone}')
    print("*********")


if __name__ == '__main__':
    main()
