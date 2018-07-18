from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail,send_mass_mail
from django.conf import settings
from django.template import loader
from .my_util import get_random_str
from django.core.cache import cache
import logging
logger = logging.getLogger('django')
# Create your views here.


def send_my_email(req):
    title = '阿里叫你回家'
    msg = '恭喜你获得一瓶老干妈'
    email_from = settings.DEFAULT_FROM_EMAIL
    recieve = [
        'liuda@1000phone.com',
    ]
    send_mail(title, msg, email_from, recieve)
    return HttpResponse('ok')

def send_email_v1(req):
    title = '阿里叫你回家'
    msg = ''
    email_from = settings.DEFAULT_FROM_EMAIL
    recieve = [
        'liuda@1000phone.com',
    ]
    #加载模板
    template = loader.get_template('email.html')
    html_str = template.render({'msg': "双击666"})
    #发送邮件
    send_mail(title, msg, email_from, recieve, html_message=html_str)
    return HttpResponse('ok')


def verify(req):
    if req.method == 'GET':
        return render(req, 'verify.html')
    else:
        param = req.POST
        eamil = param.get("email")
        #生成随机字符
        random_str = get_random_str()
        #拼接验证链接
        url ='http://123.207.38.181:12350/item8/active' + random_str
        #加载激活模板
        tmp = loader.get_template('active.html')
        #渲染
        html_str = tmp.render({'url':url})
        #准备邮件数据
        title = '阿里叫你回家'
        msg = ''
        email_from = settings.DEFAULT_FROM_EMAIL
        recieve = [
            eamil,
        ]
        # 加载模板
        send_mail(title, msg, email_from, recieve, html_message=html_str)
        cache.set(random_str, eamil, 120)
        return HttpResponse('ok')


def active(req, random_str):
    res = cache.get(random_str)
    if res:
        return HttpResponse(res+"激活成功")
    else:
        return HttpResponse("验证链接失效")

def send_many_mail(req):
    title = '阿里叫你回家'
    content1 = '恭喜你获得一瓶老干妈'
    email_from = settings.DEFAULT_FROM_EMAIL
    recieve1 = [

        '554468924@qq.com',
    ]
    content2 = 'good！！！'
    msg1 = (title, content1, email_from, recieve1)
    msg2 = (title, content2, email_from, ['253632775@qq.com'])
    send_mass_mail((msg1, msg2))
    return HttpResponse("ok")


def text_log(req):
    logger.info('要下课了')
    return HttpResponse('好开心')