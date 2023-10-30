import requests
import json

import datetime
import collections

Post = collections.namedtuple('Post', 'id title content published view_count')

base_url = 'https://consumerservicesapi.talkpython.fm/'
auth_url = base_url + 'api/restricted/blog/'

username = 'kennedy'
password = 'super_lockdown'


def get_posts():
    # url = base_url + 'api/blog'
    # this url to be used for authenticated service
    url = auth_url
    headers = {'Accept': 'application/json'}
    resp = requests.get(url, headers=headers, auth=(username, password))
    if resp.status_code != 200:
        print(f'Could not get the posts {resp.status_code} with {resp.text}')
        return []
    return [
        Post(**post)
        for post in resp.json()
    ]


def show_posts(posts):
    print('----------BLOG POSTS------------')
    if not posts:
        print('No posts to show')
        return None
    for num, post in enumerate(posts):
        print(f'{num + 1}. {post.id} {[post.view_count]}: {post.title}')


def add_post():
    now = datetime.datetime.now()
    published_text = f'{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)}'

    title = input('title: ')
    content = input('content: ')
    view_count = input('view count: ')
    published = published_text

    post_data = dict(title=title, content=content, view_count=view_count, published=published)
    url = auth_url
    headers = {'content-type': 'application/json'}

    resp = requests.post(url, json=post_data, headers=headers,auth=(username,password))

    if resp.status_code != 201:
        print(f'Error creating post: {resp.status_code}, {resp.text}')

    post = resp.json()
    print('Created this...')
    print(post)


def update_post():
    print(f'To update a post choose the number from the list below: ')
    posts = get_posts()
    show_posts(posts)
    print()

    post = posts[int(input('number: ')) - 1]

    title = input('title: [' + post.title + ']')
    title = title if title else post.title

    content = input('content: [' + post.content + ']')
    content = content if content else post.content

    view_count = input('view_count: [' + str(post.view_count) + ']')
    view_count = int(view_count if view_count else post.view_count)

    post_data = dict(title=title, content=content, view_count=view_count, published=post.published)
    url = auth_url + post.id
    resp = requests.put(url, json=post_data,auth=(username,password))

    if resp.status_code != 204:
        print(f"Error updating the post {resp.status_code},{resp.text}")
        return None
    print(f'Successfully Update the post {post.title} ')


def delete_post():
    print(f'To delete a post choose the number from the list below: ')
    posts = get_posts()
    show_posts(posts)
    print()

    post = posts[int(input('number of post to delete: ')) - 1]

    print(f"Deleting {post.title}")

    url = auth_url + post.id
    resp = requests.delete(url,auth=(username,password))

    if resp.status_code != 202:
        print(f"Error Deleting the post {resp.status_code}, {resp.text}")
        return
    print(f'Deleted the post {post.title}')


def main():
    while True:
        action = input('What do you want to do with this blog post ? [l]ist, [a]dd , [u]pdate, [d]elete, e[x]it: ')
        if action == 'x':
            print("Exiting...")
            break
        if action == 'l':
            posts = get_posts()
            show_posts(posts)
        if action == 'a':
            add_post()
        if action == 'u':
            update_post()
        if action == 'd':
            delete_post()


if __name__ == '__main__':
    main()
