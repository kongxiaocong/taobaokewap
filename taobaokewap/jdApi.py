# coding:utf-8
import sys
import requests
import re
import ast
import json
reload(sys)
sys.setdefaultencoding('utf-8')

def request_html(jd_list_cookie,jd_list_url):
    jd_list_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                       'Accept-Encoding': 'gzip, deflate, sdch, br',
                       'Accept-Language': 'zh-CN,zh;q=0.8',
                       'Cache-Control': 'no-cache',
                       'Connection': 'keep-alive',
                       'Cookie': jd_list_cookie,
                       'Host': 'media.jd.com',
                       'Pragma': 'no-cache',
                       'Referer': jd_list_url,
                       'Upgrade-Insecure-Requests': '1',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'}
    html_temp = requests.get(url=jd_list_url, headers=jd_list_headers).content
    return html_temp


def  catch_html_list(html_temp):
    reg=r'<li skuid="(.*?)</li>'
    temp=re.findall(reg, html_temp, re.S)
    tempgoodall=[]
    for ihtml in temp:
        reg = r'"color: #ff5400;">满(.*?)</span>'
        j=re.findall(reg, ihtml, re.S)
        if len(j)>0:
           tempcoupon="\r\n                       'couponnum':'{}'".format('满'+j[0])
           jiaqian="\r\n                       'jiaqian':'{}'".format('￥')
        else:
           tempcoupon = "\r\n                       'couponnum':{}".format("'0'")
           jiaqian = "\r\n                       'jiaqian':'{}'".format('特价￥')
        reg = r'onclick="Gmodal.init\((.*?),this'
        k=re.findall(reg, ihtml, re.S)
        tempgoodall.append(k[0].replace('{', '{' + tempcoupon+',' +jiaqian+ ','))
    reg = r'<input type="hidden" name="requestId" id="requestId" value="(.*?)">'
    requestId = re.findall(reg, html_temp)
    return tempgoodall,requestId


def request_coupon(jd_list_cookie,jd_list_url,html_json_list,requestId):
    good_temp_html=''
    p=0
    for html_json_temp in html_json_list:
        p=p+1
        if p<10:
            html_json = ast.literal_eval(html_json_temp)
            logTitle = html_json['logTitle']
            couponnum=html_json['couponnum']
            jiaqian = html_json['jiaqian']
            imgUrl = html_json['imgUrl']
            logUnitPrice = html_json['logUnitPrice']
            wareUrl = html_json['pcDetails']
            materialType = html_json['promotionType']
            actId = html_json['materialId']
            couponLink = html_json['couponLink']
            PopId = html_json['PopId']
            materialId = html_json['materialId']
            adOwner = html_json['adOwner']
            skuIdList = html_json['materialId']
            planId = html_json['orienPlanId']
            category = html_json['logCategory']
            saler = html_json['logSaler']
            logCommissionRate = html_json['pcComm']
            RequestURL='https://media.jd.com/gotoadv/getCustomCodeURL'
            jd_coupon_headers = {'Accept': '*/*',
                                 'Accept-Encoding': 'gzip, deflate, br',
                                 'Accept-Language': 'zh-CN,zh;q=0.8',
                                 'Cache-Control': 'no-cache',
                                 'Connection': 'keep-alive',
                                 'Content-Length': '1206',
                                 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                 'Cookie': jd_list_cookie,
                                 'Host': 'media.jd.com',
                                 'Origin': 'https://media.jd.com',
                                 'Pragma': 'no-cache',
                                 'Referer': jd_list_url,
                                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
                                 'X-Requested-With': 'XMLHttpRequest'}
            jd_coupon_data={'adtType':'6',
                            'siteName':'逝去的回忆',
                            'unionWebId':'1523421913',
                            'protocol':'2',
                            'codeType':'2',
                            'type':'1',
                            'positionId':'1533838214',
                            'positionName':'柚子桑',
                            'sizeId':'-1',
                            'logSizeName':'-1',
                            'unionAppId':'-1',
                            'unionMediaId':'-1',
                            'logTitle':logTitle,
                            'imgUrl':imgUrl,
                            'logUnitPrice':logUnitPrice,
                            'wareUrl':wareUrl,
                            'materialType':materialType,
                            'actId':actId,
                            'couponLink':couponLink,
                            'orienPlanId':'-1',
                            'landingPageType':'-1',
                            'PopId':PopId,
                            'materialId':materialId,
                            'adOwner':adOwner,
                            'skuIdList':skuIdList,
                            'planId':planId,
                            'category':category,
                            'saler':saler,
                            'logCommissionRate':logCommissionRate,
                            'requestId':requestId,
                            'isApp':'-1',
                            'shopPlanId':'-1'}
            counpon=requests.post(url=RequestURL, data=jd_coupon_data, headers=jd_coupon_headers).content
            newcoupon=json.loads(counpon)
            newdic=dict(newcoupon.items()+jd_coupon_data.items())
            good_temp_html=good_temp_html+jdgoodhtml(newdic,couponnum,jiaqian)
    return good_temp_html


def jdgoodhtml(newdic,couponnum,jiaqian):
    if newdic['data']['shotCouponUrl']:
        herf = newdic['data']['shotCouponUrl']
    else:
        herf = newdic['data']['shotUrl']
    if newdic['category']:
        shop_title = newdic['category']
    else:
        shop_title = ''
    good_temp_html =  '    <div class="sl-products">\n' \
                                      '        <a href="{}">\n' \
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
                                      '                        <span class="sl-product-price">{}</span>\n' \
                                      '                    </li>\n                    <li class="sl-product-msg-item"></li>\n' \
                                      '                    <li class="sl-product-msg-item">\n' \
                                      '                        <span class="sl-product-price-unit">{}</span>\n' \
                                      '                        <span class="sl-product-price">{}</span>\n' \
                                      '                    </li>\n' \
                                      '                    <li class="sl-product-msg-item"></li>\n' \
                                      '                    <li class="sl-product-msg-item">\n' \
                                      '                        <span class="sl-product-business">券</span><span class="sl-product-price-ora">{}</span>\n' \
                                      '                        <span class="sl-product-comment-count">&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</span>\n' \
                                      '                   </li>\n' \
                                      '                   <li class="sl-product-msg-item"></li>\n' \
                                      '                </ul>\n' \
                                      '            </section>\n' \
                                      '        </article>\n' \
                                      '        </a>\n' \
                                      '    </div>\n'.format(herf,newdic['imgUrl'],
                                                            newdic['logTitle'],shop_title,jiaqian,
                                                            newdic['logUnitPrice'], couponnum)
    return good_temp_html