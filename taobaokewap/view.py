# coding:utf-8
from django.shortcuts import render
from django.conf import settings
from . import taobaokeApi,tools,jdApi,wxapi
import sys
from django.utils.safestring import mark_safe
import logging
from .models import lunbotu,jdcookie
import hashlib
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import xml.etree.ElementTree as ET
import time
logger=logging.getLogger("django")
reload(sys)
sys.setdefaultencoding('utf8')
appkey = settings.APPKEY
secret = settings.SECRET
adzone_id = settings.ADZONE_ID



def hello(request):
    good_html={}
    with open('falseredis/indexhtml.txt') as f:
        data=f.read()
    good_html['goods'] = mark_safe(data)
    lunbotuhtml=''
    lunbotus=lunbotu.objects.all()
    for lunbotus in lunbotus:
        shortcouponUrl=tools.get_short_url(lunbotus.couponUrl)
        lunbotuhtml=lunbotuhtml+'<a href="coupon?TK={}&curl={}&cimg={}"><img src="{}"></a>'.format(shortcouponUrl,shortcouponUrl,lunbotus.imageUrl,lunbotus.imageUrl)
    good_html['lunbo'] = mark_safe(lunbotuhtml)
    return render(request, "index.html",good_html)

def searchlist(request):
    good_html = {}
    #print request.GET
    if request.GET:
       if request.GET['search'].count("￥")==2 or request.GET['search'].count("€")==2:
           good_list=taobaokeApi.taokouling_get_tk_coupon(request.GET['search'])
           try:
               good_count = len(good_list)
               logger.info('接受一条淘口令搜索:%s   返回商品数量:%s' % (request.GET['search'], good_count))
               good_html['goods'] = mark_safe(tools.make_search_goods_html(good_list))
               return render(request, "searchlist.html", good_html)
           except:
               good_html = tools.make_nogoods_html()
               return render(request, "searchlist.html", good_html)
       elif request.GET['search'].find(".com") != -1:
           print 'url'
           good_list = taobaokeApi.url_get_tk_coupon(request.GET['search'])
           try:
               good_count = len(good_list)
               logger.info('接受一条url搜索:%s   返回商品数量:%s' % (request.GET['search'], good_count))
               good_html['goods'] = mark_safe(tools.make_search_goods_html(good_list))
               return render(request, "searchlist.html", good_html)
           except:
               good_html = tools.make_nogoods_html()
               return render(request, "searchlist.html", good_html)
       else:
            good_list=taobaokeApi.get_tk_coupon(request.GET['search'])
            try:
                good_count=len(good_list)
                logger.info('接受一条搜索:%s   返回商品数量:%s' % (request.GET['search'],good_count))
                good_html['goods']=mark_safe(tools.make_search_goods_html(good_list))
                return render(request, "searchlist.html", good_html)
            except :
                good_html=tools.make_nogoods_html()
                return render(request, "searchlist.html", good_html)
    else:
        return  hello(request)


def coupon(request):
    print request.GET
    if request.GET:
        coupon_html={}
        TKL = taobaokeApi.get_token(url=tools.get_long_url(request.GET['TK']), text='柚子桑优惠券',logo=request.GET['cimg'])
        coupon_html['cimg'] = request.GET['cimg']
        coupon_html['TK'] = TKL
        coupon_html['curl'] = request.GET['curl']
        return render(request, "coupon.html",coupon_html)


def reFreshIndex(request):
    tools.reFreshIndexHtml()
    return HttpResponse("<p>首页数据刷新！</p>")

# def reFreshDH(request):
#     tools.reFreshIndexHtml()
#     return HttpResponse("<p>首页数据刷新！</p>")

def jdsearch(request):
    good_html = {}
    if request.GET:
        jd_list_cookie=jdcookie.objects.all()[0].cookies
        pasge_num=1
        jd_list_url = 'https://media.jd.com/gotoadv/goods?searchId=2011125541%23%23%23st3%23%23%23kt0%23%23%2307f9b85c-b071-4833-b0b8-a68ce0131b5d&pageIndex=' + str(
            pasge_num) + '&pageSize=50&property=&sort=&goodsView=&adownerType=&pcRate=&wlRate=&category1=&category=&category3=&condition=1&fromPrice=&toPrice=&dataFlag=0&keyword='+request.GET['search']+'&input_keyword='+request.GET['search']+'&hasCoupon='
        print jd_list_url
        html_temp=jdApi.request_html(jd_list_cookie,jd_list_url)
        if html_temp.find('jd_5ebdb8a09295c') != -1 and html_temp.find('没有找到') == -1:
            html_json_list, requestId = jdApi.catch_html_list(html_temp)
            if len(html_json_list)>0:
                good_temp_html=jdApi.request_coupon(jd_list_cookie, jd_list_url, html_json_list,requestId)
                good_html['goods'] = mark_safe(good_temp_html)
    return render(request, "jdsearchlist.html",good_html)

@csrf_exempt
def wxapi(request):
    if request.method == "GET":
        #接收微信服务器get请求发过来的参数
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        #服务器配置中的token
        token = 'hello567'
        #把参数放到list中排序后合成一个字符串，再用sha1加密得到新的字符串与微信发来的signature对比，如果相同就返回echostr给服务器，校验通过
        hashlist = [token, timestamp, nonce]
        hashlist.sort()
        hashstr = ''.join([s for s in hashlist])
        hashstr = hashlib.sha1(hashstr).hexdigest()
        if hashstr == signature:
          return HttpResponse(echostr)
        else:
          return HttpResponse("field")
    else:
        othercontent = wxapi.autoreply(request)
        return HttpResponse(othercontent)
