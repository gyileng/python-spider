# 爬虫

标签： python 爬虫

---
&emsp;&emsp;1、时隔多日再次拾起爬虫，以后尽量隔段时间都可以更新一个爬虫，我的打算是先爬取国内大部分的旅游网站(携程；去哪儿；58同城...)，后续在考虑其他的，或者也可以提一些需求，有时间我会去写。<br><br>
&emsp;&emsp;2、系统使用Linux,Python版本使用的是3.6，虚拟环境使用virtualenv，IDE使用Pycharm，数据库使用MongoDB。<br><br>
&emsp;&emsp;3、开发环境:Ubuntu+Python3.6+virtualenv+Pycharm+MongoDB

---

 - [00-以前的杂项][1]<br>
 - [01-携程各大城市酒店实时信息][2]<br>
 &emsp;&emsp;目前只支持北京，上海，天津，连云港城市的酒店信息查询，需要其他的城市需要配置config.py
 - [02-飞猪各大城市酒店实时信息][3]<br>
 &emsp;&emsp;由于阿里的反爬策略高明，各种请求参数都是JS加密的本人能力有限。所以只能使用seleinum + Chrome来获取数据，这个版本的程序是在Win10下写的，所以需要早Linux下运行的需要自行调试修改，后续有精力在想解密的事情吧。
 - 待定

**联系方式：gaoyang950616@gmail.com**
 


  [1]: https://github.com/gyileng/python-spider/tree/master/00-%E6%9D%82%E9%A1%B9
  [2]: https://github.com/gyileng/python-spider/tree/master/01-%E6%90%BA%E7%A8%8B
  [3]: https://github.com/gyileng/python-spider/tree/master/02-%E9%A3%9E%E7%8C%AA
