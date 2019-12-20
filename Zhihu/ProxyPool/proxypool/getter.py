import requests
from lxml import etree
'''
改造思路：
    我想用for循环来做到调用所有的crawl_方法，那应该将这些方法名保存起来，放到一个list中
    将来使用循环就可以知道调用什么方法。
'''
#代理元类
class ProxyMetaclass(type):

    '''
    name:类的名称
    bases:类的继承元组
    attrs:类的属性字典
    '''
    def __new__(cls, name, bases,attrs):
        print('元类')
        count = 0
        attrs['__CrawlFunc__'] = []# 记录爬虫方法名字，把方法放到这里
        for k,v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count+=1
        attrs['__CrwalCount__'] = count#记录爬虫方法个数
        return type.__new__(cls,name,bases,attrs)#

#metaclass=ProxyMetaclass用上面的类创建这个对象
class FreeProxyGetter(object,metaclass=ProxyMetaclass):
    #crawl_xicidaili
    #callback你只要给我传了名字过来，get_raw_proxies这个方法就会调用crawl_89ip这个方法。
    def get_raw_proxies(self,callback):
        proxies = []
        print('callback',callback)
        for proxy in eval('self.{}()'.format(callback)):
            proxies.append(proxy)
        return proxies
    # def crawl_xicidaili(self):
    #     print(1)
    #     # proxies = []
    #     # print(1)
    #     base_url = 'https://www.xicidaili.com/nn/%s'
    #     headers= {
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
    #     }
    #     for i in range(1,50):
    #         response = requests.get(base_url %i,headers=headers)
    #         # print(response.text)
    #         html =etree.HTML(response.text)
    #         ip_list = html.xpath('//tr[position()>1]/td[2]/text()')
    #         port_list = html.xpath('//tr[position()>1]/td[3]/text()')
    #         # print(port_list)
    #         for i ,ip in enumerate(ip_list):
    #             proxy = ip.strip()+':'+port_list[i].strip()
    #             # proxies.append(proxy)
    #             # yield proxy
    #             print(proxy)
    def crawl_89ip(self):
        print(1)
        # proxies = []
        # print(1)
        base_url = 'http://www.89ip.cn/index_%s.html'
        headers= {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        }
        # 分页
        for i in range(1,7):
            response = requests.get(base_url %i,headers=headers)
            # print(response.text)
            html =etree.HTML(response.text)
            ip_list = html.xpath('//tbody/tr/td[1]/text()')
            port_list = html.xpath('//tbody/tr/td[2]/text()')
            # print(port_list)
            for i ,ip in enumerate(ip_list):
                #提前去除空格预防一下
                proxy = ip.strip()+':'+port_list[i].strip()
                # proxies.append(proxy)#返回一个list
                yield proxy
                # print(proxy)


if __name__ == '__main__':
    FreeProxyGetter().crawl_89ip()#先进元类，再进crawl_89ip()
    # print(FreeProxyGetter.__CrawlFunc__)
    # print(FreeProxyGetter.__CrwalCount__)
    '''
    ['crawl_89ip']
    1
    '''