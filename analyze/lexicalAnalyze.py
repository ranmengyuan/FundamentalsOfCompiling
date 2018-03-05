class wordForm:
    """
    单词表
    """
    word = ''  # 单词
    wordtype = ''  # 类别
    index = 0  # 种别码

    def __init__(self):
        self.word = ''
        self.wordtype = ''
        self.index = 0


class token:
    """
    Token表
    """
    word = ''  # 单词
    tokenValue = 0  # Token值
    line = 0  # 行数
    wordtype = ''  # 单词类别

    def __init__(self):
        self.word = ''
        self.tokenValue = 0


def defineForm():
    """
    定义单词表
    :return:
    """
    form = []
    data = wordForm()
    data.word = "program"
    data.index = 1
    data.wordtype = "keyword"
    form.append(data)

    data = wordForm()
    data.word = "var"
    data.index = 2
    data.wordtype = "keyword"
    form.append(data)

    data = wordForm()
    data.word = "integer"
    data.index = 3
    data.wordtype = "keyword"
    form.append(data)

    data = wordForm()
    data.word = "bool"
    data.index = 4
    data.wordtype = "keyword"
    form.append(data)

    data = wordForm()
    data.word = "real"
    data.index = 5
    data.wordtype = "keyword"
    form.append(data)

    data = wordForm()
    data.word = "char"
    data.index = 6
    data.wordtype = "keyword"
    form.append(data)

    data = wordForm()
    data.word = "const"
    data.index = 7
    data.wordtype = "keyword"
    form.append(data)

    data = wordForm()
    data.word = "begin"
    data.index = 8
    data.wordtype = "keyword"
    form.append(data)

    data = wordForm()
    data.word = "if"
    data.index = 9
    data.wordtype = "keyword"
    form.append(data)

    data = wordForm()
    data.word = "then"
    data.index = 10
    data.wordtype = "keyword"
    form.append(data)

    data = wordForm()
    data.word = "else"
    data.index = 11
    data.wordtype = "keyword"
    form.append(data)

    data = wordForm()
    data.word = "while"
    data.index = 12
    data.wordtype = "keyword"
    form.append(data)

    data = wordForm()
    data.word = "do"
    data.index = 13
    data.wordtype = "keyword"
    form.append(data)

    data = wordForm()
    data.word = "for"
    data.index = 14
    data.wordtype = "keyword"
    form.append(data)

    data = wordForm()
    data.word = "to"
    data.index = 15
    data.wordtype = "keyword"
    form.append(data)

    data = wordForm()
    data.word = "end"
    data.index = 16
    data.wordtype = "keyword"
    form.append(data)

    data = wordForm()
    data.word = "read"
    data.index = 17
    data.wordtype = "keyword"
    form.append(data)

    data = wordForm()
    data.word = "write"
    data.index = 18
    data.wordtype = "keyword"
    form.append(data)

    data = wordForm()
    data.word = "true"
    data.index = 19
    data.wordtype = "keyword"
    form.append(data)

    data = wordForm()
    data.word = "false"
    data.index = 20
    data.wordtype = "keyword"
    form.append(data)

    data = wordForm()
    data.word = "not"
    data.index = 21
    data.wordtype = "operator"
    form.append(data)

    data = wordForm()
    data.word = "and"
    data.index = 22
    data.wordtype = "operator"
    form.append(data)

    data = wordForm()
    data.word = "or"
    data.index = 23
    data.wordtype = "operator"
    form.append(data)

    data = wordForm()
    data.word = "+"
    data.index = 24
    data.wordtype = "operator"
    form.append(data)

    data = wordForm()
    data.word = "-"
    data.index = 25
    data.wordtype = "operator"
    form.append(data)

    data = wordForm()
    data.word = "*"
    data.index = 26
    data.wordtype = "operator"
    form.append(data)

    data = wordForm()
    data.word = "/"
    data.index = 27
    data.wordtype = "operator"
    form.append(data)

    data = wordForm()
    data.word = "<"
    data.index = 28
    data.wordtype = "operator"
    form.append(data)

    data = wordForm()
    data.word = ">"
    data.index = 29
    data.wordtype = "operator"
    form.append(data)

    data = wordForm()
    data.word = "<="
    data.index = 30
    data.wordtype = "operator"
    form.append(data)

    data = wordForm()
    data.word = ">="
    data.index = 31
    data.wordtype = "operator"
    form.append(data)

    data = wordForm()
    data.word = "=="
    data.index = 32
    data.wordtype = "operator"
    form.append(data)

    data = wordForm()
    data.word = "<>"
    data.index = 33
    data.wordtype = "operator"
    form.append(data)

    data = wordForm()
    data.word = "id"
    data.index = 34
    data.wordtype = "identifier"
    form.append(data)

    data = wordForm()
    data.word = "constInt"
    data.index = 35
    data.wordtype = "const"
    form.append(data)

    data = wordForm()
    data.word = "constFloat"
    data.index = 36
    data.wordtype = "const"
    form.append(data)

    data = wordForm()
    data.word = "constChar"
    data.index = 37
    data.wordtype = "const"
    form.append(data)

    data = wordForm()
    data.word = "constBool"
    data.index = 38
    data.wordtype = "const"
    form.append(data)

    data = wordForm()
    data.word = "="
    data.index = 39
    data.wordtype = "delimiter"
    form.append(data)

    data = wordForm()
    data.word = ";"
    data.index = 40
    data.wordtype = "delimiter"
    form.append(data)

    data = wordForm()
    data.word = ","
    data.index = 41
    data.wordtype = "delimiter"
    form.append(data)

    data = wordForm()
    data.word = "'"
    data.index = 42
    data.wordtype = "delimiter"
    form.append(data)

    data = wordForm()
    data.word = "/*"
    data.index = 43
    data.wordtype = "delimiter"
    form.append(data)

    data = wordForm()
    data.word = "*/"
    data.index = 44
    data.wordtype = "delimiter"
    form.append(data)

    data = wordForm()
    data.word = ":"
    data.index = 45
    data.wordtype = "delimiter"
    form.append(data)

    data = wordForm()
    data.word = "("
    data.index = 46
    data.wordtype = "delimiter"
    form.append(data)

    data = wordForm()
    data.word = ")"
    data.index = 47
    data.wordtype = "delimiter"
    form.append(data)

    data = wordForm()
    data.word = "."
    data.index = 48
    data.wordtype = "delimiter"
    form.append(data)

    return form


def findDfine(word, form):
    """
    查找单词表
    :param word:
    :param form:
    :return:
    """
    data = wordForm()
    for i in range(len(form)):
        if word == form[i].word:
            return form[i]
    return data


def isConstChar(word):
    """
    判断一个词是否为字符常量
    :param word:
    :return:
    """
    if len(word) != 3:
        return 0
    else:
        if (word[0] == "'") & (word[2] == "'"):
            return 1
        else:
            return 0


def isConstFloat(word):
    """
    判断一个词是否为实数常量
    :param word:
    :return:
    """
    flag = 1
    try:
        float(word)
    except Exception:
        flag = 0
    finally:
        return flag


def creatToken(word):
    """
    生成Token表
    :param word:
    :return:
    """
    form = defineForm()
    if word.isdigit():
        data = findDfine("constInt", form)
    elif isConstFloat(word) == 1:
        data = findDfine("constFloat", form)
    elif (word == "True") | (word == "False"):
        data = findDfine("constBool", form)
    elif isConstChar(word) == 1:
        data = findDfine("constChar", form)
    else:
        data = findDfine(word, form)
        if data.index == 0:
            data = findDfine("id", form)
    return data


def isEnd(word1, word2):
    """
    判断是否为备注结束
    :param word1:
    :param word2:
    :return:
    """
    if (word1 == '*') & (word2 == '/'):
        flag = 1
    else:
        flag = 0
    return flag


def participle(line, remark, remarkContent):
    """
    分词
    :param line:
    :return:
    """
    state = 0
    words = []  # 分词信息
    tempData = ''
    flag = 0  # 判断是否出错
    exceptData = []  # 错误信息
    tempRe = ''
    flag1 = 0
    flag2 = 0
    i = 0
    while 1:
        control = 1
        if i >= len(line):
            break
        if i < len(line) - 1:
            if isEnd(line[i], line[i + 1]) == 1:
                control = 0
        if (remark == 0) | ((remark == 1) & (control == 0)):
            if tempRe != '':
                remarkContent.append(tempRe)
                tempRe = ''
                remark = 0
                i += 1
                flag1 = 1
            if state == 0:
                if line[i].isalpha():
                    state = 1
                    tempData += line[i]
                elif line[i].isdigit():
                    state = 3
                    tempData += line[i]
                elif line[i] == ' ':
                    state = 0
                elif (line[i] == '+') | (line[i] == '-') | (line[i] == '(') | (line[i] == ')') | (line[i] == ';') | \
                        (line[i] == ',') | (line[i] == ':'):
                    tempData += line[i]
                    flag2 = 1
                    state = 2
                elif line[i] == '<':
                    state = 9
                    tempData += line[i]
                elif line[i] == '>':
                    state = 10
                    tempData += line[i]
                elif line[i] == '=':
                    state = 10
                    tempData += line[i]
                elif line[i] == '/':
                    state = 11
                    tempData += line[i]
                elif line[i] == '*':
                    state = 12
                    tempData += line[i]
                elif line[i] == '.':
                    state = 13
                    tempData += line[i]
                elif line[i] == '\'':
                    state = 14
                    tempData += line[i]
                else:
                    flag = 1
                    state = 2
                    tempData += line[i]

            elif state == 1:
                if line[i].isalpha() | line[i].isdigit():
                    tempData += line[i]
                    state = 1
                else:
                    flag2 = 1
                    i -= 1
                    state = 2
            elif state == 2:
                if flag == 0:
                    if flag2 == 0:
                        i -= 2
                    elif flag2 == 1:
                        i -= 1
                        flag2 = 0
                    words.append(tempData)
                else:
                    i -= 1
                    exceptData.append(tempData)
                    flag = 0
                tempData = ''
                tempRe = ''
                state = 0
            elif state == 3:
                if line[i].isdigit():
                    state = 3
                    tempData += line[i]
                elif line[i] == '.':
                    state = 4
                    tempData += line[i]
                elif (line[i] == 'E') | (line[i] == 'e'):
                    state = 5
                    tempData += line[i]
                else:
                    flag2 = 1
                    i -= 1
                    state = 2
            elif state == 4:
                if line[i].isdigit():
                    tempData += line[i]
                    state = 6
                else:
                    flag = 1
                    state = 2
                    i -= 1
            elif state == 5:
                if line[i].isdigit():
                    state = 7
                    tempData += line[i]
                elif line[i] == '+':
                    state = 8
                    tempData += line[i]
                elif line[i] == '-':
                    state = 8
                    tempData += line[i]
                else:
                    flag = 1
                    i -= 1
                    state = 2
            elif state == 6:
                if line[i].isdigit():
                    state = 6
                    tempData += line[i]
                elif (line[i] == 'E') | (line[i] == 'e'):
                    tempData += line[i]
                    state = 5
                else:
                    flag2 = 1
                    i -= 1
                    state = 2
            elif state == 7:
                if line[i].isdigit():
                    tempData += line[i]
                    state = 7
                else:
                    flag2 = 1
                    i -= 1
                    state = 2
            elif state == 8:
                if line[i].isdigit():
                    tempData += line[i]
                    state = 7
                else:
                    flag = 1
                    i -= 1
                    state = 2
            elif state == 9:
                if (line[i] == '=') | (line[i] == '>'):
                    tempData += line[i]
                    flag2 = 1
                    state = 2
                else:
                    flag2 = 1
                    i -= 1
                    state = 2
            elif state == 10:
                if line[i] == '=':
                    tempData += line[i]
                    flag2 = 1
                    state = 2
                else:
                    flag2 = 1
                    i -= 1
                    state = 2
            elif state == 11:
                if line[i] == '*':
                    tempData += line[i]
                    remark = 1
                else:
                    if flag1 == 1:
                        i -= 1
                        flag1 = 0
                    flag2 = 1
                    i -= 1
                    state = 2
            elif state == 12:
                if line[i] == '/':
                    tempData += line[i]
                    flag2 = 1
                    state = 2
                else:
                    flag2 = 1
                    i -= 1
                    state = 2
            elif state == 13:
                if line[i].isdigit():
                    flag = 1
                    tempData += line[i]
                    state = 13
                else:
                    flag2 = 1
                    i -= 1
                    state = 2
            elif state == 14:
                leng = length(line, i)
                if leng == 1:
                    words.append(tempData)
                    words.append('\'' + line[i] + '\'')
                    i += 1
                    flag2 = 1
                    state = 2
                elif leng == -1:
                    flag2 = 1
                    i -= 1
                    state = 2
                else:
                    for k in range(leng + 1):
                        tempData += line[i + k]
                    i = i + leng
                    flag = 1
                    state = 2
        else:
            tempRe += line[i]
        i += 1
    if tempRe != '':
        remarkContent.append(tempRe)
    if (flag == 0) & (state != 4) & (state != 5) & (state != 8):
        if len(tempData) != 0:
            words.append(tempData)
    else:
        if len(tempData) != 0:
            exceptData.append(tempData)
    return words, exceptData, remark, remarkContent


def isRepate(name, word):
    """
    判断单词是否在符号表中重复
    :param name:
    :param word:
    :return:
    """
    for i in range(len(name)):
        if word == name[i]:
            return 1
    return 0


def length(line, index):
    """
    获得两个单引号之间的长度
    :param line:
    :param i:
    :return:
    """
    i = index
    while 1:
        if i >= len(line):
            break
        if line[i] == '\'':
            return i - index
        i += 1
    return -1
