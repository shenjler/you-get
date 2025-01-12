#!/usr/bin/env python
import base64
import requests
import binascii
import subprocess


from ..common import *
import random
import string
import ctypes
from json import loads
from urllib import request

__all__ = ['ixigua_download', 'ixigua_download_playlist_by_url']

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 "
                  "Safari/537.36",
    "Connection":"keep-alive",
    "Cache-Control":"no-cache",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Dest":"document",

}


def int_overflow(val):
    maxint = 2147483647
    if not -maxint - 1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val


def unsigned_right_shitf(n, i):
    if n < 0:
        n = ctypes.c_uint32(n).value
    if i < 0:
        return -int_overflow(n << abs(i))
    return int_overflow(n >> i)


def get_video_url_from_video_id(video_id):
    """Splicing URLs according to video ID to get video details"""
    # from js
    data = [""] * 256
    for index, _ in enumerate(data):
        t = index
        for i in range(8):
            t = -306674912 ^ unsigned_right_shitf(t, 1) if 1 & t else unsigned_right_shitf(t, 1)
        data[index] = t

    def tmp():
        rand_num = random.random()
        path = "/video/urls/v/1/toutiao/mp4/{video_id}?r={random_num}".format(video_id=video_id,
                                                                              random_num=str(rand_num)[2:])
        e = o = r = -1
        i, a = 0, len(path)
        while i < a:
            e = ord(path[i])
            i += 1
            if e < 128:
                r = unsigned_right_shitf(r, 8) ^ data[255 & (r ^ e)]
            else:
                if e < 2048:
                    r = unsigned_right_shitf(r, 8) ^ data[255 & (r ^ (192 | e >> 6 & 31))]
                    r = unsigned_right_shitf(r, 8) ^ data[255 & (r ^ (128 | 63 & e))]
                else:
                    if 55296 <= e < 57344:
                        e = (1023 & e) + 64
                        i += 1
                        o = 1023 & t.url(i)
                        r = unsigned_right_shitf(r, 8) ^ data[255 & (r ^ (240 | e >> 8 & 7))]
                        r = unsigned_right_shitf(r, 8) ^ data[255 & (r ^ (128 | e >> 2 & 63))]
                        r = unsigned_right_shitf(r, 8) ^ data[255 & (r ^ (128 | o >> 6 & 15 | (3 & e) << 4))]
                        r = unsigned_right_shitf(r, 8) ^ data[255 & (r ^ (128 | 63 & o))]
                    else:
                        r = unsigned_right_shitf(r, 8) ^ data[255 & (r ^ (224 | e >> 12 & 15))]
                        r = unsigned_right_shitf(r, 8) ^ data[255 & (r ^ (128 | e >> 6 & 63))]
                        r = unsigned_right_shitf(r, 8) ^ data[255 & (r ^ (128 | 63 & e))]

        return "https://ib.365yg.com{path}&s={param}".format(path=path, param=unsigned_right_shitf(r ^ -1, 0))

    while 1:
        url = tmp()
        if url.split("=")[-1][0] != "-":  # 参数s不能为负数
            return url


# __ac_nonce=061c6d40b006f0e0cd18b; 
# __ac_signature=_02B4Z6wo00f01g2hi9wAAIDCjaNxnHyZXh4NgY9AAOK879; 
# __ac_referer=__ac_blank
def get_signature(__ac_nonce):
    cmd = 'node -e "require(\\"%s\\").init(\\"%s\\")"' % ('C:\\\\Users\\\\user\\\\Desktop\\\\test.js', __ac_nonce)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True,
                         stderr=subprocess.PIPE)
    res, err = p.communicate()
    sign = res.decode().replace("\n","")
    # 读取结果
    print('结果是:', sign)

    # out_bytes = subprocess.check_output(['node D:\\you-get\\src\\you_get\\extractors\\test.js',__ac_nonce],stderr=subprocess.STDOUT)
    # log.e("out_bytes: {}".format(out_bytes))
    # sign = os.popen('node sign.js {ac_nonce}'.format(__ac_nonce)).read()
    return "__ac_signature=" + sign+";"

def ixigua_download2(url, output_dir='.', merge=True, info_only=False, **kwargs):
    session = requests.session()
    # 需要先访问一次视频网站获取cookies才行
    resp = session.get(url,headers=headers)

    _cookies = []
    if resp.headers['Set-Cookie']:
        for c in resp.headers['Set-Cookie'].split("httponly,"):
            _cookies.append(c.strip().split(' ')[0])
    headers['cookie'] = ' '.join(_cookies)
    # headers[':authority']='www.ixigua.com'
    # headers[':method']='GET'
    # headers[':path']='/7043782360277451271'
    # headers[':scheme']='https'
    # headers['accept']='text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    # headers['accept-encoding']='gzip, deflate'
    # headers['sec-ch-ua']='" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"'
    # headers['sec-ch-ua-mobile']='?0'
    # headers['sec-ch-ua-platform']="Windows"
    # headers['sec-fetch-dest']='document'
    # headers['sec-fetch-mode']='navigate'
    # headers['sec-fetch-site']='same-origin'
    # headers['upgrade-insecure-requests']='1'
    # headers['referer'] = url
    # headers["user-agent"]="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    # headers['cookie'] = "__ac_nonce=061c7029800621ea58f8d; __ac_signature=_02B4Z6wo00f01ajpOhgAAIDBKOvAW222ue2oyT6AAAv-94; __ac_referer=__ac_blank"
    # log.e(headers)

    suffix = "?wid_try=1"
    if not url.endswith(suffix):
        url +=suffix
    result = get_content(url, headers=headers)
    title = match1(result, r'"video":.*?"title":"(.*?)"')
    # log.e("title: {}".format(title))
    if not title:
        return
    url2 = match1(result, r'definition":"720p"[\s|\S]*?main_url":"(.*?)"')
    videoUrl= base64.b64decode(url2).decode("utf8","ignore").replace(r".M","?")
    # log.e("videoUrl: {}".format(videoUrl))
    
    if videoUrl:
        video_url = videoUrl
        size = None
        download_urls([video_url], title, "mp4", size, output_dir, merge=merge, headers=headers, **kwargs)

    audio = match1(result, r'dynamic_audio_list".*?"main_url":"(.*?)"')
    if audio :
        audioUrl = base64.b64decode(audio).decode("utf8","ignore").replace(r".M","?")
        size =None
        download_urls([audioUrl], title, "m4a", size, output_dir, merge=merge, headers=headers, **kwargs)
        cmd = 'ffmpeg -i "%s.mp4" -i "%s.m4a" -vcodec copy -acodec copy -y "%sAV.mp4" ' % (title, title, title)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True,
                            stderr=subprocess.PIPE)
        res, err = p.communicate()
        # https://www.cnblogs.com/security-darren/p/4733368.html
        if p.returncode == 0 :
            afile = "%s.m4a" % (title)
            vfile = "%s.mp4" % (title)
            log.i("")
            log.i("remove afile %s" %(afile))
            os.remove(afile) 
            log.i("remove vfile %s" %(vfile))
            os.remove(vfile) 




def ixigua_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    # example url: https://www.ixigua.com/i6631065141750268420/#mid=63024814422
    resp = urlopen_with_retry(request.Request(url))
    html = resp.read().decode('utf-8')

    _cookies = []
    for c in resp.getheader('Set-Cookie').split("httponly,"):
        _cookies.append(c.strip().split(' ')[0])
    headers['cookie'] = ' '.join(_cookies)

    conf = loads(match1(html, r"window\.config = (.+);"))
    if not conf:
        log.e("Get window.config from url failed, url: {}".format(url))
        return
    verify_url = conf['prefix'] + conf['url'] + '?key=' + conf['key'] + '&psm=' + conf['psm'] \
        + '&_signature=' + ''.join(random.sample(string.ascii_letters + string.digits, 31))
    try:
        ok = get_content(verify_url)
    except Exception as e:
        ok = e.msg
    if ok != 'OK':
        log.e("Verify failed, verify_url: {}, result: {}".format(verify_url, ok))
        return
    html = get_content(url, headers=headers)

    video_id = match1(html, r"\"vid\":\"([^\"]+)")
    title = match1(html, r"\"player__videoTitle\">.*?<h1.*?>(.*)<\/h1><\/div>")
    if not video_id:
        log.e("video_id not found, url:{}".format(url))
        return
    video_info_url = get_video_url_from_video_id(video_id)
    video_info = loads(get_content(video_info_url))
    if video_info.get("code", 1) != 0:
        log.e("Get video info from {} error: server return code {}".format(video_info_url, video_info.get("code", 1)))
        return
    if not video_info.get("data", None):
        log.e("Get video info from {} error: The server returns JSON value"
              " without data or data is empty".format(video_info_url))
        return
    if not video_info["data"].get("video_list", None):
        log.e("Get video info from {} error: The server returns JSON value"
              " without data.video_list or data.video_list is empty".format(video_info_url))
        return
    if not video_info["data"]["video_list"].get("video_1", None):
        log.e("Get video info from {} error: The server returns JSON value"
              " without data.video_list.video_1 or data.video_list.video_1 is empty".format(video_info_url))
        return
    bestQualityVideo = list(video_info["data"]["video_list"].keys())[-1] #There is not only video_1, there might be video_2
    size = int(video_info["data"]["video_list"][bestQualityVideo]["size"])
    print_info(site_info=site_info, title=title, type="mp4", size=size)  # 该网站只有mp4类型文件
    if not info_only:
        video_url = base64.b64decode(video_info["data"]["video_list"][bestQualityVideo]["main_url"].encode("utf-8"))
        download_urls([video_url.decode("utf-8")], title, "mp4", size, output_dir, merge=merge, headers=headers, **kwargs)


def ixigua_download_playlist_by_url(url, output_dir='.', merge=True, info_only=False, **kwargs):
    assert "user" in url, "Only support users to publish video list,Please provide a similar url:" \
                          "https://www.ixigua.com/c/user/6907091136/"

    user_id = url.split("/")[-2] if url[-1] == "/" else url.split("/")[-1]
    params = {"max_behot_time": "0", "max_repin_time": "0", "count": "20", "page_type": "0", "user_id": user_id}
    while 1:
        url = "https://www.ixigua.com/c/user/article/?" + "&".join(["{}={}".format(k, v) for k, v in params.items()])
        video_list = loads(get_content(url, headers=headers))
        params["max_behot_time"] = video_list["next"]["max_behot_time"]
        for video in video_list["data"]:
            ixigua_download("https://www.ixigua.com/i{}/".format(video["item_id"]), output_dir, merge, info_only,
                            **kwargs)
        if video_list["next"]["max_behot_time"] == 0:
            break


site_info = "ixigua.com"
download = ixigua_download2
download_playlist = ixigua_download_playlist_by_url
