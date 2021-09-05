from django import forms
from django.urls import reverse_lazy
from .models import *
from .widgets import SuggestWidget
import re

class SongCreateForm(forms.ModelForm):
    #nameをrequired = Falseにするのもforms.py側で下記のようにできるらしい
    # def __init__(self, *args, **kwd):
    #     super(UserForm, self).__init__(*args, **kwd)
    #     self.fields["name"].required = False
    class Meta:
        model = Song
        fields = "__all__"
        widgets = {
            'title': SuggestWidget(attrs={
                'data-url': reverse_lazy('app_music_db:api_songs_get'),
                'class': 'form-control',
            }),
            'composer': SuggestWidget(attrs={
                'data-url': reverse_lazy('app_music_db:api_composers_get'),
                'class': 'form-control',
            }),
            'arranger': SuggestWidget(attrs={
                'data-url': reverse_lazy('app_music_db:api_arrangers_get'),
                'class': 'form-control',
            }),
            'artist': SuggestWidget(attrs={
                'data-url': reverse_lazy('app_music_db:api_artists_get'),
                'class': 'form-control',
            }),
            'cd': SuggestWidget(attrs={
                'class': 'form-control',
                'id': 'cd-input',  #idは「id_フィールド名」で自動で振られる、今回は直さない（というかsuggest.htmlでid改めて全て振られていて、たまたま書式がcd-inputで同じだったので問題が出ていない）
                "placeholder": "CD名を入力",
                'data-url': reverse_lazy('app_music_db:api_cds_get'),
            }),
            'cd_link': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'cdYear': forms.TextInput(attrs={
                'class': 'form-control',
                "placeholder": "年度（西暦4桁）",
            }),
            'cdVol': forms.TextInput(attrs={
                'class': 'form-control',
                "placeholder": "該当曲の収録Vol.番号（1~17）",
            }),
        }

    def clean_cd_link(self):
        # form.save()をしていないのでこの関数はアルバム一括追加だと通らない。
        # cd_link = self.urlNormalization(self.cleaned_data['cd_link'])
        return self.cleaned_data['cd_link'] + "?tag=wo-music-22"


# ページリダイレクト後のフォームへのあたいセットもjsで書いてしまった今、formを使うメリットがなにもない（現状知る限りでは）ので、利用をやめる。
# class SearchForm(forms.Form): # {{ form }}で表示するとGETパラメータがあるときはページ読み後にちゃんとその表示がセットされる。手動HTMLだと毎回フォームがリセットされてしまっていた。
#     c = forms.ModelChoiceField(
#         queryset=CdType.objects,
#         label="CDタイプ",
#         required=False,
#         widget=forms.Select(attrs={
#             'class': 'form-control',
#         }),
#     )
#     n = forms.Select(
#         label="最近追加されたものだけ表示(30日以内)",
#         required=False,
#         widget=forms.CheckboxInput(attrs={
#             "class": "form-check form-check-inline",
#         }),
#     )


class CsvImportForm(forms.Form):
    file = forms.FileField(
        label='CSVファイル',
        help_text='※[.csv]のみ',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file',
        }),
    )


class CommentPostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "text", "song",)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
            }),
        }



# forms.Formだとform.save()などが使えない。なんか調べてもイマイチヒットせず、DBへの保存を伴う場合はModelFormを使うのが一般的っぽい？→ただしModelFormをベースに各フォームのカスタマイズをするのはかなりコードが増えそうだった
# class SongCreateForm(forms.Form):
#     title = forms.CharField()  #バリエーションがありすぎるので手動で我慢
#     composer = forms.CharField()  #入力中に類似を出したい
#     arranger = forms.CharField(required=False)  #入力中に類似を出したい
#     artist = forms.CharField()  #同じく我慢
#     cd = forms.CharField()
#     cd_link = forms.CharField()





