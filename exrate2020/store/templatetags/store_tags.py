from django import template

register = template.Library()  # Djangoのテンプレートタグライブラリ


# カスタムフィルタとして登録する
@register.filter
def orderpluarl(value):
    if value == 1:
        return str(value)+" order"
    else:
        return str(value)+" orders"


# カスタムタグとして登録する
@register.simple_tag
def multiply6(value1, value2):
    return value1 * value2
