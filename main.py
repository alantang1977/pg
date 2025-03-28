import urllib.request
from urllib.parse import urlparse
import re #正则
import os
from datetime import datetime, timedelta, timezone
import random
import opencc #简繁转换

# 执行开始时间
timestart = datetime.now()

#读取文本方法
def read_txt_to_array(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
            return lines
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

#read BlackList 2024-06-17 15:02
def read_blacklist_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    BlackList = [line.split(',')[1].strip() for line in lines if ',' in line]
    return BlackList

blacklist_auto=read_blacklist_from_txt('assets/whitelist-blacklist/blacklist_auto.txt') 
blacklist_manual=read_blacklist_from_txt('assets/whitelist-blacklist/blacklist_manual.txt') 
combined_blacklist = set(blacklist_auto + blacklist_manual)  #list是个列表，set是个集合，据说检索速度集合要快很多。2024-08-08

# 定义多个对象用于存储不同内容的行文本
# 主频道
ys_lines = [] #央视频道
ws_lines = [] #卫视频道
ty_lines = [] #体育频道
dy_lines = [] #电影频道
dsj_lines = [] #电视剧频道
gat_lines = [] #港澳台
gj_lines = [] #国际台
jlp_lines = [] #记录片
xq_lines = [] #戏曲
js_lines = [] #解说
newtv_lines = [] #NewTV
ihot_lines = [] #iHot
et_lines = [] #儿童
zy_lines = [] #综艺频道
mdd_lines = [] #埋堆堆
yy_lines = [] #音乐频道
game_lines = [] #游戏频道
radio_lines = [] #收音机频道
zb_lines = [] #直播中国
cw_lines = [] #春晚
mtv_lines = [] #MTV
migu_lines = [] #咪咕直播

# 地方台
sh_lines = [] #地方台-上海频道
zj_lines = [] #地方台-浙江频道
jsu_lines = [] #地方台-江苏频道
gd_lines = [] #地方台-广东频道
hn_lines = [] #地方台-湖南频道
ah_lines = [] #地方台-安徽频道
hain_lines = [] #地方台-海南频道
nm_lines = [] #地方台-内蒙频道
hb_lines = [] #地方台-湖北频道
ln_lines = [] #地方台-辽宁频道
sx_lines = [] #地方台-陕西频道
shanxi_lines = [] #地方台-山西频道
shandong_lines = [] #地方台-山东频道
yunnan_lines = [] #地方台-云南频道
bj_lines = [] #地方台-北京频道
cq_lines = [] #地方台-重庆频道
fj_lines = [] #地方台-福建频道
gs_lines = [] #地方台-甘肃频道
gx_lines = [] #地方台-广西频道
gz_lines = [] #地方台-贵州频道
heb_lines = [] #地方台-河北频道
hen_lines = [] #地方台-河南频道
hlj_lines = [] #地方台-黑龙江频道
jl_lines = [] #地方台-吉林频道
jx_lines = [] #地方台-江西频道
nx_lines = [] #地方台-宁夏频道
qh_lines = [] #地方台-青海频道
sc_lines = [] #地方台-四川频道
tj_lines = [] #地方台-天津频道
xj_lines = [] #地方台-新疆频道

other_lines = [] #其他
other_lines_url = [] # 为降低other文件大小，剔除重复url添加

whitelist_lines=read_txt_to_array('assets/whitelist-blacklist/whitelist_manual.txt') #白名单
whitelist_auto_lines=read_txt_to_array('assets/whitelist-blacklist/whitelist_auto.txt') #白名单

#读取文本
# 主频道
ys_dictionary=read_txt_to_array('主频道/央视频道.txt')
ws_dictionary=read_txt_to_array('主频道/卫视频道.txt') 
ty_dictionary=read_txt_to_array('主频道/体育频道.txt') 
dy_dictionary=read_txt_to_array('主频道/电影.txt') 
dsj_dictionary=read_txt_to_array('主频道/电视剧.txt') 
gat_dictionary=read_txt_to_array('主频道/港澳台.txt') 
gj_dictionary=read_txt_to_array('主频道/国际台.txt') 
jlp_dictionary=read_txt_to_array('主频道/纪录片.txt') 
xq_dictionary=read_txt_to_array('主频道/戏曲频道.txt') 
js_dictionary=read_txt_to_array('主频道/解说频道.txt') 
cw_dictionary=read_txt_to_array('主频道/春晚.txt') 
newtv_dictionary=read_txt_to_array('主频道/NewTV.txt') 
ihot_dictionary=read_txt_to_array('主频道/iHOT.txt')
et_dictionary=read_txt_to_array('主频道/儿童频道.txt')
zy_dictionary=read_txt_to_array('主频道/综艺频道.txt') 
mdd_dictionary=read_txt_to_array('主频道/埋堆堆.txt') 
yy_dictionary=read_txt_to_array('主频道/音乐频道.txt') 
game_dictionary=read_txt_to_array('主频道/游戏频道.txt') 
radio_dictionary=read_txt_to_array('主频道/收音机频道.txt') 
zb_dictionary=read_txt_to_array('主频道/直播中国.txt') 
mtv_dictionary=read_txt_to_array('主频道/MTV.txt') 
migu_dictionary=read_txt_to_array('主频道/咪咕直播.txt') 

# 地方台
sh_dictionary=read_txt_to_array('地方台/上海频道.txt') 
zj_dictionary=read_txt_to_array('地方台/浙江频道.txt') 
jsu_dictionary=read_txt_to_array('地方台/江苏频道.txt') 
gd_dictionary=read_txt_to_array('地方台/广东频道.txt') 
hn_dictionary=read_txt_to_array('地方台/湖南频道.txt') 
ah_dictionary=read_txt_to_array('地方台/安徽频道.txt') 
hain_dictionary=read_txt_to_array('地方台/海南频道.txt') 
nm_dictionary=read_txt_to_array('地方台/内蒙频道.txt') 
hb_dictionary=read_txt_to_array('地方台/湖北频道.txt') 
ln_dictionary=read_txt_to_array('地方台/辽宁频道.txt') 
sx_dictionary=read_txt_to_array('地方台/陕西频道.txt') 
shanxi_dictionary=read_txt_to_array('地方台/山西频道.txt') 
shandong_dictionary=read_txt_to_array('地方台/山东频道.txt') 
yunnan_dictionary=read_txt_to_array('地方台/云南频道.txt') 
bj_dictionary=read_txt_to_array('地方台/北京频道.txt') 
cq_dictionary=read_txt_to_array('地方台/重庆频道.txt') 
fj_dictionary=read_txt_to_array('地方台/福建频道.txt') 
gs_dictionary=read_txt_to_array('地方台/甘肃频道.txt') 
gx_dictionary=read_txt_to_array('地方台/广西频道.txt') 
gz_dictionary=read_txt_to_array('地方台/贵州频道.txt') 
heb_dictionary=read_txt_to_array('地方台/河北频道.txt') 
hen_dictionary=read_txt_to_array('地方台/河南频道.txt') 
hlj_dictionary=read_txt_to_array('地方台/黑龙江频道.txt') 
jl_dictionary=read_txt_to_array('地方台/吉林频道.txt') 
jx_dictionary=read_txt_to_array('地方台/江西频道.txt') 
nx_dictionary=read_txt_to_array('地方台/宁夏频道.txt') 
qh_dictionary=read_txt_to_array('地方台/青海频道.txt') 
sc_dictionary=read_txt_to_array('地方台/四川频道.txt') 
tj_dictionary=read_txt_to_array('地方台/天津频道.txt') 
xj_dictionary=read_txt_to_array('地方台/新疆频道.txt') 

# 自定义源
urls = read_txt_to_array('assets/urls.txt')

#简繁转换
def traditional_to_simplified(text: str) -> str:
    # 初始化转换器，"t2s" 表示从繁体转为简体
    converter = opencc.OpenCC('t2s')
    simplified_text = converter.convert(text)
    return simplified_text

#M3U格式判断
def is_m3u_content(text):
    lines = text.splitlines()
    first_line = lines[0].strip()
    return first_line.startswith("#EXTM3U")

def convert_m3u_to_txt(m3u_content):
    # 分行处理
    lines = m3u_content.split('\n')
    
    # 用于存储结果的列表
    txt_lines = []
    
    # 临时变量用于存储频道名称
    channel_name = ""
    
    for line in lines:
        # 过滤掉 #EXTM3U 开头的行
        if line.startswith("#EXTM3U"):
            continue
        # 处理 #EXTINF 开头的行
        if line.startswith("#EXTINF"):
            # 获取频道名称（假设频道名称在引号后）
            channel_name = line.split(',')[-1].strip()
        # 处理 URL 行
        elif line.startswith("http") or line.startswith("rtmp") or line.startswith("p3p") :
            txt_lines.append(f"{channel_name},{line.strip()}")
        
        # 处理后缀名为m3u，但是内容为txt的文件
        if "#genre#" not in line and "," in line and "://" in line:
            # 定义正则表达式，匹配频道名称,URL 的格式，并确保 URL 包含 "://"
            # xxxx,http://xxxxx.xx.xx
            pattern = r'^[^,]+,[^\s]+://[^\s]+$'
            if bool(re.match(pattern, line)):
                txt_lines.append(line)
    
    # 将结果合并成一个字符串，以换行符分隔
    return '\n'.join(txt_lines)

# 在list是否已经存在url 2024-07-22 11:18
def check_url_existence(data_list, url):
    """
    Check if a given URL exists in a list of data.

    :param data_list: List of strings containing the data
    :param url: The URL to check for existence
    :return: True if the URL exists in the list, otherwise False
    """
    if "127.0.0.1" in url:
        return False
    # Extract URLs from the data list
    urls = [item.split(',')[1] for item in data_list]
    return url not in urls #如果不存在则返回true，需要

# 处理带$的URL，把$之后的内容都去掉（包括$也去掉） 【2024-08-08 22:29:11】
def clean_url(url):
    last_dollar_index = url.rfind('$')  # 安全起见找最后一个$处理
    if last_dollar_index != -1:
        return url[:last_dollar_index]
    return url

# 添加channel_name前剔除部分特定字符
removal_list = ["「IPV4」","「IPV6」","[ipv6]","[ipv4]","_电信", "电信","（HD）","[超清]","高清","超清", "-HD","(HK)","AKtv","@","IPV6","🎞️","🎦"," ","[BD]","[VGA]","[HD]","[SD]","(1080p)","(720p)","(480p)"]
def clean_channel_name(channel_name, removal_list):
    for item in removal_list:
        channel_name = channel_name.replace(item, "")
    channel_name = channel_name.replace("CCTV-", "CCTV");
    channel_name = channel_name.replace("CCTV0","CCTV");
    channel_name = channel_name.replace("PLUS", "+");
    channel_name = channel_name.replace("NewTV-", "NewTV");
    channel_name = channel_name.replace("iHOT-", "iHOT");
    channel_name = channel_name.replace("NEW", "New");
    channel_name = channel_name.replace("New_", "New");
    return channel_name

#读取纠错频道名称方法
def load_corrections_name(filename):
    corrections = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): #跳过空行
                continue
            parts = line.strip().split(',')
            correct_name = parts[0]
            for name in parts[1:]:
                corrections[name] = correct_name
    return corrections

#读取纠错文件
corrections_name = load_corrections_name('assets/corrections_name.txt')
def correct_name_data(name):
    if name in corrections_name and name != corrections_name[name]:
        name = corrections_name[name]
    return name
    
# 分发直播源，归类，把这部分从process_url剥离出来，为以后加入whitelist源清单做准备。
def process_channel_line(line):
    if  "#genre#" not in line and "#EXTINF:" not in line and "," in line and "://" in line:
        channel_name = line.split(',')[0]
        channel_name = traditional_to_simplified(channel_name)  #繁转简
        channel_name = clean_channel_name(channel_name, removal_list)  #分发前清理channel_name中特定字符
        channel_name = correct_name_data(channel_name).strip() #根据纠错文件处理
        
        channel_address = clean_url(line.split(',')[1]).strip()  #把URL中$之后的内容都去掉
        line=channel_name+","+channel_address #重新组织line
        
        if len(channel_address) > 0 and channel_address not in combined_blacklist: # 判断当前源是否在blacklist中
            # 根据行内容判断存入哪个对象，开始分发
            if channel_name in ys_dictionary: #央视频道
                if check_url_existence(ys_lines, channel_address):
                    ys_lines.append(line)
            elif channel_name in ws_dictionary: #卫视频道
                if check_url_existence(ws_lines, channel_address):
                    ws_lines.append(line)
            elif channel_name in ty_dictionary: #体育频道
                if check_url_existence(ty_lines, channel_address):
                    ty_lines.append(line)
            elif channel_name in dy_dictionary: #电影频道
                if check_url_existence(dy_lines, channel_address):  
                    dy_lines.append(line)
            elif channel_name in dsj_dictionary: #电视剧频道
                if check_url_existence(dsj_lines, channel_address):  
                    dsj_lines.append(line)
            elif channel_name in gat_dictionary: #港澳台
                if check_url_existence(gat_lines, channel_address):
                    gat_lines.append(line)
            elif channel_name in gj_dictionary: #国际台
                if check_url_existence(gj_lines, channel_address):
                    gj_lines.append(line)
            elif channel_name in jlp_dictionary: #纪录片
                if check_url_existence(jlp_lines, channel_address):
                    jlp_lines.append(line)
            elif channel_name in xq_dictionary: #戏曲
                if check_url_existence(xq_lines, channel_address):
                    xq_lines.append(line)
            elif channel_name in js_dictionary: #解说
                if check_url_existence(js_lines, channel_address):
                    js_lines.append(line)
            elif channel_name in cw_dictionary: #春晚
                if check_url_existence(cw_lines, channel_address):
                    cw_lines.append(line)
            elif channel_name in newtv_dictionary: #NewTV
                if check_url_existence(newtv_lines, channel_address):
                    newtv_lines.append(line)
            elif channel_name in ihot_dictionary: #iHOT
                if check_url_existence(ihot_lines, channel_address):
                    ihot_lines.append(line)
            elif channel_name in et_dictionary: #儿童
                if check_url_existence(et_lines, channel_address):
                    et_lines.append(line)
            elif channel_name in zy_dictionary: #综艺频道
                if check_url_existence(zy_lines, channel_address):
                    zy_lines.append(line)
            elif channel_name in mdd_dictionary: #埋堆堆
                if check_url_existence(mdd_lines, channel_address):
                    mdd_lines.append(line)
            elif channel_name in yy_dictionary: #音乐频道
                if check_url_existence(yy_lines, channel_address): 
                    yy_lines.append(line)
            elif channel_name in game_dictionary: #游戏频道
                if check_url_existence(game_lines, channel_address):
                    game_lines.append(line)
            elif channel_name in radio_dictionary: #收音机频道
                if check_url_existence(radio_lines, channel_address):
                    radio_lines.append(line)
            elif channel_name in migu_dictionary: #咪咕直播
                if check_url_existence(migu_lines, channel_address):
                    migu_lines.append(line)
            elif channel_name in sh_dictionary: #地方台-上海频道
                if check_url_existence(sh_lines, channel_address): 
                    sh_lines.append(line)
            elif channel_name in zj_dictionary: #地方台-浙江频道
                if check_url_existence(zj_lines, channel_address):
                    zj_lines.append(line)
            elif channel_name in jsu_dictionary: #地方台-江苏频道
                if check_url_existence(jsu_lines, channel_address):
                    jsu_lines.append(line)
            elif channel_name in gd_dictionary: #地方台-广东频道
                if check_url_existence(gd_lines, channel_address):
                    gd_lines.append(line)
            elif channel_name in hn_dictionary: #地方台-湖南频道
                if check_url_existence(hn_lines, channel_address):
                    hn_lines.append(line)
            elif channel_name in hb_dictionary: #地方台-湖北频道
                if check_url_existence(hb_lines, channel_address):
                    hb_lines.append(line)
            elif channel_name in ah_dictionary: #地方台-安徽频道
                if check_url_existence(ah_lines, channel_address):
                    ah_lines.append(line)
            elif channel_name in hain_dictionary: #地方台-海南频道
                if check_url_existence(hain_lines, channel_address):
                    hain_lines.append(line)
            elif channel_name in nm_dictionary: #地方台-内蒙频道
                if check_url_existence(nm_lines, channel_address):
                    nm_lines.append(line)
            elif channel_name in ln_dictionary: #地方台-辽宁频道
                if check_url_existence(ln_lines, channel_address):
                    ln_lines.append(line)
            elif channel_name in sx_dictionary: #地方台-陕西频道
                if check_url_existence(sx_lines, channel_address): 
                    sx_lines.append(line)
            elif channel_name in shanxi_dictionary: #地方台-山西频道
                if check_url_existence(shanxi_lines, channel_address):
                    shanxi_lines.append(line)
            elif channel_name in shandong_dictionary: #地方台-山东频道
                if check_url_existence(shandong_lines, channel_address):
                    shandong_lines.append(line)
            elif channel_name in yunnan_dictionary: #地方台-云南频道
                if check_url_existence(yunnan_lines, channel_address):
                    yunnan_lines.append(line)
            elif channel_name in bj_dictionary: #地方台-北京频道
                if check_url_existence(bj_lines, channel_address):
                    bj_lines.append(line)
            elif channel_name in cq_dictionary: #地方台-重庆频道
                if check_url_existence(cq_lines, channel_address):
                    cq_lines.append(line)
            elif channel_name in fj_dictionary: #地方台-福建频道
                if check_url_existence(fj_lines, channel_address):
                    fj_lines.append(line)
            elif channel_name in gs_dictionary: #地方台-甘肃频道
                if check_url_existence(gs_lines, channel_address):
                    gs_lines.append(line)
            elif channel_name in gx_dictionary: #地方台-广西频道
                if check_url_existence(gx_lines, channel_address): 
                    gx_lines.append(line)
            elif channel_name in gz_dictionary: #地方台-贵州频道
                if check_url_existence(gz_lines, channel_address):
                    gz_lines.append(line)
            elif channel_name in heb_dictionary: #地方台-河北频道
                if check_url_existence(heb_lines, channel_address):
                    heb_lines.append(line)
            elif channel_name in hen_dictionary: #地方台-河南频道
                if check_url_existence(hen_lines, channel_address):
                    hen_lines.append(line)
            elif channel_name in hlj_dictionary: #地方台-黑龙江频道
                if check_url_existence(hlj_lines, channel_address):
                    hlj_lines.append(line)
            elif channel_name in jl_dictionary: #地方台-吉林频道
                if check_url_existence(jl_lines, channel_address):
                    jl_lines.append(line)
            elif channel_name in nx_dictionary: #地方台-宁夏频道
                if check_url_existence(nx_lines, channel_address):
                    nx_lines.append(line)
            elif channel_name in jx_dictionary: #地方台-江西频道
                if check_url_existence(jx_lines, channel_address):
                    jx_lines.append(line)
            elif channel_name in qh_dictionary: #地方台-青海频道
                if check_url_existence(qh_lines, channel_address):
                    qh_lines.append(line)
            elif channel_name in sc_dictionary: #地方台-四川频道
                if check_url_existence(sc_lines, channel_address):
                    sc_lines.append(line)
            elif channel_name in tj_dictionary: #地方台-天津频道
                if check_url_existence(tj_lines, channel_address):
                    tj_lines.append(line)
            elif channel_name in xj_dictionary: #地方台-新疆频道
                if check_url_existence(xj_lines, channel_address):
                    xj_lines.append(line)
            elif channel_name in zb_dictionary: #直播中国
                if check_url_existence(zb_lines, channel_address):
                    zb_lines.append(line)
            elif channel_name in mtv_dictionary: #MTV
                if check_url_existence(mtv_lines, channel_address):
                    mtv_lines.append(line)
            else:
                if channel_address not in other_lines_url:
                    other_lines_url.append(channel_address)   #记录已加url
                    other_lines.append(line)
                    
def process_url(url):
    print(f"处理URL: {url}")
    try:
        other_lines.append(url+",#genre#")  # 存入other_lines便于check 2024-08-02 10:41
        
        # 创建一个请求对象并添加自定义header
        headers = {
            'User-Agent': 'PostmanRuntime-ApipostRuntime/1.1.0',
        }
        req = urllib.request.Request(url, headers=headers)
        # 打开URL并读取内容
        with urllib.request.urlopen(req,timeout=10) as response:
            # 以二进制方式读取数据
            data = response.read()
            # 将二进制数据解码为字符串
            try:
                # 先尝试 UTF-8 解码
                text = data.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    # 若 UTF-8 解码失败，尝试 GBK 解码
                    text = data.decode('gbk')
                except UnicodeDecodeError:
                    try:
                        # 若 GBK 解码失败，尝试 ISO-8859-1 解码
                        text = data.decode('iso-8859-1')
                    except UnicodeDecodeError:
                        print("无法确定合适的编码格式进行解码。")
                        
            #处理m3u提取channel_name和channel_address
            if is_m3u_content(text):
                text=convert_m3u_to_txt(text)

            # 逐行处理内容
            lines = text.split('\n')
            print(f"行数: {len(lines)}")
            for line in lines:
                if  "#genre#" not in line and "," in line and "://" in line:
                    # 拆分成频道名和URL部分
                    channel_name, channel_address = line.split(',', 1)
                    #需要加处理带#号源=予加速源
                    if "#" not in channel_address:
                        process_channel_line(line) # 如果没有井号，则照常按照每行规则进行分发
                    else: 
                        # 如果有“#”号，则根据“#”号分隔
                        url_list = channel_address.split('#')
                        for channel_url in url_list:
                            newline=f'{channel_name},{channel_url}'
                            process_channel_line(newline)

            other_lines.append('\n') #每个url处理完成后，在other_lines加个回车 2024-08-02 10:46

    except Exception as e:
        print(f"处理URL时发生错误：{e}")

def sort_data(order, data):
    # 创建一个字典来存储每行数据的索引
    order_dict = {name: i for i, name in enumerate(order)}
    
    # 定义一个排序键函数，处理不在 order_dict 中的字符串
    def sort_key(line):
        name = line.split(',')[0]
        return order_dict.get(name, len(order))
    
    # 按照 order 中的顺序对数据进行排序
    sorted_data = sorted(data, key=sort_key)
    return sorted_data

#白名单加入
other_lines.append("白名单,#genre#")
print(f"添加白名单 whitelist.txt")
for line in whitelist_lines:
    process_channel_line(line)

#读取whitelist,把高响应源从白名单中抽出加入。
other_lines.append("白名单测速,#genre#")
print(f"添加白名单 whitelist_auto.txt")
for line in whitelist_auto_lines:
    if  "#genre#" not in line and "," in line and "://" in line:
        parts = line.split(",")
        try:
            response_time = float(parts[0].replace("ms", ""))
        except ValueError:
            print(f"response_time转换失败: {line}")
            response_time = 60000  # 单位毫秒，转换失败给个60秒
        if response_time < 2000: #2s以内的高响应源
            process_channel_line(",".join(parts[1:]))

#加入配置的url
for url in urls:
    if url.startswith("http"):        
        process_url(url)

# 获取当前的 UTC 时间
utc_time = datetime.now(timezone.utc)
# 北京时间
beijing_time = utc_time + timedelta(hours=8)
# 格式化为所需的格式
formatted_time = beijing_time.strftime("%Y%m%d %H:%M")
version=formatted_time+",https://gcalic.v.myalicdn.com/gc/wgw05_1/index.m3u8?contentid=2820180516001"

# 瘦身版
all_lines_simple =  ["更新时间,#genre#"] + [version] + ['\n'] +\
                    ["央视频道,#genre#"] + sort_data(ys_dictionary,ys_lines) + ['\n'] + \
                    ["卫视频道,#genre#"] + sort_data(ws_dictionary,ws_lines) + ['\n'] + \
                    ["港澳台,#genre#"] + sort_data(gat_dictionary,gat_lines) + ['\n'] + \
                    ["电影频道,#genre#"] + sort_data(dy_dictionary,dy_lines) + ['\n'] + \
                    ["电视剧频道,#genre#"] + sort_data(dsj_dictionary,dsj_lines) + ['\n'] + \
                    ["综艺频道,#genre#"] + sort_data(zy_dictionary,zy_lines) + ['\n'] + \
                    ["NewTV,#genre#"] + sort_data(newtv_dictionary,newtv_lines) + ['\n'] + \
                    ["iHOT,#genre#"] + sort_data(ihot_dictionary,ihot_lines) + ['\n'] + \
                    ["体育频道,#genre#"] + sort_data(ty_dictionary,ty_lines) + ['\n'] + \
                    ["咪咕直播,#genre#"] + sort_data(migu_dictionary,migu_lines)+ ['\n'] + \
                    ["埋堆堆,#genre#"] + sort_data(mdd_dictionary,mdd_lines) + ['\n'] + \
                    ["音乐频道,#genre#"] + sorted(yy_lines) + ['\n'] + \
                    ["游戏频道,#genre#"] + sorted(game_lines) + ['\n'] + \
                    ["解说频道,#genre#"] + sorted(js_lines)

# 合并所有对象中的行文本（去重，排序后拼接）
all_lines =  all_lines_simple + ['\n'] + \
             ["儿童,#genre#"] + sort_data(et_dictionary,et_lines) + ['\n'] + \
             ["国际台,#genre#"] + sort_data(gj_dictionary,gj_lines) + ['\n'] + \
             ["纪录片,#genre#"] + sort_data(jlp_dictionary,jlp_lines)+ ['\n'] + \
             ["戏曲频道,#genre#"] + sort_data(xq_dictionary,xq_lines) + ['\n'] + \
             ["上海频道,#genre#"] + sort_data(sh_dictionary,sh_lines) + ['\n'] + \
             ["湖南频道,#genre#"] + sort_data(hn_dictionary,hn_lines) + ['\n'] + \
             ["湖北频道,#genre#"] + sort_data(hb_dictionary,hb_lines) + ['\n'] + \
             ["广东频道,#genre#"] + sort_data(gd_dictionary,gd_lines) + ['\n'] + \
             ["浙江频道,#genre#"] + sort_data(zj_dictionary,zj_lines) + ['\n'] + \
             ["山东频道,#genre#"] + sort_data(shandong_dictionary,shandong_lines) + ['\n'] + \
             ["江苏频道,#genre#"] + sorted(jsu_lines) + ['\n'] + \
             ["安徽频道,#genre#"] + sorted(ah_lines) + ['\n'] + \
             ["海南频道,#genre#"] + sorted(hain_lines) + ['\n'] + \
             ["内蒙频道,#genre#"] + sorted(nm_lines) + ['\n'] + \
             ["辽宁频道,#genre#"] + sorted(ln_lines) + ['\n'] + \
             ["陕西频道,#genre#"] + sorted(sx_lines) + ['\n'] + \
             ["山西频道,#genre#"] + sorted(shanxi_lines) + ['\n'] + \
             ["云南频道,#genre#"] + sorted(yunnan_lines) + ['\n'] + \
             ["北京频道,#genre#"] + sorted(bj_lines) + ['\n'] + \
             ["重庆频道,#genre#"] + sorted(cq_lines) + ['\n'] + \
             ["福建频道,#genre#"] + sorted(fj_lines) + ['\n'] + \
             ["甘肃频道,#genre#"] + sorted(gs_lines) + ['\n'] + \
             ["广西频道,#genre#"] + sorted(gx_lines) + ['\n'] + \
             ["贵州频道,#genre#"] + sorted(gz_lines) + ['\n'] + \
             ["河北频道,#genre#"] + sorted(heb_lines) + ['\n'] + \
             ["河南频道,#genre#"] + sorted(hen_lines) + ['\n'] + \
             ["黑龙江频道,#genre#"] + sorted(hlj_lines) + ['\n'] + \
             ["吉林频道,#genre#"] + sorted(jl_lines) + ['\n'] + \
             ["江西频道,#genre#"] + sorted(jx_lines) + ['\n'] + \
             ["宁夏频道,#genre#"] + sorted(nx_lines) + ['\n'] + \
             ["青海频道,#genre#"] + sorted(qh_lines) + ['\n'] + \
             ["四川频道,#genre#"] + sorted(sc_lines) + ['\n'] + \
             ["天津频道,#genre#"] + sorted(tj_lines) + ['\n'] + \
             ["新疆频道,#genre#"] + sorted(xj_lines) + ['\n'] + \
             ["春晚,#genre#"] + sort_data(cw_dictionary,cw_lines)  + ['\n'] + \
             ["直播中国,#genre#"] + sorted(zb_lines) + ['\n'] + \
             ["MTV,#genre#"] + sorted(mtv_lines) + ['\n'] + \
             ["收音机频道,#genre#"] + sort_data(radio_dictionary,radio_lines)

# 将合并后的文本写入文件
output_file = "live.txt"
output_file_simple = "live_lite.txt"
# 未匹配的写入文件
others_file = "others.txt"

try:
    # 瘦身版
    with open(output_file_simple, 'w', encoding='utf-8') as f:
        for line in all_lines_simple:
            f.write(line + '\n')
    print(f"合并后的精简文本已保存到文件: {output_file_simple}")

    # 全集版
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in all_lines:
            f.write(line + '\n')
    print(f"合并后的文本已保存到文件: {output_file}")

    # 其他
    with open(others_file, 'w', encoding='utf-8') as f:
        for line in other_lines:
            f.write(line + '\n')
    print(f"其他已保存到文件: {others_file}")

except Exception as e:
    print(f"保存文件时发生错误：{e}")

def make_m3u(txt_file, m3u_file):
    try:
        output_text = '#EXTM3U x-tvg-url="https://epg.112114.xyz/pp.xml.gz"\n'
        with open(txt_file, "r", encoding='utf-8') as file:
            input_text = file.read()

        lines = input_text.strip().split("\n")
        group_name = ""
        for line in lines:
            parts = line.split(",")
            if len(parts) == 2 and "#genre#" in line:
                group_name = parts[0]
            elif len(parts) == 2:
                channel_name = parts[0]
                channel_url = parts[1]
                logo_url="https://epg.112114.free.hr/logo/"+channel_name+".png"
                if logo_url is None: #not found logo
                    output_text += f"#EXTINF:-1 group-title=\"{group_name}\",{channel_name}\n"
                    output_text += f"{channel_url}\n"
                else:
                    output_text += f"#EXTINF:-1  tvg-name=\"{channel_name}\" tvg-logo=\"{logo_url}\"  group-title=\"{group_name}\",{channel_name}\n"
                    output_text += f"{channel_url}\n"

        with open(f"{m3u_file}", "w", encoding='utf-8') as file:
            file.write(output_text)
        print(f"M3U文件 '{m3u_file}' 生成成功。")
    except Exception as e:
        print(f"发生错误: {e}")

make_m3u(output_file, "live.m3u")
make_m3u(output_file_simple, "live_lite.m3u")

# 执行结束时间
timeend = datetime.now()

# 计算时间差
elapsed_time = timeend - timestart
total_seconds = elapsed_time.total_seconds()

# 转换为分钟和秒
minutes = int(total_seconds // 60)
seconds = int(total_seconds % 60)

print(f"执行时间: {minutes} 分 {seconds} 秒")

combined_blacklist_hj = len(combined_blacklist)
all_lines_hj = len(all_lines)
other_lines_hj = len(other_lines)
print(f"blacklist行数: {combined_blacklist_hj} ")
print(f"live.txt行数: {all_lines_hj} ")
print(f"others.txt行数: {other_lines_hj} ")

#备用1：http://tonkiang.us
#备用2：https://www.zoomeye.hk,https://www.shodan.io,https://tv.cctv.com/live/
#备用3：(BlackList检测对象)http,rtmp,p3p,rtp（rtsp，p2p）
