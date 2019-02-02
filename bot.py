import wxpy
from aiocqhttp import CQHttp
import asyncio
import threading

bots=[]
def bots_add(set_receive_callback, send_message):
    id=str(set_receive_callback)+str(send_message)
    def on_receive(msg):
        for bot in bots:
            if bot != send_message:
                msg = '[{}]{}({})\n{}'.format(id, msg['sender'], msg['sender_id'], msg['message'])
                print(str(bot)+"('"+msg+"')");
                bot(msg)
    set_receive_callback(on_receive)
    bots.append(send_message)

def bots_add_wechat_groupName(group_name):
    wxbot = wxpy.Bot()
    wxbot.enable_puid()
    wxgroup = wxbot.groups().search(group_name)[0]
    wxbot_receiver = None
    def set_wxbot_receiver(on_receive):
        nonlocal wxbot_receiver
        wxbot_receiver = on_receive
    @wxbot.register(wxgroup, wxpy.TEXT)
    def wxbot_receive_raw(rawmsg):
        print(rawmsg)
        msg = {}
        msg['sender'] = rawmsg.member.name
        msg['sender_id'] = rawmsg.member.puid
        msg['message'] = rawmsg.text
        wxbot_receiver(msg)
    def wxbot_sendmsg(message):
        wxgroup.send(message)
    bots_add(set_wxbot_receiver, wxbot_sendmsg)

def bots_add_qq_cqhttp_groupId(
        api_root = None,
        access_token = None,
        secret = None,
        enable_http_post = False,
        message_class = None,
        host = '127.0.0.1',
        port = None,
        group_id = None):
    qqbot = CQHttp(api_root=api_root,
                   access_token=access_token,
                   secret=secret,
                   enable_http_post=enable_http_post,
                   message_class=message_class)
    qqbot_receiver = None
    def set_qqbot_receiver(on_receive):
        nonlocal qqbot_receiver
        qqbot_receiver = on_receive
    @qqbot.on_message()
    async def qq_handle_msg(context):
        if context['post_type'] == 'message' and context['message_type'] == 'group' and context['group_id'] == group_id:
            print(context)
            msg = {}
            msg['sender'] = context['sender']['nickname']
            msg['sender_id'] = context['sender']['user_id']
            msg['message'] = context['message']
            qqbot_receiver(msg)
    def qqbot_sendmsg(message):
        asyncio.run(qqbot.send_group_msg(group_id=group_id, message=message))
    bots_add(set_qqbot_receiver, qqbot_sendmsg)

    def run():
        from hypercorn.asyncio import serve
        from hypercorn.config import Config
        config = Config()
        config.bind = [host+":"+str(port)]
        asyncio.run(serve(qqbot.asgi, config))
    run() # 阻塞！
    #qqbot.run(host=host, port=port)

with open('conf.py', 'r', encoding='utf-8') as f:
    conf = f.read()
#WIP#eval(conf)

wxpy.embed()
