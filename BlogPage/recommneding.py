import blog
import random
from BlogPage.utils import get_category

def get_score(post, user):
    user_categories = user.account.categories_liked.all()
    post_categories = blog.models.Category.objects.filter(posts=post)

    common_categories = []
    score = 0
    multiplier = 1
    adder = 0
    for user_category in user_categories:
        user_pobalbility_num = 0
        for user_category2 in user_categories:
            if user_category.word == user_category2.word:
                user_pobalbility_num += 1
                user_probability = user_pobalbility_num / len(user_categories)
        for post_category in post_categories:
            if user_category.word == post_category.word:
                common_categories.append(user_category)
                score += post_category.probability * user_probability

    if post.author.account.subscribers.filter(id=user.id).exists():
        multiplier = 1.3
        adder = 0.1

    if user.account.history.filter(id=post.id).exists():
        multiplier = -0.5
    else:
        multiplier = 1
    
    if post.dislikes.filter(id=user.id).exists():
        multiplier = -2
        adder = -3

    score *= multiplier
    score += adder
    return score

def score(post):
    likes = post.total_likes()
    dislikes = post.total_dislikes()
    views = post.total_views()
    subscribers = post.author.account.total_subscribers()

    if dislikes == 0:
        dislikes = 1

    score = int(3 * (likes/dislikes) + 2 * (views) + 3 * (subscribers)) + random.randint(-10, 10)
    return score
