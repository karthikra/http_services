import requests
from xml.etree import ElementTree
import collections
import os

Course = collections.namedtuple('Course', 'title room building')


def main():
    folder = os.path.dirname(__file__)
    xml_file = os.path.join(folder, 'xml_data', 'reed.xml')

    with open(xml_file) as fin:
        xml__text = fin.read()

    dom = ElementTree.fromstring(xml__text)

    course_node = dom.findall('course')

    courses = [Course(c.find('title').text,
                      c.find('place/room').text,
                      c.find('place/building').text) for c in course_node]

    building = input('What building are you in ? ')
    room = input('What room are you in ? ')

    room_course = [c.title for c in courses if c.building == building and c.room == room]

    for c in room_course:
        print(f'* {c}')


if __name__ == '__main__':
    main()
