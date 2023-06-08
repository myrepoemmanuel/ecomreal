from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
    print(value, "abssplit")
    return str(value).split(key)[0]

