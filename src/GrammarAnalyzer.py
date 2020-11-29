FIRST = {}

FOLLOW = {}
# Follow的三种情况：
# S->...Ab...: 将b加入Follow(A)
# S->...AB...: 将First(B)-{ε}加入Follow(A)
# S->...aB...: 将Follow(A)加入Follow(B)
# S为开始符号，将$加入Follow(S)

# M-->E` N-->T`
sentences = ['E->TM', 'M->+TM', 'M->ε', 'T->FN', 'N->*FN', 'N->ε', 'F->(E)', 'F->i']


# 初始化 first集和 follow集合字典中的键值对中的 值 为空
def init():
    for sentence in sentences:
        part_begin = sentence.split("->")[0]
        FIRST[part_begin] = ""
        FOLLOW[part_begin] = "$"
    # print('初始化First和Follow：\n', FIRST, '\n', FOLLOW)
    # {'E': '', 'M': '', 'T': '', 'N': '', 'F': ''}
    # {'E': '$', 'M': '$', 'T': '$', 'N': '$', 'F': '$'}


# 求first集中第一部分，针对 A->b 型，直接推出第一个字符为终结符的部分，把b追加到first集合中
def getFirst_1():
    for sentence in sentences:
        part_begin = sentence.split("->")[0]
        part_end = sentence.split("->")[1]  # 箭头后第一个元素
        # 如果是小写字母就追加到First中
        # 'ε'.isupper() --> False
        # '+'.isupper() --> False
        if not part_end[0].isupper():
            FIRST[part_begin] = FIRST.get(part_begin) + part_end[0]
    # print('First1: \t', FIRST)  # {'E': '', 'M': '+ε', 'T': '', 'N': '*ε', 'F': '(i'}


# 求first第二部分，针对 A->B... 型，把B的first集加追加到A的first集合中
# First(AB) == First(A)，忽略这种
def getFirst_2():
    for sentence in sentences:
        part_begin = sentence.split('->')[0]
        part_end = sentence.split('->')[1]  # 箭头后第一个元素
        if part_end[0].isupper():
            FIRST[part_begin] = FIRST.get(part_begin) + FIRST.get(part_end[0])


# 去重
def getFirstFinal():
    getFirst_2()
    # set去重
    for key, value in FIRST.items():
        temp = ''
        for word in set(value):
            temp += word
        FIRST[key] = temp


def getFollow_3():
    while 1:
        test = FOLLOW
        getFollow()
        ##去除重复项
        for i, j in FOLLOW.items():
            temp = ""
            for word in list(set(j)):
                temp += word
            FOLLOW[i] = temp
        if test == FOLLOW:
            break


def getMyFollow():
    part_begin = set([])
    part_end = set([])
    for sentence in sentences:
        part_begin.add(sentence.split("->")[0])
        part_end.add(sentence.split("->")[1])
        # 如果是 S->a 直接推出终结符，则continue，例如'F->i'，默认不存在'F->M'类型？？？
    print(part_begin, part_end)
    for s in part_begin:
        for e in part_end:
            if s in e:
                index = e.index(s)
                print(index, s)


def getFollow():
    for sentence in sentences:
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
                FOLLOW[temp_end[0]] = FOLLOW.get(temp_end[0]) + FOLLOW.get(part_begin)
                temp = temp_end[0]
                for i in temp_end[1:]:
                    if not i.isupper():
                        temp = i
                    else:
                        if temp.isupper():
                            FOLLOW[i] = FOLLOW.get(i) + FIRST.get(temp).replace("ε", "")
                        if 'ε' in FIRST.get(temp):
                            FOLLOW[i] = FOLLOW.get(i) + FOLLOW.get(part_begin)
                        else:
                            FOLLOW[i] = FOLLOW.get(i) + temp
                        temp = i
            # 如果终结符在句型的末端
            else:
                temp = temp_end[0]
                for i in temp_end[1:]:
                    if not i.isupper():
                        temp = i
                    else:
                        if temp.isupper():
                            FOLLOW[i] = FOLLOW.get(i) + FIRST.get(temp)
                        else:
                            FOLLOW[i] = FOLLOW.get(i) + temp
                        temp = i


def main():
    init()
    # 求First
    getFirst_1()
    getFirst_2()
    getFirstFinal()
    # 输出FIRST
    for key, value in FIRST.items():
        s = value[0]
        for temp in value[1:]:
            s = s + ', ' + temp
        print('FIRST(' + key + ')' + ' = { ' + s + ' }')

    # 求Follow
    getMyFollow()
    # getFollow()
    # getFollow_3()
    # print(FOLLOW)
    # 输出Follow


if __name__ == '__main__':
    main()

# init()
# getFirst()
# print('1: ', FIRST)
# getFisrt_3()
# getFisrt_3()
# # print(  FIRST )
# getFOLLOW_3()
# getFOLLOW_3()
# # print(FOLLOW)

# for i, j in FIRST.items():
#     s = j[0]
#     for temp in j[1:]:
#         s = s + ',' + temp
#     print("FIRST(" + i + ")" + " = {" + s + "}")
#
# for i, j in FOLLOW.items():
#     s = j[0]
#     for temp in j[1:]:
#         s = s + ',' + temp
#     print("FOLLOW(" + i + ")" + " = {" + s + "}")
