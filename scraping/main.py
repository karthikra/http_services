import collections
import requests
from xml.etree import ElementTree
from bs4 import BeautifulSoup
import re

Page = collections.namedtuple('Page', 'url title paragraphs')
Paragraph = collections.namedtuple('Paragraphs', 'text seconds')


def build_page_from_url(url):
    print(f'Downloading data from {url}', flush=True)
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Version/17.0 Safari/605.1.15'

        # 'User-Agent': 'Karthik Ramesh 1879 '
    }

    resp = requests.get(url, headers=header)
    html = resp.text

    soup = BeautifulSoup(html, features='lxml')

    title = soup.find('h1').get_text()
    paragraphs = [
        Paragraph(clean_line(p.get_text()), int(p['seconds']))
        for p in soup.select(".transcript-segment")]

    return Page(url, title, paragraphs)


def download_transcript_pages(txt_urls):
    pages = []

    for url in txt_urls:
        page = build_page_from_url(url)
        pages.append(page)

    return pages


def get_transcript_urls():
    sitemap_url = 'https://talkpython.fm/sitemap.xml'
    resp = requests.get(sitemap_url)
    if resp.status_code != 200:
        print(f'Could not get the data {resp.status_code} with message {resp.text}')
        return []
    xml_tree = resp.text.replace('http://www.sitemaps.org/schemas/sitemap/0.9', '')
    dom = ElementTree.fromstring(xml_tree)
    txt_urls = [n.text for n in dom.findall('url/loc') if n.text.find('/episodes/transcript') > 0]
    return txt_urls


def clean_line(line):
    # re.sub(r'(\n+)',r' ')
    line = line.replace('\n', '')
    line = line.replace('   ', '')
    line = re.sub(r'[0-9:0-9]', '', line)
    line = line.strip()
    return line


def show_pages(pages):
    for p in pages:
        print(p.title)
        print(f'* URL : {p.url}')
        print(f'* {len(p.paragraphs):,} paragraphs')
        print(f'1. {p.paragraphs[0].text}')
        print()


def main():
    txt_urls = get_transcript_urls()
    pages = download_transcript_pages(txt_urls[:1])
    show_pages(pages)


if __name__ == '__main__':
    main()
