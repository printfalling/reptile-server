# reptile server

***still updating***

> this is a simple application with some simple HTML and python knowledge, in order to apply to some useful functions.

Simple introduction of the functions:

+ Getting informations in  opac.lib.ustc.edu.cn

+ Checking whether a book is avaliable, if avaliable it will sent a e-mail to the given e-mail address.

Way of application:

### reptile-server.py

This file is the mail file of the server

1. apply get approach, and post approach 

> In get approach, if will return an index html, which contains four blocks. The first block is used for enteringthe given e-mail; 
the second block is used to enter the name of the book; the thrid block is used to enter the index of the book in USTC lib, and the
forth block is a choice block, it ask the user to choose whether to start the checking approach.

> In post approach, it get three inputs, the given e-mail, the name of the book and the index of the book, then the post approach 
will check whether the book is valid in the library, whether it is avalibable, and then tell the user the reeult

2. Checking approach

> These approach will apply in a asynchronous way, it will check whether the book in the checking all the book in the checking the 
book in the list whether list is is avaliable every one hour.If it is avaliable is will sent an e-mail to the gven e-mail and delete
the book in the checking list.

3. Updeting approach

> The server will be designed to update and clean all the infomations for a period of times(for example : a month)

### reptile\_sarcher.py

This file is serve as the reptile that collect information from the opac.lib.ustc.edu.com.

1. Get index page

> This methon is a test methon that tell you whether the reptile can work. If it don't work there maybe some ploblem in you packages or you computer can't connect to the aim address

2. Search Book name

> This methon is designed to search the name of hte book on the opac.lib.ustc.edu.com.

