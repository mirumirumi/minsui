//indexページの判定
let flg = document.getElementById("contents");
let current = location.href;
let wsH = window.innerWidth;


/**
 * 遅延読み込みの設定
 */
Tada.default.setup({
    delay: 13, //msec
    threshold: '20%' //違いが全く分からないのでデフォルトのまま
});
Tada.default.add("img.lazy");


/**
 * ナビバーにactive付与
 */
if (current.indexOf("/add-album") !== -1) {
    $(".nav-link.3").addClass("active");
} else if (current.indexOf("/add") !== -1) {
    $(".nav-link.2").addClass("active");
} else if ((current.indexOf("edit") !== -1) || (current.indexOf("delete") !== -1) || (current.indexOf("contact") !== -1) || (current.indexOf("about") !== -1) || (current.indexOf("policy") !== -1)) {
    ;
} else {
    $(".nav-link.1").addClass("active");
}


/**
 * 説明セクションをもう表示しない
 */
$('#is-desc-open').change(function () {
    if ($("#is-desc-open").prop("checked") === true) {
        $(".desc-wrap").css("display", "none");
        document.cookie = "is_desc_open=none;max-age=94608000"; //3年
    } else {
        $(".desc-wrap").css("display", "block");
        document.cookie = "is_desc_open=open;max-age=94608000";
    }
});
let gc = "";
$(document).ready(function() {
    let cookies = document.cookie.split(";");
    for (let c of cookies) {
        let ac = c.split("=");
        ac[0] = ac[0].trim(" ");
        if (ac[0] == "is_desc_open") {
            gc = ac[1];
        }
    }
    if (flg && gc === "none") {
        $("#is-desc-open").prop("checked", true);
        $(".desc-wrap").css("display", "none");
    }
});


/**
 * モバイル端末の人には横スクロール可能を示す
 */
if ((flg)  && (wsH <= 768)) {
    var t = $("table#contents").offset().top; 
    var p = t - $(window).height();
    $(window).scroll(function () {
        if ($("#is-desc-open").prop("checked") === true) {
            scrollVol = 800;
        } else {
            scrollVol = -400;            
        }
        if ($(window).scrollTop() > p - scrollVol) {
            $(".scroll-hint-icon").addClass("flicker-animation");
            $(".scroll-hint-icon").css("opacity", "1");
            setTimeout(function() {
                $(".scroll-hint-icon").fadeOut(273);
            }, 3973);
        }
    });
}


/**
 * GET検索のパラメータに応じてフォームの内容をセットする（{{ form }}を使えばこれは自動化されるが、HTMLの自由度が低すぎるため今回は不採用。他のメリットはまだ知らん。
 */
if (flg) {
    let url = new URL(location);
    let get_param = url.searchParams.get("s");
    if (get_param !== "") {
        $("#keyword-search").val(get_param);
    }
    get_param = url.searchParams.get("c");
    if (get_param == "1") {
        $("#id_isContest").val(1);
    } else if (get_param == "2") {
        $("#id_isContest").val(2);
    }
    get_param = url.searchParams.get("n");
    if (get_param == "add") {
        $("#id_add-edit").val("add");
    } else if (get_param == "edit") {
        $("#id_add-edit").val("edit");        
    }
    get_param = url.searchParams.get("q");
    switch (get_param) {
        case "25":
            $("#disp-quantity").val("25");
            break;
        case "50":
            $("#disp-quantity").val("50");
            break;
        case "500":
            $("#disp-quantity").val("500");
            break;
        case "1000":
            $("#disp-quantity").val("1000");
            break;
        case "all":
            $("#disp-quantity").val("all");
            break;
    }
        
}


/**
 * コメント欄などを展開する
 */
$(".expand-down").click(function () {
    let songId = $(this).attr("id");
    if (!$(".row-invisible." + songId).hasClass("is-expand")) {
        $(".row-invisible." + songId).fadeIn(399);
        $(".row-invisible." + songId).addClass("is-expand");
        $("#" + songId +  " .fa-chevron-down").addClass("rotate");
    } else {
        $(".row-invisible." + songId).fadeOut(277);
        $(".row-invisible." + songId).removeClass("is-expand");
        $("#" + songId + " .fa-chevron-down").removeClass("rotate");
    }
    //モバイルだったときは展開欄の横幅を画面横幅と同じになるようにpaddingをセット（table内の要素にwidthは効かない）
    if (wsH <= 768) {
        let tableWidth = $("table#contents").width();
        $("tr.row-invisible td").attr("style", "padding: 1em 0 1.7em calc(" + tableWidth + "px - " + wsH + "px + " + (wsH*0.037)*2 + "px) !important;");
    }
});


/**
 * シェア情報をクリップボードにコピー
 */
$('.a-copy').click(function () {
    let id = $(this).attr("class").replace("a-copy ", "");
    let content =
        $(".row-visible." + id + " .song-title").text() + "\n"
         + $(".row-visible." + id + " .song-composer").text() + "\n"
         + $(".row-visible." + id + " .song-artist").text() + "\n"
         + $(".row-visible." + id + " .song-cd").text();
    execCopy(content);
    $(".copy-alert").fadeIn(273);
    setTimeout(function() {
        $(".copy-alert").fadeOut(273);
    }, 1733);
});
function execCopy(string) {
    var tmp = document.createElement("div");
    var pre = document.createElement("pre");
    tmp.appendChild(pre).textContent = string;
    var s = tmp.style;
    s.position = "fixed";
    s.right = "200%";
    document.body.appendChild(tmp);
    document.getSelection().selectAllChildren(tmp);
    var result = document.execCommand("copy");
    document.body.removeChild(tmp);
    return result;
}


/**
 * 各フォームのUIを表示する
 */
$('input[name="blnContest"]:radio').change(function() {
    let val = $(this).val();
    if (val == "contest") { 
        $("#year").css("display", "block");
        $("#vol").css("display", "block");
        $("#cd-input").css("display", "none");
    } else { 
        $("#cd-input").css("display", "block");
        $("#year").css("display", "none");
        $("#vol").css("display", "none");
    }
}); 


/**
 * フォーム上ではアフィタグを付加しない
 */
if (!flg) {
    if (current.indexOf("edit") !== -1) {
        $("#id_cd_link").val($("#id_cd_link").val().replace("?tag=wo-music-22", ""));
    }
    if (current.indexOf("delete") !== -1) {
        $("#cd-link").text($("#cd-link").text().replace("?tag=wo-music-22", ""));
    }
}

/**
 * CD名のラジオボタンによって入力忘れを止める
 */
$("#add-edit-submit, .album-submit").click(function(e) {
    if (($('input:radio[name="blnContest"]:checked').val()=="contest") && ($("#id_cdYear").val() == false)) {
        e.preventDefault(); 
        alert("コンクールCDの年度情報が未入力です。");
    }
    if (($('input:radio[name="blnContest"]:checked').val()=="contest") && ($("#id_cdVol").val() == false)) {
        e.preventDefault(); 
        alert("コンクールCDのVol情報が未入力です。");
    }
    if (($('input:radio[name="blnContest"]:checked').val()=="other") && ($("#cd-input").val() == false)) {
        e.preventDefault(); 
        alert("CD名が入力されていません。");
    }
    /**
     * コンクールCDだった場合は送信前に結合して#cd-inputに渡す
     */
    if ($('input:radio[name="blnContest"]:checked').val() == "contest") {
        $("#cd-input").val("全日本吹奏楽コンクール" + $("#id_cdYear").val() + " Vol." + $("#id_cdVol").val());
    }
    /**
     * コンクール2019年以降の場合は「中学校編」などに名前を変える（実際に投稿する人はほぼいないだろう＆コンクール音源は自分で既に足している＆2020年はコンクールない＆2021もどうせ自分で足すなどの理由により、今は実装をやめる。）
     */
    if (1) {
        ;
    }
    /**
     * AmazonのURLかどうかバリデーションし、ゴミを消去
     */
    if (($("#id_cd_link").val().indexOf("www.amazon.co") == -1) && ($("#id_cd_link").val() != false)) {
        e.preventDefault(); 
        alert("CDの購入先リンクがAmazonのURLではないようです…。")
    } else {
        $("#id_cd_link").val($("#id_cd_link").val().replace(/(https?:\/\/www\.amazon\.co\.jp\/)(.*\/)?(dp\/B[0-9A-Z]{9}).*/gmi, "$1$3"));
        //注文履歴などの画面からアクセスしたページはURL構造が違うパターンになる
        $("#id_cd_link").val($("#id_cd_link").val().replace(/(https?:\/\/www\.amazon\.co\.jp\/)(gp\/product\/)(B[0-9A-Z]{9}).*/gmi, "$1dp\/$3"));
    }
});
    

/**
 * 修正のとき、CDのラジオボタンに応じてボックスを最初から表示する
 */
if ($("#id_cdYear").val() != false) {
    $('input:radio[value="contest"]').prop('checked', true);
    $("#year").css("display", "block");
    $("#vol").css("display", "block");
    $("#cd-input").css("display", "none");
} else if ($("#cd-input").val() != false) {
    $('input:radio[value="other"]').prop("checked", true);
    $("#cd-input").css("display", "block");
    $("#year").css("display", "none");
    $("#vol").css("display", "none");
}


/**
 * reCAPTCHAのコールバック関数（フロントエンド上からはCORSで弾かれるのでバックエンドからAPIを叩かないといけないらしい。そういうものなんだな？
 */
function recaptcha(code) {
    $.ajax({
        url: "/ajax_recaptcha",
        type: "POST",
        data: {
            code: code
        },
        cache: false,
        timeout: 5000 //タイムアウトでエラー処理
    }).done(function (response) {
        if (response.success === true) {
            $(".submit, #comment-submit").removeAttr("disabled");
            setTimeout(function () {
                $(".submit, #comment-submit").attr("disabled","disabled");
            }, 60000);
        } else {
            alert("認証が不正です。再度お試しください。");
        }
    }).fail(function() {
        alert("認証に失敗しました。再度お試しください。");
    });
}


/**
 * ソート順のクエリパラメータを付与する
 */
let nowUrl = new URL(location);
switch (nowUrl.searchParams.get("order")) {
    case "title":
        $(".song-title .fa-sort-up").css("display", "block");
        $(".song-title .fa-sort-down").css("display", "none");
        break;
    case "-title":
        $(".song-title .fa-sort-up").css("display", "none");
        $(".song-title .fa-sort-down").css("display", "block");
        break;
    case "composer":
        $(".song-composer .fa-sort-up").css("display", "block");
        $(".song-composer .fa-sort-down").css("display", "none");
        $(".song-title .fa-sort-up").css("display", "none");
        $(".song-title .fa-sort-down").css("display", "block");
        break;
    case "-composer":
        $(".song-composer .fa-sort-up").css("display", "none");
        $(".song-composer .fa-sort-down").css("display", "block");
        $(".song-title .fa-sort-up").css("display", "none");
        $(".song-title .fa-sort-down").css("display", "block");
        break;
    case "arranger":
        $(".song-arranger .fa-sort-up").css("display", "block");
        $(".song-arranger .fa-sort-down").css("display", "none");
        $(".song-title .fa-sort-up").css("display", "none");
        $(".song-title .fa-sort-down").css("display", "block");
        break;
    case "-arranger":
        $(".song-arranger .fa-sort-up").css("display", "none");
        $(".song-arranger .fa-sort-down").css("display", "block");
        $(".song-title .fa-sort-up").css("display", "none");
        $(".song-title .fa-sort-down").css("display", "block");
        break;
    case "artist":
        $(".song-artist .fa-sort-up").css("display", "block");
        $(".song-artist .fa-sort-down").css("display", "none");
        $(".song-title .fa-sort-up").css("display", "none");
        $(".song-title .fa-sort-down").css("display", "block");
        break;
    case "-artist":
        $(".song-artist .fa-sort-up").css("display", "none");
        $(".song-artist .fa-sort-down").css("display", "block");
        $(".song-title .fa-sort-up").css("display", "none");
        $(".song-title .fa-sort-down").css("display", "block");
        break;
    case "cd":
        $(".song-cd .fa-sort-up").css("display", "block");
        $(".song-cd .fa-sort-down").css("display", "none");
        $(".song-title .fa-sort-up").css("display", "none");
        $(".song-title .fa-sort-down").css("display", "block");
        break;
    case "-cd":
        $(".song-cd .fa-sort-up").css("display", "none");
        $(".song-cd .fa-sort-down").css("display", "block");
        $(".song-title .fa-sort-up").css("display", "none");
        $(".song-title .fa-sort-down").css("display", "block");
        break;
    case "comment":
        $(".comment-quantity .fa-sort-up").css("display", "block");
        $(".comment-quantity .fa-sort-down").css("display", "none");
        $(".song-title .fa-sort-up").css("display", "none");
        $(".song-title .fa-sort-down").css("display", "block");
        break;
    case "-comment":
        $(".comment-quantity .fa-sort-up").css("display", "none");
        $(".comment-quantity .fa-sort-down").css("display", "block");
        $(".song-title .fa-sort-up").css("display", "none");
        $(".song-title .fa-sort-down").css("display", "block");
        break;
}
$(".song-title .fa-sort-up").click(function() {
    let url = new URL(location);
    url.searchParams.set("order", "-title");
    location.href = url.toString();
});
$(".song-title .fa-sort-down").click(function() {
    let url = new URL(location);
    url.searchParams.set("order", "title");
    location.href = url.toString();
});
$(".song-composer .fa-sort-up").click(function() {
    let url = new URL(location);
    url.searchParams.set("order", "-composer");
    location.href = url.toString();
});
$(".song-composer .fa-sort-down").click(function() {
    let url = new URL(location);
    url.searchParams.set("order", "composer");
    location.href = url.toString();
});
$(".song-arranger .fa-sort-up").click(function() {
    let url = new URL(location);
    url.searchParams.set("order", "-arranger");
    location.href = url.toString();
});
$(".song-arranger .fa-sort-down").click(function() {
    let url = new URL(location);
    url.searchParams.set("order", "arranger");
    location.href = url.toString();
});
$(".song-artist .fa-sort-up").click(function() {
    let url = new URL(location);
    url.searchParams.set("order", "-artist");
    location.href = url.toString();
});
$(".song-artist .fa-sort-down").click(function() {
    let url = new URL(location);
    url.searchParams.set("order", "artist");
    location.href = url.toString();
});
$(".song-cd .fa-sort-up").click(function() {
    let url = new URL(location);
    url.searchParams.set("order", "-cd");
    location.href = url.toString();
});
$(".song-cd .fa-sort-down").click(function() {
    let url = new URL(location);
    url.searchParams.set("order", "cd");
    location.href = url.toString();
});
$(".comment-quantity .fa-sort-up").click(function() {
    let url = new URL(location);
    url.searchParams.set("order", "-comment");
    location.href = url.toString();
});
$(".comment-quantity .fa-sort-down").click(function() {
    let url = new URL(location);
    url.searchParams.set("order", "comment");
    location.href = url.toString();
});


/**
 * 感想投稿を画面遷移なしでモーダル的にURL変更、紐づくsong.pkも取得してフォームにセットする→ajax導入成功したのでURLうんぬんは廃止、idセットだけ使う
 */
$(".comment-window-open").click(function () {
    let songPk = $($(this).parents(".row-invisible")).attr("class").replace("row-invisible ", "").replace(" is-expand", "");
    // param = location.search;
    // history.pushState(null, null, "/comment/" + songPk + "/" + param);
    $("#id_song").val(songPk);
});
// //感想投稿ウィンドウが閉じられたらURLを元に戻す
// if (flg) {
//     $("#exampleModalCentered").on("DOMSubtreeModified propertychange", function () {
//         if ($("#exampleModalCentered").css("display") == "none") {
//             param = location.search;
//             history.pushState(null, null, "/" + param);
//         }
//     });
// }


/**
 * 感想投稿のユーザー名をcookieに保存する
 */
$("#comment-submit").click(function () {
    let userName = $("#id_name").val();
    document.cookie = "wom_user_name=" + encodeURIComponent(userName) + ";max-age=94608000"; //3年
});
let cookieName = "";
$(document).ready(function () {
    let arrayCookies = document.cookie.split(";");
    for (let c of arrayCookies) {
        let aC = c.split("=");
        aC[0] = aC[0].trim(" ");
        if (aC[0] == "wom_user_name") {
            cookieName = aC[1];
        }   
    }
});
$(".comment-window-open").click(function() {
    if (cookieName) {
        $("#id_name").val(decodeURIComponent(cookieName));
    }
});


/**
 * 非同期で検索できるようにする。単一ワードで消去法の絞り込みのみ。→全件表示だと重すぎて使い物にならないのでページを分けて普通の検索対応にした。起動はしないのでコメントアウトはしていない。
 */
$("#free-word").keyup(function(){
    let s = $(this).val();
    $(".row-visible").css("display", "none");
    if ($(".row-invisible").hasClass("is-expand")) {
        $(".row-invisible").css("display", "none");
        $(".row-invisible").removeClass("is-expand");
        $(".fa-chevron-down").removeClass("rotate");
    }
    if (s === "") {
        $(".row-visible").css("display", "table-row");
    } else {
        $(".row-visible").each(function () {
            // let id = ($(this).attr("class")).replace("row-visible ", "");
            let result = $(this).text();
            if (result.toLowerCase().indexOf(s) !== -1) {
                $(this).css("display", "table-row");
            }
        })
    }
});


/**
 * 検索ワードのクリアボタン
 */
$("#word-clear").click(function(){ 
    $("#free-word").val("");
    $(".row-visible").css("display", "table-row");
});


/**
 * GET検索のリセットボタン
 */
$("#get-reset").click(function () {
    let nowUrl = new URL(location);
    nowUrl = nowUrl.toString().replace(/\?.*/gmi, "");
    location.href = nowUrl;
});


/**
 * 非同期で感想投稿後にインデックスに戻る
 */
//CSRFトークンに関する処理です。Djangoにおいて、AjaxでデータをPOSTする際はこの記述が必要だと思っても差し支えないです。Django公式ドキュメントで紹介されているものをそのまま利用しています。（勝手にminifyした）
function getCookie(e){var t=null;if(document.cookie&&""!==document.cookie)for(var o=document.cookie.split(";"),n=0;n<o.length;n++){var r=jQuery.trim(o[n]);if(r.substring(0,e.length+1)===e+"="){t=decodeURIComponent(r.substring(e.length+1));break}}return t}var csrftoken=getCookie("csrftoken");function csrfSafeMethod(e){return/^(GET|HEAD|OPTIONS|TRACE)$/.test(e)}$.ajaxSetup({beforeSend:function(e,t){csrfSafeMethod(t.type)||this.crossDomain||e.setRequestHeader("X-CSRFToken",csrftoken)}});
$("#comment-submit").click(function(e){
    e.preventDefault();
    $.ajax({
        url: '/ajax_comment_add',
        type: "POST",
        data: {
            name: $("#id_name").val(),
            text: $("#id_text").val(),
            song: $("#id_song").val()
        },
        dataType: "json"
    }).done(response => {
        let elemCommentBody = $("<div>", { "class": "comment-body" });
        let elemCommentMeta = $("<div>", { "class": "comment-meta" });
        let keySong = $("#id_song").val();
        $("." + keySong + " .comment").append(elemCommentBody);
        $("." + keySong + " .comment-body:last").append(elemCommentMeta);
        let elemName = $("<span>", {text: response.name, "class":"comment-author"});
        let elemTime = $("<span>", {text: response.time, "class":"comment-datetime"});
        let elemText = $("<div>", {text: response.text, "class":"comment-text"});
        $("." + keySong + " .comment-meta:last").append(elemName);
        $("." + keySong + " .comment-meta:last").append(elemTime);
        $("." + keySong + " .comment-body:last").append(elemText);
        $("#close-button").trigger("click");
        // $("#id_name").val("");
        $("#id_text").val("");
        $("#id_song").val("");
        //リアルタイムで感想の数をプラス1する
        $("#comment-" + keySong).text(parseInt($("#comment-" + keySong).text()) + 1);
        //現在の状況も感想の数をプラス1する
        $("#current-comment-quantity").text(parseInt($("#current-comment-quantity").text()) + 1);
        //成功メッセージ
        let songTitle = $("." + keySong + " .song-title").html();
        $(".notify-area").html(songTitle + " の感想を投稿しました。");
        setTimeout(function() {
            $(".notify-area").css("background-color", "#49ae54");
            $(".notify-area").fadeIn(273).css("display", "flex");
        }, 777);
        setTimeout(function() {
            $(".notify-area").fadeOut(273);
        }, 5555);  
    });
});


/**
 * アルバム一括追加のとき、演奏団体の入力をまとめるかどうかを変える
 */
let blnArtist = true;
$("#is-same-artist").change(function () {
    if (blnArtist == true) {
        $("#artist-input").css("display", "none");
        $("#artist-textarea").css("display", "block");
        $("#artist-input").removeAttr("required");
        $("#artist-textarea").attr("required");
        blnArtist = false;
    } else {
        $("#artist-textarea").css("display", "none");
        $("#artist-input").css("display", "block");
        $("#artist-textarea").removeAttr("required");
        $("#artist-input").attr("required");
        blnArtist = true;
    }
});


/**
 * アルバム一括追加のとき、何曲追加するか知るためにtextareaの入力行数を取得して見えないフォームにセットする
 */
$(".album-submit").click(function (e) {
    //まず空白行があったら消してあげる（編曲者以外）（フォームの最後が空白行の場合はどう調べても取得できないみたいなので諦める）
    $("#artist-textarea").val($("#artist-textarea").val().replace(/(\r\n|\n)(\r\n|\n)/, "\n"));
    $("#title-textarea").val($("#title-textarea").val().replace(/(\r\n|\n)(\r\n|\n)/, "\n"));
    $("#composer-textarea").val($("#composer-textarea").val().replace(/(\r\n|\n)(\r\n|\n)/, "\n"));

    $("body").removeClass("artist-textarea-red title-textarea-red composer-textarea-red arranger-textarea-red");

    let lineArtist = $("#artist-textarea").val().match(/\r\n|\n/gmi);
    if (lineArtist) {
        lineArtist = lineArtist.length + 1;    
    } else if(blnArtist === false) {
        e.preventDefault(); 
        alert("演奏団体が1行しか入力されていません。");
        $("body").addClass("artist-textarea-red");
        $("#artist-textarea").focus();    
    }
    let lineTitle = $("#title-textarea").val().match(/\r\n|\n/gmi);
    if (lineTitle) {
        lineTitle = lineTitle.length + 1;
    } else {
        e.preventDefault(); 
        alert("曲名が1行しか入力されていません。");
        $("body").addClass("title-textarea-red");
        $("#title-textarea").focus();
    }
    let lineComposer = $("#composer-textarea").val().match(/\r\n|\n/gmi);
    if (lineComposer) {
        lineComposer = lineComposer.length + 1;
    } else {
        e.preventDefault(); 
        alert("作曲者が1行しか入力されていません。");
        $("body").addClass("composer-textarea-red");
        $("#composer-textarea").focus();
    }
    let lineArranger = $("#arranger-textarea").val().match(/\r\n|\n/gmi);
    if (lineArranger) {
        lineArranger = lineArranger.length + 1;
    } else {
        e.preventDefault(); 
        alert("編曲者が1行しか入力されていません。");
        $("body").addClass("arranger-textarea-red");
        $("#arranger-textarea").focus();
    }
    //最後、全ての行数が同じじゃないときはエラーを出す
    if ((blnArtist === false) && !((lineArtist === lineTitle) && (lineArtist === lineComposer) && (lineArtist === lineArranger))) {
        e.preventDefault(); 
        alert("それぞれの入力欄への入力行数が一致していません。");
    }
    //演奏団体が一括のときも
    if ((blnArtist === true) && !((lineTitle === lineComposer) && (lineTitle === lineArranger))) {
        e.preventDefault(); 
        alert("それぞれの入力欄への入力行数が一致していません。");
    }
    //行数をセット
    $("#line-number").val(lineTitle);
});


/**
 * topbtn
 */
let topBtn = $(".top-btn");
$(window).scroll(function() {
    if ($(this).scrollTop() > 273) {
        topBtn.fadeIn("503");
    } else {
        topBtn.fadeOut("503");
    }
});
$(".top-btn").click(function() {
    $("html, body").animate({ scrollTop: 0 }, 313);
});


/**
 * 削除申請の提出が成功したことを伝える
 */
if (flg) {
    let url = new URL(location);
    let get_param = url.searchParams.get("delete_req");
    if (get_param == "true") {
        $(".notify-area").html("削除リクエストの送信に成功しました。");
        setTimeout(function () {
            $(".notify-area").css("background-color", "#49ae54");
            $(".notify-area").fadeIn(273).css("display", "flex");
        }, 777);
        setTimeout(function () {
            $(".notify-area").fadeOut(273);
        }, 5555);        
    } else if(get_param == "false") {
        $(".notify-area").html("なんらかの原因により削除リクエストの送信に失敗しました。再度お試しください。");
        setTimeout(function () {
            $(".notify-area").css("background-color", "#db4545");
            $(".notify-area").fadeIn(273).css("display", "flex");
        }, 777);
        setTimeout(function () {
            $(".notify-area").fadeOut(273);
        }, 5555);
    }
}
//お問い合わせ送信が成功したことを伝える
if (flg) {
    let url = new URL(location);
    let get_param = url.searchParams.get("inquiry_submit");
    if (get_param == "true") {
        $(".notify-area").html("お問い合わせを正常に受け付けました。");
        setTimeout(function () {
            $(".notify-area").css("background-color", "#49ae54");
            $(".notify-area").fadeIn(273).css("display", "flex");
        }, 777);
        setTimeout(function () {
            $(".notify-area").fadeOut(273);
        }, 5555);        
    } else if (get_param == "false") {
        $(".notify-area").html("お問い合わせの受け付けに失敗しました。再度お試しください。");
        setTimeout(function() {
            $(".notify-area").css("background-color", "#db4545");
            $(".notify-area").fadeIn(273).css("display", "flex");}, 777);
        setTimeout(function() {
            $(".notify-area").fadeOut(273);
        }, 5555);
    }
}
//修正が成功したことを伝える
if (flg) {
    let url = new URL(location);
    let get_param = url.searchParams.get("fix");
    if (get_param == "true") {
        $(".notify-area").html("情報の修正内容を登録しました。");
        setTimeout(function () {
            $(".notify-area").css("background-color", "#49ae54");
            $(".notify-area").fadeIn(273).css("display", "flex");
        }, 777);
        setTimeout(function () {
            $(".notify-area").fadeOut(273);
        }, 5555);        
    } else if (get_param == "false") {
        $(".notify-area").html("情報の修正登録に失敗しました。再度お試しください。");
        setTimeout(function() {
            $(".notify-area").css("background-color", "#db4545");
            $(".notify-area").fadeIn(273).css("display", "flex");}, 777);
        setTimeout(function() {
            $(".notify-area").fadeOut(273);
        }, 5555);
    }
}
//曲の新規追加が成功したことを伝える
if (flg) {
    let url = new URL(location);
    let get_param = url.searchParams.get("new_add");
    if (get_param == "true") {
        $(".notify-area").html("新しい曲データの追加に成功しました。");
        setTimeout(function () {
            $(".notify-area").css("background-color", "#49ae54");
            $(".notify-area").fadeIn(273).css("display", "flex");
        }, 777);
        setTimeout(function () {
            $(".notify-area").fadeOut(273);
        }, 5555);        
    } else if (get_param == "false") {
    $(".notify-area").html(
        "なんらかの原因により新しい曲データの追加に失敗しました。"
    );
    setTimeout(function() {
        $(".notify-area").css("background-color", "#db4545");
        $(".notify-area")
            .fadeIn(273)
            .css("display", "flex");
    }, 777);
    setTimeout(function() {
        $(".notify-area").fadeOut(273);
    }, 5555);
}
}
//アルバム一括追加の失敗はリダイレクト先がトップページではないので分ける
let url = new URL(location);
let get_param = url.searchParams.get("new_add");
if (get_param == "false") {
    $(".notify-area").html(
        "新しい曲データの追加に失敗しました。行数に注意して再度お試しください。"
    );
    setTimeout(function() {
        $(".notify-area").css("background-color", "#db4545");
        $(".notify-area")
            .fadeIn(273)
            .css("display", "flex");
    }, 777);
    setTimeout(function() {
        $(".notify-area").fadeOut(273);
    }, 5555);
}
