import re

# id就是下标
keywords = ['auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'if', 'main',
            'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'int', 'struct',
            'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static', 'printf',
            'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while', 'include']

# 运算符和其他符号
# id就是下标+keywords.len
operators = ["+", "-", "*", "/", "<", "<=", ">", ">=", "=", "==", "!=", ";",
             "(", ")", "^", ",", "\"", "\'", "#", "&", "&&", "|", "||", " %",
             "~", "<<", ">>", "[", "]", "{", "}", "\\", ".", "?", ":", "!"]

# 分隔符
delimiters = [';', ' ', '\n', '\t', '<', '>', '#', '(', ')', '{', '}']


# 读文件，返回一个str
def readFile(fileName):
    with open(fileName) as f:
        return f.read()


# 获取字符串数组
def getStringList(fileName):
    chars = list(readFile(fileName))
    result = []
    index = 0
    i = 0
    for char in chars:
        if char in delimiters:
            string = ''.join(chars[index + 1:i])
            index = i
            # result.append(chars[i])
            if string != '':
                result.append(string)
            result.append(chars[index])
        i += 1

    while ' ' in result:
        result.remove(' ')
    while '\n' in result:
        result.remove('\n')
    return result


# 判断string是否为标识符，返回true或者false
def isId(string):
    pattern = r'^[A-Za-z_][A-Za-z0-9_]*$'
    result = re.match(pattern, string)
    return False if (result is None) else True


# 判断word是否为关键字，是就返回id，不是就返回-1
def isKeyword(word):
    return keywords.index(word) if word in keywords else -1


# 判断是否为操作符，是就返回id，不是就返回-1
def isOperator(word):
    return operators.index(word) + len(keywords) if word in operators else -1


# 判断是否为数字
def isDigit(num):
    pattern = r'\d+(\.\d+)?'
    result = re.match(pattern, num)
    return False if (result is None) else True


def main():
    stringList = getStringList('../file/s.txt')
    attr = []
    index = len(keywords) + len(operators)
    length = index
    for word in stringList:
        if isKeyword(word) > 0:
            print('< id =', isKeyword(word), '=====> "', word, '" >')
        elif isOperator(word) > 0:
            print('< id =', isOperator(word), '=====> "', word, '" >')
        elif isDigit(word):
            print('< id =', word, '=====> "', word, '" >')
        else:
            if word in attr:
                print('< id =', attr.index(word) + length, '=====> "', word, '" >')
            else:
                print('< id =', index, '=====> "', word, '" >')
                attr.append(word)
            index += 1


if __name__ == '__main__':
    main()
