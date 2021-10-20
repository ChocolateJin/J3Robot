import miraicle,json,re,time,os,xlwt
import pandas as pd 
import matplotlib.pyplot as plt
from pandas.plotting import table
from pylab import mpl
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
        
def create_tuan_xinxi(tuan_xinxi,tuanming):
    zhiye_type=list(tuan_xinxi.keys())
    wb=xlwt.Workbook(encoding='ascii')
    sheet=wb.add_sheet(tuanming)
    sheet.write_merge(0,0,0,15,tuanming);
    for iter_zhiye in range(len(zhiye_type)):
        bias=4*iter_zhiye;
        sheet.write_merge(1,1,(bias),(bias+2),zhiye_type[iter_zhiye])
        sheet.write(2,(bias),'编号')
        sheet.write(2,(bias)+1,'ID')
        sheet.write(2,(bias)+2,'职业')
        sheet.write(2,(bias)+3,'装分')
        sheet.write_merge(3,3,bias,bias+3,'总数:'+tuan_xinxi[zhiye_type[iter_zhiye]]['总数'])
        single_zhiye=list((tuan_xinxi[zhiye_type[iter_zhiye]].keys()))
        for single_zhiye_iter in range(len(single_zhiye)):
            if single_zhiye_iter==0:continue
            tmp_jvesexinxi=tuan_xinxi[zhiye_type[iter_zhiye]]['角色'+str(single_zhiye_iter)];
            sheet.write(3+single_zhiye_iter,bias,str(single_zhiye_iter))
            sheet.write(3+single_zhiye_iter,bias+1,tmp_jvesexinxi['角色名'])
            sheet.write(3+single_zhiye_iter,bias+2,tmp_jvesexinxi['职业'])
            sheet.write(3+single_zhiye_iter,bias+3,tmp_jvesexinxi['装分'])
    save_path='./data/'+tuanming+'.xls'
    wb.save(save_path);
    draw_picture_from_excel(save_path)
def draw_picture_from_excel(excel_path):
    mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    mpl.rcParams['axes.unicode_minus'] =False
    fig = plt.figure(figsize=(9,10),dpi=900)
    ax=fig.add_subplot(111,frame_on=False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    datas=pd.read_excel(excel_path,header=None).fillna(' ')
    datas=datas.iloc[:,0:]
    print(datas)
    table(ax,datas,loc='center')
    plt.savefig('./data/photo.jpg')
@miraicle.Mirai.receiver('GroupMessage')
#开团格式:'开团 团名 若干数字+位置的组合 备注'
#用于团长开团
def kaituan_function(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    level_data=my_open_json('./data/level_data.json');
    kaituan_data=my_open_json('./data/kaituan_data.json')
    sentense_re='开团 [\u4E00-\u9FA5A-Za-z0-9_]+ \d{1,}[\u4E00-\u9FA5A-Za-z0-9_]+ [\u4E00-\u9FA5A-Za-z0-9_]+'
    is_equal=re.search(sentense_re,msg.plain)
    if is_equal: #符合开团语句
        if (str(msg.sender) in level_data )==True: #存在等级
            if level_data[str(msg.sender)]>=3: #权限足够
                seperate_word=str.split(msg.plain)
                tuanming=seperate_word[1];peizhi=seperate_word[2];beizhu=seperate_word[3];
                if tuanming in kaituan_data:
                    bot.send_group_msg(group=msg.group, msg='存在同名团,本次开团将覆盖原开团数据')
                to_add_dict={
                    '备注':beizhu,
                    '创建时间':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    '职业信息':{},
                    '开团者':msg.sender,
                    };
                peizhi_pattern=re.compile(r'\d{1,}[\u4E00-\u9FA5A-Za-z]+')
                peizhi_sepe=peizhi_pattern.findall(peizhi)
                
                for i in range(len(peizhi_sepe)):
                    tmp_type=(re.search('[\u4E00-\u9FA5A-Za-z]+',peizhi_sepe[i]).group())
                    tmp_number=(re.search('\d{1,}',peizhi_sepe[i]).group())
                    to_add_dict['职业信息'].update({
                        tmp_type:{'总数':tmp_number}
                        });
                kaituan_data[tuanming]=to_add_dict
                my_write_json(kaituan_data,'./data/kaituan_data.json')
                bot.send_group_msg(group=msg.group, msg='成功开团!')
            else:
                bot.send_group_msg(group=msg.group, msg='等级不足，无法开团!')
        else:
            bot.send_group_msg(group=msg.group, msg='你还没有绑定等级!')
            

@miraicle.Mirai.receiver('GroupMessage')
def baoming_function_2(bot:miraicle.Mirai,msg: miraicle.GroupMessage):
    #用于团员报名
    #报名格式为'报名 团名 角色名 职业 装分 位置'
    kaituan_data=my_open_json('./data/kaituan_data.json')
    sentense_re='报名 [\u4E00-\u9FA5A-Za-z0-9_]+ ([\u4e00-\u9fa5])+ [\u4E00-\u9FA5A-Za-z0-9_]+ \d+(\.\d+)? [\u4E00-\u9FA5A-Za-z0-9_]'
    is_equal=re.search(sentense_re,msg.plain) #判断是否符合报名格式
    if is_equal: #首先判断是否符合报名语句
        seperate_word=str.split(msg.plain) #分离信息
        tuanming=seperate_word[1];jvese=seperate_word[2];zhiye=seperate_word[3];
        zhuangfen=seperate_word[4];weizhi=seperate_word[5];
        if tuanming in kaituan_data: #判断是否存在该团
            if weizhi in kaituan_data[tuanming]['职业信息']: #存在报名的职业
                max_zhiye_number= int(kaituan_data[tuanming]['职业信息'][weizhi]['总数'])
                current_zhiye_number=len(kaituan_data[tuanming]['职业信息'][weizhi])-1
                if max_zhiye_number >current_zhiye_number: #最大数大于当前人数
                    to_add_dict={'角色'+str(current_zhiye_number+1):{
                        '角色名':jvese,
                        '职业':zhiye,
                        '装分':zhuangfen,
                        'QQ':msg.sender,
                        '报名时间':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
                        }};
                    kaituan_data[tuanming]['职业信息'][weizhi].update(to_add_dict);
                    my_write_json(kaituan_data,'./data/kaituan_data.json')
                    bot.send_group_msg(msg.group,jvese+'报名成功!');
                else:
                    bot.send_group_msg(msg.group,'本次团本'+weizhi+'已满');
            else:
                bot.send_group_msg(msg.group,'本次团本不存在'+weizhi+'位置');
        else:
            bot.send_group_msg(msg.group,'不存在名为'+tuanming+'的团');
            
@miraicle.Mirai.receiver('GroupMessage')
#用于查询当前已开团
def chaxun_kaituan(bot:miraicle.Mirai,msg: miraicle.GroupMessage):
    kaituan_data=my_open_json('./data/kaituan_data.json')
    is_equal=re.search('查询开团',msg.plain)
    if is_equal:
        if len(kaituan_data)==0:
            bot.send_group_msg(msg.group,'目前无开团记录')
        else:
            to_send_message='当前开团如下:\n';
            A=list(kaituan_data.keys())
            for i in range(len(A)):
                to_send_message+=str(i+1)+'.'+A[i]+' 备注:'+kaituan_data[A[i]]['备注']+'\n';
            bot.send_group_msg(msg.group, to_send_message)

@miraicle.Mirai.receiver('GroupMessage')
#用于团员查询自己的报名记录
def baoming_chaxun(bot:miraicle.Mirai,msg: miraicle.GroupMessage):
    if msg.plain=='报名查询':
        exist_baoming_mark=0;to_send_message='你的报名情况如下:\n';
        kaituan_data=my_open_json('./data/kaituan_data.json');
        all_tuanming=list(kaituan_data.keys())
        for iter_tuanming in range(len(all_tuanming)):
            all_zhiyexinxi = list(kaituan_data[all_tuanming[iter_tuanming]]['职业信息'].keys())
            for iter_zhiyexinxi in range(len(all_zhiyexinxi)):
                current_dict=kaituan_data[all_tuanming[iter_tuanming]]['职业信息'][all_zhiyexinxi[iter_zhiyexinxi]]
                all_character_data=list(current_dict.keys())
                for iter_chara in range(len(all_character_data)):
                    if iter_chara==0:continue
                    current_dict_2=current_dict[all_character_data[iter_chara]]
                    if current_dict_2['QQ']==msg.sender:
                        exist_baoming_mark+=1;
                        to_send_message+=str(exist_baoming_mark)+'.你报名了'+all_tuanming[iter_tuanming]+'的'+ \
all_zhiyexinxi[iter_zhiyexinxi]+',角色ID为:'+current_dict_2['角色名']+'\n'
        if exist_baoming_mark ==0:
            bot.send_group_msg(msg.group, '未查询到与你QQ相关的报名记录')
        else:
            bot.send_group_msg(msg.group, to_send_message)
            
            
@miraicle.Mirai.receiver('GroupMessage')
#用于查询某个团的详细信息
def tuan_xinxi_chaxun(bot:miraicle.Mirai,msg: miraicle.GroupMessage):
    is_equal1 = re.search('团信息查询 [\u4E00-\u9FA5A-Za-z0-9_]+',msg.plain)
    is_equal2 =re.search('团信息查询 \d{1}$',msg.plain)
    kaituan_data=my_open_json('./data/kaituan_data.json');
    if is_equal1: check_type=1;
    if is_equal2:check_type=2;
    if is_equal1 or is_equal2: #符合查询团格式
        tuanming=str.split(msg.plain)[1]
        if check_type ==2:
            tuanming_keys=list(kaituan_data.keys())
            if int(tuanming) > len(tuanming_keys):
                bot.send_group_msg(msg.group,'错误!序号超过当前已有的团数')
            else:
                tuanming = tuanming_keys[int(tuanming)-1]
                
        # if tuanming in kaituan_data:
        #     create_tuan_xinxi(kaituan_data[tuanming]['职业信息'],tuanming)
        #     bot.send_group_msg(msg.group,miraicle.Image(path='E:/my_robot/data/photo.jpg')
        to_send_msg = '团名:'+tuanming+'\n'
        zhiyexinxi_list=list(kaituan_data[tuanming]['职业信息'].keys())
        for i in range(len(zhiyexinxi_list)):
            tmp_zhiye=zhiyexinxi_list[i]
            tmp_zhiyexiangxi=kaituan_data[tuanming]['职业信息'][tmp_zhiye]
            to_send_msg +=tmp_zhiye+' 总数:'+tmp_zhiyexiangxi['总数']+' 当前:'+str(len(list(tmp_zhiyexiangxi.keys()))-1)+'\n'
            zhiyexiangxi_list=list(tmp_zhiyexiangxi.keys())
            for n in range(len(zhiyexiangxi_list)):
                if n ==0:continue
                tmp_zhiyeiter=zhiyexiangxi_list[n];
                to_send_msg +='角色'+str(n)+':'+tmp_zhiyexiangxi[tmp_zhiyeiter]['角色名']
                to_send_msg +=' 职业:' +tmp_zhiyexiangxi[tmp_zhiyeiter]['职业']
                to_send_msg +=' 装分:' +str(tmp_zhiyexiangxi[tmp_zhiyeiter]['装分'])+'\n'
        to_send_msg+='备注:'+kaituan_data[tuanming]['备注']
        bot.send_group_msg(msg.group,to_send_msg)

@miraicle.Mirai.receiver('GroupMessage')
def shanchu_kaituan (bot:miraicle.Mirai,msg: miraicle.GroupMessage):
    is_equal1 = re.search('删除开团 [\u4E00-\u9FA5A-Za-z0-9_]+',msg.plain)
    if is_equal1:
        level_data=my_open_json('./data/level_data.json')
        kaituan_data=my_open_json('./data/kaituan_data.json');
        if (str(msg.sender) in level_data ==0) or level_data[str(msg.sender)]<=4:
            bot.send_group_msg(msg.group,'错误!你还未绑定权限或权限不足!')
        else:
            tuanming = str.split(msg.plain)[1]
            if tuanming in kaituan_data :
                kaituan_data.pop(tuanming)
                bot.send_group_msg(msg.group,'删除团:"'+tuanming+'"成功!')
                my_write_json(kaituan_data,'./data/kaituan_data.json')
            else:
                bot.send_group_msg(msg.group,'错误!未查询到同名团')
    