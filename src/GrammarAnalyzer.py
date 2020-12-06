FIRST = {}

FOLLOW = {}
# Follow(A) 的三种情况：
# A为开始符号，将$加入Follow(A)
# S->...Ab...: 将b加入Follow(A)
# S->...AB...: 将First(B)-{ε}加入Follow(A)
# B->...aA...或者B->...aAC..，且First(C)包含ε: 将Follow(B)加入Follow(A)；a可以是终结符或者非终结符？？？


# M-->E` N-->T`
sentences = ['E->TM', 'M->+TM', 'M->ε', 'T->FN', 'N->*FN', 'N->ε', 'F->(E)', 'F->i']


# 初始化 first集和 follow集合字典中的键值对中的 值 为空
def init():
    for sentence in sentences:
        part_begin = sentence.split('->')[0]
        FIRST[part_begin] = ''
        FOLLOW[part_begin] = '$'


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


def getFollowFinal():
    while 1:
        test = FOLLOW
        getFollow()
        # 去除重复项
        for i, j in FOLLOW.items():
            temp = ""
            for word in list(set(j)):
                temp += word
            FOLLOW[i] = temp
        if test == FOLLOW:
            break


# sentences = ['E->TM', 'M->+TM', 'M->ε', 'T->FN', 'N->*FN', 'N->ε', 'F->(E)', 'F->i']

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
    # 初始化
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
    getFollow()
    getFollowFinal()
    # 输出Follow
    for key, value in FOLLOW.items():
        s = value[0]
        for temp in value[1:]:
            s = s + ',' + temp
        print("FOLLOW(" + key + ")" + " = {" + s + "}")


if __name__ == '__main__':
    main()
