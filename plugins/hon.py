import miraicle,json,re,os,random,math
def my_open_json(string_path):
    if os.path.exists(string_path) ==0:
        open(string_path,'w').write('{}');
    with open(string_path,'r',encoding='utf-8') as load_f:
        data=json.load(load_f)
        return data
def my_write_json(input_data,string_path):
    
    input_data_str=json.dumps(input_data,indent=4,ensure_ascii=False)
    with open(string_path,'w+',encoding='utf-8') as load_f:
        load_f.write(input_data_str)
        
@miraicle.Mirai.receiver('GroupMessage')
def chahon(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    sentense_re='查宏 [\u4e00-\u9fa5]{0,}'
    is_equal=re.search(sentense_re,msg.plain)
    if is_equal:
        split_str=msg.plain.split()
        zhiye = split_str[1]
        hon_data=my_open_json('./data/hon_data.json')
        list1=list(hon_data.keys())
        correct_number=[]
        for i in range(len(list1)):
            sub_dict=hon_data[list1[i]]
            if sub_dict['职业']==zhiye:
                correct_number.append(i)
        if correct_number == []:
            bot.send_group_msg(group=msg.group, msg='没有查到'+zhiye+'的宏，请重新检查字是否出错后重试')
        else:
            num=math.floor(random.random()*len(correct_number))
            num_dict=hon_data[list1[correct_number[num]]]
            to_send_msg=''
            to_send_msg+='宏名:'+list1[correct_number[num]]+'\n'
            to_send_msg+='备注1:'+num_dict['备注1']+'\n'
            to_send_msg+='宏:'+num_dict['宏']+'\n'
            to_send_msg+='奇穴:'+num_dict['奇穴']+'\n'
            to_send_msg+='备注2:'+num_dict['加速']+'\n'
            bot.send_group_msg(group=msg.group, msg=to_send_msg)