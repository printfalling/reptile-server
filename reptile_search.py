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
            "displaypg": "20",
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
        print(str(num_list[0]))
        page_num = re.compile('<font .*?>(\d)</font>').findall(str(num_list.pop()))
        return page_num

    def search_page_num(self, page_num):
        """
        <a class="blue" href="?location=ALL&amp;title=python&amp;doctype=ALL&amp;lang_code=ALL&amp;match_flag=forward&
        amp;displaypg=20&amp;showmode=list&amp;orderby=DESC&amp;sort=CATA_DATE&amp;onlylendable=no&amp;count=82&amp;
        with_ebook=&amp;page=2">下一页</a>

        :param page_num:
        :return:
        """

if __name__ == '__main__':
    handler = MyRequestHandler()
    index_soup = handler.post_search('python')
    assert isinstance(index_soup, BeautifulSoup)
    url_list = list(set(handler.get_page_num(index_soup)))
    assert isinstance(url_list, list)
    print(str(url_list).replace('\'', '\n'))
    print(len(url_list))
