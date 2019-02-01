config = {}
config['WxGroup'] = 'The Language'
config['QqGroupId'] = 949144378

import wxpy
wxbot = wxpy.Bot()
wxgroup = wxbot.groups().search(config['WxGroup'])[0]
@wxbot.register(wxgroup, wxpy.TEXT)
def wxbot_receive_raw(rawmsg):
	print(rawmsg)
	msg = {}
	msg['sender'] = rawmsg.member
	msg['text'] = rawmsg.text
	receive_wx_text(msg)

from aiocqhttp import CQHttp
import asyncio

qqbot = CQHttp(access_token='',
             enable_http_post=False)

@qqbot.on_message()
async def qq_handle_msg(context):
	if context['post_type'] == 'message' and context['message_type'] == 'group' and context['group_id'] == config['QqGroupId']:
		print(context)
		msg = {}
		msg['sender'] = context['sender']['nickname']
		msg['text'] = context['message']
		receive_qq_text(msg)

def receive_wx_text(msg):
	asyncio.run(qqbot.send_group_msg(group_id=config['QqGroupId'], message='【微信】{}|{}'.format(msg['sender'], msg['text'])))

def receive_qq_text(msg):
	wxgroup.send('【QQ】{}|{}'.format(msg['sender'], msg['text']))

qqbot.run(host='127.0.0.1', port=8194)
wxbot.join()
