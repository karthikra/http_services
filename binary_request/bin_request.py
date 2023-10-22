import shutil

import requests
from xml.etree import ElementTree
import os


def get_episode_files(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        return None

    xml_text = resp.text
    dom = ElementTree.fromstring(xml_text)

    return [
        enclosure_node.attrib['url'] for enclosure_node in dom.findall('channel/item/enclosure')
    ]


def download_file(file, dest_folder):
    resp = requests.get(file, stream=True)
    resp.decode_content = True

    base_file = os.path.basename(file)
    dest_file = os.path.join(dest_folder, base_file)
    if resp.status_code != 200:
        print("Could not get the requested file")
        return None
    with open(dest_file, 'wb') as fout:
        shutil.copyfileobj(resp.raw, fout)



def main():
    url = 'https://talkpython.com/rss'
    mp3_files = get_episode_files(url)

    for file in mp3_files[:3]:
        base_folder = os.path.dirname(__file__)
        dest_folder = os.path.join(base_folder, 'bin_data')
        download_file(file, dest_folder)


if __name__ == '__main__':
    main()
