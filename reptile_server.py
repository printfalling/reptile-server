import random

import tornado.gen
import tornado.httpserver
import tornado.options
import tornado.web
from tornado.concurrent import run_on_executor
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import RequestHandler, Application
from test_email import send_mail

from reptile_search import MyRequestHandler

# python 3+ with the futures itself,however you should install it while using python2+
from concurrent.futures import ThreadPoolExecutor

define("port", default=8000, help="run on the given port", type=int)

used_rand = []
book_list = []


class Book(object):
    def __init__(self, book_name, book_index, related_mail, is_on):
        self.name = book_name
        self.index = book_index
        self.mail = related_mail
        self.url = None
        self.exist = False
        self.is_on = is_on
        self.info = (str(self.name), str(self.index))

    def set_url(self, url):
        self.url = url

    def set_exist(self, is_exist):
        self.exist = is_exist


def generate_rand():
    rand = 0
    while rand in used_rand:
        rand = random.randint(1, 100000)
    return rand


class TestHandler(RequestHandler):
    def get(self, *args, **kwargs):
        info_list = [book.info for book in book_list]
        mail_list = [book.mail for book in book_list]
        self.write('TestHandler: ')
        self.write(str(book_list)+'\n'+str(info_list)+'\n'+str(mail_list))



class IndexHandler(RequestHandler):
    def get(self):
        self.render('index.html')


class SetHandler(RequestHandler):
    executor = ThreadPoolExecutor(20)

    @run_on_executor
    def post(self):
        mail = self.get_argument('mail')
        book_name = self.get_argument('book_name')
        book_index = self.get_argument('index')
        is_on = self.get_argument('is_on')
        book = Book(book_name, book_index, mail, is_on)
        exist = self.check_book_exist(book)
        if exist:
            book_list.append(book)
            self.write("This book is surely exist!!\n\r")
            if MyRequestHandler().check_avalible(book.name, book.index):
                self.write("This book is avaliable")


        else:
            self.write("This book is not exist...")

    def check_book_exist(self, book):
        assert isinstance(book, Book)
        handler = MyRequestHandler()
        search_soup = handler.post_search(book_name=book.name)
        info_list = handler.get_book_info(search_soup)
        if book.info in info_list:
            return True
        else:
            return False


settings = {
    "cookie_secret": "udhdchgwjnG^&*Y%76798UH&*GfD%^&TG%^$D^%&TXg*(YG7xf677",
    #"xsrf_cookies": True,
    "xheaders": True,
}

applications = Application([
    (r"/", IndexHandler),
    (r"/test", TestHandler),
    (r"/set", SetHandler),
], **settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    applications.listen(options.port)
    IOLoop.instance().start()
