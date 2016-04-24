import random

import tornado.gen
import tornado.httpserver
import tornado.options
import tornado.web
from tornado.concurrent import run_on_executor
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import RequestHandler, Application

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
        self.write('TestHandler: ')
        self.write(str(book_list))


class IndexHandler(RequestHandler):
    def get(self):
        self.render('index.html')


class SetHandler(RequestHandler):
    @run_on_executor
    def post(self):
        mail = self.get_argument('mail')
        book_name = self.get_argument('book_name')
        book_index = self.get_argument('index')
        is_on = self.get_argument('is_on')
        book = Book(book_name, book_index, mail, is_on)
        exist = self.check_book_exist(book)
        book_list.append(book)

    def check_book_exist(self, book):
        pass;


settings = {
    "cookie_secret": "udhdchgwjnG^&*Y%76798UH&*GfD%^&TG%^$D^%&TXg*(YG7xf677",
    "xsrf_cookies": True,
    "xheaders": True
}

applications = Application([
    (r"/", IndexHandler),
    (r"/test", TestHandler),
], **settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    applications.listen(options.port)
    IOLoop.instance().start()
