import xlrd,re,json,os

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
        


data=xlrd.open_workbook('e:/数据完整.xls')
table=data.sheets()[0]
hon_data=my_open_json('../data/hon_data.json')
for i in range(table.nrows):
    if i ==0:
        continue
    tmp_text=table.cell(i,1).value
    tmp_text=tmp_text.replace('复制宏内容轉換為繁體复制云端宏','')
    tmp_name=table.cell(i,0).value
    if '自用' in tmp_name:
        continue
    hon_p=tmp_text.find('/cast') #第一个宏本体出现
    hon_p2=tmp_text.find('/fcast')
    if hon_p >hon_p2 and hon_p2 !=-1:
        hon_p=hon_p2
    qixve_p=tmp_text.find('奇穴\n') #第一个气血出现标志
    end_p=tmp_text.find('复制奇穴编码复制奇穴文字复制奇穴序列') #奇穴部分结束标志，部分宏后面还带备注
    beizhu1=tmp_text[0:hon_p] #宏本体前的备注
    beizhu2=''
    hon=tmp_text[hon_p:qixve_p]
    hon=hon.replace('/cast','\n/cast')
    hon=hon.replace('/fcast','\n/fcast')
    hon=hon.replace('字数','\n字数')
    qixve=tmp_text[qixve_p:end_p]
    qixve=qixve.replace('\n            \n                ',' ')
    qixve=qixve.replace('\n                 \n                ',' ')
    qixve=qixve.replace('\n            \n         \n                ',' ')
    qixve=qixve.replace('\n            \n        \n                \n            \n        ','')
    zhiye=qixve[3:len(qixve)].find(' ')
    zhiye=qixve[3:3+zhiye]
    if int(end_p)+17 <=len(tmp_text)-1:
        beizhu2=tmp_text[end_p+18:len(tmp_text)]
    to_add_dict={
        tmp_name:{
        '职业':zhiye,
        '宏':hon,
        '奇穴':qixve,
        '备注1':beizhu1,
        '加速':beizhu2}
        }
    hon_data.update(to_add_dict)
my_write_json(hon_data,'../data/hon_data.json')
    