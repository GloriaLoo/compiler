# LL1文法
# 构造预测分析表

from src.GrammarAnalyzer import GrammarAnalyzer


class LL1:
    __FIRST = {}
    __FOLLOW = {}
    __sentences = []
    __Vt = ['$']
    __Vn = []
    __TABLE = dict({
        # 'M': {
        #     '$': '',
        #     '+': 'M->+TM',
        #     '*': '',
        #     '(': '',
        #     ')': '',
        #     'i': ''
        # },
        # 'F': {},
        # 'T': {},
        # 'E': {},
        # 'N': {}
    })

    def __init__(self, sentences):
        self.__sentences = sentences
        g = GrammarAnalyzer(self.__sentences)
        self.__FIRST = g.getFirst()
        self.__FOLLOW = g.getFollow()
        print('=' * 31, 'FIRST', '=' * 32)
        for key in self.__FIRST.keys():
            print('FIRST(', key, ') = {', self.__FIRST.get(key), '}')
        print('=' * 31, 'FOLLOW', '=' * 31)
        for key in self.__FOLLOW.keys():
            print('FOLLOW(', key, ') = {', self.__FOLLOW.get(key), '}')
        pass

    def __getVtVn(self):
        temp = ''
        for sentence in self.__sentences:
            part_begin = sentence.split('->')[0]
            part_end = sentence.split('->')[1]
            temp += part_end
            self.__Vn.append(part_begin)
        self.__Vn = list(set(self.__Vn))
        for s in temp:
            if s not in self.__Vt and s not in self.__Vn:
                self.__Vt.append(s)
        # print(self.__Vn)
        if 'ε' in self.__Vt:
            self.__Vt.remove('ε')
        # print(self.__Vt)

    def getTable(self):
        self.__getVtVn()
        # print(self.__Vt)
        # print(self.__Vn)
        for vn in self.__Vn:
            self.__TABLE[vn] = {}
            for vt in self.__Vt:
                self.__TABLE[vn][vt] = 'error'
        # self.__TABLE['M']['+'] = 'M->+TM'
        # print('FIRST: ', self.__FIRST)
        # print('FOLLOW: ', self.__FOLLOW)

        # 对文法的每个生产式A->β，执行1、2：
        # 1、对FIRST(β)的每个终结符a，把A->β加入M[A, a]
        # 2、如果ε在FIRST(β)中，对FOLLOW(A)的每个终结符b（包括$），把A->β加入M[A, b]（包括M[A, $]）
        for sentence in self.__sentences:
            part_begin = sentence.split("->")[0]
            part_end = sentence.split("->")[1]  # 箭头后第一个元素
            temp = ''
            if not part_end[0].isupper():
                temp = part_end
            else:
                temp = part_end[0]
            # E->TM
            # print('temp: ', temp)
            first = self.__FIRST.get(temp)
            # print('first(temp): ', first)
            # temp: T
            # first(temp): (i
            # temp:  +TM
            # first(temp):  +
            # temp: ε
            # first(temp): ε
            if 'ε' not in first:
                for s in first:
                    self.__TABLE[part_begin][s] = sentence
            else:
                follow = self.__FOLLOW.get(part_begin)
                # print('follow(', part_begin, '): ', follow)
                for s in follow:
                    self.__TABLE[part_begin][s] = sentence
        return self.__TABLE

    def printTable(self):
        self.getTable()
        print('='*31, 'TABLE', '='*32)
        print('\t', end='')
        for vt in self.__Vt:
            print(vt, '\t\t\t', end='')
        print()
        for line in self.__TABLE:
            print(line, '\t', end='')
            temps = self.__TABLE[line]
            for temp in temps:
                print(self.__TABLE[line][temp], '\t\t', end='')
            print()


sentences = ['E->TM', 'M->+TM', 'M->ε', 'T->FN', 'N->*FN', 'N->ε', 'F->(E)', 'F->i']
ll1 = LL1(sentences)
# print(ll1.getTable())  # 以字典形式打印
ll1.printTable()
