import sys
import requests
import hmac
import hashlib
import base64
import urllib.parse
from datetime import datetime
from bs4 import BeautifulSoup

class Pa_API:
    def __init__(self, associate_id='miilkcat-22'):
        """ 初期化処理 """
        # ハッシュ関数とエンコードをset
        self.hash_func = hashlib.sha256
        self.encode_func = base64.b64encode
        #id,keyのset
        self.ACCESS_KEY = 'AKIAIXP5JH2554U3YZQA'
        self.SECRET_KEY = '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'
        self.ASSOCIATE_ID = associate_id

    def get_info(self, asin_code='XXXXXXXXXX'):
        api_domain = 'webservices.amazon.co.jp'
        api_page = '/onca/xml'
        # 商品のASINコード、ASINコードがない場合はISBN-10
        asin_code = asin_code
        # パラメーター用のタイムスタンプを生成
        time_stamp = urllib.parse.quote(datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
        # URLパラメータのセット
        query='AWSAccessKeyId=' + self.ACCESS_KEY + \
            '&AssociateTag=' + self.ASSOCIATE_ID + \
            '&ItemId=' + asin_code + \
            '&Operation=ItemLookup' + \
            '&ResponseGroup=Images%2CItemAttributes%2COffers%2CReviews' + \
            '&Service=AWSECommerceService' + \
            '&Timestamp=' + time_stamp + \
            '&Version=2013-08-01'
        message = '\n'.join(['GET', api_domain, api_page, query])
        # HMACのSignature生成（ハッシュ値を算出）
        sing_gen = hmac.new(self.SECRET_KEY.encode('utf8'), message.encode('utf8'), self.hash_func)
        raw_sign = sing_gen.digest()
        sign = urllib.parse.quote(self.encode_func(raw_sign))

        # API用URLの生成
        url = 'http://' + api_domain + api_page + '?' + query + '&Signature=' + sign
        print(url)

        res = requests.get(url)
        soup = BeautifulSoup(res.text,'lxml')
        
        # 商品情報を取得
        productgroup = self.get_productgroup(soup)
        detailpageurl = self.get_url(soup)
        largeimage = self.get_largeimage(soup)
        title = self.get_title(soup)
        price = self.get_price(soup)
        amount = self.get_amount(soup)
        price_time = datetime.now().strftime('%Y年%m月%d日 %H時%M分時点')
        author = self.get_author(soup)
        brand = self.get_brand(soup)
        link_text = 'Amazon 詳細ページへ'

        result = {'productgroup':productgroup, 'asin_code':asin_code, 'detailpageurl':detailpageurl, 'largeimage':largeimage, 'title':title, 'price':price, 'amount':amount, 'author':author, 'brand':brand, 'price_time':price_time, 'link_text':link_text}

        return result

    def get_productgroup(self, soup):
        print(soup)
        return soup.find('itemattributes').find('productgroup').text.strip()

    def get_url(self, soup):
        return soup.find('item').find('detailpageurl').text.strip()

    def get_largeimage(self, soup):
        return soup.find('largeimage').find('url').text.strip()

    def get_title(self, soup):
        return soup.find('itemattributes').find('title').text.strip()

    def get_price(self, soup):
        return soup.find('offersummary').find('formattedprice').text.strip()

    def get_amount(self, soup):
        return soup.find('offersummary').find('amount').text.strip()

    def get_brand(self, soup):
        return soup.find('itemattributes').find('publisher').text.strip()

    def get_author(self, soup):
        return soup.find('itemattributes').find('author').text.strip()



if __name__ == "__main__":
    obj = Pa_API()
    obj.get_info("B00KKS0KAC")