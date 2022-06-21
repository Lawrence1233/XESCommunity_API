import requests
import time

def save(Name :str,xml,Cookie :str,headers={},type_='webpy')->object:
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
        headers={'Cookie':Cookie,
                 'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"
                 }

    base = "https://code.xueersi.com/api/compilers/save"
    data = {"name": Name, "xml": xml, "type": type_, "lang": type_, "id": '',
            "original_id": 3, "version": "webpy", "args": [], "planid": 'null', "problemid": '', "projectid": 3,
            "code_complete": 1, "removed": 0, "user_id": 8510061,
            "assets": {"assets": [], "cdns": ["https://livefile.xesimg.com"], "hide_filelist": False}}
    res=requests.post(base,data=data,headers=headers)
    return res

def push(res,name='NONE')->object:
    """
    发布作品
    :param res: 请求变量
    :param name: 作品名
    :return: 请求变量
    """

    res=eval(res.replace('true',"True").replace('false',"False"))
    ID=res['data']['id']
    print(ID)
    base = "https://code.xueersi.com/api/python/%s/publish"  # 作品id
    data = {"projectId": str(ID), "name": name,"description": "", "created_source": "original",
            "hidden_code": 2, "thumbnail": "https://static0.xesimg.com/talcode/assets/py/default-python-thumbnail.png",
            "tags": "其他"}
    res=requests.post(base%ID,headers=headers,data=data)
    return res

def report(Cookie :str,Reason :str,reason_detail :int,complaint_reason_url :str,id_ :int)->object:
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
    data = {"reason": Reason, "reason_detail": reason_detail, "complaint_reason_images": [],
            "complaint_reason_url": complaint_reason_url, "id": id_}

    res = requests.post(base, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33',
        'Cookie': Cookie},
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

def get_info(ID :int)->dict:
    """
    获取作品信息
    :param ID: 作品ID
    :return: dict
    """
    base="https://code.xueersi.com/api/compilers/v2/%s?id=%s"%(ID,ID)
    res=requests.get(base,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33'})
    f=eval(res.text.replace('null','\'null\'').replace('true','\'true\'').replace('false','\'false\''))
    return f


def check(ID) -> bool:
    """
    检查作品是否存在
    :param ID:作品ID
    :return: 作品是否存在（bool）是（True）否（False）
    """
    get_info(ID)
    if 'status_code' in f:
        return False
    else:
        if f['data']['published_at'] != '0000-00-00 00:00:00':
            return True
        else:
            return False


def parse(Dict :dict)->dict:
    """
    解析作品常用信息

    name: 作品名
    type: 类型（homework或normal等）
    description: 通常为简介，也有可能显示在xml项
    xml: 可能为简介
    user_id: 作者ID
    thumbnail: 封面链接
    modified_at: 最后一次修改日期
    likes: 点赞
    views: 浏览、观看数
    comments: 评论数
    deleted_at: 删除时间（通常为空）
    created_at: 创建时间
    updated_at: 提交时间

    :param Dict: get_info的返回值（或其他可分析的字典）
    :return:


    """
    if 'status_code' in Dict:#失败
        return {'stat':'0','msg':Dict['msg']}

    _output={
        "name":Dict['data']['name'],
        'type':Dict['data']['type'],
        'description':Dict['data']['description'],
        'xml': Dict['data']['xml'],
        'user_id': Dict['data']['user_id'],
        'thumbnail':Dict['data']['thumbnail'],
        'modified_at':Dict['data']['modified_at'],
        'likes':Dict['data']['likes'],
        'views':Dict['data']['views'],
        'comments':Dict['data']['comments'],
        'deleted_at':Dict['data']['deleted_at'],
        'created_at':Dict['data']['created_at'],
        'updated_at':Dict['data']['updated_at']
    }
    return _output

def get_user_info(user_id,cookie='')->dict:
    """
    获取用户信息

    已知信息：
    fans 粉丝
    follows 关注
    is_my 是我自己
    realname 真名
    signature 个性签名

    协议：GET
    :param user_id 用户id
    :return:
    """
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33'
    }
    if cookie != '':
        _output=requests.get('https://code.xueersi.com/api/space/profile?user_id=%s'%user_id,headers,cookies=cookie)
    else:
        _output=requests.get('https://code.xueersi.com/api/space/profile?user_id=%s' % user_id, headers)
    _output=eval(_output.text.replace('true','True').replace('false','False'))
    return _output

def get_index_info(user_id)->dict:
    """
    首页信息
    https://code.xueersi.com/api/space/index?user_id=?

    已知信息：（data下）
    overview 我的成就
    fans 粉丝列表
    favorites 收藏列表
    follows 关注列表
    representative_work 代表作信息
    works 作品列表

    协议 GET
    :param user_id: 用户id
    :return: 输出以上
    """
    _output=requests.get('https://code.xueersi.com/api/space/index?user_id=%s'%user_id)
    _output=eval(_output.text.replace('true','True').replace('false','False'))
    return _output




