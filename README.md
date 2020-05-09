<h1 align="center">
  易班自动打卡
  <br>
</h1>
<p align="center">
<img src="https://cdn.looyeagee.cn/github/yiban/license.svg"/>
<img src="https://cdn.looyeagee.cn/github/yiban/platform.svg"/>
<img src="https://cdn.looyeagee.cn/github/yiban/python.svg"/>
</p>

## 👀简介

长沙理工大学易班疫情一键上报健康打卡并自动截图，你还可以指定截图目录保存到自己的站点，这样每天访问一个网站就能获取到今天的打卡截图啦～

对原理感兴趣的话，建议看看抓包过程视频：https://www.bilibili.com/video/BV1a741117hQ/

博客文章地址：https://looyeagee.cn/software/yiban/

## :sparkles: 使用说明

Linux环境下，请先根据自己的系统环境安装好谷歌浏览器最新版，然后克隆本仓库后转到目录下执行


```shell
# 安装必要依赖
pip3 install -r requirements.txt

# 赋予谷歌驱动执行权限
chmod +x ./data/chromedriver

# 启动打卡
python3 yiban.py
```

不过，在打卡之前，请修改如下数据：

1.`data/account.txt` 帐号密码以空格隔开，一行一个。

2.`data/data.txt` 提交的json数据，一行一个，长沙理工大学的数据如下：修改部分关键的字段即可。其他大学可能需要自行抓包。

```json
{"69d1ca628e017a2c182902bfabdabd42":"姓名","5680543d3631077265b049b7d9ae418e":"班级","e62910f76e9d5ba63ddc84ae68606f0f":{"name":"地址名","location":"经度(小数点后6位),纬度(小数点后6位)","address":"详细地址描述"},"ba7cabc21493b23bcfd65fa79525c4e0":{"name":"地址名","location":"经度(小数点后6位),纬度(小数点后6位)","address":"详细地址描述"},"cf4bac544816ca83db09a7d8c4d69178":"当前温度","f16558084d32bee1523e085c9be35c30":"无","78bb535617d4caf28944bff53f434e32":"无","43cfde1796a98708e3df57f8088460e4":"无","8f472f4a665f93acf3de5c4ecab8c213":"无","e8578087affe7bde28eb5b6ffa5149e1":"否","24d085dd92e3a2bf43fef782e1fc7025":"否","bd397e1b6437a9dc6129db60d82ffd02":"否","d5adcefa1558c2759edd7c1cb41afbc4":"健康","484b372a88bb52cc0c54dcfbe618f779":"健康","f0ac1554f16879b966c2135bcf3bdb53":"否","7b771dd1f3512486fac560cfec00052b":"否","a6288aa438a4e6e9264f029cc8dc5a5d":"否"}
```

3.`yiban.py` 第30行的`WFId`，长沙理工大学无需更改，其他大学可能不一样，需要自行抓包。

## :rocket: 运行截图

<p align="center">
<img src="https://cdn.looyeagee.cn/github/yiban/yb.png"/>
</p>
自行搭建的截图站点：
<p align="center">
<img src="https://cdn.looyeagee.cn/github/yiban/web.png"/>
</p>
