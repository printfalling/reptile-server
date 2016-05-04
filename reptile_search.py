import re

from bs4 import BeautifulSoup
from requests import get, post


class MyRequestHandler(object):
    """
    ['ConnectionError', 'FileModeWarning', 'HTTPError', 'NullHandler', 'PreparedRequest', 'Request', 'RequestException',
     'Response', 'Session', 'Timeout', 'TooManyRedirects', 'URLRequired', '__author__', '__build__', '__builtins__',
     '__cached__', '__copyright__', '__doc__', '__file__', '__license__', '__loader__', '__name__', '__package__',
     '__path__', '__spec__', '__title__', '__version__', 'adapters', 'api', 'auth', 'certs', 'codes', 'compat',
     'cookies', 'delete', 'exceptions', 'get', 'head', 'hooks', 'logging', 'models', 'options', 'packages', 'patch',
     'post', 'put', 'request', 'session', 'sessions', 'status_codes', 'structures', 'utils', 'warnings']
    """

    def __init__(self):
        self.index_url = "http://opac.lib.ustc.edu.cn/opac/search.php"
        self.search_url = "http://opac.lib.ustc.edu.cn/opac/openlink.php?"
        self.sub_index_url = 'http://opac.lib.ustc.edu.cn/opac/'

    def get_soup(self):
        r = get(self.index_url)
        index_soup = BeautifulSoup(r.text)
        return index_soup

    def post_search(self, book_name):
        """
        http://opac.lib.ustc.edu.cn/opac/openlink.php?strSearchType=title&match_flag=forward&historyCount=1&
        strText=python&doctype=ALL&displaypg=20&showmode=list&sort=CATA_DATE&orderby=desc&location=ALL
        :param book_name:
        :return:
        """
        data = {
            "strSearchType": "title",
            "match_flag": "forward",
            "historyCount": "1",
            "strText": str(book_name),
            "doctype": "ALL",
            "displaypg": "200",
            "showmode": "list",
            "sort": "CATA_DATE",
            "orderby": "desc",
            "location": "ALL",
        }
        r = post(self.search_url, data=data)
        search_soup = BeautifulSoup(r.text, "lxml")
        return search_soup

    def get_url(self, soup):
        url_list_raw = soup.find_all(name='a', href=re.compile('opac\.lib\.ustc\.edu\.cn'))
        url_list_out = [acher['href'].replace('..', self.index_url) for acher in url_list_raw]
        return url_list_out

    def get_link(self, soup):
        link_list_raw = soup.find_all(name='a', href=re.compile('openlink\.php\?'))
        link_list_out = [self.sub_index_url + acher['href'] for acher in link_list_raw]
        return link_list_out

    def get_item_url(self, soup):
        item_list_raw = soup.find_all(name='a', href=re.compile('item\.php\?'))
        item_list_out = [self.sub_index_url + acher['href'] for acher in item_list_raw]
        return item_list_out

    def get_page_num(self, search_soup):
        assert isinstance(search_soup, BeautifulSoup)
        num_list = search_soup.find_all(name='font', color="black")
        if len(num_list) is not 0:
            page_num = re.compile('<font .*?>(\d)</font>').findall(str(num_list.pop()))
            return page_num
        else:
            return [1]

    def search_page_num(self, title, my_soup):
        """
        <a class="blue" href="?location=ALL&amp;title=python&amp;doctype=ALL&amp;lang_code=ALL&amp;match_flag=forward&
        amp;displaypg=20&amp;showmode=list&amp;orderby=DESC&amp;sort=CATA_DATE&amp;onlylendable=no&amp;count=82&amp;
        with_ebook=&amp;page=2">下一页</a>

        :param title:
        :return:
        """
        data = {
            'location': 'ALL',
            'title': str(title),
            'doctype': 'ALL',
            'lang_code': 'ALL',
            'match_flag': 'forward',
            'displaypg': '200',
            'showmode': 'list',
            'orderby': 'DESC',
            'sort': 'CATA_DATE',
            'onlylendable': 'no',
            'count': '',
            'with_ebook': '',
            'page': '2',
        }
        url_list = []
        num_list = self.get_page_num(my_soup)
        num = num_list.pop()
        print(num)
        for i in range(2, int(num) + 1):
            print(i)
            data['page'] = str(i)
            r = post(self.search_url, data=data)
            search_soup = BeautifulSoup(r.text, "lxml")
            url_list = url_list + self.get_item_url(search_soup)
        return url_list

    def get_book_info(self, search_soup):
        info_list = []
        info_re = re.compile(r'<h3><span>.+?</span><a href="item\.php\?marc_no=\d+">\d\.(.*?)</a>\s+(.*?)\s+</h3>')
        temp_info_list = search_soup.find_all('h3')
        info_list = info_re.findall(str(temp_info_list))
        return info_list




        pass


if __name__ == '__main__':
    handler = MyRequestHandler()
    index_soup = handler.post_search('麦田里的守望者')
    # assert isinstance(index_soup, BeautifulSoup)
    # url_list = list(set(handler.get_item_url(index_soup)))
    # url_list += list(set(handler.search_page_num('python', index_soup)))
    # assert isinstance(url_list, list)
    # print(str(url_list).replace('\'', '\n'))
    # print(len(url_list))
    # f = open('textfile.txt', 'w')
    # f.write(str(index_soup))
    # f.close()
    info_list = handler.get_book_info(index_soup)
    print(info_list[0])
    f = open('test.txt', 'w')
    f.write(str(info_list[0]))
    f.close()


