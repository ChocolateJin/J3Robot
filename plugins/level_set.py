import miraicle
import json

@miraicle.Mirai.receiver('GroupMessage')
def set_QQ_level(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    with open("./data/level_data.json",'r') as load_f:
        data=json.load(load_f)
    qqnumber=msg.sender
    print(msg.plain)
    if msg.plain =='绑定团员 Muqiu2021' :
        if str(qqnumber) in data:
            current_level=data[str(qqnumber)];
            bot.send_group_msg(group=msg.group, msg='您已绑定过，等级为：'+str(current_level))
        else:
            data[str(msg.sender)]=2
            send_msg='您已成功绑定，欢迎加入暮秋大家庭!'
            bot.send_group_msg(group=msg.group,msg=send_msg)
    json_str=json.dumps(data,indent=4)
    with open('./data/level_data.json','w+') as new_json_file:
        new_json_file.write(json_str)
@miraicle.Mirai.receiver('GroupMessage')
def check_QQ_level(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    with open("./data/level_data.json",'r') as load_f:
        data=json.load(load_f)
    qqnumber=msg.sender
    if msg.plain == '查询等级':
        if str(qqnumber) in data:
            bot.send_group_msg(group=msg.group, msg='你的等级为：'+str(data[str(qqnumber)]))
        else:
            bot.send_group_msg(group=msg.group, msg='你还没有绑定等级')
