from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.db.models import Q
from django.db.models import Count
from django.core.mail import send_mail
from functools import reduce
from operator import and_
import csv
import io
import re
import json
import datetime
import urllib.request, urllib.parse
from .forms import *
from .models import *

# ajaxにしたので未使用
class CommentPostView(generic.CreateView):
    model = Comment
    form_class = CommentPostForm
    # template_name = 'app_music_db/comment_form.html' なくても動いた
    # success_url = reverse_lazy('app_music_db:index') #/diary/文字列として返ってくるのでredirectとは違う  なくても動いた

    def form_valid(self, form):
        obj_comment = Comment()
        obj_comment.name = self.request.POST["name"]
        obj_comment.text = self.request.POST["text"]
        obj_comment.song = Song.objects.get(id=self.request.POST["song"])
        obj_comment.save()
        if (1): #.save()は真偽値返さない、特に失敗することもなさそうなのでこれでいく
            param = {
                "comment_post": "true",
            }
        else:
            param = {
                "comment_post": "false",
            }
        p = urllib.parse.urlencode(param)
        response = redirect('app_music_db:index')
        response['location'] += '?' + p
        return response


class IndexView(generic.ListView):
    model = Song  
    ordering = ['title']  #get_queryset内一番最初のqueryset初期化時でも、最後のreturn時にドットで付与するのでもOK
    paginate_by = 100
    
    def get_context_data(self):
        context = super().get_context_data()
        # context['search_form'] = SearchForm(self.request.GET) 
        context['comment_form'] = CommentPostForm()# もとの辞書に追加する書式
        context['song_quantity'] = Song.objects.all().count()
        context['comment_quantity'] = Comment.objects.all().count()
        return context
    
    def get_queryset(self):
        # form = SearchForm(self.request.GET)
        # form.is_valid()
        queryset = super().get_queryset()
        # is_contest = form.cleaned_data["c"]
        # add_edit = form.cleaned_data["n"]
        is_contest = self.request.GET.get("c")
        add_edit = self.request.GET.get("n")
        disp_quantity = self.request.GET.get("q")
        if (is_contest == "1"):
            queryset = queryset.filter(cd_type=1)
        elif (is_contest == "2"):
            queryset = queryset.filter(cd_type=2)            
        
        if (add_edit == "add"):
            today = datetime.datetime.now()
            days30 = datetime.timedelta(minutes=43200)
            queryset = queryset.filter(created_at__gte=today - days30)
        elif (add_edit == "edit"):
            today = datetime.datetime.now()
            days30 = datetime.timedelta(minutes=43200)
            queryset = queryset.filter(modified_at__gte=today - days30)

        if (disp_quantity == "25"):
            self.paginate_by = 25
        elif (disp_quantity == "50"):
            self.paginate_by = 50
        elif (disp_quantity == "500"):
            self.paginate_by = 500
        elif (disp_quantity == "1000"):
            self.paginate_by = 1000
        elif (disp_quantity == "all"):
            self.paginate_by = 99999

        if self.request.GET.get("s") != "":
            keyword = self.request.GET.get("s")
            if keyword:
                if (" " in keyword or "　" in keyword):
                    keyword = keyword.split()
                    for k in keyword:
                        queryset = queryset.filter(Q(title__icontains=k) | Q(composer__icontains=k) | Q(arranger__icontains=k) | Q(artist__icontains=k) | Q(cd__icontains=k))
                else:
                    queryset = queryset.filter(Q(title__icontains=keyword) | Q(composer__icontains=keyword) | Q(arranger__icontains=keyword) | Q(artist__icontains=keyword) | Q(cd__icontains=keyword))

        if ("order" in self.request.GET):
            if (self.request.GET["order"] == "comment"):
                queryset = super().get_queryset().annotate(comment_count=Count('comment'))
                return queryset.order_by('-comment_count', "title")
            elif (self.request.GET["order"] == "-comment"):
                queryset = super().get_queryset().annotate(comment_count=Count('comment'))
                return queryset.order_by('comment_count', "title")
            else:
                order_param = self.request.GET.get("order")
                return queryset.order_by(order_param, "title")
            
        return queryset
 

def add(request):
    form = SongCreateForm(request.POST or None)
    context = {
        'form': form
    }
    if request.method == 'POST' and form.is_valid():
        if (form.save()):
            param = {
                "new_add": "true",
            }
        else:
            param = {
                "new_add": "false",
            }

        p = urllib.parse.urlencode(param)
        response = redirect('app_music_db:index')
        # get_params = request.GET.urlencode() # 今のページにGETパラメータがあったら次へ渡せるのでかなり汎用的に使える、今回は今パラメータを作ったのでいらない
        response['location'] += '?' + p

        # asin
        song = Song.objects.last()
        song.asin = re.sub('.*(B[0-9A-Z]{9}).*', '\\1', song.cd_link, re.I)

        # CD Type
        if(request.POST['blnContest'] == "contest"):
            song.cd_type = CdType.objects.get(id=1)
        else:
            song.cd_type = CdType.objects.get(id=2)

        song.save()

        return response

    # ここにあったcontextは上に移動させた
    return render(request, 'app_music_db/song_add.html', context)


def add_album(request):
    form = SongCreateForm(request.POST or None)
    context = {
        'form': form
    }
    if request.method == 'POST':
        # ここのフォームの中身を取るのだけでなぜかめちゃめちゃ苦労した、しかも最終的な結論が「idとnameどっちも同じ名前で定義する必要がある」だった。謎。しかもついぞrequest.POSTとrequest.POST.getの違いは分からないまま（idとnameがあればどっちも同じ結果だった）
        if (request.POST.get("is-same-artist") == "on"):
            strArtist = str(request.POST.get("artist-input"))
        else:
            strArtist = str(request.POST.get("artist-textarea")).splitlines()
            
        strTitle = str(request.POST.get("title-textarea")).splitlines()
        strComposer = str(request.POST.get("composer-textarea")).splitlines()
        strArranger = str(request.POST.get("arranger-textarea")).split('\r\n')
    
        count = 1
        result = []
        while count <= int(request.POST["line-number"]):
            try:
                song = Song();
                song.cd = request.POST.get("cd") # ここはなぜかnameで取れた！！？？！？
                song.cd_link = request.POST.get("cd_link") + "?tag=wo-music-22"
                if (request.POST.get("is-same-artist")):
                    song.artist = strArtist
                else:
                    song.artist = strArtist[count - 1]

                song.title = strTitle[count - 1]
                song.composer = strComposer[count - 1]
                song.arranger = strArranger[count - 1]
                if(request.POST['blnContest'] == "contest"):
                    song.cd_type = CdType.objects.get(id=1)
                    song.cdYear = str(request.POST.get("cdYear"))#nameがある場合は優先?
                    song.cdVol = str(request.POST.get("cdVol"))
                else:
                    song.cdYear = CdType.objects.get(id=2)

                song.asin = re.sub('.*(B[0-9A-Z]{9}).*', '\\1', str(song.cd_link), re.I)
            except (IndexError):
                param = {
                    "new_add": "false",
                }
                p = urllib.parse.urlencode(param)
                response = redirect('app_music_db:add_album')
                response['location'] += '?' + p
                return response
            else:
                result.append(song)
                count += 1
        
        for obj in result:
            obj.save()

        param = {
            "new_add": "true",
        }
        p = urllib.parse.urlencode(param)
        response = redirect('app_music_db:index')
        response['location'] += '?' + p
        return response

    # ここにあったcontextは上に移動させた
    return render(request, 'app_music_db/song_add_album.html', context)


def edit(request, pk):
    song = get_object_or_404(Song, pk=pk)
    form = SongCreateForm(request.POST or None, instance=song)
    context = {
        'form': form,
        'song': song,
    }
    if song.arranger == "":
        context['form_arranger'] = "kara" # これはNoneを防いでる

    if request.method == 'POST' and form.is_valid():
        song.asin = re.sub('.*(B[0-9A-Z]{9}).*', '\\1', song.cd_link, re.I)
        if (form.save()):
            param = {
                "fix": "true",
            }
        else:
            param = {
                "fix": "false",
            }

        p = urllib.parse.urlencode(param)
        response = redirect('app_music_db:index')
        response['location'] += '?' + p
        return response

    # ここにあったcontextは上に移動させた
    return render(request, 'app_music_db/song_edit.html', context)


def delete(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if request.method == 'POST':
        subject = "[削除申請] pk={0} タイトル={1}".format(song.pk, song.title)
        message = "ユーザーから削除申請がリクエストされたよ。\n\n作曲者＝{0}\n演奏団体={1}\nの曲です。\n\n削除理由は\n「{2}」\nだそうです。\n\nお返事してね。".format(song.composer, song.artist, request.POST["reason"])
        from_email = 'info@milmemo.net'  # 送信者
        recipient_list = ["info@milmemo.net"]  # 宛先リスト
        
        if (send_mail(subject, message, from_email, recipient_list)):
            param = {
                "delete_req": "true",
            }
        else:
            param = {
                "delete_req": "false",
            }

        p = urllib.parse.urlencode(param)
        response = redirect('app_music_db:index')
        response['location'] += '?' + p
        return response

    context = {
        'song': song,
    }
    return render(request, 'app_music_db/song_confirm_delete.html', context)


def about(request):
    return render(request, 'app_music_db/about.html')


def contact(request):
    if request.method == 'POST':
        subject = "[みんすい - お問い合わせ] {0}".format(request.POST["subject"])
        message = "みんすいにお問い合わせです。\n\n送信者={0}\nメールアドレス={1}\n件名=「{2}」\n内容=\n{3}\n\nだそうです。お返事してね".format(request.POST["name"], request.POST["mail"], request.POST["subject"], request.POST["content"])
        from_email = 'info@milmemo.net'
        recipient_list = ["info@milmemo.net"]
        
        if (send_mail(subject, message, from_email, recipient_list)):
            param = {
                "inquiry_submit": "true",
            }
        else:
            param = {
                "inquiry_submit": "false",
            }

        p = urllib.parse.urlencode(param)
        response = redirect('app_music_db:index')
        response['location'] += '?' + p
        return response

    return render(request, 'app_music_db/contact.html')


def privacy_policy(request):
    return render(request, 'app_music_db/privacy_policy.html')


def sitemap(request):
    if (datetime.date.today().day == 1):
        today = datetime.date.today()
        context = {
            "today": today,
        }
    else:
        lastmod = re.sub('\d{2}$', "01", str(datetime.date.today()))
        context = {
            "lastmod": lastmod,
        }

    return render(request, 'app_music_db/sitemap.xml', context)


def ads(request):
    return render(request, 'app_music_db/ads.txt')


class CsvImport(generic.FormView):
    template_name = 'app_music_db/import.html'
    success_url = reverse_lazy('app_music_db:index')
    form_class = CsvImportForm

    def form_valid(self, form):
        # csv.readerに渡すため、TextIOWrapperでテキストモードなファイルに変換
        csvfile = io.TextIOWrapper(form.cleaned_data['file'], encoding='utf-8')
        reader = csv.reader(csvfile)
        # 1行ずつ取り出し、作成していく
        for row in reader:
            song, created = Song.objects.get_or_create(pk=row[0])
            song.title = row[1]
            song.composer = row[2]
            song.arranger = row[3]
            song.artist = row[4]
            song.cd = row[5]
            song.cd_link = row[6]
            song.cdYear = row[7]
            song.cdVol = row[8]
            song.cd_type = CdType.objects.get(id=row[9]) # ←引数の左辺はidかpkならどっちでもいいらしい！！！！（違いは謎）
            # ↑ForeignKeyの場合、データベースにはFKのIDのみが保存されるのですがDjangoの中で扱う場合はオブジェクトをわたす必要があります(今回の場合はSituation Classのオブジェクト)。　だそうです
            song.asin = row[10]
            song.save()
        return super().form_valid(form)


def CsvExport(request):
    response = HttpResponse(content_type='text/csv; charset=cp932') # cp932必須なので以降忘れない！（shift-JISはダメだった）
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    # HttpResponseオブジェクトはファイルっぽいオブジェクトなので、csv.writerにそのまま渡せます。
    writer = csv.writer(response)
    for song in Song.objects.all():
        writer.writerow([
            song.pk,
            song.title,
            song.composer,
            song.arranger,
            song.artist,
            song.cd,
            song.cd_link,
            song.cdYear,
            song.cdVol,
            song.cd_type.id,  #ダメ押しでid付けたら文字列からちゃんとkey番号に変えることができた！
            song.asin,
            song.modified_at,
            ])
    return response


def ajax_comment_add(request):
    name = request.POST.get('name')
    text = request.POST.get('text')
    song_key = request.POST.get('song')
    comment = Comment.objects.create(name=name, text=text, song=Song.objects.get(id=song_key))
    now = comment.created_at
    hours9 = datetime.timedelta(hours=9)
    nowJST = now + hours9
    d = {
        'name': comment.name,
        'text': comment.text,
        'time': re.sub('\/0(.*)\/0', "/\\1/", nowJST.strftime('%Y/%m/%d/ %H:%M'))
    }
    return JsonResponse(d)


def ajax_recaptcha(request):
    code = request.POST.get("code")
    api = "https://www.google.com/recaptcha/api/siteverify?secret=6LdbP7cZAAAAAMO86up02UdCQw_91xNiELKEn4-v&response=" + code
    req = urllib.request.Request(api)
    with urllib.request.urlopen(req) as res:
        result = json.load(res)
    return JsonResponse(result)


def api_songs_get(request):
    keyword = request.GET.get('keyword')
    if keyword:
        song_list = [
            {'pk': song.pk, 'name': str(song)}
            for song in Song.objects.filter(title__icontains=keyword)
        ]
    else:
        song_list = []
    return JsonResponse({'object_list': song_list})


def api_composers_get(request):
    keyword = request.GET.get('keyword')
    if keyword:
        song_list = [
            {'pk': song.pk, 'name': song.composer}
            for song in Song.objects.filter(composer__icontains=keyword)
        ]
    else:
        song_list = []
    return JsonResponse({'object_list': song_list})


def api_arrangers_get(request):
    keyword = request.GET.get('keyword')
    if keyword:
        song_list = [
            {'pk': song.pk, 'name': song.arranger}
            for song in Song.objects.filter(arranger__icontains=keyword)
        ]
    else:
        song_list = []
    return JsonResponse({'object_list': song_list})


def api_artists_get(request):
    keyword = request.GET.get('keyword')
    if keyword:
        song_list = [
            {'pk': song.pk, 'name': song.artist}
            for song in Song.objects.filter(artist__icontains=keyword)
        ]
    else:
        song_list = []
    return JsonResponse({'object_list': song_list})


def api_cds_get(request):
    keyword = request.GET.get('keyword')
    if keyword:
        song_list = [
            {'pk': song.pk, 'name': song.cd}
            for song in Song.objects.filter(cd__icontains=keyword)
        ]
    else:
        song_list = []
    return JsonResponse({'object_list': song_list})


# def detail(request, pk):
#     # urlのpkを基に、Dayを取得
#     song = get_object_or_404(Day, pk=pk)
#     # 通常時のページアクセスや、入力内容に誤りがあればまたページを表示
#     context = {
#         'song': song,
#     }
#     return render(request, 'app_music_db/song_detail.html', context)











