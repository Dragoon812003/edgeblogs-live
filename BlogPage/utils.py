from pstats import SortKey
import string
import random
import re

from django.utils.text import slugify 
from blog.grammer import words

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

def get_category(post):
    post_text = remove_html_tags(post.body)
    post_text = remove_punctuation(post_text)
    words = post_text.split()
    words_to_get = []

    for word in words:
    
        if word.lower() not in words and word.lower() not in words_to_get:
            words_to_get.append({
                'word': word.lower(),
                'count': 0,
            })

    for word in words:
        for word_to_get in words_to_get:
            if word.lower() == word_to_get['word']:
                word_to_get['count'] += 1
        
    newlist = sorted(words_to_get, key=lambda d: d['count'], reverse=True)
    categories = []
    for i in newlist:
        if i not in categories:
            categories.append(i)    
    if len(words_to_get) > int(len(words)/40):
        return categories[:int(len(words)/40)]
    return categories

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


    