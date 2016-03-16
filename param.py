import os


class GlobalVar5(object):
    value = dict(Params=[])

    def __init__(self, value):
        for key in value:
            self.value[key] = value[key]

    def __call__(self, c):
        for key in c:
            self.value[key] = c[key]
        return self.value


class GlobalVar6(object):
    value = dict(Params=[])

    def __init__(self, value):
        for key in value:
            self.value[key] = value[key]
        print 'in GlobalVar6', '\n', self.value

    def __call__(self, c):
        for key in c:
            self.value[key] = c[key]
        return self.value


class GlobalVar7(object):
    value = dict(Params=[])

    def __init__(self, value):
        for key in value:
            self.value[key] = value[key]

    def __call__(self, c):
        GlobalVar7.value = c
        return self.value


class GlobalVar8(object):
    value = dict(Params=[])

    def __init__(self, value):
        for key in value:
            self.value[key] = value[key]

    def __call__(self, c):
        GlobalVar8.value = c
        return self.value


class GlobalVar9(object):
    value = dict(Params=[])

    def __init__(self, value):
        for key in value:
            self.value[key] = value[key]
        print 'in GlobalVar9', '\n', self.value

    def __call__(self, c):
        for key in c:
            self.value[key] = c[key]
        return self.value


class GlobalVar(object):
    book = dict(FileName=os.environ.get('HOME'),
                EfitDir=os.environ.get('HOME'),
                RhoPsi='rho',
                Shot=100000,
                Time=3000,
                Params=[])

    def __init__(self, book):
        for key in book:
            GlobalVar.book[key] = book[key]
        print 'in GlobalVar', '\n', GlobalVar.book

    def __call__(self, c):
        for key in c:
            GlobalVar.book[key] = c[key]
        return GlobalVar.book

        # class GlobalVar:
        #     c = []
        #
        #     def __init__(self, c):
        #         GlobalVar.c = c
        #
        #     def __call__(self, c):
        #         GlobalVar.c = c
        #         return GlobalVar.c


        # def upDict():
        #     GlobalVar5.value = {'key': 'var'}
        #     GlobalVar6.value = {'key': 'var'}
        #     GlobalVar7.value = {'key': 'var'}
        #     GlobalVar8.value = {'key': 'var'}
        #     GlobalVar9.value = {'key': 'var'}
        # GlobalVar.c = {'key': 'var'}

#
# def GlobalVar(c):
#     c = [c]
#     return c
