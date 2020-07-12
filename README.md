<h1 align="center">
  易班自动打卡(20200710更新)
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

**不小心把密码传到这儿来了，麻溜改成私有并回滚了，不知道改私有star也会消失，各位同学喜欢本作品的话点个star呗~**

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

2.`data/data.txt` 提交的json数据，一行一个，长沙理工大学的数据如下：修改部分关键的字段即可。其他大学可能需要自行抓包。编辑`XX`的为要填写的。**已于20200710更新表单。注意一下最后一个暑假留校填否或是**

```json
{"98ddd090dc2a7f5ac666daa41ef113f4":"XX姓名","801a459c3503b1aebe54aef1540602ce":{"name":"地址名","location":"XX经度(小数点后6位),XX纬度(小数点后6位)","address":"XX详细地址描述"},"18ad14fa5b723f437254f4dc8ed92ffc":{"name":"地址名","location":"XX经度(小数点后6位),纬度(小数点后6位)","address":"XX详细地址描述"},"9e479314185767740d3fffcd4c31e2cb":"XX省/XX市/XX县(区)","3cdc6f6669f7bafddbbdeaf04beca8c5":"XX体温","88e831eb1f444f6447c7022c518e7de7":"无","5e50acc9a4fd45fc578d7682ee8799a0":"无","7d4a4f933e87ad84a323b9f893c23937":"无","06e2393cb99c5324fbabd3561c32c723":"无","9352c8ff9850b800eb2fa2453b65d846":"否","eca39739507c9309e1f562b57541b3be":"否","721478664a42a8c42563476e2452ff81":"否","1f1b87c54d448f5eafc70c617f6ef357":"健康","3a0e2ada22349c8b24c1ecd5e860f8e1":"健康","e65b3d45a5a2298bac49ee67faf2e054":"否","1f9d8ca37058562e088494e7cd07b372":"否","4ac0e4c37925e2f307d4322aa02b400f":"否","8992cd6ce8968fb4e7e75089fd73b641":"是否为暑假留校生(否或是)"}
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
