import requests

from . import storage


class Core(object):
    def __init__(self):
        """ init 是 core.py 中定义的唯一方法
            alive 是显示 core 是否正在运行的值
                - 您应该调用 logout 方法来更改它
                - 注销后，核心对象可以再次登录
            storageClass 仅使用基本的 python 类型
                - 所以对于高级用途，请自己继承它
            receivingRetryCount 用于接收循环重试
                - 现在是 5 个，但实际上即使是 1 个也足够了
                - 失败就是失败
        """
        self.alive, self.isLogging = False, False
        self.storageClass = storage.Storage(self)
        self.memberList = self.storageClass.memberList
        self.mpList = self.storageClass.mpList
        self.chatroomList = self.storageClass.chatroomList
        self.msgList = self.storageClass.msgList
        self.loginInfo = {}
        self.s = requests.Session()
        self.uuid = None
        self.functionDict = {'FriendChat': {}, 'GroupChat': {}, 'MpChat': {}}
        self.useHotReload, self.hotReloadDir = False, 'itchat.pkl'
        self.receivingRetryCount = 5

    def login(self, enableCmdQR=True, picDir=None, qrCallback=None,
              loginCallback=None, exitCallback=None):
        """ 像 Web WeChat 一样登录
            用于登录
                - 将下载并打开二维码
                - 然后扫描状态为 Logged （记录），它暂停了 for you confirm
                - 最后它登录并显示您的昵称
            选项
                - enableCmdQR：在命令行中显示 qrcode
                    - 整数可用于拟合奇怪的字符长度
                - picDir： 存储 qrcode 的地方
                - qrCallback：应该接受 uuid、status 和 qrcode 的方法
                - loginCallback： 登录成功后的回调
                    - 如果未设置，则清除屏幕并删除 QRcode。
                - exitCallback： 登出后的回调
                    - 它包含调用 logout
            供使用
                ..邮编：:p YTHON

导入 itchat
                    itchat.login（）

它在 components/login.py
            当然，登录中的每一个动作都可以在外部调用
                - 您可以扫描源代码以了解
                - 并根据您的需求进行修改
        """
        raise NotImplementedError()

    def get_QRuuid(self):
        """ 获取 QR Code 的 UUID
            uuid 是 qrcode 的符号
                - 要登录，您需要先获取 UUID
                - 要下载 QRcode，您需要将 UUID 传递给它
                - 要检查登录状态，还需要 UUID
            如果 uuid 已超时，则只需获取另一个
            它在 components/login.py
        """
        raise NotImplementedError()

    def get_QR(self, uuid=None, enableCmdQR=False, picDir=None, qrCallback=None):
        """ 下载并显示 QR Code
            选项
                - uuid： 如果未设置 uuid，则使用您获取的最新 uuid
                - enableCmdQR： 在 cmd 中显示 qrcode
                - picDir：qrcode 的存储位置
                - qrCallback：应该接受 uuid、status 和 qrcode 的方法
            它在 components/login.py
        """
        raise NotImplementedError()

    def check_login(self, uuid=None):
        """ 检查登录状态
            选项：
                - uuid： 如果未设置 uuid，则使用您获取的最新 uuid
            对于返回值：
                - 将返回一个字符串
                - 对于返回值的含义
                    - 200：登录成功
                    - 201：等待 Press Confirm
                    - 408：UUID 超时
                    - 0 ： 未知错误
            用于处理：
                - 设置了 syncUrl 和 fileUrl
                - BaseRequest 已设置
            阻止，直到达到上述任何状态
            它在 components/login.py
        """
        raise NotImplementedError()

    def web_init(self):
        """ 获取初始化所需的信息
            用于处理：
                - 设置自己的帐户信息
                - 设置了 inviteStartCount
                - 设置 syncKey
                - 获取部分联系人
            它在 components/login.py
        """
        raise NotImplementedError()

    def show_mobile_login(self):
        """ 显示 Web Wechat 登录标志
            标牌在手机微信顶部
            sign 将在一段时间后添加，即使不调用此函数
            它在 components/login.py
        """
        raise NotImplementedError()

    def start_receiving(self, exitCallback=None, getReceivingFnOnly=False):
        """ 打开一个线程以进行 Heart 循环并接收消息
            选项：
                - exitCallback： 登出后的回调
                    - 它包含调用 logout
                - getReceivingFnOnly：如果不会创建和启动 True 线程。相反，将返回 receive fn。
            用于处理：
                - 消息：消息被格式化并传递给已注册的 FN
                - Contact ： 收到相关信息时，聊天室会更新
            它在 components/login.py
        """
        raise NotImplementedError()

    def get_msg(self):
        ''' 获取消息
            用于获取
                - method 阻塞一段时间，直到
                    - 将接收新消息

                    - 或者他们喜欢的任何时间
                - 使用返回的 synccheckkey 更新 synckey
            它在 components/login.py
        '''
        raise NotImplementedError()

    def logout(self):
        ''' logout
            if core is now alive
                logout will tell wechat backstage to logout
            and core gets ready for another login
            it is defined in components/login.py
        '''
        raise NotImplementedError()

    def update_chatroom(self, userName, detailedMember=False):
        ''' update chatroom
            for chatroom contact
                - a chatroom contact need updating to be detailed
                - detailed means members, encryid, etc
                - auto updating of heart loop is a more detailed updating
                    - member uin will also be filled
                - once called, updated info will be stored
            for options
                - userName: 'UserName' key of chatroom or a list of it
                - detailedMember: whether to get members of contact
            it is defined in components/contact.py
        '''
        raise NotImplementedError()

    def update_friend(self, userName):
        ''' update chatroom
            for friend contact
                - once called, updated info will be stored
            for options
                - userName: 'UserName' key of a friend or a list of it
            it is defined in components/contact.py
        '''
        raise NotImplementedError()

    def get_contact(self, update=False):
        ''' fetch part of contact
            for part
                - all the massive platforms and friends are fetched
                - if update, only starred chatrooms are fetched
            for options
                - update: if not set, local value will be returned
            for results
                - chatroomList will be returned
            it is defined in components/contact.py
        '''
        raise NotImplementedError()

    def get_friends(self, update=False):
        ''' fetch friends list
            for options
                - update: if not set, local value will be returned
            for results
                - a list of friends' info dicts will be returned
            it is defined in components/contact.py
        '''
        raise NotImplementedError()

    def get_chatrooms(self, update=False, contactOnly=False):
        ''' fetch chatrooms list
            for options
                - update: if not set, local value will be returned
                - contactOnly: if set, only starred chatrooms will be returned
            for results
                - a list of chatrooms' info dicts will be returned
            it is defined in components/contact.py
        '''
        raise NotImplementedError()

    def get_mps(self, update=False):
        ''' fetch massive platforms list
            for options
                - update: if not set, local value will be returned
            for results
                - a list of platforms' info dicts will be returned
            it is defined in components/contact.py
        '''
        raise NotImplementedError()

    def set_alias(self, userName, alias):
        ''' set alias for a friend
            for options
                - userName: 'UserName' key of info dict
                - alias: new alias
            it is defined in components/contact.py
        '''
        raise NotImplementedError()

    def set_pinned(self, userName, isPinned=True):
        ''' set pinned for a friend or a chatroom
            for options
                - userName: 'UserName' key of info dict
                - isPinned: whether to pin
            it is defined in components/contact.py
        '''
        raise NotImplementedError()

    def accept_friend(self, userName, v4, autoUpdate=True):
        ''' accept a friend or accept a friend
            for options
                - userName: 'UserName' for friend's info dict
                - status:
                    - for adding status should be 2
                    - for accepting status should be 3
                - ticket: greeting message
                - userInfo: friend's other info for adding into local storage
            it is defined in components/contact.py
        '''
        raise NotImplementedError()

    def get_head_img(self, userName=None, chatroomUserName=None, picDir=None):
        ''' place for docs
            for options
                - if you want to get chatroom header: only set chatroomUserName
                - if you want to get friend header: only set userName
                - if you want to get chatroom member header: set both
            it is defined in components/contact.py
        '''
        raise NotImplementedError()

    def create_chatroom(self, memberList, topic=''):
        ''' create a chatroom
            for creating
                - its calling frequency is strictly limited
            for options
                - memberList: list of member info dict
                - topic: topic of new chatroom
            it is defined in components/contact.py
        '''
        raise NotImplementedError()

    def set_chatroom_name(self, chatroomUserName, name):
        ''' set chatroom name
            for setting
                - it makes an updating of chatroom
                - which means detailed info will be returned in heart loop
            for options
                - chatroomUserName: 'UserName' key of chatroom info dict
                - name: new chatroom name
            it is defined in components/contact.py
        '''
        raise NotImplementedError()

    def delete_member_from_chatroom(self, chatroomUserName, memberList):
        ''' deletes members from chatroom
            for deleting
                - you can't delete yourself
                - if so, no one will be deleted
                - strict-limited frequency
            for options
                - chatroomUserName: 'UserName' key of chatroom info dict
                - memberList: list of members' info dict
            it is defined in components/contact.py
        '''
        raise NotImplementedError()

    def add_member_into_chatroom(self, chatroomUserName, memberList,
                                 useInvitation=False):
        ''' add members into chatroom
            for adding
                - you can't add yourself or member already in chatroom
                - if so, no one will be added
                - if member will over 40 after adding, invitation must be used
                - strict-limited frequency
            for options
                - chatroomUserName: 'UserName' key of chatroom info dict
                - memberList: list of members' info dict
                - useInvitation: if invitation is not required, set this to use
            it is defined in components/contact.py
        '''
        raise NotImplementedError()

    def send_raw_msg(self, msgType, content, toUserName):
        ''' 许多消息以一种常见的方式发送
            用于演示
                ..代码：： Python

@itchat.msg_register（itchat.content.CARD）
                    def 回复（msg）：
                        itchat.send_raw_msg（msg['MsgType']， msg['内容']， msg['FromUserName']）

这里有一些小技巧，你可能会自己发现
            但请记住，它们是诡计
            它在 components/messages.py 中定义
        '''
        raise NotImplementedError()

    def send_msg(self, msg='Test Message', toUserName=None):
        ''' 发送纯文本消息
            选项
                - msg：如果 msg 中有非 ASCII 单词，则应为 unicode
                - toUserName： 好友字典的 'UserName' 键
            它在 components/messages.py 中定义
        '''
        raise NotImplementedError()

    def upload_file(self, fileDir, isPicture=False, isVideo=False,
                    toUserName='filehelper', file_=None, preparedFile=None):
        ''' 将文件上传到服务器并获取 mediaId
            选项
                - fileDir： 准备上传的文件的目录
                - isPicture：文件是否为图片
                - isVideo：文件是否为视频
            对于返回值
                将返回一个 ReturnValue
                如果成功，则 mediaId 位于 r['MediaId'] 中
            它在 components/messages.py 中定义
        '''
        raise NotImplementedError()

    def send_file(self, fileDir, toUserName=None, mediaId=None, file_=None):
        ''' 发送附件
            选项
                - fileDir： 准备上传的文件的目录
                - mediaId： 文件的 mediaId。
                    - 如果设置，文件将不会上传两次
                - toUserName： 好友字典的 'UserName' 键
            它在 components/messages.py 中定义
        '''
        raise NotImplementedError()

    def send_image(self, fileDir=None, toUserName=None, mediaId=None, file_=None):
        ''' 发送图片
            选项
                - fileDir： 准备上传的文件的目录
                    - 如果是 gif，请将其命名为 'xx.gif'
                - mediaId： 文件的 mediaId。
                    - 如果设置，文件将不会上传两次
                - toUserName： 好友字典的 'UserName' 键
            它在 components/messages.py 中定义
        '''
        raise NotImplementedError()

    def send_video(self, fileDir=None, toUserName=None, mediaId=None, file_=None):
        ''' 发送视频
            选项
                - fileDir： 准备上传的文件的目录
                    - 如果设置了 mediaId，则无需设置 fileDir
                - mediaId： 文件的 mediaId。
                    - 如果设置，文件将不会上传两次
                - toUserName： 好友字典的 'UserName' 键
            它在 components/messages.py 中定义
        '''
        raise NotImplementedError()

    def send(self, msg, toUserName=None, mediaId=None):
        ''' wrapped 函数
            选项
                - msg：以不同字符串开头的消息表示不同的类型
                    - 字符串类型列表： ['@fil@'， '@img@'， '@msg@'， '@vid@']
                    - 它们用于文件、图像、纯文本、视频
                    - 如果它们都不匹配，它将以纯文本的形式发送
                - toUserName： 好友字典的 'UserName' 键
                - mediaId：如果设置，则不会重复上传
            它在 components/messages.py 中定义
        '''
        raise NotImplementedError()

    def revoke(self, msgId, toUserName, localId=None):
        ''' 撤销带有其 和 msgId 的消息
            选项
                - msgId：服务器上的消息 ID
                - toUserName： 好友字典的 'UserName' 键
                - localId：本地的消息 ID（可选）
            它在 components/messages.py 中定义
        '''
        raise NotImplementedError()

    def dump_login_status(self, fileDir=None):
        ''' 将登录状态转储到特定文件
            for 选项
                - fileDir： 用于转储登录状态的目录
            它在 components/hotreload.py 中定义
        '''
        raise NotImplementedError()

    def load_login_status(self, fileDir,
                          loginCallback=None, exitCallback=None):
        ''' 从特定文件加载登录状态
            for 选项
                - fileDir： 用于加载登录状态的文件
                - loginCallback： 登录成功后的回调
                    - 如果未设置，则清除屏幕并删除 QRcode。
                - exitCallback： 登出后的回调
                    - 它包含调用 logout
            它在 components/hotreload.py 中定义
        '''
        raise NotImplementedError()

    def auto_login(self, hotReload=False, statusStorageDir='itchat.pkl',
                   enableCmdQR=False, picDir=None, qrCallback=None,
                   loginCallback=None, exitCallback=None):
        ''' log in like web wechat does
            for log in
                - a QR code will be downloaded and opened
                - then scanning status is logged, it paused for you confirm
                - finally it logged in and show your nickName
            for options
                - hotReload: enable hot reload
                - statusStorageDir: dir for storing log in status
                - enableCmdQR: show qrcode in command line
                    - integers can be used to fit strange char length
                - picDir: place for storing qrcode
                - loginCallback: callback after successfully logged in
                    - if not set, screen is cleared and qrcode is deleted
                - exitCallback: callback after logged out
                    - it contains calling of logout
                - qrCallback: method that should accept uuid, status, qrcode
            for usage
                ..code::python

                    import itchat
                    itchat.auto_login()

            it is defined in components/register.py
            and of course every single move in login can be called outside
                - you may scan source code to see how
                - and modified according to your own demond
        '''
        raise NotImplementedError()

    def configured_reply(self):
        ''' determine the type of message and reply if its method is defined
            however, I use a strange way to determine whether a msg is from massive platform
            I haven't found a better solution here
            The main problem I'm worrying about is the mismatching of new friends added on phone
            If you have any good idea, pleeeease report an issue. I will be more than grateful.
        '''
        raise NotImplementedError()

    def msg_register(self, msgType,
                     isFriendChat=False, isGroupChat=False, isMpChat=False):
        ''' a decorator constructor
            return a specific decorator based on information given
        '''
        raise NotImplementedError()

    def run(self, debug=True, blockThread=True):
        ''' start auto respond
            for option
                - debug: if set, debug info will be shown on screen
            it is defined in components/register.py
        '''
        raise NotImplementedError()

    def search_friends(self, name=None, userName=None, remarkName=None, nickName=None,
                       wechatAccount=None):
        return self.storageClass.search_friends(name, userName, remarkName,
                                                nickName, wechatAccount)

    def search_chatrooms(self, name=None, userName=None):
        return self.storageClass.search_chatrooms(name, userName)

    def search_mps(self, name=None, userName=None):
        return self.storageClass.search_mps(name, userName)
