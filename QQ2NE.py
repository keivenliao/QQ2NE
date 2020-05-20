# -*- coding: UTF-8 -*-

#import pandas as pd

import requests
import json
import pandas as pd
import os
import sys
import getpass
import time
from colorama import Fore,Back,Style,init
init(autoreset=True)
gcookie = ''



def netease_login(user,passwd):
    url = 'http://192.168.1.202:3000/login/cellphone?phone='+user+'&password='+passwd
    r = requests.get(url)
    team = json.loads(r.text)
    code = team['code']
    msg = ''
    if code != 200:
        msg = team['message']
        return '-1',str(code),msg
    else:
        userid = team['account']['id']
        global gcookie
        gcookie = r.cookies
        return str(userid),str(code),msg

    
def getneplaylist(userid):
    url = 'http://192.168.1.202:3000/user/playlist?uid='+userid
    r = requests.get(url)
    team = json.loads(r.text)
    nl = []
    for i in range(len(team['playlist'])):
        pname = team['playlist'][i]['name']
        pid =  team['playlist'][i]['id']
        nl.append(str(i) +'|'+str(pid)+'|'+pname)
    return nl



def getnesonglist(playlistid):
    url = 'http://192.168.1.202:3000/playlist/detail?id='+playlistid
    r = requests.get(url)
    team = json.loads(r.text)
    sl = []
    for i in range(len(team['playlist']['tracks'])):
        sname = team['playlist']['tracks'][i]['name']
        nid = team['playlist']['tracks'][i]['id']        
        arts = team['playlist']['tracks'][i]['ar']
        aname = arts[0]['name']
        if len(arts) > 1:
            aname = ''
            for j in range(len(arts)):
                aname = arts[j]['name'] + ','+ aname
            aname = aname[0:len(aname)-1]
        sl.append(str(i)+'|'+str(nid)+'|'+sname+'|'+aname)
    return sl


def getnid(sname,aname):
    sname = sname.lower()
    aname = aname.lower()
    url = 'http://192.168.1.202:3000/search?keywords='+ sname + ' ' + aname
    r = requests.get(url)
    team = json.loads(r.text)
    try :
        songs_list = team['result']['songs']
    finally:
        for i in range(len(songs_list)):
            nsongname = team['result']['songs'][i]['name'].lower()
            nsongid =  team['result']['songs'][i]['id']
            nsinger = team['result']['songs'][i]['artists']
            nsingername = nsinger[0]['name'].lower()
            if len(nsinger) > 1:
                nsingername = ''
                for j in range(len(nsinger)):
                    nsingername = nsinger[j]['name'].lower() + ','+ nsingername
                nsingername = nsingername[0:len(nsingername)-1]
            if ((nsongname in sname) or (sname in nsongname)) and nsingername == aname:
                return str(nsongid)
                break    
        
def getlikenid(sname,aname):
    sname = sname.lower()
    aname = aname.lower()    
    url = 'http://192.168.1.202:3000/search?keywords='+ sname + ' ' + aname
    r = requests.get(url)
    team = json.loads(r.text)
    songs_list = team['result']['songs']
    rlist = []
    for i in range(len(songs_list)):
        nsongname = team['result']['songs'][i]['name'].lower()
        nsongid =  team['result']['songs'][i]['id']
        nsinger = team['result']['songs'][i]['artists']
        nsingername = nsinger[0]['name'].lower()
        if len(nsinger) > 1:
            nsingername = ''
            for j in range(len(nsinger)):
                nsingername = nsinger[j]['name'].lower() + ','+ nsingername
            nsingername = nsingername[0:len(nsingername)-1]
        rlist.append(str(i)+'|'+str(nsongid)+'|'+nsongname+'|'+nsingername)
    return rlist
    
        


def addplaylist(songid,playlistid):
    url = 'http://192.168.1.202:3000/playlist/tracks?op=add&pid='+playlistid+'&tracks='+songid+','+songid
    r = requests.get(url,cookies=gcookie)
    team = json.loads(r.text)
    return team['code']
    



def getqqplaylist(qqno):
    url = 'http://192.168.1.202:3300/user/songlist?id='+qqno
    r = requests.get(url)
    team = json.loads(r.text)
    ql = []
    for i in range(len(team['data']['list'])):
        qlistid = str(team['data']['list'][i]['tid'])
        qlistname = team['data']['list'][i]['diss_name']
        ql.append(qlistid + '|' + qlistname)
    return ql



def getqqsonglist(playlistid):
    url = 'http://192.168.1.202:3300/songlist?id='+playlistid
    r = requests.get(url)
    team = json.loads(r.text)
    sl = []
    try:
        for i in range(len(team['data']['songlist'])):    
            singer = team['data']['songlist'][i]['singer']
            singername=singer[0]['name']
            if len(singer) > 1:
                singername = ''
                for j in range(len(singer)):
                      singername = singer[j]['name'] +','+ singername
                singername = singername[0:len(singername)-1]     
            songname = team['data']['songlist'][i]['songname']
            sl.append(songname+'|'+singername)
    finally:
        return sl

        
#=======================================================================================
#   script begin
#=======================================================================================
#pd.set_option('display.max_colwidth',100)

print('''

 QQ音乐歌单导出至网易云音乐
          
 也不知道叫啥好，暂定名称： QQ2NE v1.0
 
 keivenliao@gmail.com
          
      
      ''')


if not os.path.isfile("cache"):
    while True:
        qq = input('请输入你的QQ号码: ')
        if qq.isdigit():
            break
        else:
            print('QQ 号码错误')
            continue
    qpl = getqqplaylist(qq)
    for i in range(len(qpl)):
        print(str(i)+'    '+qpl[i])
        
    while True:
         ip = input('请输入歌单 id: ')
         if ip == 'quit':
             sys.exit()
             
         if ip.isdigit():
             if int(ip) in range(0,len(qpl)):
                 pid = qpl[int(ip)].split('|')
                 print('获取歌单内歌曲清单，请稍候...\r\n') 
                 
                 qsl = getqqsonglist(pid[0])
                 if len(qsl) == 0:
                     print('歌单内容获取失败，请重新选择 \r\n')
                     continue
                 else:
                     break
             else:
              print('input error')
              continue                
         else:
             print('input error')
             continue
       
    for i in qsl:
        a = i.split('|')
        sname = a[0]
        aname = a[1]
        print(sname+' , '+aname)
    
    print('\r\n有以上共 '+Fore.RED+str(len(qsl))+Style.RESET_ALL+' 首歌需要匹配网易云音乐歌曲 ID, 按 <回车> 继续 ')
    input()
    df=pd.DataFrame()
    for i in qsl:
        a = i.split('|')
        sname = a[0]
        aname = a[1]
        nid = getnid(sname,aname)
        if nid == None:
            print(sname+' , '+aname+' , '+Fore.RED+str(nid)+Style.RESET_ALL)
        else:
            print(sname+' , '+aname+' , '+str(nid))
        df = df.append({'songname':sname,'artname':aname,'nid':nid}, ignore_index=True)
        
    df = df.applymap(lambda s:s.lower() if isinstance(s, str) else s) # lower all str
    df.to_csv('cache',index=None)
    print('\r\n匹配完毕，本地缓存已更新 \r\n')

else: #有本地缓存
    df = pd.read_csv('cache',dtype=str)
    df = df.applymap(lambda s:s.lower() if isinstance(s, str) else s) # lower all str
    input('发现本地缓存文件，按 <回车> 继续... '+'\r\n')
    for i in range(len(df)):
        sname = df.loc[i,'songname'].lower()
        aname = df.loc[i,'artname'].lower()
        if pd.isna(df.loc[i,'nid']):
            nid = Fore.RED+'None'+Style.RESET_ALL
        else:
            nid = df.loc[i,'nid']
        print(sname+' , '+aname+' , '+str(nid))
        
    print('\r\n本地缓存包含以上共 '+ str(len(df)) +' 首歌曲\r\n')

if len(df[df['nid'].isnull()]) > 0:
    print('有 '+Fore.RED+str(len(df[df['nid'].isnull()]))+Style.RESET_ALL+' 首歌未找到网易云音乐歌曲 ID, 按 <回车> 开始手动匹配 ')
    input()
    while len(df[df['nid'].isnull()]) > 0:
        j = df[df['nid'].isnull()].index.tolist()
        sname = df.loc[j[0],'songname'].lower()
        aname = df.loc[j[0],'artname'].lower()
        print('\r\n现在匹配: '+sname+' , '+aname+'  找到以下可能的结果: \r\n')
        likelist = getlikenid(sname,aname)
        for i in likelist:
            i = i.lower()
            a = i.split('|')
            if sname == a[2]:
                a[2] = Fore.RED + a[2] + Style.RESET_ALL
            if aname == a[3]:
                a[3] = Fore.RED + a[3] + Style.RESET_ALL
            print(a[0]+' , '+a[1]+' , '+a[2]+' , '+a[3])
        while True:
            ip=input('\r\n请输入歌曲 id: ')
            if ip.isdigit():
                if int(ip) in range(0,len(likelist)):
                    break
                else:
                    print('input error')
                    continue
            else:
                print('input error')
                continue  
            
        
        usersel = likelist[int(ip)].split('|')
        selsid = usersel[1]
        selsname = usersel[2]
        selaname = usersel[3]
        dfindex = df[(df.songname==sname)&(df.artname==aname)].index.tolist()
        df.loc[dfindex,'nid'] = selsid
        noiddf = df[df['nid'].isnull()]
        if len(df[df['nid'].isnull()]) >0:
            print('\r\n剩余 '+str(len(df[df['nid'].isnull()]))+' 首歌需要匹配 ')
            time.sleep(1)
        
    df.to_csv('cache',index=None)
    print('\r\n匹配完毕，本地缓存已更新 \r\n')


x = input('\r\n现在需要登录到网易云音乐，按 <回车> 继续\r\n')
if x == 'quit':
    sys.exit()

code =0;
while code != 200:
    while True:
        u = input('手机号码: ')
        if u.isdigit() and len(u) == 11:
            break
        else:
            print('手机号码错误\r\n')
            continue 
    while True:
        p = getpass.getpass('密码: ')
        if p !='' :
            break
        else:
            print('密码不能为空\r\n')
            continue   
        
    uid,code,msg = netease_login(u,p)
    if code != '200':
        print('\r\n登录失败: '+msg+'  code: '+code+'\r\n')
        continue
    else:
        break



print('\r\n登录成功，你的网易云音乐用户ID是: '+Fore.RED+uid+Style.RESET_ALL+' 按 <回车> 继续 ')
input()
Neplaylist = getneplaylist(uid) 

for i in Neplaylist:
    a = i.split('|')
    print(a[0]+'   '+a[1]+'  '+a[2])

while True:
    ip = input('\r\n请选择导入目标歌单 ID: ')
    if ip.isdigit():
        if int(ip) in range(0,len(Neplaylist)):
            break
        else:
            print('input error')
            continue 
    else:
        print('input error')
        continue 

usersel= Neplaylist[int(ip)].split('|') 
tplaylistid = usersel[1]

print('你选择的歌单 ID 是: '+tplaylistid+' \r\n')




nsl = getnesonglist(tplaylistid)
for i in nsl:
    a = i.split('|')
    rnid = a[1]
    rsname = a[2]
    raname = a[3]
    dfindex = df[df['nid'] == rnid].index.tolist()
    df = df.drop(dfindex)
df = df.reset_index(drop=True)
    

if len(df) == 0:
    input('你选择的网易云音乐歌单已包含QQ音乐歌单的所有歌曲, 按 <回车> 退出 ')
    os.remove('cache')
    sys.exit()
else:
    for i in range(len(df)):
        s_sname = df.loc[i,'songname']
        s_aname = df.loc[i,'artname']
        s_nid = df.loc[i,'nid']
        print(s_sname +' , '+s_aname+' , '+s_nid)    



while True:
    print('\r\n以上 '+Fore.RED+str(len(df))+Style.RESET_ALL+' 首歌曲，可以添加到此歌单，请输入 "start" 开始导入 ')
    ip = input()
    if ip == 'quit':
        sys.exit()
    if ip == 'start':
        break
    else:
        print('type error')
        continue         

for i in range(len(df)):
    s_sname = df.loc[i,'songname']
    s_aname = df.loc[i,'artname']
    s_nid = df.loc[i,'nid']
    code = addplaylist(s_nid,tplaylistid)
    if code != 200:
        print('add "'+ s_sname +' , '+s_aname+' , '+str(s_nid)+'"  error: '+Fore.RED+str(code)+Style.RESET_ALL)
        time.sleep(2)
        print('如果错误码为 "405" 是因为添加歌曲过多导致, 按 <ctrl + c> 终止运行. 2分钟后再重新运行 ')
        
    else:
        print(s_sname +' , '+s_aname+' , '+str(s_nid)+'"  导入成功')

 
print('\r\n======导完收工======')
os.remove('cache')


    
 
    

