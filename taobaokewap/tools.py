# coding:utf-8
import re
import sys
from . import taobaokeApi
import random
from django.utils.safestring import mark_safe
import requests
import json
import operator
reload(sys)
sys.setdefaultencoding('utf8')
def catch_str_num(txt):
    temp = re.findall(r"\d+\.?\d*", txt)
    return temp


# 通过新浪微博API生成优惠券链接的短链
def  get_short_url(url):
    link = url
    link_resp = requests.get(
        'http://api.weibo.com/2/short_url/shorten.json?source=2849184197&url_long=' + link).text
    link_short = json.loads(link_resp, encoding='utf-8')['urls'][0]['url_short']
    return link_short

def  get_long_url(url):
    link = url
    link_resp = requests.get(
        'http://api.t.sina.com.cn/short_url/expand.json?url_short=' + link).text
    link_long = json.loads(link_resp, encoding='utf-8')[0]['url_long']
    return link_long

#搜索页展示商品
def make_search_goods_html(good_list):
    good_list2 = sorted(good_list, key=operator.itemgetter('user_type'), reverse=True)
    good_temp_html = ''
    j=0
    for i in good_list2:
        j=j+1
        if i['user_type'] == 0:
            user_type = '淘宝'
        else:
            user_type = '天猫'
        if j < 20:
            price_list = catch_str_num(i['coupon_info'])
            couponurl=i['coupon_click_url']
            short_coupon_url=get_short_url(couponurl)
            short_img_url=i['pict_url']
            #TKL=taobaokeApi.get_token(url=couponurl, text=i['title'])
            TKL = short_coupon_url
            good_temp_html = good_temp_html + '    <div class="sl-products">\n' \
                                              '        <a href="coupon?TK={}&curl={}&cimg={}">\n' \
                                              '        ' \
                                              '<article class="sl-product">\n' \
                                              '            <section class="sl-product-img-box">\n ' \
                                              '               ' \
                                              '<img src="{}" alt="图片加载失败" class="sl-product-img "">\n' \
                                              '           ' \
                                              ' </section>\n' \
                                              '            <section class="sl-product-msg-box global-border-box">\n' \
                                              '                ' \
                                              '<ul class="sl-product-msg-list">\n' \
                                              '                    <li class="sl-product-msg-item sl-product-productname">\n' \
                                              '                        <h5>{}</h5>\n' \
                                              '                    </li>\n                    <li class="sl-product-msg-item"></li>\n' \
                                              '                    <li class="sl-product-msg-item">\n' \
                                              '                        <span class="sl-product-price">{}       |{}</span>\n' \
                                              '                    </li>\n                    <li class="sl-product-msg-item"></li>\n' \
                                              '                    <li class="sl-product-msg-item">\n' \
                                              '                        <span class="sl-product-price-unit">￥</span>\n' \
                                              '                        <span class="sl-product-price">{}</span>\n' \
                                              '                    </li>\n' \
                                              '                    <li class="sl-product-msg-item"></li>\n' \
                                              '                    <li class="sl-product-msg-item">\n' \
                                              '                        <span class="sl-product-business">券</span><span class="sl-product-price-ora">{}元</span>\n' \
                                              '                        <span class="sl-product-comment-count">&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp月销：{}</span>\n' \
                                              '                   </li>\n' \
                                              '                   <li class="sl-product-msg-item"></li>\n' \
                                              '                </ul>\n' \
                                              '            </section>\n' \
                                              '        </article>\n' \
                                              '        </a>\n' \
                                              '    </div>\n'.format(TKL,short_coupon_url,short_img_url,i['pict_url'],i['title'][:38],i['shop_title'],user_type,i['zk_final_price'],price_list[1],i['volume'])
    return good_temp_html

#搜索页展示无商品
def make_nogoods_html():
    good_html = {}
    good_list=taobaokeApi.get_tk_coupon(kw='秋冬',size=10)+taobaokeApi.get_tk_coupon(kw='女装',size=10)+taobaokeApi.get_tk_coupon(kw='婴儿',size=10)
    random.shuffle(good_list)
    good_temp_html = '<br><div class="center-text">没有查找到与你关键字相关的优惠券</div><div class="center-text">下面是为你推荐的热卖品</div><br> <br><br> '
    j=0
    for i in good_list:
        j=j+1
        if i['user_type'] == 0:
            user_type = '淘宝'
        else:
            user_type = '天猫'
        if j < 11:
                price_list = catch_str_num(i['coupon_info'])
                couponurl=i['coupon_click_url']
                short_coupon_url=get_short_url(couponurl)
                short_img_url=i['pict_url']
                #TKL=taobaokeApi.get_token(url=couponurl, text=i['title'])
                TKL = short_coupon_url
                good_temp_html = good_temp_html + '    <div class="sl-products">\n' \
                                                  '        <a href="coupon?TK={}&curl={}&cimg={}">\n' \
                                                  '        ' \
                                                  '<article class="sl-product">\n' \
                                                  '            <section class="sl-product-img-box">\n ' \
                                                  '               ' \
                                                  '<img src="{}" alt="图片加载失败" class="sl-product-img "">\n' \
                                                  '           ' \
                                                  ' </section>\n' \
                                                  '            <section class="sl-product-msg-box global-border-box">\n' \
                                                  '                ' \
                                                  '<ul class="sl-product-msg-list">\n' \
                                                  '                    <li class="sl-product-msg-item sl-product-productname">\n' \
                                                  '                        <h5>{}</h5>\n' \
                                                  '                    </li>\n                    <li class="sl-product-msg-item"></li>\n' \
                                                  '                    <li class="sl-product-msg-item">\n' \
                                                  '                        <span class="sl-product-price">{}       |{}</span>\n' \
                                                  '                    </li>\n                    <li class="sl-product-msg-item"></li>\n' \
                                                  '                    <li class="sl-product-msg-item">\n' \
                                                  '                        <span class="sl-product-price-unit">￥</span>\n' \
                                                  '                        <span class="sl-product-price">{}</span>\n' \
                                                  '                    </li>\n' \
                                                  '                    <li class="sl-product-msg-item"></li>\n' \
                                                  '                    <li class="sl-product-msg-item">\n' \
                                                  '                        <span class="sl-product-business">券</span><span class="sl-product-price-ora">{}元</span>\n' \
                                                  '                        <span class="sl-product-comment-count">&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp月销：{}</span>\n' \
                                                  '                   </li>\n' \
                                                  '                   <li class="sl-product-msg-item"></li>\n' \
                                                  '                </ul>\n' \
                                                  '            </section>\n' \
                                                  '        </article>\n' \
                                                  '        </a>\n' \
                                                  '    </div>\n'.format(TKL,short_coupon_url,short_img_url,i['pict_url'],i['title'][:38],i['shop_title'],user_type,i['zk_final_price'],price_list[1],i['volume'])
        good_html['goods'] = mark_safe(good_temp_html)
    return good_html

def reFreshIndexHtml():
    good_list = taobaokeApi.get_tk_coupon(kw='秋冬') + taobaokeApi.get_tk_coupon(kw='女装') + taobaokeApi.get_tk_coupon(kw='婴儿') + taobaokeApi.get_tk_coupon(kw='丝袜') + taobaokeApi.get_tk_coupon(kw='鞋')+ taobaokeApi.get_tk_coupon(kw='超市')
    #random.shuffle(good_list)
    good_list2 = sorted(good_list, key=operator.itemgetter('volume'), reverse=True)
    good_temp_html = ''
    n=1
    for i in good_list2:
        if i['user_type'] != 0 and n<21:
            user_type = '天猫'
            price_list = catch_str_num(i['coupon_info'])
            couponurl = i['coupon_click_url']
            short_coupon_url = get_short_url(couponurl)
            short_img_url = i['pict_url']
            # TKL=taobaokeApi.get_token(url=couponurl, text=i['title'])
            TKL = short_coupon_url
            good_temp_html = good_temp_html + '    <div class="sl-products">\n' \
                                              '        <a href="coupon?TK={}&curl={}&cimg={}">\n' \
                                              '        ' \
                                              '<article class="sl-product">\n' \
                                              '            <section class="sl-product-img-box">\n ' \
                                              '               ' \
                                              '<img src="{}" alt="图片加载失败" class="sl-product-img "">\n' \
                                              '           ' \
                                              ' </section>\n' \
                                              '            <section class="sl-product-msg-box global-border-box">\n' \
                                              '                ' \
                                              '<ul class="sl-product-msg-list">\n' \
                                              '                    <li class="sl-product-msg-item sl-product-productname">\n' \
                                              '                        <h5>{}</h5>\n' \
                                              '                    </li>\n                    <li class="sl-product-msg-item"></li>\n' \
                                              '                    <li class="sl-product-msg-item">\n' \
                                              '                        <span class="sl-product-price">{}       |{}</span>\n' \
                                              '                    </li>\n                    <li class="sl-product-msg-item"></li>\n' \
                                              '                    <li class="sl-product-msg-item">\n' \
                                              '                        <span class="sl-product-price-unit">￥</span>\n' \
                                              '                        <span class="sl-product-price">{}</span>\n' \
                                              '                    </li>\n' \
                                              '                    <li class="sl-product-msg-item"></li>\n' \
                                              '                    <li class="sl-product-msg-item">\n' \
                                              '                        <span class="sl-product-business">券</span><span class="sl-product-price-ora">{}元</span>\n' \
                                              '                        <span class="sl-product-comment-count">&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp月销：{}</span>\n' \
                                              '                   </li>\n' \
                                              '                   <li class="sl-product-msg-item"></li>\n' \
                                              '                </ul>\n' \
                                              '            </section>\n' \
                                              '        </article>\n' \
                                              '        </a>\n' \
                                              '    </div>\n'.format(TKL,short_coupon_url,short_img_url,i['pict_url'],i['title'][:38],i['shop_title'],user_type,i['zk_final_price'],price_list[1],i['volume'])
            n=n+1
    with open('falseredis/indexhtml.txt','w') as f:
        f.writelines(good_temp_html)

def reFreshIndexHtml():
    good_list = taobaokeApi.get_tk_coupon(kw='华为') + taobaokeApi.get_tk_coupon(kw='iPhone') + taobaokeApi.get_tk_coupon(kw='小米') + taobaokeApi.get_tk_coupon(kw='丝袜') + taobaokeApi.get_tk_coupon(kw='鞋')+ taobaokeApi.get_tk_coupon(kw='超市')
    #random.shuffle(good_list)
    good_list2 = sorted(good_list, key=operator.itemgetter('volume'), reverse=True)
    good_temp_html = ''
    n=1
    for i in good_list2:
        if i['user_type'] != 0 and n<21:
            user_type = '天猫'
            price_list = catch_str_num(i['coupon_info'])
            couponurl = i['coupon_click_url']
            short_coupon_url = get_short_url(couponurl)
            short_img_url = i['pict_url']
            # TKL=taobaokeApi.get_token(url=couponurl, text=i['title'])
            TKL = short_coupon_url
            good_temp_html = good_temp_html + '    <div class="sl-products">\n' \
                                              '        <a href="coupon?TK={}&curl={}&cimg={}">\n' \
                                              '        ' \
                                              '<article class="sl-product">\n' \
                                              '            <section class="sl-product-img-box">\n ' \
                                              '               ' \
                                              '<img src="{}" alt="图片加载失败" class="sl-product-img "">\n' \
                                              '           ' \
                                              ' </section>\n' \
                                              '            <section class="sl-product-msg-box global-border-box">\n' \
                                              '                ' \
                                              '<ul class="sl-product-msg-list">\n' \
                                              '                    <li class="sl-product-msg-item sl-product-productname">\n' \
                                              '                        <h5>{}</h5>\n' \
                                              '                    </li>\n                    <li class="sl-product-msg-item"></li>\n' \
                                              '                    <li class="sl-product-msg-item">\n' \
                                              '                        <span class="sl-product-price">{}       |{}</span>\n' \
                                              '                    </li>\n                    <li class="sl-product-msg-item"></li>\n' \
                                              '                    <li class="sl-product-msg-item">\n' \
                                              '                        <span class="sl-product-price-unit">￥</span>\n' \
                                              '                        <span class="sl-product-price">{}</span>\n' \
                                              '                    </li>\n' \
                                              '                    <li class="sl-product-msg-item"></li>\n' \
                                              '                    <li class="sl-product-msg-item">\n' \
                                              '                        <span class="sl-product-business">券</span><span class="sl-product-price-ora">{}元</span>\n' \
                                              '                        <span class="sl-product-comment-count">&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp月销：{}</span>\n' \
                                              '                   </li>\n' \
                                              '                   <li class="sl-product-msg-item"></li>\n' \
                                              '                </ul>\n' \
                                              '            </section>\n' \
                                              '        </article>\n' \
                                              '        </a>\n' \
                                              '    </div>\n'.format(TKL,short_coupon_url,short_img_url,i['pict_url'],i['title'][:38],i['shop_title'],user_type,i['zk_final_price'],price_list[1],i['volume'])
            n=n+1
    with open('falseredis/indexhtml.txt','w') as f:
        f.writelines(good_temp_html)