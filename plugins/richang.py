import miraicle,re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as BS
@miraicle.Mirai.receiver('GroupMessage')
def chahon(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    if '今日日常' == msg.plain:
        chrom_options = Options()
        chrom_options.add_argument('--headless')
        bro=webdriver.Chrome(options=chrom_options)
        bro.get('https://www.jx3box.com/index/')
        source=bro.page_source
        re_dazhan='<td>大战</td><td>全服</td><td>大战！[\u4E00-\u9FA5A-Za-z0-9_]+'
        re_zhanchang='<td>战场首胜</td><td>全服</td><td>[\u4E00-\u9FA5A-Za-z0-9_]+</td>'
        re_zhenyin='阵营日常</td><td>全服</td><td>战！[\u4E00-\u9FA5A-Za-z0-9_]+</td></tr><tr><td>'
        re_meiren='[\u4E00-\u9FA5A-Za-z0-9_]+画像'
        dazhan_name=re.search(re_dazhan,source).group().replace('<td>','').replace('</td>','').replace('全服','').replace('大战大战','大战')
        zhanchang_name=re.search(re_zhanchang,source).group().replace('<td>','').replace('</td>','').replace('首胜全服',':')
        zhenyin_name=re.search(re_zhenyin,source).group().replace('<td>','').replace('</td>','').replace('日常全服',':').replace('</tr><tr>','')
        meiren_name=re.search(re_meiren,source)
        to_send_msg='今日活动如下:\n'
        to_send_msg+=dazhan_name
        to_send_msg+=zhanchang_name
        to_send_msg+=zhenyin_name
        bot.send_group_msg(group=msg.group,msg=to_send_msg)