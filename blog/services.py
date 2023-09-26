import random
from builtins import *

from blog.models import Blog


def get_posts():
    posts_list = list(Blog.objects.all())  # Convert queryset to a list
    if len(posts_list) >= 3:
        random_posts = random.sample(posts_list, 3)
    else:
        random_posts = posts_list

    return random_posts
