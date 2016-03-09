import os


class Globalvar5:
    book = dict(FileName=os.environ.get('HOME'), EfitDir=os.environ.get('HOME'), RhoPsi='rho', Shot=100000, Time=3000,
                Params=[])

    def __init__(self, book):
        for key in book:
            Globalvar5.book[key] = book[key]

            # def __call__(self, c):
            # print 'in Globalvar5 c=', c
            # for key in c:
            #     Globalvar5.book[key] = c[key]
            # print 'in Globalvar5', Globalvar5.book
            # return Globalvar5.book


class Globalvar6:
    book = dict(FileName=os.environ.get('HOME'), EfitDir=os.environ.get('HOME'), RhoPsi='rho', Shot=100000, Time=3000,
                Params=[])

    def __init__(self, book):
        for key in book:
            Globalvar6.book[key] = book[key]
        print 'in Globalvar6', '\n', Globalvar6.book

    def __call__(self, c):
        for key in c:
            Globalvar6.book[key] = c[key]
        return Globalvar6.book


class Globalvar7:
    book = dict(FileName=os.environ.get('HOME'), EfitDir=os.environ.get('HOME'), RhoPsi='rho', Shot=100000, Time=3000,
                Params=[])

    def __init__(self, book):
        for key in book:
            Globalvar7.book[key] = book[key]

            # def __call__(self, c):
            #     Globalvar7.value = c
            #     return Globalvar7.value


class Globalvar8:
    book = dict(FileName=os.environ.get('HOME'), EfitDir=os.environ.get('HOME'), RhoPsi='rho', Shot=100000, Time=3000,
                Params=[])

    def __init__(self, book):
        for key in book:
            Globalvar8.book[key] = book[key]

            # def __call__(self, c):
            #     Globalvar8.value = c
            #     return Globalvar8.value


class Globalvar9:
    book = dict(FileName=os.environ.get('HOME'), EfitDir=os.environ.get('HOME'), RhoPsi='rho', Shot=100000, Time=3000,
                Params=[])

    def __init__(self, book):
        for key in book:
            Globalvar9.book[key] = book[key]
        print 'in Globalvar9', '\n', Globalvar9.book

    def __call__(self, c):
        for key in c:
            Globalvar9.book[key] = c[key]
        return Globalvar9.book


class Globalvar:
    book = dict(FileName=os.environ.get('HOME'), EfitDir=os.environ.get('HOME'), RhoPsi='rho', Shot=100000, Time=3000,
                Params=[])

    def __init__(self, book):
        for key in book:
            Globalvar.book[key] = book[key]
        print 'in Globalvar', '\n', Globalvar.book

    def __call__(self, c):
        for key in c:
            Globalvar.book[key] = c[key]
        return Globalvar.book

        # class Globalvar:
        #     c = []
        #
        #     def __init__(self, c):
        #         Globalvar.c = c
        #
        #     def __call__(self, c):
        #         Globalvar.c = c
        #         return Globalvar.c


        # def upDict():
        #     Globalvar5.value = {'key': 'var'}
        #     Globalvar6.value = {'key': 'var'}
        #     Globalvar7.value = {'key': 'var'}
        #     Globalvar8.value = {'key': 'var'}
        #     Globalvar9.value = {'key': 'var'}
        # Globalvar.c = {'key': 'var'}

#
# def Globalvar(c):
#     c = [c]
#     return c
