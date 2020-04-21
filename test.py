import requests
from lxml import etree
from urllib.parse import quote
import random


ualist = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]


def receive_keyword(keyword, *maxlength):
    """
    返回不同页数的主页url
    :param keyword: 搜索关键词
    :param maxlength: 从1开始直到maxlength结束， 无则返回第一页url
    :return: 返回的url列表或第一页url
    """
    url_model = 'https://search.51job.com/list/000000,000000,0000,00,9,99,%s,2,%s.html'

    if maxlength:
        return [url_model % (quote(keyword), i) for i in range(1, int(maxlength[0]) + 1)]

    else:
        return url_model % (quote(keyword), 1)


def get_index_info(get_url, t_h):
    """
    得到主页公司名称与链接
    :param get_url: 页面网址
    :param t_h: 空列表
    :return: [(公司名称, 链接), (...)]
    """
    headers = dict()

    headers['User-Agent'] = random.choice(ualist)

    res = requests.get(get_url, headers=headers)
    res.encoding = 'gbk'

    index_html = etree.HTML(res.text)

    titles = index_html.xpath('//div[@class="el"]/p/span/a/@title')
    hrefs = index_html.xpath('//div[@class="el"]/p/span/a/@href')

    for title, href in zip(titles, hrefs):
        if 'https://jobs.51job.com/' in href:
            t_h.append((title, href))

        else:
            continue

    return t_h


def gx(lists):
    try:
        return str(''.join(lists)).replace('\xa0', '').replace(' ', '').replace('\r', '').replace('\n', '')

    except IndexError:
        return None


def get_detail_info(t_h, keyword):
    """
    得到职位详细信息
    :param t_h: (公司名称， 公司网址)
    :param keyword: 搜索关键词
    :return: dict()
    """
    detail_info = dict()
    headers = dict()

    headers['User-Agent'] = random.choice(ualist)

    res = requests.get(t_h[1], headers=headers)
    res.encoding = 'gbk'

    detail_html = etree.HTML(res.text)
    print(t_h)

    company_url = gx(detail_html.xpath('/html/body/div[3]/div[2]/div[4]/div[1]/div[1]/a/@href'))

    res = requests.get(company_url, headers=headers)
    res.encoding = 'gbk'

    company_html = etree.HTML(res.text)

    detail_info['工作名称'] = t_h[0]
    detail_info['工资薪酬'] = gx(detail_html.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/strong/text()'))
    detail_info['公司名称'] = gx(detail_html.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a[1]/@title'))
    detail_info['工作地点'] = gx(detail_html.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()[1]'))
    detail_info['经验要求'] = gx(detail_html.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()[2]'))
    detail_info['学历要求'] = gx(detail_html.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()[3]'))
    detail_info['招聘人数'] = gx(detail_html.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()[4]'))
    detail_info['发布时间'] = gx(detail_html.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()[5]'))
    detail_info['岗位类型'] = keyword
    detail_info['公司规模'] = gx(detail_html.xpath('/html/body/div[3]/div[2]/div[4]/div[1]/div[2]/p[2]/@title'))
    detail_info['行业领域'] = gx(detail_html.xpath('/html/body/div[3]/div[2]/div[4]/div[1]/div[2]/p[3]/a/text()'))
    detail_info['公司地址'] = gx(company_html.xpath('/html/body/div[2]/div[2]/div[3]/div[2]/div/p[1]/text()'))
    detail_info['公司官网'] = gx(company_html.xpath('/html/body/div[2]/div[2]/div[3]/div[2]/div/p[2]/span[2]/text()'))
    detail_info['公司性质'] = gx(company_html.xpath('/html/body/div[2]/div[2]/div[2]/div/p[1]/text()[1]'))
    detail_info['公司Logo'] = gx(detail_html.xpath('/html/body/div[3]/div[2]/div[4]/div[1]/div[1]/a/img/@src'))
    detail_info['公司福利'] = ','.join(detail_html.xpath('//div[@class="jtag"]/div/span/text()'))

    print(detail_info)

    return detail_info

def spider(keyword, maxlength):
    """
    爬虫主程序
    :param keyword: 搜索关键词
    :param maxlength: 爬取页数
    :return: [{...}, {...}]
    """
    title_href = list()
    data = list()

    urls = receive_keyword(keyword, maxlength)
    for url in urls:
        title_href += get_index_info(url, title_href)
        print(title_href)

        for i in title_href:
            data.append(get_detail_info(i, keyword))

    return data


if __name__ == '__main__':
    spider('Java', 10)
