import requests
import time

def save(name,xml,cookie,headers={},type_='webpy'):
    """
    保存作品
    :param name: 作品名
    :param xml: 作品内容
    :param cookie: COOKIE
    :param headers: 自定义请求头
    :param type_: 作品类型 scratch python cpp
    :return: 返回请求变量
    """
    if headers=={}:
        headers={'Cookie':cookie,
                 'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"
                 }

    base = "https://code.xueersi.com/api/compilers/save"
    data = {"name": name, "xml": xml, "type": type_, "lang": type_, "id": '',
            "original_id": 3, "version": "webpy", "args": [], "planid": 'null', "problemid": '', "projectid": 3,
            "code_complete": 1, "removed": 0, "user_id": 8510061,
            "assets": {"assets": [], "cdns": ["https://livefile.xesimg.com"], "hide_filelist": False}}
    res=requests.post(base,data=data,headers=headers)
    return res

def push(res,name='NONE'):
    """
    发布作品
    :param res: 请求变量
    :param name: 作品名
    :return: 请求变量
    """
    global cookie
    global headers
    res=eval(res.replace('true',"True").replace('false',"False"))
    ID=res['data']['id']
    print(ID)
    base = "https://code.xueersi.com/api/python/%s/publish"  # 作品id
    data = {"projectId": str(ID), "name": name,"description": "", "created_source": "original",
            "hidden_code": 2, "thumbnail": "https://static0.xesimg.com/talcode/assets/py/default-python-thumbnail.png",
            "tags": "其他"}
    res=requests.post(base%ID,headers=headers,data=data)
    return res

def report(cookie,reason,reason_detail,complaint_reason_url,id_):
    """
    举报作品
    :param cookie:COOKIE
    :param reason: 理由
    :param reason_detail: 理由类型 1 2 3等
    :param complaint_reason_url: （被抄袭）源地址
    :param id_: 作品ID
    :return: 请求变量
    """
    base = "https://code.xueersi.com/api/projects/submit_complaint"
    data = {"reason": reason, "reason_detail": reason_detail, "complaint_reason_images": [],
            "complaint_reason_url": complaint_reason_url, "id": id_}

    res = requests.post(base, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33',
        'Cookie': cookie},
                        data=data)
    return res
    
def Send(Content : str,Type : int,Cookie: str,Id_ : int,UserAgent='',headers={})->object:
    """
    发送评论

    type_:
    1:Python（包含webpy等）
    2:Cpp
    3:Scratch
    # 严重警告： 如果不填写会导致发送失败！

    :param Content: 内容
    :param Cookie: COOKIE
    :param Id_: 作品id
    :param Type_: 作品类型
    :param UserAgent: 用户代理（可不填，有默认UA）
    :param headers: 请求头（可不填，会默认设置）
    :return: 访问变量
    """

    if UserAgent == '':
        UserAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.30"

    if headers == {}:
        headers={'Cookie':Cookie,
                 'User-Agent':UserAgent
                 }

    if Type == 1:
        Type='CP_'
    elif Type == 2:
        Type='CC_'
    elif Type == 3:
        Type='CS_'
    else:
        raise ValueError('变量Type 包含意外的值:%s 应为1、2或3'%Type)

    res = requests.post("https://code.xueersi.com/api/comments/submit",
                        headers=headers,
                        data={"appid": 1001108, 'topic_id': Type + str(Id_), 'target_id': '0', 'content': Content})
    return res

def check(ID):
    """
    检查作品是否存在
    :param ID:作品ID
    :return: 作品是否存在（bool）是（True）否（False）
    """
    base="https://code.xueersi.com/api/compilers/v2/%s?id=%s"%(ID,ID)
    res=requests.get(base,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33'})
    f=eval(res.text.replace('null','\'null\'').replace('true','\'true\'').replace('false','\'false\''))
    if 'status_code' in f:
        return False,0
    else:
        if f['data']['published_at'] != '0000-00-00 00:00:00':
            return True
        else:
            return False