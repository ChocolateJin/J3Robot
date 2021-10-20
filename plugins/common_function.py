import miraicle,re
@miraicle.Mirai.receiver('GroupMessage')
def function_check(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    if msg.plain=='功能查询':
        to_send_message='目前开放功能如下:\n1.团长开团\n2.团员报名\n3.查询开团\n4.报名查询\n5.团信息查询\n6.查宏功能\n有帮助需要请按照\'帮助 功能名字进行查询\''
        bot.send_group_msg(msg.group, to_send_message)
    if msg.plain =='帮助 团员报名':
        bot.send_group_msg(msg.group, '报名格式为:\'报名 团名称 角色名 职业 装分 位置\'')
    if msg.plain =='帮助 团长开团':
        bot.send_group_msg(msg.group, '开团格式为:\'开团 团名称 配置(例:1dps2奶3T4老板) 备注\'')
    if msg.plain =='帮助 查宏':
        bot.send_group_msg(msg.group, '查询格式为:\'查宏 职业名\'')
        
        

    