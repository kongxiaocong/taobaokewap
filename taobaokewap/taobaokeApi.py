# coding:utf-8
import top
import top.api
from django.conf import settings
import sys
import re
import requests
reload(sys)
sys.setdefaultencoding('utf8')

appkey = settings.APPKEY
secret = settings.SECRET
adzone_id = settings.ADZONE_ID

def get_tk_coupon(kw, size=50):
    req = top.api.TbkDgItemCouponGetRequest()
    req.set_app_info(top.appinfo(appkey, secret))
    req.adzone_id = int(adzone_id)
    req.platform = 2
    req.page_size = size
    req.q = kw
    req.page_no = 1
    try:
        resp = req.getResponse()['tbk_dg_item_coupon_get_response']['results']['tbk_coupon']
        return resp
    except Exception as e:
        print(e)
        return None


#获取淘口令
def get_token(url, text,logo):
    req = top.api.TbkTpwdCreateRequest()
    req.set_app_info(top.appinfo(appkey, secret))

    req.text = text
    req.url = url
    req.logo = logo
    try:
        resp = req.getResponse()['tbk_tpwd_create_response']['data']['model']
        return resp
    except Exception as e:
        print(e)
        return None

# 解释淘口令
def get_taokouling_url(password_content):
    req = top.api.WirelessShareTpwdQueryRequest()
    req.set_app_info(top.appinfo(appkey, secret))
    req.password_content = password_content
    try:
        resp = req.getResponse()
        # print(resp)
        return resp
    except Exception, e:
        print(e)
        return None

# 捉淘宝页面title
def catchtile(url):
    print url
    file = requests.get(url)
    data = file.text
    reg = r'name="keywords" content="(.*?)"/>'
    try:
        temp1 = re.findall(reg, data)[0].encode('utf-8')
        return temp1
    except Exception, e:
        print(e)
        return None


#通過淘口令查找優惠券
def taokouling_get_tk_coupon(kw):
        # 解析淘口令
        taokouling_url = get_taokouling_url(password_content=kw)
        print taokouling_url
        new_url=taokouling_url['wireless_share_tpwd_query_response']['url'].replace('item.taobao.com','detail.tmall.com')
        searchword = catchtile(new_url)
        # 通过搜索词获取淘宝客商品优惠券信息
        response = get_tk_coupon(searchword)
        # 遍历获取到的淘宝客商品优惠券信息
        return response

#通過url查找優惠券
def url_get_tk_coupon(url):
        searchword = catchtile(url)
        # 通过搜索词获取淘宝客商品优惠券信息
        response = get_tk_coupon(searchword)
        # 遍历获取到的淘宝客商品优惠券信息
        return response
