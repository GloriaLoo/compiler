# 计算FIRST、FOLLOW集合


class GrammarAnalyzer:
    def __init__(self, sentences):
        self.__sentences = sentences

    __FIRST = {}

    __FOLLOW = {}
    # Follow(A) 的三种情况：
    # A为开始符号，将$加入Follow(A)
    # S->...Ab...: 将b加入Follow(A)
    # S->...AB...: 将First(B)-{ε}加入Follow(A)
    # B->...aA...或者B->...aAC..，且First(C)包含ε: 将Follow(B)加入Follow(A)；a可以是终结符或者非终结符？？？

    # M-->E` N-->T`
    __sentences = []

    # 初始化 first集和 follow集合字典中的键值对中的 值 为空
    def __init(self):
        for sentence in self.__sentences:
            part_begin = sentence.split('->')[0]
            self.__FIRST[part_begin] = ''
            self.__FOLLOW[part_begin] = '$'

    # 求first集中第一部分，针对 A->b 型，直接推出第一个字符为终结符的部分，把b追加到first集合中
    def __getFirst_1(self):
        for sentence in self.__sentences:
            part_begin = sentence.split("->")[0]
            part_end = sentence.split("->")[1]  # 箭头后第一个元素
            # 如果是小写字母就追加到First中
            # 'ε'.isupper() --> False
            # '+'.isupper() --> False
            if not part_end[0].isupper():
                self.__FIRST[part_begin] = self.__FIRST.get(part_begin) + part_end[0]
                self.__FIRST[part_end] = part_end[0]
        # print('First1: \t', FIRST)  # {'E': '', 'M': '+ε', 'T': '', 'N': '*ε', 'F': '(i'}

    # 求first第二部分，针对 A->B... 型，把B的first集加追加到A的first集合中
    # First(AB) == First(A)，忽略这种
    def __getFirst_2(self):
        for sentence in self.__sentences:
            part_begin = sentence.split('->')[0]
            part_end = sentence.split('->')[1]  # 箭头后第一个元素
            if part_end[0].isupper():
                self.__FIRST[part_begin] = self.__FIRST.get(part_begin) + self.__FIRST.get(part_end[0])

    # 去重
    def __getFirstFinal(self):
        self.__getFirst_2()
        # set去重
        for key, value in self.__FIRST.items():
            temp = ''
            for word in set(value):
                temp += word
            self.__FIRST[key] = temp

    # sentences = ['E->TM', 'M->+TM', 'M->ε', 'T->FN', 'N->*FN', 'N->ε', 'F->(E)', 'F->i']

    def __getFollow_1(self):
        for sentence in self.__sentences:
            part_begin = sentence.split("->")[0]
            part_end = sentence.split("->")[1]
            # 如果是 S->a 直接推出终结符，则continue，例如'F->i'，默认不存在'F->M'类型？？？
            if len(part_end) == 1:
                continue
            # 否则执行下面的操作
            else:
                # 将->后面的分开再倒序
                temp_end = []
                for i in part_end:
                    temp_end.append(i)
                temp_end.reverse()

                # 如果非终结符在句型的末端则把 $ 加入进去
                if temp_end[0].isupper():
                    self.__FOLLOW[temp_end[0]] = self.__FOLLOW.get(temp_end[0]) + self.__FOLLOW.get(part_begin)
                    temp = temp_end[0]
                    for i in temp_end[1:]:
                        if not i.isupper():
                            temp = i
                        else:
                            if temp.isupper():
                                self.__FOLLOW[i] = self.__FOLLOW.get(i) + self.__FIRST.get(temp).replace("ε", "")
                            if 'ε' in self.__FIRST.get(temp):
                                self.__FOLLOW[i] = self.__FOLLOW.get(i) + self.__FOLLOW.get(part_begin)
                            else:
                                self.__FOLLOW[i] = self.__FOLLOW.get(i) + temp
                            temp = i
                # 如果终结符在句型的末端
                else:
                    temp = temp_end[0]
                    for i in temp_end[1:]:
                        if not i.isupper():
                            temp = i
                        else:
                            if temp.isupper():
                                self.__FOLLOW[i] = self.__FOLLOW.get(i) + self.__FIRST.get(temp)
                            else:
                                self.__FOLLOW[i] = self.__FOLLOW.get(i) + temp
                            temp = i

    def __getFollowFinal(self):
        while 1:
            test = self.__FOLLOW
            self.__getFollow_1()
            # 去除重复项
            for i, j in self.__FOLLOW.items():
                temp = ""
                for word in list(set(j)):
                    temp += word
                self.__FOLLOW[i] = temp
            if test == self.__FOLLOW:
                break

    def getFirst(self):
        # 初始化
        self.__init()
        self.__getFirst_1()
        self.__getFirst_2()
        self.__getFirstFinal()
        return self.__FIRST

    def getFollow(self):
        # 初始化
        self.__init()
        # 求First
        self.__getFirst_1()
        self.__getFirst_2()
        self.__getFirstFinal()
        self.__getFollow_1()
        self.__getFollowFinal()
        return self.__FOLLOW

# g = GrammarAnalyzer(['E->TM', 'M->+TM', 'M->ε', 'T->FN', 'N->*FN', 'N->ε', 'F->(E)', 'F->i'])
# print(g.getFirst())
# print(g.getFollow())
