import requests
from bs4 import BeautifulSoup


def main():
    url = "https://whatmyuseragent.com"
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Version/17.0 Safari/605.1.15 '

        # 'User-Agent': 'Karthik Ramesh 1879 '
    }
    resp = requests.get(url,headers=header)
    if resp.status_code != 200:
        print(f'Could not get to the url {resp.status_code} with message {resp.text}')
        return
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')
    user_agent = soup.find('h5').text
    print(user_agent)


if __name__ == '__main__':
    main()
