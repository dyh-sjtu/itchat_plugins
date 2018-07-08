# -*- coding: utf-8 -*-
# @author dyh_sjtu@163.com
# @time 05/07/2018 4:16 PM
# @function to count the suitable time for people who can take a bus by YiDong


import itchat
from itchat.content import *
import re

msg_arr = []


@itchat.msg_register(TEXT, isGroupChat=True)
def receive_msg(msg):
    # groups = itchat.get_chatrooms(update=True)
    # friends = itchat.get_friends(update=True)
    # print("群数量:", len(groups))
    # for i in range(0, len(groups)):
    #     print(i+1, "--", groups[i]['NickName'], groups[i]['MemberCount'], "人", groups[i])
    # print("好友数量", len(friends)-1)
    # for f in range(1, len(friends)):  # 第0个好友是自己,不统计
    #     if friends[f]['RemarkName']:  # 优先使用好友的备注名称，没有则使用昵称
    #         user_name = friends[f]['RemarkName']
    #     else:
    #         user_name = friends[f]['NickName']
    #     sex = friends[f]['Sex']
    #     print(f, "--", user_name, sex)
    print(msg)
    try:
        if msg.text.index('早上') >= 0 and msg.text.index('晚上') >= 0 and msg['User']['NickName'] == '2041':
            # 字典存储消息对象
            user = msg['ActualNickName'] or msg['FromUserName']
            raw = msg.text
            pattern = re.compile(r'\d+')
            text_arr = pattern.findall(raw)
            if len(text_arr) == 4:
                text = ':'.join(text_arr[0:2]) + '-' + ':'.join(text_arr[2:])
                if len(msg_arr) == 0 or find_index_people(user, msg_arr) == -1:
                    msg_dict = {'text': text, 'from': user}
                    msg_arr.append(msg_dict)
                    # todo 将群关于乘车的时间发送给服务器
                elif find_index_people(user, msg_arr) > -1:
                    index = find_index_people(user, msg_arr)
                    if msg_arr[index]['text'] != text:
                        msg_arr[index]['text'] = text
                    else:
                        pass
            show_count(msg_arr, msg)
    except ValueError:
        print('没有类似消息出现!')


def find_index_people(user, arr):
    index = -1
    for idx in range(len(arr)):
        if arr[idx]['from'] == user:
            index = idx
            break
    return index


def show_count(arr, msg):
    message_arr = []
    if len(arr) > 0:
        for index in range(len(arr)):
            message_arr.append('第%s个乘客%s, 具体时间为: %s' % (index + 1, arr[index]['from'], arr[index]['text']))
        msg.user.send('\n'.join(message_arr) + '\n截止目前%s人' % (len(arr)))


itchat.auto_login(hotReload=True)
itchat.run()
