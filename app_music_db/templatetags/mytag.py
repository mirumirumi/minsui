from django import template

register = template.Library()

@register.simple_tag #デコレーターという、便利機能の登録
def url_replace(request, field, value):
    # GETパラメータの一部を置き換える
    url_dict = request.GET.copy()
    url_dict[field] = value
    return url_dict.urlencode()


# このタグの使い方

# {% load mytag %}　して、

# href="?{% url_replace request 'page' page_obj.previous_page_number %}"
# など
# ※requestはテンプレートに暗黙で渡されるらしい

# テンプレートなどファイルを追加した場合、runserverとかはもう一回やり直すといい



