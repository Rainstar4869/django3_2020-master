from django import template

register = template.Library()  # Djangoのテンプレートタグライブラリ


# カスタムフィルタとして登録する
@register.filter
def multiply5(value1, value2):
    return value1 * value2


@register.filter
def shorten_id(value):
    return "..."+str(value)[-6:-1]


# カスタムタグとして登録する
@register.simple_tag
def multiply6(value1, value2):
    return value1 * value2
