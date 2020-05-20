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
from tabulate import tabulate


gcookie = ''

neteasemusicapi='http://192.168.1.202:3000' 
qqmusicapi='http://192.168.1.202:3300'


def netease_login(user,passwd):
    url = neteasemusicapi+'/login/cellphone?phone='+user+'&password='+passwd
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
    url = neteasemusicapi+'/user/playlist?uid='+userid
    r = requests.get(url)
    team = json.loads(r.text)
    npldf = pd.DataFrame()
    for i in range(len(team['playlist'])):
        pname = team['playlist'][i]['name']
        pid =  team['playlist'][i]['id']
        npldf = npldf.append({'listid':str(pid),'listname':pname}, ignore_index=True) 
        #nl.append(str(i) +'|'+str(pid)+'|'+pname)
    return npldf



def getnesonglist(playlistid):
    url = neteasemusicapi+'/playlist/detail?id='+playlistid
    r = requests.get(url)
    team = json.loads(r.text)
    nsldf = pd.DataFrame(columns=['songname','artname','nid'])
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
        nsldf = nsldf.append({'songname':sname.lower(),'artname':aname.lower(),'nid':str(nid)}, ignore_index=True)
        #sl.append(str(i)+'|'+str(nid)+'|'+sname+'|'+aname)
    return nsldf


def getnid(sname,aname,mode):
    sname = sname.lower().strip()
    aname = aname.lower().strip()
    url = neteasemusicapi+'/search?keywords='+ sname + ' ' + aname
    r = requests.get(url)
    team = json.loads(r.text)
    gdf = pd.DataFrame(columns=['songname','artname','nid'])
    nid = ''
    try :
        songs_list = team['result']['songs']
        for i in range(len(songs_list)):
            nsongname = team['result']['songs'][i]['name']
            nsongid =  team['result']['songs'][i]['id']
            nsinger = team['result']['songs'][i]['artists']
            artname = nsinger[0]['name'].lower()
            if len(nsinger) > 1:
                artname = ''
                for j in range(len(nsinger)):
                    artname = nsinger[j]['name']+ ','+ artname
                artname = artname[0:len(artname)-1]
            
            artname = artname.lower().strip()
            nsongname = nsongname.lower().strip()

            if mode == 1:
                if ((nsongname in sname) or (sname in nsongname)) and artname == aname:
                    return str(nsongid)
                    break   
            if mode == 0:
                gdf = gdf.append({'songname':nsongname.lower(),'artname':artname.lower(),'nid':str(nsongid)}, ignore_index=True)
                #rlist.append(str(i)+'|'+str(nsongid)+'|'+nsongname+'|'+artname)
        if mode == 0: 
            return gdf        
    except:
        print('匹配错误')



def addplaylist(songid,playlistid):
    url = neteasemusicapi+'/playlist/tracks?op=add&pid='+playlistid+'&tracks='+songid+','+songid
    r = requests.get(url,cookies=gcookie)
    team = json.loads(r.text)
    return team['code']
    



def getqqplaylist(qqno):
    url = qqmusicapi+'/user/songlist?id='+qqno
    r = requests.get(url)
    team = json.loads(r.text)
    qpldf = pd.DataFrame()
    for i in range(len(team['data']['list'])):
        qlistid = team['data']['list'][i]['tid']
        qlistname = team['data']['list'][i]['diss_name']        
        qpldf = qpldf.append({'listid':str(qlistid),'listname':qlistname}, ignore_index=True) 
    return qpldf



def getqqsonglist(playlistid):
    url = qqmusicapi+'/songlist?id='+playlistid
    r = requests.get(url)
    team = json.loads(r.text)
    #sl = []
    df = pd.DataFrame() 
    try:
        for i in range(len(team['data']['songlist'])):    
            singer = team['data']['songlist'][i]['singer']
            artname=singer[0]['name']
            if len(singer) > 1:
                artname = ''
                for j in range(len(singer)):
                      artname = singer[j]['name']+','+ artname
                artname = artname[0:len(artname)-1]  
            songname = team['data']['songlist'][i]['songname']
            df = df.append({'songname':songname.lower(),'artname':artname.lower()}, ignore_index=True) 
            #sl.append(songname.lower()+'|'+artname.lower())
    finally:
        return df

        
#=======================================================================================
#   script begin
#=======================================================================================
#pd.set_option('display.max_colwidth',100)

print('''

 QQ音乐歌单导出至网易云音乐
          
 也不知道叫啥好，暂定名称： QQ2NE v1.0
 
 keivenliao@gmail.com
 https://github.com/keivenliao/QQ2NE         
      
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
    print(tabulate(qpl, headers='', tablefmt='fancy_grid'))
        
    while True:
         ip = input('请输入歌单 id: ')
         if ip == 'quit':
             sys.exit()
             
         if ip.isdigit():
             if int(ip) in range(0,len(qpl)):
                 
                 pid = qpl.loc[int(ip),'listid']
                 print('获取歌单内歌曲清单，请稍候...\r\n') 
                 
                 qsl = getqqsonglist(pid)
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
    
    
    print(tabulate(qsl, headers='', tablefmt='fancy_grid')) 
    qsl.to_csv('cache',index=None) 
    df = qsl
    df['nid']='none'
    print('\r\n歌单内共有 '+Fore.RED+str(len(qsl))+Style.RESET_ALL+' 首歌曲, 本地缓存已保存，按 <回车> 继续 ')
    input()

    
#有本地缓存
else:
    print('发现本地缓存文件，请稍候.. \r\n')
    time.sleep(1)
    try:
        df = pd.read_csv('cache',dtype=str)
        
        if 'nid' not in df.columns:
            df['nid']='none' #添加ID字段
            
        dfview = df.copy()
        for i in range(len(dfview)):
            nid = dfview.loc[i,'nid'].lower().strip()
            if nid == 'none':
                dfview.loc[i,'nid'] = Fore.RED+dfview.loc[i,'nid']+Style.RESET_ALL
                    
        print(tabulate(dfview, headers='', tablefmt='fancy_grid'))   
        print('\r\n本地缓存内有 '+ Fore.RED + str(len(df)) + Style.RESET_ALL + ' 首歌曲,',end='')
        print('其中未匹配网易云音乐歌曲ID有 '+Fore.RED+str(len(df[df['nid'] == 'none']))+Style.RESET_ALL+' 首歌曲，按 <回车> 继续.. ')
        input()
    except:
        print('本地缓存加载失败')
        sys.exit()


#自动匹配
if len(df[df['nid'] == 'none']) > 0:
    print('开始自动匹配网易云音乐歌曲ID: ')
    index_noid = df[df['nid'] == 'none'].index.tolist()
    for c,i in enumerate(index_noid):
        sname = df.loc[i,'songname'].lower()
        aname = df.loc[i,'artname'].lower() 
        nid = df.loc[i,'nid'].lower().strip()        
        if nid == 'none':
            nid = str(getnid(sname,aname,1)).strip().lower()
            if nid == 'none':
                nid = Fore.RED+'None'+Style.RESET_ALL
            else:
                df.loc[i,'nid']=nid
        
        
        #print('\r  '+str(i+1)+'/'+str(len(df))+':   '+sname+' , '+aname+' , '+nid+'\t\t\t\t\t\t\t',end='')
        c += 1    
        print(str(c)+'/'+str(len(index_noid))+':   '+sname+' , '+aname+' , '+nid)
        
    df.to_csv('cache',index=None)
    print('\r\n\r\n自动匹配完毕，本地缓存已更新 \r\n')        


#手动匹配
if len(df[df['nid'] == 'none']) > 0:
    print('有 '+Fore.RED+str(len(df[df['nid'] == 'none']))+Style.RESET_ALL+' 首歌未找到网易云音乐歌曲 ID, 按 <回车> 开始手动匹配 ')
    input()
    while len(df[df['nid'] == 'none']) > 0:
        index_noid = df[df['nid'] == 'none'].index.tolist()
        sname = df.loc[index_noid[0],'songname'].lower()
        aname = df.loc[index_noid[0],'artname'].lower()
        print('\r\n现在匹配:  "'+sname+' , '+aname+'"  找到以下可能的结果: \r\n')
        ndf = getnid(sname,aname,0)
        for i in range(len(ndf)):
            if ndf.loc[i,'songname'] == sname:
                ndf.loc[i,'songname'] = Fore.RED+ndf.loc[i,'songname']+Style.RESET_ALL
            if ndf.loc[i,'artname'] == aname:
                ndf.loc[i,'artname'] = Fore.RED+ndf.loc[i,'artname']+Style.RESET_ALL
                
        print(tabulate(ndf, headers='', tablefmt='fancy_grid'))    
        
       # likelist = getnid(sname,aname,0)
       #  for i in likelist:
       #      i = i.lower()
       #      a = i.split('|')
       #      if sname == a[2]:
       #          a[2] = Fore.RED + a[2] + Style.RESET_ALL
       #      if aname == a[3]:
       #          a[3] = Fore.RED + a[3] + Style.RESET_ALL
       #      print(a[0]+' , '+a[1]+' , '+a[2]+' , '+a[3])
       
        while True:
            ip=input('\r\n请输入歌曲序号: ')
            if ip.isdigit():
                if int(ip) in range(0,len(ndf)):
                    break
                else:
                    print('input error')
                    continue
            else:
                print('input error')
                continue  
            
        
        selsid = ndf.loc[int(ip),'nid']

        #dfindex = df[(df.songname==sname)&(df.artname==aname)].index.tolist() #df 内的查询
        df.loc[index_noid[0],'nid'] = selsid
        if len(df[df['nid'] == 'none']) >0:
            print('\r\n剩余 '+str(len(df[df['nid'] == 'none']))+' 首歌需要匹配 ')
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
npldf = getneplaylist(uid) 
print(tabulate(npldf, headers='', tablefmt='fancy_grid')) 
# for i in Neplaylist:
#     a = i.split('|')
#     print(a[0]+'   '+a[1]+'  '+a[2])


while True:
    ip = input('\r\n请选择导入目标歌单 ID: ')
    if ip.isdigit():
        if int(ip) in range(0,len(npldf)):
            break
        else:
            print('input error')
            continue 
    else:
        print('input error')
        continue 

usersel= npldf.loc[int(ip),'listid'] 
tplaylistid = usersel

print('你选择的歌单 ID 是: '+tplaylistid+' \r\n')




nsldf = getnesonglist(tplaylistid)


for i in range(len(nsldf)):
    rnid = nsldf.loc[i,'nid']
    dfindex = df[df['nid'] == rnid].index.tolist()
    df = df.drop(dfindex)
df = df.reset_index(drop=True)
    

if len(df) == 0:
    input('你选择的网易云音乐歌单已包含QQ音乐歌单的所有歌曲, 按 <回车> 退出 ')
    os.remove('cache')
    sys.exit()
else:
    print(tabulate(df, headers='', tablefmt='fancy_grid')) 



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
        print('如果错误码为 "405" 是因为导入歌曲过多导致, 按 <ctrl + c> 终止. 2分钟后再重新执行本脚本')
        print('不必担心，导入成功的歌曲会自动过滤，如果你的歌曲确实很多，那么多运行几次本脚本即可。')
        
    else:
        print(s_sname +' , '+s_aname+' , '+str(s_nid)+'"  导入成功')

 
print('\r\n============导完收工============')
os.remove('cache')


    
 
    

