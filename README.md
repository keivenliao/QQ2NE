# QQ2NE
## 脚本描述：
将qq音乐歌单导入网易音乐歌单

## 脚本原理：
1、借用 QQMusicApi 获取QQ音乐的playlist以及包含歌曲
2、将歌曲 通过 NeteaseCloudMusicApi 匹配网易云音乐的 歌曲ID
3、登录网易云音乐
4、将匹配好ID的歌曲清单导入到指定的网易云音乐歌单

## 首先要做：
1、本地部署 QQMusicApi，NeteaseCloudMusicApi
2、可能需要将NeteaseCloudMusicApi 的https 替换为 http（可选步骤） 
3、修改脚本中的地址为你自己的

## 为什么要写这个脚本
1、网易云音乐可以解锁无版权歌曲
2、我QQ音乐歌单里有几百首歌

## 怎么弄
1、自己刷个lean大神的 openwrt（以下简称op）
2、在op上启用 UnblockNeteaseMusic

## 高级玩法
1、op安装ddns，并在阿里云注册自己的域名
2、在op上安装softether
3、在外网时，手机VPN连接op 也可以享受解锁无版权（开车听歌必选）

## 感谢
https://github.com/Binaryify/NeteaseCloudMusicApi

https://github.com/jsososo/QQMusicApi

https://github.com/coolsnowwolf/lede 

https://github.com/nondanee/UnblockNeteaseMusic




