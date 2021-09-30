"""
The script is not stable for several uses, so it's highly recommended to use once for populating an empty DB.
"""

import os
import random

import django
import lorem
from nickname_generator import generate


def create_users(max_users=5):
    print('> Creating users...')
    users_in_db = User.objects.count()
    print(f'-- Database has {users_in_db} existing users')

    if users_in_db >= max_users:
        return print(f'-- [SKIP] Number of existing users is equal/higher than {max_users}')

    for num in range(max_users - users_in_db):
        user_nickname = generate()
        user_email = f'{user_nickname.lower()}@doe.com'
        user_password = '123'

        User.objects.create_user(
            username=user_nickname,
            email=user_email,
            password=user_password,
        )
        print(f'-- {num + 1}/{max_users}: User "{user_nickname}" has been created')


def create_boards():
    print('> Creating boards...')
    boards_examples = {
        'Django': 'Discuss everything about Django!',
        'Python': 'Here you can discuss about Python.',
        'Computers': 'Are you fascinated by Computer Science?',
        'Random': 'About everything you want.',
    }
    for board_name, board_description in boards_examples.items():
        if not Board.objects.filter(name=board_name).exists():
            board = Board(name=board_name, description=board_description)
            board.save()
            print(f'-- Board "{board_name}" has been created')
        else:
            print(f'-- [SKIP] Board "{board_name}" already exists')


def create_topics():
    print('> Creating topics...')

    all_boards = Board.objects.all()
    all_users = User.objects.all()

    topics_amount = {
        'Django': 4,
        'Python': 5,
        'Computers': 3,
        'Random': 4,
    }

    for board in all_boards:
        created_posts = 0
        if board.topics.count() < topics_amount[board.name]:
            topics_diff = topics_amount[board.name] - board.topics.count()
        else:
            print(f'-- [SKIP] Board "{board.name}" has enough amount of topics')
            continue
        for topic_num in range(topics_diff):
            t_subject = lorem.sentence()
            t_starter = random.choice(all_users)
            t_views = random.randint(0, 500)
            topic = Topic.objects.create(
                subject=t_subject,
                board=board,
                starter=t_starter,
                views=t_views
            )
            if board.name == 'Django' and topic_num == topics_diff - 1:
                posts_number = 200
                print(f'-- Creating {posts_number}+ posts, please wait...')
                created_posts += create_posts(topic, all_users, t_starter, posts_number)
            else:
                created_posts += create_posts(topic, all_users, t_starter)
        print(f'-- {topics_diff} topic(s) and {created_posts} post(s) have been created within "{board.name}" board')


def create_posts(topic, all_users, t_starter, posts_number=None):
    if posts_number:
        posts_amount = posts_number
    else:
        posts_diff = 14 - topic.posts.count()
        posts_amount = random.randint(1, posts_diff)

    t_starter_post_created = False

    for post_num in range(posts_amount):
        p_message = lorem.paragraph()
        p_topic = topic
        if not t_starter_post_created:
            p_created_by = t_starter
            t_starter_post_created = True
        else:
            p_created_by = random.choice(all_users)
        Post.objects.create(
            message=p_message,
            topic=p_topic,
            created_by=p_created_by,
        )

    return posts_amount


def create_superuser():
    if User.objects.filter(is_superuser=True):
        return print('> Superuser already exists')
    admin_username = 'admin'
    admin_password = 'admin'
    User.objects.create_superuser(username=admin_username, password=admin_password)
    print(f'> Superuser with credentials \'{admin_username}: {admin_password}\' has been created '
          f'and can be accessed via http://127.0.0.1:8000/admin/')
    print(f'> Every automatically generated user has credentials: \'<nickname>: 123\'')


def populate():
    create_users(5)
    create_boards()
    create_topics()
    create_superuser()


if __name__ == '__main__':
    print("[START] Starting ForumDjango population script...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ForumDjango.settings')
    django.setup()
    from boards.models import Board, User, Topic, Post

    populate()
    print("[END] Population script finished successfully")
