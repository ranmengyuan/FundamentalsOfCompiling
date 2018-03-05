from analyze.lexicalAnalyze import token
from analyze.grammaticalAnalyze import sign


class quaternion:
    """
    四元式
    """
    no = 0
    op = ''
    args1 = ''
    args2 = ''
    result = ''

    def __init__(self):
        self.no = 0
        self.args1 = ''
        self.args2 = ''
        self.result = ''


class name:
    """
    变量名
    """
    word = 'T'
    no = 0

    def __init__(self):
        self.word = 'T'
        self.no = 0


class middle:
    def __init__(self):
        self.structure = []  # 四元式
        self.variate = []  # 变量值
        self.index = 0  # 四元式的符号编号
        self.tempName = name()  # 临时变量名

    def middleDeal(self, tokenTable):
        """
        中间代码生成总控程序
        :param tokenTable:
        :return:
        """
        i = 0
        formula = quaternion()
        if tokenTable[i].word == 'program':
            formula.no = self.index
            formula.op = tokenTable[i].word
            i += 1
            formula.args1 = tokenTable[i].word
            self.index += 1
            self.structure.append(formula)
        while 1:
            if i >= len(tokenTable):
                return self.structure
            elif tokenTable[i].word == 'const':
                i = self.handle_const(tokenTable, i + 1)
            elif tokenTable[i].word == 'var':
                i = self.handle_varite(tokenTable, i + 1)
            elif tokenTable[i].word == 'begin':
                break
            i += 1
        self.handle_mainfunction(tokenTable, i + 1)
        return self.structure

    def handle_const(self, tokenTable, start):
        """
        记录常量的定义
        :param tokenTable:
        :param start:
        :param structure:
        :return:
        """
        while 1:
            if start >= len(tokenTable):
                return start
            elif (tokenTable[start].word == 'begin') | (tokenTable[start].word == 'var') | (
                        tokenTable[start].word == 'const'):
                return start - 1
            else:
                temp = []
                while 1:
                    if tokenTable[start].word == ';':
                        break
                    elif tokenTable[start].word == '=':
                        start += 1
                        for i in range(len(temp)):
                            tempData = sign()
                            tempData.word = temp[i]
                            tempData.value = tokenTable[start].word
                            if tokenTable[start].tokenValue == 35:
                                tempData.signType = 'integer'
                            elif tokenTable[start].tokenValue == 36:
                                tempData.signType = 'real'
                            elif tokenTable[start].tokenValue == 37:
                                tempData.signType = 'bool'
                            elif tokenTable[start].tokenValue == 38:
                                tempData.signType = 'char'
                            self.variate.append(tempData)
                    else:
                        temp.append(tokenTable[start].word)
                        start += 1
                    start += 1
            start += 1
        return start

    def handle_varite(self, tokenTable, start):
        """
        记录变量定义
        :param tokenTable:
        :param start:
        :return:
        """
        while 1:
            if start >= len(tokenTable):
                return start
            elif (tokenTable[start].word == 'begin') | (tokenTable[start].word == 'var') | (
                        tokenTable[start].word == 'const'):
                return start - 1
            else:
                temp = []
                while 1:
                    if tokenTable[start].word == ';':
                        break
                    elif tokenTable[start].word == ':':
                        start += 1
                        for i in range(len(temp)):
                            tempData = sign()
                            tempData.word = temp[i]
                            tempData.signType = tokenTable[start].word
                            self.variate.append(tempData)
                    else:
                        temp.append(tokenTable[start].word)
                        if tokenTable[start + 1].word == ',':
                            start += 1
                    start += 1
            start += 1
        return start

    def handle_mainfunction(self, tokenTable, start):
        """
        处理主函数
        :param tokenTable:
        :param start:
        :param structure:
        :return:
        """
        while 1:
            if tokenTable[start].word == 'end':
                break
            elif tokenTable[start].word == 'if':
                start = self.handle_if(tokenTable, start)
            elif tokenTable[start].word == 'repeat':
                start = self.handle_repeat(tokenTable, start)
            elif tokenTable[start].word == 'for':
                start = self.handle_for(tokenTable, start)
            elif tokenTable[start].word == 'while':
                start = self.handle_while(tokenTable, start)
            else:
                start = self.handle_evaluation(tokenTable, start)
        formula = quaternion()
        formula.no = self.index
        self.structure.append(formula)
        return start + 2

    def getValueIndex(self, name):
        """
        获得一个变量的序号
        :param name:
        :return:
        """
        i = 0
        while 1:
            if i >= len(self.variate):
                return -1
            elif name == self.variate[i].word:
                return i
            i += 1

    def handle_evaluation(self, tokenTable, start):
        """
        处理赋值语句
        :param tokenTable:
        :param start:
        :param flag:
        :return:
        """
        line = tokenTable[start].line
        result = tokenTable[start].word
        n = self.getValueIndex(result)
        while 1:
            if start >= len(tokenTable):
                return start
            elif tokenTable[start].word == '=':
                break
            start += 1
        start += 1
        if (self.variate[n].signType == 'bool') | (self.variate[n].signType == 'char'):
            formula = quaternion()
            formula.no = self.index
            formula.op = ":="
            formula.args1 = tokenTable[start].word
            formula.result = result
            self.structure.append(formula)
            self.index += 1
            if tokenTable[start].tokenValue == 34:
                index = self.getValueIndex(tokenTable[start].word)
                self.variate[n].value = self.variate[index].value
            else:
                self.variate[n].value = tokenTable[start].word
            start += 2
            return start
        elif self.variate[n].signType == 'integer':
            tempExpress = []
            temp1 = []
            while 1:
                if start >= len(tokenTable):
                    return start

                elif tokenTable[start].line != line:
                    return start

                elif tokenTable[start].word == ';':
                    start += 1
                    break
                tempExpress.append(tokenTable[start])

                element = token()
                element.word = tokenTable[start].word
                element.wordtype = tokenTable[start].wordtype
                element.tokenValue = tokenTable[start].tokenValue
                element.line = tokenTable[start].line
                temp1.append(element)

                start += 1
            formula = quaternion()
            length = len(tempExpress)
            flag, value = self.calExpressInt(tempExpress, temp1, 0, 0)
            if length == 1:
                formula.args1 = str(value)
            else:
                formula.args1 = self.tempName.word + str(self.tempName.no)
            if flag == 0:
                self.variate[n].value = value
                formula.no = self.index
                formula.op = ":="
                formula.result = result
                self.structure.append(formula)
                self.index += 1
            return start
        elif self.variate[n].signType == 'real':
            tempExpress = []
            temp1 = []
            while 1:
                if start >= len(tokenTable):
                    return start

                elif tokenTable[start].line != line:
                    return start

                elif tokenTable[start].word == ';':
                    start += 1
                    break
                tempExpress.append(tokenTable[start])

                element = token()
                element.word = tokenTable[start].word
                element.wordtype = tokenTable[start].wordtype
                element.tokenValue = tokenTable[start].tokenValue
                element.line = tokenTable[start].line
                temp1.append(element)

                start += 1
            formula = quaternion()
            length = len(tempExpress)
            flag, value = self.calExpressFloat(tempExpress, temp1, 0, 0)
            if length == 1:
                formula.args1 = str(value)
            else:
                formula.args1 = self.tempName.word + str(self.tempName.no)
            if flag == 0:
                self.variate[n].value = value
                formula.no = self.index
                formula.op = ":="
                formula.result = result
                self.structure.append(formula)
                self.index += 1
            return start

    def remove(self, list, start, end):
        """
        删除数组中的元素
        :param list:
        :param start:
        :param end:
        :return:
        """
        leng = len(list)
        while 1:
            if len(list) == leng - (end - start + 1):
                return list
            del list[start]

    def calExpressInt(self, express, contrastExpress, index, flag):
        """
        判定算数表达式(整数)
        :param express:
        :return:
        """
        while 1:
            if len(express) == 1:
                if express[0].tokenValue == 34:
                    n = self.getValueIndex(express[0].word)
                    return 0, int(self.variate[n].value)
                else:
                    return 0, int(express[0].word)
            elif flag == 1:
                return 1, 0
            elif express[index].word == '(':
                i = index + 1
                temp = []
                temp1 = []
                sum = 1
                while 1:
                    if i >= len(express):
                        return 1, 0
                    elif express[i].word == ')':
                        sum -= 1
                    elif express[i].word == '(':
                        sum += 1
                    if sum == 0:
                        break
                    temp.append(express[i])

                    element = token()
                    element.word = express[i].word
                    element.wordtype = express[i].wordtype
                    element.tokenValue = express[i].tokenValue
                    element.line = express[i].line
                    temp1.append(element)

                    i += 1
                flag, express[index].word = self.calExpressInt(temp, temp1, 0, flag)
                contrastExpress[index].word = self.tempName.word + str(self.tempName.no)
                if flag == 0:
                    self.remove(express, index + 1, i)
                    self.remove(contrastExpress, index + 1, i)
                    express[index].tokenValue = 35
                    contrastExpress[index].tokenValue = 35
            elif (express[index].word == '*') | (express[index].word == '/'):
                if (index >= len(express) - 1) | (index < 1):
                    return 1, 0
                elif (express[index - 1].tokenValue != 35) & (express[index - 1].tokenValue != 34):
                    return 1, 0
                elif express[index + 1].word == '(':
                    i = index + 2
                    temp = []
                    temp1 = []
                    sum = 1
                    while 1:
                        if i >= len(express):
                            return 1, 0
                        elif express[i].word == ')':
                            sum -= 1
                        elif express[i].word == '(':
                            sum += 1
                        if sum == 0:
                            break
                        temp.append(express[i])

                        element = token()
                        element.word = express[i].word
                        element.wordtype = express[i].wordtype
                        element.tokenValue = express[i].tokenValue
                        element.line = express[i].line
                        temp1.append(element)

                        i += 1
                    flag, express[index + 1].word = self.calExpressInt(temp, temp1, 0, flag)
                    contrastExpress[index + 1].word = self.tempName.word + str(self.tempName.no)
                    if flag == 0:
                        self.remove(express, index + 2, i)
                        self.remove(contrastExpress, index + 2, i)

                        express[index + 1].tokenValue = 35
                        contrastExpress[index + 1].tokenValue = 35

                elif (express[index + 1].tokenValue != 35) & (express[index + 1].tokenValue != 34):
                    return 1, 0

                formula = quaternion()
                formula.no = self.index

                if express[index - 1].tokenValue == 34:
                    k = self.getValueIndex(express[index - 1].word)
                    express[index - 1].word = self.variate[k].value

                if express[index + 1].tokenValue == 34:
                    k = self.getValueIndex(express[index + 1].word)
                    express[index + 1].word = self.variate[k].value

                if express[index].word == '*':
                    express[index - 1].word = int(express[index - 1].word) * int(express[index + 1].word)
                    formula.op = "*"
                else:
                    express[index - 1].word = int(express[index - 1].word) / int(express[index + 1].word)
                    formula.op = "/"
                formula.args1 = str(contrastExpress[index - 1].word)
                formula.args2 = str(contrastExpress[index + 1].word)
                self.tempName.no += 1
                formula.result = self.tempName.word + str(self.tempName.no)
                self.structure.append(formula)
                self.index += 1

                self.remove(express, index, index + 1)
                self.remove(contrastExpress, index, index + 1)
                express[index - 1].tokenValue = 35
                contrastExpress[index - 1].tokenValue = 35

            elif express[index].word == '+':
                if (index >= len(express) - 1) | (index < 1):
                    return 1, 0
                elif (express[index - 1].tokenValue != 35) & (express[index - 1].tokenValue != 34):
                    return 1, 0
                elif (express[index + 1].tokenValue == 35) | (express[index + 1].tokenValue == 34):
                    if index < len(express) - 3:
                        if (express[index + 2].word == '*') | (express[index + 2].word == '/'):
                            temp = []
                            temp.append(express[index + 1])
                            temp.append(express[index + 2])
                            temp.append(express[index + 3])

                            temp1 = []

                            element = token()
                            element.word = express[index + 1].word
                            element.wordtype = express[index + 1].wordtype
                            element.tokenValue = express[index + 1].tokenValue
                            element.line = express[index + 1].line
                            temp1.append(element)

                            element = token()
                            element.word = express[index + 2].word
                            element.wordtype = express[index + 2].wordtype
                            element.tokenValue = express[index + 2].tokenValue
                            element.line = express[index + 2].line
                            temp1.append(element)

                            element = token()
                            element.word = express[index + 3].word
                            element.wordtype = express[index + 3].wordtype
                            element.tokenValue = express[index + 3].tokenValue
                            element.line = express[index + 3].line
                            temp1.append(element)

                            flag, express[index + 1].word = self.calExpressInt(temp, temp1, 0, flag)
                            contrastExpress[index + 1].word = self.tempName.word + str(self.tempName.no)

                            if flag == 0:
                                express[index + 1].tokenValue = 35
                                contrastExpress[index + 1].tokenValue = 35

                                self.remove(express, index + 2, index + 3)
                                self.remove(contrastExpress, index + 2, index + 3)

                elif express[index + 1].word == '(':
                    i = index + 2
                    temp = []
                    temp1 = []
                    sum = 1
                    while 1:
                        if i >= len(express):
                            return 1, 0
                        elif express[i].word == ')':
                            sum -= 1
                        elif express[i].word == '(':
                            sum += 1
                        if sum == 0:
                            break
                        temp.append(express[i])

                        element = token()
                        element.word = express[i].word
                        element.wordtype = express[i].wordtype
                        element.tokenValue = express[i].tokenValue
                        element.line = express[i].line
                        temp1.append(element)

                        i += 1
                    flag, express[index + 1].word = self.calExpressInt(temp, temp1, 0, flag)
                    contrastExpress[index + 1].word = self.tempName.word + str(self.tempName.no)
                    if flag == 0:
                        self.remove(express, index + 2, i)
                        self.remove(contrastExpress, index + 2, i)
                        express[index + 1].tokenValue = 35
                        contrastExpress[index + 1].tokenValue = 35

                else:
                    return 1, 0

                if express[index - 1].tokenValue == 34:
                    k = self.getValueIndex(express[index - 1].word)
                    express[index - 1].word = self.variate[k].value

                if express[index + 1].tokenValue == 34:
                    k = self.getValueIndex(express[index + 1].word)
                    express[index + 1].word = self.variate[k].value

                express[index - 1].word = int(express[index - 1].word) + int(express[index + 1].word)

                formula = quaternion()
                formula.no = self.index
                formula.op = "+"
                formula.args1 = str(contrastExpress[index - 1].word)
                formula.args2 = str(contrastExpress[index + 1].word)
                self.tempName.no += 1
                formula.result = self.tempName.word + str(self.tempName.no)
                self.structure.append(formula)
                self.index += 1

                self.remove(express, index, index + 1)
                self.remove(contrastExpress, index, index + 1)
                express[index - 1].tokenValue = 35
                contrastExpress[index - 1].tokenValue = 35

            elif express[index].word == '-':
                if index >= len(express) - 1:
                    return 1, 0
                elif index == 0:
                    if express[index + 1].tokenValue == 34:
                        k = self.getValueIndex(express[index + 1].word)
                        express[index + 1].word = self.variate[k].value

                    express[index].word = int(express[index + 1].word) * (-1)

                    formula = quaternion()
                    formula.no = self.index
                    formula.op = "@"
                    formula.args1 = str(contrastExpress[index + 1].word)
                    self.tempName.no += 1
                    formula.result = self.tempName.word + str(self.tempName.no)
                    self.structure.append(formula)
                    self.index += 1
                    contrastExpress[index].word = self.tempName.word + str(self.tempName.no)

                    self.remove(express, index + 1, index + 1)
                    self.remove(contrastExpress, index + 1, index + 1)
                    express[index].tokenValue = 35
                    contrastExpress[index].tokenValue = 35
                else:
                    if (index >= len(express) - 1) | (index < 1):
                        return 1, 0
                    elif (express[index - 1].tokenValue != 35) & (express[index - 1].tokenValue != 34):
                        return 1, 0
                    elif (express[index + 1].tokenValue == 35) | (express[index + 1].tokenValue == 34):
                        if index < len(express) - 3:
                            if (express[index + 2].word == '*') | (express[index + 2].word == '/'):
                                temp = []
                                temp.append(express[index + 1])
                                temp.append(express[index + 2])
                                temp.append(express[index + 3])

                                temp1 = []

                                element = token()
                                element.word = express[index + 1].word
                                element.wordtype = express[index + 1].wordtype
                                element.tokenValue = express[index + 1].tokenValue
                                element.line = express[index + 1].line
                                temp1.append(element)

                                element = token()
                                element.word = express[index + 2].word
                                element.wordtype = express[index + 2].wordtype
                                element.tokenValue = express[index + 2].tokenValue
                                element.line = express[index + 2].line
                                temp1.append(element)

                                element = token()
                                element.word = express[index + 3].word
                                element.wordtype = express[index + 3].wordtype
                                element.tokenValue = express[index + 3].tokenValue
                                element.line = express[index + 3].line
                                temp1.append(element)

                                flag, express[index + 1].word = self.calExpressInt(temp, temp1, 0, flag)
                                contrastExpress[index + 1].word = self.tempName.word + str(self.tempName.no)
                                if flag == 0:
                                    express[index + 1].tokenValue = 35
                                    contrastExpress[index + 1].tokenValue = 35
                                    self.remove(express, index + 2, index + 3)
                                    self.remove(contrastExpress, index + 2, index + 3)

                    elif express[index + 1].word == '(':
                        i = index + 2
                        temp = []
                        temp1 = []
                        sum = 1
                        while 1:
                            if i >= len(express):
                                return 1, 0
                            elif express[i].word == ')':
                                sum -= 1
                            elif express[i].word == '(':
                                sum += 1
                            if sum == 0:
                                break
                            temp.append(express[i])

                            element = token()
                            element.word = express[i].word
                            element.wordtype = express[i].wordtype
                            element.tokenValue = express[i].tokenValue
                            element.line = express[i].line
                            temp1.append(element)

                            i += 1
                        flag, express[index + 1].word = self.calExpressInt(temp, temp1, 0, flag)
                        contrastExpress[index + 1].word = self.tempName.word + str(self.tempName.no)
                        if flag == 0:
                            self.remove(express, index + 2, i)
                            self.remove(contrastExpress, index + 2, i)
                            express[index + 1].tokenValue = 35
                            contrastExpress[index + 1].tokenValue = 35

                    else:
                        return 1, 0

                    if express[index - 1].tokenValue == 34:
                        k = self.getValueIndex(express[index - 1].word)
                        express[index - 1].word = self.variate[k].value

                    if express[index + 1].tokenValue == 34:
                        k = self.getValueIndex(express[index + 1].word)
                        express[index + 1].word = self.variate[k].value

                    express[index - 1].word = int(express[index - 1].word) - int(express[index + 1].word)

                    formula = quaternion()
                    formula.no = self.index
                    formula.op = "-"
                    formula.args1 = str(contrastExpress[index - 1].word)
                    formula.args2 = str(contrastExpress[index + 1].word)
                    self.tempName.no += 1
                    formula.result = self.tempName.word + str(self.tempName.no)
                    self.structure.append(formula)
                    self.index += 1

                    self.remove(express, index, index + 1)
                    self.remove(contrastExpress, index, index + 1)
                    express[index - 1].tokenValue = 35
                    contrastExpress[index - 1].tokenValue = 35

            elif (express[index].tokenValue == 35) | (express[index].tokenValue == 34):
                index += 1
            else:
                return 1, 0

    def calExpressFloat(self, express, contrastExpress, index, flag):
        """
        判定算数表达式(整数)
        :param express:
        :return:
        """
        while 1:
            if len(express) == 1:
                if express[0].tokenValue == 34:
                    n = self.getValueIndex(express[0].word)
                    return 0, float(self.variate[n].value)
                else:
                    return 0, float(express[0].word)
            elif flag == 1:
                return 1, 0
            elif express[index].word == '(':
                i = index + 1
                temp = []
                temp1 = []
                sum = 1
                while 1:
                    if i >= len(express):
                        return 1, 0
                    elif express[i].word == ')':
                        sum -= 1
                    elif express[i].word == '(':
                        sum += 1
                    if sum == 0:
                        break
                    temp.append(express[i])

                    element = token()
                    element.word = express[i].word
                    element.wordtype = express[i].wordtype
                    element.tokenValue = express[i].tokenValue
                    element.line = express[i].line
                    temp1.append(element)

                    i += 1
                flag, express[index].word = self.calExpressFloat(temp, temp1, 0, flag)
                contrastExpress[index].word = self.tempName.word + str(self.tempName.no)
                if flag == 0:
                    self.remove(express, index + 1, i)
                    self.remove(contrastExpress, index + 1, i)
                    express[index].tokenValue = 36
                    contrastExpress[index].tokenValue = 36
            elif (express[index].word == '*') | (express[index].word == '/'):
                if (index >= len(express) - 1) | (index < 1):
                    return 1, 0
                elif (express[index - 1].tokenValue != 36) & (express[index - 1].tokenValue != 34) & (
                            express[index - 1].tokenValue != 35):
                    return 1, 0
                elif express[index + 1].word == '(':
                    i = index + 2
                    temp = []
                    temp1 = []
                    sum = 1
                    while 1:
                        if i >= len(express):
                            return 1, 0
                        elif express[i].word == ')':
                            sum -= 1
                        elif express[i].word == '(':
                            sum += 1
                        if sum == 0:
                            break
                        temp.append(express[i])

                        element = token()
                        element.word = express[i].word
                        element.wordtype = express[i].wordtype
                        element.tokenValue = express[i].tokenValue
                        element.line = express[i].line
                        temp1.append(element)

                        i += 1
                    flag, express[index + 1].word = self.calExpressFloat(temp, temp1, 0, flag)
                    contrastExpress[index + 1].word = self.tempName.word + str(self.tempName.no)
                    if flag == 0:
                        self.remove(express, index + 2, i)
                        self.remove(contrastExpress, index + 2, i)

                        express[index + 1].tokenValue = 36
                        contrastExpress[index + 1].tokenValue = 36

                elif (express[index + 1].tokenValue != 36) & (express[index + 1].tokenValue != 34) & (
                            express[index + 1].tokenValue != 35):
                    return 1, 0

                formula = quaternion()
                formula.no = self.index

                if express[index - 1].tokenValue == 34:
                    k = self.getValueIndex(express[index - 1].word)
                    express[index - 1].word = self.variate[k].value

                if express[index + 1].tokenValue == 34:
                    k = self.getValueIndex(express[index + 1].word)
                    express[index + 1].word = self.variate[k].value

                if express[index].word == '*':
                    express[index - 1].word = float(express[index - 1].word) * float(express[index + 1].word)
                    formula.op = "*"
                else:
                    express[index - 1].word = float(express[index - 1].word) / float(express[index + 1].word)
                    formula.op = "/"
                formula.args1 = str(contrastExpress[index - 1].word)
                formula.args2 = str(contrastExpress[index + 1].word)
                self.tempName.no += 1
                formula.result = self.tempName.word + str(self.tempName.no)
                self.structure.append(formula)
                self.index += 1

                self.remove(express, index, index + 1)
                self.remove(contrastExpress, index, index + 1)
                express[index - 1].tokenValue = 36
                contrastExpress[index - 1].tokenValue = 36
            elif express[index].word == '+':
                if (index >= len(express) - 1) | (index < 1):
                    return 1, 0
                elif (express[index - 1].tokenValue != 36) & (express[index - 1].tokenValue != 34) & (
                            express[index - 1].tokenValue != 35):
                    return 1, 0
                elif (express[index + 1].tokenValue == 36) | (express[index + 1].tokenValue == 34) | (
                            express[index + 1].tokenValue == 35):
                    if index < len(express) - 3:
                        if (express[index + 2].word == '*') | (express[index + 2].word == '/'):
                            temp = []
                            temp.append(express[index + 1])
                            temp.append(express[index + 2])
                            temp.append(express[index + 3])

                            temp1 = []

                            element = token()
                            element.word = express[index + 1].word
                            element.wordtype = express[index + 1].wordtype
                            element.tokenValue = express[index + 1].tokenValue
                            element.line = express[index + 1].line
                            temp1.append(element)

                            element = token()
                            element.word = express[index + 2].word
                            element.wordtype = express[index + 2].wordtype
                            element.tokenValue = express[index + 2].tokenValue
                            element.line = express[index + 2].line
                            temp1.append(element)

                            element = token()
                            element.word = express[index + 3].word
                            element.wordtype = express[index + 3].wordtype
                            element.tokenValue = express[index + 3].tokenValue
                            element.line = express[index + 3].line
                            temp1.append(element)

                            flag, express[index + 1].word = self.calExpressFloat(temp, temp1, 0, flag)
                            contrastExpress[index + 1].word = self.tempName.word + str(self.tempName.no)

                            if flag == 0:
                                express[index + 1].tokenValue = 36
                                contrastExpress[index + 1].tokenValue = 36

                                self.remove(express, index + 2, index + 3)
                                self.remove(contrastExpress, index + 2, index + 3)

                elif express[index + 1].word == '(':
                    i = index + 2
                    temp = []
                    temp1 = []
                    sum = 1
                    while 1:
                        if i >= len(express):
                            return 1, 0
                        elif express[i].word == ')':
                            sum -= 1
                        elif express[i].word == '(':
                            sum += 1
                        if sum == 0:
                            break
                        temp.append(express[i])

                        element = token()
                        element.word = express[i].word
                        element.wordtype = express[i].wordtype
                        element.tokenValue = express[i].tokenValue
                        element.line = express[i].line
                        temp1.append(element)

                        i += 1
                    flag, express[index + 1].word = self.calExpressFloat(temp, temp1, 0, flag)
                    contrastExpress[index + 1].word = self.tempName.word + str(self.tempName.no)
                    if flag == 0:
                        self.remove(express, index + 2, i)
                        self.remove(contrastExpress, index + 2, i)
                        express[index + 1].tokenValue = 36
                        contrastExpress[index + 1].tokenValue = 36

                else:
                    return 1, 0

                if express[index - 1].tokenValue == 34:
                    k = self.getValueIndex(express[index - 1].word)
                    express[index - 1].word = self.variate[k].value

                if express[index + 1].tokenValue == 34:
                    k = self.getValueIndex(express[index + 1].word)
                    express[index + 1].word = self.variate[k].value

                express[index - 1].word = float(express[index - 1].word) + float(express[index + 1].word)

                formula = quaternion()
                formula.no = self.index
                formula.op = "+"
                formula.args1 = str(contrastExpress[index - 1].word)
                formula.args2 = str(contrastExpress[index + 1].word)
                self.tempName.no += 1
                formula.result = self.tempName.word + str(self.tempName.no)
                self.structure.append(formula)
                self.index += 1

                self.remove(express, index, index + 1)
                self.remove(contrastExpress, index, index + 1)
                express[index - 1].tokenValue = 36
                contrastExpress[index - 1].tokenValue = 36

            elif express[index].word == '-':
                if index >= len(express) - 1:
                    return 1, 0
                elif index == 0:
                    if express[index + 1].tokenValue == 34:
                        k = self.getValueIndex(express[index + 1].word)
                        express[index + 1].word = self.variate[k].value

                    express[index].word = float(express[index + 1].word) * (-1)

                    formula = quaternion()
                    formula.no = self.index
                    formula.op = "@"
                    formula.args1 = str(contrastExpress[index + 1].word)
                    self.tempName.no += 1
                    formula.result = self.tempName.word + str(self.tempName.no)
                    self.structure.append(formula)
                    self.index += 1
                    contrastExpress[index].word = self.tempName.word + str(self.tempName.no)

                    self.remove(express, index + 1, index + 1)
                    self.remove(contrastExpress, index + 1, index + 1)
                    express[index].tokenValue = 36
                    contrastExpress[index].tokenValue = 36
                else:
                    if (index >= len(express) - 1) | (index < 1):
                        return 1, 0
                    elif (express[index - 1].tokenValue != 36) & (express[index - 1].tokenValue != 34) & (
                                express[index - 1].tokenValue != 35):
                        return 1, 0
                    elif (express[index + 1].tokenValue == 36) | (express[index + 1].tokenValue == 34) | (
                                express[index + 1].tokenValue == 35):
                        if index < len(express) - 3:
                            if (express[index + 2].word == '*') | (express[index + 2].word == '/'):
                                temp = []
                                temp.append(express[index + 1])
                                temp.append(express[index + 2])
                                temp.append(express[index + 3])

                                temp1 = []

                                element = token()
                                element.word = express[index + 1].word
                                element.wordtype = express[index + 1].wordtype
                                element.tokenValue = express[index + 1].tokenValue
                                element.line = express[index + 1].line
                                temp1.append(element)

                                element = token()
                                element.word = express[index + 2].word
                                element.wordtype = express[index + 2].wordtype
                                element.tokenValue = express[index + 2].tokenValue
                                element.line = express[index + 2].line
                                temp1.append(element)

                                element = token()
                                element.word = express[index + 3].word
                                element.wordtype = express[index + 3].wordtype
                                element.tokenValue = express[index + 3].tokenValue
                                element.line = express[index + 3].line
                                temp1.append(element)

                                flag, express[index + 1].word = self.calExpressFloat(temp, temp1, 0, flag)
                                contrastExpress[index + 1].word = self.tempName.word + str(self.tempName.no)
                                if flag == 0:
                                    express[index + 1].tokenValue = 36
                                    contrastExpress[index + 1].tokenValue = 36
                                    self.remove(express, index + 2, index + 3)
                                    self.remove(contrastExpress, index + 2, index + 3)

                    elif express[index + 1].word == '(':
                        i = index + 2
                        temp = []
                        temp1 = []
                        sum = 1
                        while 1:
                            if i >= len(express):
                                return 1, 0
                            elif express[i].word == ')':
                                sum -= 1
                            elif express[i].word == '(':
                                sum += 1
                            if sum == 0:
                                break
                            temp.append(express[i])

                            element = token()
                            element.word = express[i].word
                            element.wordtype = express[i].wordtype
                            element.tokenValue = express[i].tokenValue
                            element.line = express[i].line
                            temp1.append(element)

                            i += 1
                        flag, express[index + 1].word = self.calExpressFloat(temp, temp1, 0, flag)
                        contrastExpress[index + 1].word = self.tempName.word + str(self.tempName.no)
                        if flag == 0:
                            self.remove(express, index + 2, i)
                            self.remove(contrastExpress, index + 2, i)
                            express[index + 1].tokenValue = 36
                            contrastExpress[index + 1].tokenValue = 36

                    else:
                        return 1, 0

                    if express[index - 1].tokenValue == 34:
                        k = self.getValueIndex(express[index - 1].word)
                        express[index - 1].word = self.variate[k].value

                    if express[index + 1].tokenValue == 34:
                        k = self.getValueIndex(express[index + 1].word)
                        express[index + 1].word = self.variate[k].value

                    express[index - 1].word = float(express[index - 1].word) - float(express[index + 1].word)

                    formula = quaternion()
                    formula.no = self.index
                    formula.op = "-"
                    formula.args1 = str(contrastExpress[index - 1].word)
                    formula.args2 = str(contrastExpress[index + 1].word)
                    self.tempName.no += 1
                    formula.result = self.tempName.word + str(self.tempName.no)
                    self.structure.append(formula)
                    self.index += 1

                    self.remove(express, index, index + 1)
                    self.remove(contrastExpress, index, index + 1)
                    express[index - 1].tokenValue = 36
                    contrastExpress[index - 1].tokenValue = 36

            elif (express[index].tokenValue == 36) | (express[index].tokenValue == 34) | (
                        express[index].tokenValue == 35):
                index += 1
            else:
                return 1, 0

    def judgeSort(self, express):
        """
        判断布尔表达式类型
        :param express:
        :return:
        """
        index = 0
        while 1:
            if index >= len(express):
                if self.haveCompare(express) == 1:
                    return 1
                else:
                    return 2
            elif (express[index].word == 'and') | (express[index].word == 'or') | (express[index].word == 'not'):
                return 2
            index += 1

    def haveCompare(self, express):
        """
        判断是否有判断运算符
        :param express:
        :return:
        """
        index = 0
        while 1:
            if index >= len(express):
                return 0
            elif (express[index].word == '>') | (express[index].word == '<') | (express[index].word == '=='):
                return 1
            index += 1

    def simpyBool(self, express, contrastExpress, index, flag):
        """
        简单的比较处理
        :param express:
        :param contrastExpress:
        :param index:
        :param flag:
        :return:
        """
        left = 0.0
        right = 0.0
        leftIndex = 0
        rightIndex = 0
        character = ''
        while 1:
            if index >= len(express):
                break
            elif (express[index].word == '>') | (express[index].word == '==') | (express[index].word == '<'):
                character = express[index].word
                temp = []
                temp1 = []
                index += 1
                rightIndex = index
                while 1:
                    if index >= len(express):
                        break
                    temp.append(express[index])
                    element = token()
                    element.word = express[index].word
                    element.wordtype = express[index].wordtype
                    element.tokenValue = express[index].tokenValue
                    element.line = express[index].line
                    temp1.append(element)
                    index += 1
                length = len(temp)
                rig = temp[0].word
                flag, right = self.calExpressFloat(temp, temp1, 0, flag)

            else:
                leftIndex = index
                if express[index].tokenValue == 34:
                    i = self.getValueIndex(express[index].word)
                    left = float(self.variate[i].value)
                else:
                    left = float(express[index].word)
                index += 1
        result = ''
        formula = quaternion()
        formula.no = self.index
        if length == 1:
            formula.args2 = rig
        else:
            formula.args2 = self.tempName.word + str(self.tempName.no)
        formula.args1 = express[leftIndex].word
        if character == '>':
            result = left > right
            formula.op = 'j>'
        elif character == '<':
            result = left < right
            formula.op = 'j<'
        else:
            result = left == right
            formula.op = 'j='

        formula.result = '#'
        self.structure.append(formula)
        self.index += 1

        formula = quaternion()
        formula.no = self.index
        formula.op = 'j'
        formula.result = '-1'
        self.structure.append(formula)
        self.index += 1

        return result

    def boolExpress(self, express):
        index = 0
        while 1:
            if index >= len(express):
                break
            elif express[index].word == 'and':
                if express[index - 1].word == ')':
                    flag = 1
                    temp = []
                    i = index - 1
                    while 1:
                        if flag == 0:
                            break
                        elif i < 0:
                            break
                        elif express[i].word == '(':
                            flag -= 1
                        elif express[i].word == ')':
                            flag += 1
                        temp.append(express[i])
                        i -= 1
                    temp = temp[::1]
                    self.boolExpress(temp)
                elif index >= 3:
                    if (express[index - 2].word == '>') | (express[index - 2].word == '<') | (
                                express[index - 2].word == '=='):
                        formula = quaternion()
                        if express[index - 2].word == '>':
                            formula.op = "j>"
                        elif express[index - 2].word == '<':
                            formula.op = 'j<'
                        elif express[index - 2].word == '==':
                            formula.op = 'j='
                        formula.no = self.index
                        formula.op = "jnz"
                        formula.args1 = express[index - 3].word
                        formula.args2 = express[index - 1].word
                        formula.result = str(self.index + 2)
                        self.structure.append(formula)
                        self.index += 1

                        formula = quaternion()
                        formula.no = self.index
                        formula.op = 'j'
                        formula.result = '-1'
                        self.structure.append(formula)
                        self.index += 1
                    else:
                        formula = quaternion()
                        formula.no = self.index
                        formula.op = "jnz"
                        formula.args1 = express[index - 1].word
                        formula.result = str(self.index + 2)
                        self.structure.append(formula)
                        self.index += 1

                        formula = quaternion()
                        formula.no = self.index
                        formula.op = 'j'
                        formula.result = '-1'
                        self.structure.append(formula)
                        self.index += 1
                else:
                    formula = quaternion()
                    formula.no = self.index
                    formula.op = "jnz"
                    formula.args1 = express[index - 1].word
                    formula.result = str(self.index + 2)
                    self.structure.append(formula)
                    self.index += 1

                    formula = quaternion()
                    formula.no = self.index
                    formula.op = 'j'
                    formula.result = '-1'
                    self.structure.append(formula)
                    self.index += 1

                if express[index + 1].word == '(':
                    flag = 1
                    temp = []
                    index = index + 1
                    while 1:
                        if flag == 0:
                            break
                        elif index >= len(express):
                            break
                        elif express[index].word == '(':
                            flag += 1
                        elif express[index].word == ')':
                            flag -= 1
                        temp.append(express[index])
                        i += 1
                    self.boolExpress(temp)
                elif index < len(express) - 3:
                    if (express[index + 2].word == '>') | (express[index + 2].word == '<') | (
                                express[index + 2].word == '=='):
                        formula = quaternion()
                        if express[index - 2].word == '>':
                            formula.op = "j>"
                        elif express[index - 2].word == '<':
                            formula.op = 'j<'
                        elif express[index - 2].word == '==':
                            formula.op = 'j='
                        formula.no = self.index
                        formula.op = "jnz"
                        formula.args1 = express[index + 1].word
                        formula.args2 = express[index + 3].word
                        formula.result = str(self.index + 2)
                        self.structure.append(formula)
                        self.index += 1

                        formula = quaternion()
                        formula.no = self.index
                        formula.op = 'j'
                        formula.result = '-1'
                        self.structure.append(formula)
                        self.index += 1

                        index += 3
                    else:
                        formula = quaternion()
                        formula.no = self.index
                        formula.op = "jnz"
                        formula.args1 = express[index + 1].word
                        formula.result = str(self.index + 2)
                        self.structure.append(formula)
                        self.index += 1

                        formula = quaternion()
                        formula.no = self.index
                        formula.op = 'j'
                        formula.result = '-1'
                        self.structure.append(formula)
                        self.index += 1
                else:
                    formula = quaternion()
                    formula.no = self.index
                    formula.op = "jnz"
                    formula.args1 = express[index + 1].word
                    formula.result = str(self.index + 2)
                    self.structure.append(formula)
                    self.index += 1

                    formula = quaternion()
                    formula.no = self.index
                    formula.op = 'j'
                    formula.result = '-1'
                    self.structure.append(formula)
                    self.index += 1

            elif express[index].word == 'or':
                if express[index - 1].word == ')':
                    flag = 1
                    temp = []
                    i = index - 1
                    while 1:
                        if flag == 0:
                            break
                        elif i < 0:
                            break
                        elif express[i].word == '(':
                            flag -= 1
                        elif express[i].word == ')':
                            flag += 1
                        temp.append(express[i])
                        i -= 1
                    temp = temp[::1]
                    self.boolExpress(temp)
                elif index >= 3:
                    if (express[index - 2].word == '>') | (express[index - 2].word == '<') | (
                                express[index - 2].word == '=='):
                        formula = quaternion()
                        if express[index - 2].word == '>':
                            formula.op = "j>"
                        elif express[index - 2].word == '<':
                            formula.op = 'j<'
                        elif express[index - 2].word == '==':
                            formula.op = 'j='
                        formula.no = self.index
                        formula.op = "jnz"
                        formula.args1 = express[index - 3].word
                        formula.args2 = express[index - 1].word
                        formula.result = '#'
                        self.structure.append(formula)
                        self.index += 1

                        formula = quaternion()
                        formula.no = self.index
                        formula.op = 'j'
                        formula.result = str(self.index + 1)
                        self.structure.append(formula)
                        self.index += 1
                    else:
                        formula = quaternion()
                        formula.no = self.index
                        formula.op = "jnz"
                        formula.args1 = express[index - 1].word
                        formula.result = '#'
                        self.structure.append(formula)
                        self.index += 1

                        formula = quaternion()
                        formula.no = self.index
                        formula.op = 'j'
                        formula.result = str(self.index + 1)
                        self.structure.append(formula)
                        self.index += 1
                else:
                    formula = quaternion()
                    formula.no = self.index
                    formula.op = "jnz"
                    formula.args1 = express[index - 1].word
                    formula.result = '#'
                    self.structure.append(formula)
                    self.index += 1

                    formula = quaternion()
                    formula.no = self.index
                    formula.op = 'j'
                    formula.result = str(self.index + 1)
                    self.structure.append(formula)
                    self.index += 1

                if express[index + 1].word == '(':
                    flag = 1
                    temp = []
                    index = index + 1
                    while 1:
                        if flag == 0:
                            break
                        elif index >= len(express):
                            break
                        elif express[index].word == '(':
                            flag += 1
                        elif express[index].word == ')':
                            flag -= 1
                        temp.append(express[index])
                        i += 1
                    self.boolExpress(temp)
                elif index < len(express) - 3:
                    if (express[index + 2].word == '>') | (express[index + 2].word == '<') | (
                                express[index + 2].word == '=='):
                        formula = quaternion()
                        if express[index - 2].word == '>':
                            formula.op = "j>"
                        elif express[index - 2].word == '<':
                            formula.op = 'j<'
                        elif express[index - 2].word == '==':
                            formula.op = 'j='
                        formula.no = self.index
                        formula.op = "jnz"
                        formula.args1 = express[index + 1].word
                        formula.args2 = express[index + 3].word
                        formula.result = '#'
                        self.structure.append(formula)
                        self.index += 1

                        formula = quaternion()
                        formula.no = self.index
                        formula.op = 'j'
                        if index == len(express) - 4:
                            formula.result = '-1'
                        else:
                            formula.result = str(self.index + 1)
                        self.structure.append(formula)
                        self.index += 1

                        index += 3
                    else:
                        formula = quaternion()
                        formula.no = self.index
                        formula.op = "jnz"
                        formula.args1 = express[index + 1].word
                        formula.result = '#'
                        self.structure.append(formula)
                        self.index += 1

                        formula = quaternion()
                        formula.no = self.index
                        formula.op = 'j'
                        formula.result = str(self.index + 1)
                        self.structure.append(formula)
                        self.index += 1
                else:
                    formula = quaternion()
                    formula.no = self.index
                    formula.op = "jnz"
                    formula.args1 = express[index + 1].word
                    formula.result = "#"
                    self.structure.append(formula)
                    self.index += 1

                    formula = quaternion()
                    formula.no = self.index
                    formula.op = 'j'
                    if index == len(express) - 2:
                        formula.result = '-1'
                    else:
                        formula.result = str(self.index + 1)
                    self.structure.append(formula)
                    self.index += 1

            index += 1

    # def boolExpress(self, express, contrastExpress, index, flag):
    #     """
    #     判别布尔表达式
    #     :param express:
    #     :param index:
    #     :param flag:
    #     :return:
    #     """
    #     while 1:
    #         if len(express) == 1:
    #             return 0, express[0].word
    #         elif flag == 1:
    #             return 1, 0
    #         elif express[index].word == '(':
    #             i = index + 1
    #             temp = []
    #             temp1 = []
    #             sum = 1
    #             while 1:
    #                 if i >= len(express):
    #                     return 1, 0
    #                 elif express[i].word == ')':
    #                     sum -= 1
    #                 elif express[i].word == '(':
    #                     sum += 1
    #                 if sum == 0:
    #                     break
    #                 temp.append(express[i])
    #
    #                 element = token()
    #                 element.word = express[i].word
    #                 element.wordtype = express[i].wordtype
    #                 element.tokenValue = express[i].tokenValue
    #                 element.line = express[i].line
    #                 temp1.append(element)
    #
    #                 i += 1
    #             flag, express[index].word = self.boolExpress(temp, temp1, 0, flag)
    #             contrastExpress[index].word = self.tempName.word + str(self.tempName.no)
    #             if flag == 0:
    #                 self.remove(express, index + 1, i)
    #                 self.remove(contrastExpress, index + 1, i)
    #                 express[index].tokenValue = 38
    #                 contrastExpress[index].tokenValue = 0
    #         elif express[index].word == 'and':
    #             if (index >= len(express) - 1) | (index < 1):
    #                 return 1, 0
    #             elif (express[index - 1].tokenValue != 38) & (express[index - 1].tokenValue != 34) & (
    #                         express[index - 1].tokenValue != 35):
    #                 return 1, 0
    #             elif express[index + 1].word == '(':
    #                 i = index + 2
    #                 temp = []
    #                 temp1 = []
    #                 sum = 1
    #                 while 1:
    #                     if i >= len(express):
    #                         return 1, 0
    #                     elif express[i].word == ')':
    #                         sum -= 1
    #                     elif express[i].word == '(':
    #                         sum += 1
    #                     if sum == 0:
    #                         break
    #                     temp.append(express[i])
    #
    #                     element = token()
    #                     element.word = express[i].word
    #                     element.wordtype = express[i].wordtype
    #                     element.tokenValue = express[i].tokenValue
    #                     element.line = express[i].line
    #                     temp1.append(element)
    #
    #                     i += 1
    #                 flag, express[index + 1].word = self.boolExpress(temp, temp1, 0, flag)
    #                 contrastExpress[index + 1].word = self.tempName.word + str(self.tempName.no)
    #                 if flag == 0:
    #                     self.remove(express, index + 2, i)
    #                     self.remove(contrastExpress, index + 2, i)
    #
    #                     express[index + 1].tokenValue = 38
    #                     contrastExpress[index + 1].tokenValue = 0
    #
    #             elif (express[index + 1].tokenValue != 38) & (express[index + 1].tokenValue != 34) & (
    #                         express[index + 1].tokenValue != 35):
    #                 return 1, 0
    #
    #             if express[index - 1].tokenValue == 34:
    #                 k = self.getValueIndex(express[index - 1].word)
    #                 express[index - 1].word = self.variate[k].value
    #
    #             if express[index + 1].tokenValue == 34:
    #                 k = self.getValueIndex(express[index + 1].word)
    #                 express[index + 1].word = self.variate[k].value
    #
    #             if index >= 3:
    #                 if express[index - 2].word == '<':
    #                     if express[index - 3].tokenValue == 34:
    #                         k = self.getValueIndex(express[index - 3].word)
    #                         express[index - 3].word = self.variate[k].value
    #
    #                     formula = quaternion()
    #                     formula.no = self.index
    #                     formula.op = "j<"
    #                     formula.args1 = str(contrastExpress[index - 3].word)
    #                     formula.args2 = str(contrastExpress[index - 1].word)
    #                     formula.result = str(self.index + 2)
    #                     self.structure.append(formula)
    #                     self.index += 1
    #
    #                     express[i - 1].word = int(express[i - 3].word) < int(express[i - 1].word)
    #                     express[i - 1].tokenValue = 38
    #                     contrastExpress[i - 1].tokenValue = 0
    #                     self.remove(express, i - 3, i - 2)
    #                     self.remove(contrastExpress, i - 3, i - 2)
    #
    #                 elif express[index - 2].word == '>':
    #                     if express[index - 3].tokenValue == 34:
    #                         k = self.getValueIndex(express[index - 3].word)
    #                         express[index - 3].word = self.variate[k].value
    #
    #                     formula = quaternion()
    #                     formula.no = self.index
    #                     formula.op = "j>"
    #                     formula.args1 = str(contrastExpress[index - 3].word)
    #                     formula.args2 = str(contrastExpress[index - 1].word)
    #                     formula.result = str(self.index + 2)
    #                     self.structure.append(formula)
    #                     self.index += 1
    #
    #                     express[index - 1].word = int(express[index - 3].word) > int(express[index - 1].word)
    #                     express[index - 1].tokenValue = 38
    #                     contrastExpress[index - 1].tokenValue = 0
    #                     self.remove(express, index - 3, index - 2)
    #                     self.remove(contrastExpress, index - 3, index - 2)
    #
    #                 elif express[index - 2].word == '==':
    #                     if express[index - 3].tokenValue == 34:
    #                         k = self.getValueIndex(express[index - 3].word)
    #                         express[index - 3].word = self.variate[k].value
    #
    #                     formula = quaternion()
    #                     formula.no = self.index
    #                     formula.op = "j="
    #                     formula.args1 = str(contrastExpress[index - 3].word)
    #                     formula.args2 = str(contrastExpress[index - 1].word)
    #                     formula.result = str(self.index + 2)
    #                     self.structure.append(formula)
    #                     self.index += 1
    #
    #                     express[index - 1].word = int(express[index - 3].word) == int(express[index - 1].word)
    #                     express[index - 1].tokenValue = 38
    #                     contrastExpress[index - 1].tokenValue = 0
    #                     self.remove(express, index - 3, index - 2)
    #                     self.remove(contrastExpress, index - 3, index - 2)
    #
    #                 else:
    #                     if contrastExpress[index - 1].tokenValue == 38:
    #                         formula = quaternion()
    #                         formula.no = self.index
    #                         formula.op = "jnz"
    #                         formula.args1 = str(contrastExpress[index - 1].word)
    #                         formula.result = str(self.index + 2)
    #                         self.structure.append(formula)
    #                         self.index += 1
    #
    #                 formula1 = quaternion()
    #                 formula1.no = self.index
    #                 formula1.op = "j"
    #                 formula.result = '-1'
    #                 self.structure.append(formula)
    #                 self.index += 1
    #             if index <= len(express) - 4:
    #                 if express[index + 2].word == '<':
    #                     if express[index + 3].tokenValue == 34:
    #                         k = self.getValueIndex(express[index + 3].word)
    #                         express[index + 3].word = self.variate[k].value
    #
    #                     formula = quaternion()
    #                     formula.no = self.index
    #                     formula.op = "j<"
    #                     formula.args1 = str(contrastExpress[index + 1].word)
    #                     formula.args2 = str(contrastExpress[index + 3].word)
    #                     formula.result = str(self.index + 2)
    #                     self.structure.append(formula)
    #                     self.index += 1
    #
    #                     express[i + 1].word = int(express[i + 1].word) < int(express[i + 3].word)
    #                     express[i + 1].tokenValue = 38
    #                     contrastExpress[i + 1].tokenValue = 0
    #                     self.remove(express, i + 2, i + 3)
    #                     self.remove(contrastExpress, i + 2, i + 3)
    #
    #                 elif express[index - 2].word == '>':
    #                     if express[index + 3].tokenValue == 34:
    #                         k = self.getValueIndex(express[index + 3].word)
    #                         express[index + 3].word = self.variate[k].value
    #
    #                     formula = quaternion()
    #                     formula.no = self.index
    #                     formula.op = "j>"
    #                     formula.args1 = str(contrastExpress[index + 1].word)
    #                     formula.args2 = str(contrastExpress[index + 3].word)
    #                     formula.result = str(self.index + 2)
    #                     self.structure.append(formula)
    #                     self.index += 1
    #
    #                     express[index + 1].word = int(express[index + 1].word) > int(express[index + 3].word)
    #                     express[index + 1].tokenValue = 38
    #                     contrastExpress[index + 1].tokenValue = 0
    #                     self.remove(express, index + 2, index + 3)
    #                     self.remove(contrastExpress, index + 2, index + 3)
    #
    #                 elif express[index - 2].word == '==':
    #                     if express[index + 3].tokenValue == 34:
    #                         k = self.getValueIndex(express[index + 3].word)
    #                         express[index + 3].word = self.variate[k].value
    #
    #                     formula = quaternion()
    #                     formula.no = self.index
    #                     formula.op = "j="
    #                     formula.args1 = str(contrastExpress[index + 1].word)
    #                     formula.args2 = str(contrastExpress[index + 3].word)
    #                     formula.result = str(self.index + 2)
    #                     self.structure.append(formula)
    #                     self.index += 1
    #
    #                     express[index + 1].word = int(express[index + 1].word) == int(express[index + 3].word)
    #                     express[index + 1].tokenValue = 38
    #                     contrastExpress[index + 1].tokenValue = 0
    #                     self.remove(express, index + 2, index + 3)
    #                     self.remove(contrastExpress, index + 2, index + 3)
    #
    #                 else:
    #                     if contrastExpress[index + 1].tokenValue == 38:
    #                         formula = quaternion()
    #                         formula.no = self.index
    #                         formula.op = "jnz"
    #                         formula.args1 = str(contrastExpress[index + 1].word)
    #                         formula.result = str(self.index + 2)
    #                         self.structure.append(formula)
    #                         self.index += 1
    #
    #                 formula1 = quaternion()
    #                 formula1.no = self.index
    #                 formula1.op = "j"
    #                 formula.result = '-1'
    #                 self.structure.append(formula)
    #                 self.index += 1
    #
    #             if (index < 3) & (index > len(express) - 4):
    #                 if (contrastExpress[index - 1].tokenValue == 38) | (contrastExpress[index - 1].tokenValue == 34):
    #                     formula = quaternion()
    #                     formula.no = self.index
    #                     formula.op = "jnz"
    #                     formula.args1 = str(contrastExpress[index - 1].word)
    #                     formula.result = str(self.index + 2)
    #                     self.structure.append(formula)
    #                     self.index += 1
    #
    #                 formula1 = quaternion()
    #                 formula1.no = self.index
    #                 formula1.op = "j"
    #                 formula1.result = '-1'
    #                 self.structure.append(formula1)
    #                 self.index += 1
    #
    #                 if (contrastExpress[index + 1].tokenValue == 38) | (contrastExpress[index + 1].tokenValue == 34):
    #                     formula = quaternion()
    #                     formula.no = self.index
    #                     formula.op = "jnz"
    #                     formula.args1 = str(contrastExpress[index + 1].word)
    #                     formula.result = str(self.index + 2)
    #                     self.structure.append(formula)
    #                     self.index += 1
    #
    #                 formula1 = quaternion()
    #                 formula1.no = self.index
    #                 formula1.op = "j"
    #                 formula1.result = '-1'
    #                 self.structure.append(formula1)
    #                 self.index += 1
    #
    #                 if express[index - 1].tokenValue == 34:
    #                     n = self.getValueIndex(express[index - 1].word)
    #                 express[index - 1].word = self.variate[n].word
    #                 express[index - 1].tokenValue = 38
    #                 if express[index + 1].tokenValue == 34:
    #                     n = self.getValueIndex(express[index + 1].word)
    #                 express[index + 1].word = self.variate[n].word
    #                 express[index + 1].tokenValue = 38
    #                 express[index - 1].word = bool(express[index - 1].word) & bool(express[index + 1].word)
    #                 self.remove(express, index, index + 1)
    #                 self.remove(contrastExpress, index, index + 1)
    #         elif express[index].word == 'or':
    #             if (index >= len(express) - 1) | (index < 1):
    #                 return 1, 0
    #             elif (express[index - 1].tokenValue != 38) & (express[index - 1].tokenValue != 34) & (
    #                         express[index - 1].tokenValue != 35):
    #                 return 1, 0
    #             elif (express[index + 1].tokenValue == 38) | (express[index + 1].tokenValue == 34) | (
    #                         express[index + 1].tokenValue == 35):
    #                 if index < len(express) - 3:
    #                     if express[index + 2].word == 'and':
    #                         temp = []
    #                         temp.append(express[index + 1])
    #                         temp.append(express[index + 2])
    #                         temp.append(express[index + 3])
    #
    #                         temp1 = []
    #
    #                         element = token()
    #                         element.word = express[index + 1].word
    #                         element.wordtype = express[index + 1].wordtype
    #                         element.tokenValue = express[index + 1].tokenValue
    #                         element.line = express[index + 1].line
    #                         temp1.append(element)
    #
    #                         element = token()
    #                         element.word = express[index + 2].word
    #                         element.wordtype = express[index + 2].wordtype
    #                         element.tokenValue = express[index + 2].tokenValue
    #                         element.line = express[index + 2].line
    #                         temp1.append(element)
    #
    #                         element = token()
    #                         element.word = express[index + 3].word
    #                         element.wordtype = express[index + 3].wordtype
    #                         element.tokenValue = express[index + 3].tokenValue
    #                         element.line = express[index + 3].line
    #                         temp1.append(element)
    #
    #                         flag, express[index + 1].word = self.boolExpress(temp, temp1, 0, flag)
    #                         contrastExpress[index + 1].word = self.tempName.word + str(self.tempName.no)
    #
    #                         if flag == 0:
    #                             express[index + 1].tokenValue = 38
    #                             contrastExpress[index + 1].tokenValue = 0
    #
    #                             self.remove(express, index + 2, index + 3)
    #                             self.remove(contrastExpress, index + 2, index + 3)
    #
    #             elif express[index + 1].word == '(':
    #                 i = index + 2
    #                 temp = []
    #                 temp1 = []
    #                 sum = 1
    #                 while 1:
    #                     if i >= len(express):
    #                         return 1, 0
    #                     elif express[i].word == ')':
    #                         sum -= 1
    #                     elif express[i].word == '(':
    #                         sum += 1
    #                     if sum == 0:
    #                         break
    #                     temp.append(express[i])
    #
    #                     element = token()
    #                     element.word = express[i].word
    #                     element.wordtype = express[i].wordtype
    #                     element.tokenValue = express[i].tokenValue
    #                     element.line = express[i].line
    #                     temp1.append(element)
    #
    #                     i += 1
    #                 flag, express[index + 1].word = self.boolExpress(temp, temp1, 0, flag)
    #                 contrastExpress[index + 1].word = self.tempName.word + str(self.tempName.no)
    #                 if flag == 0:
    #                     self.remove(express, index + 2, i)
    #                     self.remove(contrastExpress, index + 2, i)
    #                     express[index + 1].tokenValue = 38
    #                     contrastExpress[index + 1].tokenValue = 0
    #
    #             else:
    #                 return 1, 0
    #
    #             if express[index - 1].tokenValue == 34:
    #                 k = self.getValueIndex(express[index - 1].word)
    #                 express[index - 1].word = self.variate[k].value
    #
    #             if express[index + 1].tokenValue == 34:
    #                 k = self.getValueIndex(express[index + 1].word)
    #                 express[index + 1].word = self.variate[k].value
    #             patch = 0
    #             if index >= 3:
    #                 patch = 1
    #                 if express[index - 2].word == '<':
    #                     if express[index - 3].tokenValue == 34:
    #                         k = self.getValueIndex(express[index - 3].word)
    #                         express[index - 3].word = self.variate[k].value
    #
    #                     formula = quaternion()
    #                     formula.no = self.index
    #                     formula.op = "j<"
    #                     formula.args1 = str(contrastExpress[index - 3].word)
    #                     formula.args2 = str(contrastExpress[index - 1].word)
    #                     formula.result = "#"
    #                     self.structure.append(formula)
    #                     self.index += 1
    #
    #                     express[index - 1].word = int(express[index - 3].word) < int(express[index - 1].word)
    #                     express[index - 1].tokenValue = 38
    #                     contrastExpress[index - 1].tokenValue = 0
    #                     self.remove(express, index - 3, index - 2)
    #                     self.remove(contrastExpress, index - 3, index - 2)
    #                     index -= 2
    #
    #                 elif express[index - 2].word == '>':
    #                     if express[index - 3].tokenValue == 34:
    #                         k = self.getValueIndex(express[index - 3].word)
    #                         express[index - 3].word = self.variate[k].value
    #
    #                     formula = quaternion()
    #                     formula.no = self.index
    #                     formula.op = "j>"
    #                     formula.args1 = str(contrastExpress[index - 3].word)
    #                     formula.args2 = str(contrastExpress[index - 1].word)
    #                     formula.result = "#"
    #                     self.structure.append(formula)
    #                     self.index += 1
    #
    #                     express[index - 1].word = int(express[index - 3].word) > int(express[index - 1].word)
    #                     express[index - 1].tokenValue = 38
    #                     contrastExpress[index - 1].tokenValue = 0
    #                     self.remove(express, index - 3, index - 2)
    #                     self.remove(contrastExpress, index - 3, index - 2)
    #                     index -= 2
    #
    #                 elif express[index - 2].word == '==':
    #                     if express[index - 3].tokenValue == 34:
    #                         k = self.getValueIndex(express[index - 3].word)
    #                         express[index - 3].word = self.variate[k].value
    #
    #                     formula = quaternion()
    #                     formula.no = self.index
    #                     formula.op = "j="
    #                     formula.args1 = str(contrastExpress[index - 3].word)
    #                     formula.args2 = str(contrastExpress[index - 1].word)
    #                     formula.result = "#"
    #                     self.structure.append(formula)
    #                     self.index += 1
    #
    #                     express[index - 1].word = int(express[index - 3].word) == int(express[index - 1].word)
    #                     express[index - 1].tokenValue = 38
    #                     contrastExpress[index - 1].tokenValue = 0
    #                     self.remove(express, index - 3, index - 2)
    #                     self.remove(contrastExpress, index - 3, index - 2)
    #                     index -= 2
    #
    #                 else:
    #                     if contrastExpress[index - 1].tokenValue == 38:
    #                         formula = quaternion()
    #                         formula.no = self.index
    #                         formula.op = "jnz"
    #                         formula.args1 = str(contrastExpress[index - 1].word)
    #                         formula.result = "#"
    #                         self.structure.append(formula)
    #                         self.index += 1
    #
    #                 formula1 = quaternion()
    #                 formula1.no = self.index
    #                 formula1.op = "j"
    #                 formula.result = str(self.index + 1)
    #                 self.structure.append(formula)
    #                 self.index += 1
    #             if index <= len(express) - 4:
    #                 patch = 1
    #                 if express[index + 2].word == '<':
    #                     if express[index + 3].tokenValue == 34:
    #                         k = self.getValueIndex(express[index + 3].word)
    #                         express[index + 3].word = self.variate[k].value
    #
    #                     formula = quaternion()
    #                     formula.no = self.index
    #                     formula.op = "j<"
    #                     formula.args1 = str(contrastExpress[index + 1].word)
    #                     formula.args2 = str(contrastExpress[index + 3].word)
    #                     formula.result = "#"
    #                     self.structure.append(formula)
    #                     self.index += 1
    #
    #                     express[index + 1].word = int(express[index + 1].word) < int(express[index + 3].word)
    #                     express[index + 1].tokenValue = 38
    #                     contrastExpress[index + 1].tokenValue = 0
    #                     self.remove(express, index + 2, index + 3)
    #                     self.remove(contrastExpress, index + 2, index + 3)
    #
    #                 elif express[index - 2].word == '>':
    #                     if express[index + 3].tokenValue == 34:
    #                         k = self.getValueIndex(express[index + 3].word)
    #                         express[index + 3].word = self.variate[k].value
    #
    #                     formula = quaternion()
    #                     formula.no = self.index
    #                     formula.op = "j>"
    #                     formula.args1 = str(contrastExpress[index + 1].word)
    #                     formula.args2 = str(contrastExpress[index + 3].word)
    #                     formula.result = "#"
    #                     self.structure.append(formula)
    #                     self.index += 1
    #
    #                     express[index + 1].word = int(express[index + 1].word) > int(express[index + 3].word)
    #                     express[index + 1].tokenValue = 38
    #                     contrastExpress[index + 1].tokenValue = 0
    #                     self.remove(express, index + 2, index + 3)
    #                     self.remove(contrastExpress, index + 2, index + 3)
    #
    #                 elif express[index - 2].word == '==':
    #                     if express[index + 3].tokenValue == 34:
    #                         k = self.getValueIndex(express[index + 3].word)
    #                         express[index + 3].word = self.variate[k].value
    #
    #                     formula = quaternion()
    #                     formula.no = self.index
    #                     formula.op = "j="
    #                     formula.args1 = str(contrastExpress[index + 1].word)
    #                     formula.args2 = str(contrastExpress[index + 3].word)
    #                     formula.result = "#"
    #                     self.structure.append(formula)
    #                     self.index += 1
    #
    #                     express[index + 1].word = int(express[index + 1].word) == int(express[index + 3].word)
    #                     express[index + 1].tokenValue = 38
    #                     contrastExpress[index + 1].tokenValue = 0
    #                     self.remove(express, index + 2, index + 3)
    #                     self.remove(contrastExpress, index + 2, index + 3)
    #
    #                 else:
    #                     if contrastExpress[index + 1].tokenValue == 38:
    #                         formula = quaternion()
    #                         formula.no = self.index
    #                         formula.op = "jnz"
    #                         formula.args1 = str(contrastExpress[index + 1].word)
    #                         formula.result = "#"
    #                         self.structure.append(formula)
    #                         self.index += 1
    #
    #                 formula1 = quaternion()
    #                 formula1.no = self.index
    #                 formula1.op = "j"
    #                 formula.result = str(self.index + 1)
    #                 self.structure.append(formula)
    #                 self.index += 1
    #
    #             if (index < 3) & (index > len(express) - 4) & (patch == 0):
    #                 if (contrastExpress[index - 1].tokenValue == 38) | (contrastExpress[index - 1].tokenValue == 34):
    #                     formula = quaternion()
    #                     formula.no = self.index
    #                     formula.op = "jnz"
    #                     formula.args1 = str(contrastExpress[index - 1].word)
    #                     formula.result = "#"
    #                     self.structure.append(formula)
    #                     self.index += 1
    #
    #                 formula1 = quaternion()
    #                 formula1.no = self.index
    #                 formula1.op = "j"
    #                 formula1.result = str(self.index + 1)
    #                 self.structure.append(formula1)
    #                 self.index += 1
    #
    #                 if (contrastExpress[index + 1].tokenValue == 38) | (contrastExpress[index + 1].tokenValue == 34):
    #                     formula = quaternion()
    #                     formula.no = self.index
    #                     formula.op = "jnz"
    #                     formula.args1 = str(contrastExpress[index + 1].word)
    #                     formula.result = "#"
    #                     self.structure.append(formula)
    #                     self.index += 1
    #
    #                 formula1 = quaternion()
    #                 formula1.no = self.index
    #                 formula1.op = "j"
    #                 formula1.result = '-1'
    #                 self.structure.append(formula1)
    #                 self.index += 1
    #
    #             if express[index - 1].tokenValue == 34:
    #                 n = self.getValueIndex(express[index - 1].word)
    #                 express[index - 1].word = self.variate[n].word
    #                 express[index - 1].tokenValue = 38
    #             if express[index + 1].tokenValue == 34:
    #                 n = self.getValueIndex(express[index + 1].word)
    #                 express[index + 1].word = self.variate[n].word
    #                 express[index + 1].tokenValue = 38
    #             express[index - 1].word = bool(express[index - 1].word) | bool(express[index + 1].word)
    #             self.remove(express, index, index + 1)
    #             self.remove(contrastExpress, index, index + 1)
    #         elif express[index].word == 'not':
    #             if index >= len(express) - 1:
    #                 return 1, 0
    #             elif index == 0:
    #                 if express[index + 1].tokenValue == 34:
    #                     k = self.getValueIndex(express[index + 1].word)
    #                     express[index + 1].word = self.variate[k].value
    #
    #                 if express[index + 1].word == 'False':
    #                     express[index].word = 'True'
    #                 else:
    #                     express[index].word = 'False'
    #
    #                 formula = quaternion()
    #                 formula.no = self.index
    #                 formula.op = "@"
    #                 formula.args1 = str(contrastExpress[index + 1].word)
    #                 self.tempName.no += 1
    #                 formula.result = self.tempName.word + str(self.tempName.no)
    #                 self.structure.append(formula)
    #                 self.index += 1
    #                 contrastExpress[index].word = self.tempName.word + str(self.tempName.no)
    #
    #                 self.remove(express, index + 1, index + 1)
    #                 self.remove(contrastExpress, index + 1, index + 1)
    #                 express[index].tokenValue = 38
    #                 contrastExpress[index].tokenValue = 38
    #
    #         elif (express[index].tokenValue == 38) | (express[index].tokenValue == 34) | (
    #                     express[index].tokenValue == 35) | (express[index].word == '>') | (
    #                     express[index].word == '<') | (express[index].word == '=='):
    #             index += 1
    #         else:
    #             return 1, 0

    def handle_if(self, tokenTable, start):
        """
        处理if语句
        :param tokenTable:
        :param start:
        :return:
        """
        index = start + 1
        line = tokenTable[index].line
        tempExpress = []
        temp1 = []
        while 1:
            if index >= len(tokenTable):
                return index
            elif tokenTable[index].word == ';':
                return index + 1
            elif (tokenTable[index].word == 'then') | (tokenTable[index].line != line):
                break
            element = token()
            element.word = tokenTable[index].word
            element.wordtype = tokenTable[index].wordtype
            element.tokenValue = tokenTable[index].tokenValue
            element.line = tokenTable[index].line
            temp1.append(element)
            tempExpress.append(tokenTable[index])
            index += 1
        if tokenTable[index].word != 'then':
            return index
        else:
            beg = len(self.structure) - 1
            if len(tempExpress) == 1:
                formula = quaternion()
                formula.no = self.index
                formula.op = 'jnz'
                formula.args1 = tempExpress[0].word
                formula.result = '#'
                self.structure.append(formula)
                self.index += 1

                formula = quaternion()
                formula.no = self.index
                formula.op = 'j'
                formula.result = '-1'
                self.structure.append(formula)
                self.index += 1

            else:
                swi = self.judgeSort(tempExpress)
                if swi == 1:
                    value = self.simpyBool(tempExpress, temp1, 0, 0)
                else:
                    self.boolExpress(tempExpress)
            self.replace(beg, 1)
            if tokenTable[index + 1].word == 'begin':
                tempIndex = index + 2
                while 1:
                    if tempIndex >= len(tokenTable):
                        return tempIndex

                    elif tokenTable[tempIndex].word == 'end':
                        tempIndex += 1
                        break
                    elif tokenTable[tempIndex].word == 'if':
                        tempIndex = self.handle_if(tokenTable, tempIndex)
                    elif tokenTable[tempIndex].word == 'repeat':
                        tempIndex = self.handle_repeat(tokenTable, tempIndex)
                    elif tokenTable[tempIndex].word == 'for':
                        tempIndex = self.handle_for(tokenTable, tempIndex)
                    elif tokenTable[tempIndex].word == 'while':
                        tempIndex = self.handle_while(tokenTable, tempIndex)
                    else:
                        tempIndex = self.handle_evaluation(tokenTable, tempIndex)
                index = tempIndex + 1

            else:
                index = self.handle_evaluation(tokenTable, index + 1)

            formula = quaternion()
            formula.no = self.index
            formula.op = 'j'
            formula.result = '$'
            self.structure.append(formula)
            self.index += 1

            if tokenTable[index].word != 'else':
                self.replace(beg, 0)
                self.replace(beg, 2)
                return index
            elif tokenTable[index].word == 'else':
                self.replace(beg, 0)
                if index > len(tokenTable) - 1:
                    return index
                elif tokenTable[index + 1].word == 'begin':
                    tempIndex = index + 2
                    while 1:
                        if tempIndex >= len(tokenTable):
                            return tempIndex

                        elif tokenTable[tempIndex].word == 'end':
                            tempIndex += 1
                            break
                        elif tokenTable[tempIndex].word == 'if':
                            tempIndex = self.handle_if(tokenTable, tempIndex)
                        elif tokenTable[tempIndex].word == 'repeat':
                            tempIndex = self.handle_repeat(tokenTable, tempIndex)
                        elif tokenTable[tempIndex].word == 'for':
                            tempIndex = self.handle_for(tokenTable, tempIndex)
                        elif tokenTable[tempIndex].word == 'while':
                            tempIndex = self.handle_while(tokenTable, tempIndex)
                        else:
                            tempIndex = self.handle_evaluation(tokenTable, tempIndex)
                    index = tempIndex + 1

                else:
                    tempList = []
                    index = self.handle_evaluation(tokenTable, index + 1)
                    self.variateList = []
                self.replace(beg, 2)
        return index

    def handle_repeat(self, tokenTable, start):
        """
        处理repeat
        :param tokenTable:
        :param start:
        :return:
        """
        index = start + 1
        line = tokenTable[index].line
        start = self.index
        if tokenTable[index + 1].word == 'begin':
            tempIndex = index + 2
            while 1:
                if tempIndex >= len(tokenTable):
                    return tempIndex

                elif tokenTable[tempIndex].word == 'end':
                    tempIndex += 1
                    break
                elif tokenTable[tempIndex].word == 'if':
                    tempIndex = self.handle_if(tokenTable, tempIndex)
                elif tokenTable[tempIndex].word == 'repeat':
                    tempIndex = self.handle_repeat(tokenTable, tempIndex)
                elif tokenTable[tempIndex].word == 'for':
                    tempIndex = self.c(tokenTable, tempIndex)
                elif tokenTable[tempIndex].word == 'while':
                    tempIndex = self.handle_while(tokenTable, tempIndex)
                else:
                    tempIndex = self.handle_evaluation(tokenTable, tempIndex)
            index = tempIndex + 1

        else:
            index = self.handle_evaluation(tokenTable, index)
        tempExpress = []
        temp1 = []
        index += 1
        while 1:
            if tokenTable[index].word == ';':
                break
            tempExpress.append(tokenTable[index])
            temp1.append(tokenTable[index])
            index += 1
        beg = self.index - 1
        swi = self.judgeSort(tempExpress)
        if swi == 1:
            value = self.simpyBool(tempExpress, temp1, 0, 0)
        else:
            self.boolExpress(tempExpress)
        self.wanreplace(beg, 0, start)
        self.wanreplace(beg, 1, self.index)

        index += 1
        return index

    def handle_for(self, tokenTable, start):
        """
        处理for语句
        :param tokenTable:
        :param start:
        :return:
        """
        index = start + 1
        de = index
        index += 3
        tempExpress = []
        temp1 = []
        while 1:
            if tokenTable[index].word == 'to':
                break
            tempExpress.append(tokenTable[index])
            temp1.append(tokenTable[index])
            index += 1
        self.calExpressInt(tempExpress, temp1, 0, 0)

        formula = quaternion()
        formula.no = self.index
        self.index += 1
        beg = self.index
        formula.op = ':='
        formula.args1 = self.tempName.word + str(self.tempName.no)
        self.tempName.no += 1
        formula.result = tokenTable[de].word
        self.structure.append(formula)

        index += 1
        formula = quaternion()
        formula.no = self.index
        self.index += 1
        formula.op = ':='
        formula.args1 = tokenTable[index].word
        formula.result = self.tempName.word + str(self.tempName.no)
        self.structure.append(formula)

        formula = quaternion()
        formula.no = self.index
        self.index += 1
        formula.op = 'j<'
        formula.args2 = self.tempName.word + str(self.tempName.no)
        self.tempName.no += 1
        formula.args1 = tokenTable[de].word
        formula.result = str(self.index + 1)
        self.structure.append(formula)

        formula = quaternion()
        formula.no = self.index
        self.index += 1
        formula.op = 'j'
        formula.result = '-1'
        self.structure.append(formula)

        index += 1

        if tokenTable[index + 1].word == 'begin':
            tempIndex = index + 2
            while 1:
                if tempIndex >= len(tokenTable):
                    return tempIndex

                elif tokenTable[tempIndex].word == 'end':
                    tempIndex += 1
                    break
                elif tokenTable[tempIndex].word == 'if':
                    tempIndex = self.handle_if(tokenTable, tempIndex)
                elif tokenTable[tempIndex].word == 'repeat':
                    tempIndex = self.handle_repeat(tokenTable, tempIndex)
                elif tokenTable[tempIndex].word == 'for':
                    tempIndex = self.c(tokenTable, tempIndex)
                elif tokenTable[tempIndex].word == 'while':
                    tempIndex = self.handle_while(tokenTable, tempIndex)
                else:
                    tempIndex = self.handle_evaluation(tokenTable, tempIndex)
            index = tempIndex + 1

        else:
            index = self.handle_evaluation(tokenTable, index + 1)

        formula = quaternion()
        formula.no = self.index
        self.index += 1
        formula.op = 'j'
        formula.result = str(beg)
        self.structure.append(formula)

        self.wanreplace(beg, 0, self.index)
        return index

    def handle_while(self, tokenTable, start):
        """
        处理while语句
        :param tokenTable:
        :param start:
        :return:
        """
        index = start + 1
        tempExpress = []
        temp1 = []
        beg = self.index
        while 1:
            if tokenTable[index].word == 'do':
                break
            tempExpress.append(tokenTable[index])
            temp1.append(tokenTable[index])
            index += 1
        swi = self.judgeSort(tempExpress)
        if swi == 1:
            value = self.simpyBool(tempExpress, temp1, 0, 0)
        else:
            self.boolExpress(tempExpress)
        self.wanreplace(beg, 1, self.index)

        if tokenTable[index + 1].word == 'begin':
            tempIndex = index + 2
            while 1:
                if tempIndex >= len(tokenTable):
                    return tempIndex

                elif tokenTable[tempIndex].word == 'end':
                    tempIndex += 1
                    break
                elif tokenTable[tempIndex].word == 'if':
                    tempIndex = self.handle_if(tokenTable, tempIndex)
                elif tokenTable[tempIndex].word == 'repeat':
                    tempIndex = self.handle_repeat(tokenTable, tempIndex)
                elif tokenTable[tempIndex].word == 'for':
                    tempIndex = self.c(tokenTable, tempIndex)
                elif tokenTable[tempIndex].word == 'while':
                    tempIndex = self.handle_while(tokenTable, tempIndex)
                else:
                    tempIndex = self.handle_evaluation(tokenTable, tempIndex)
            index = tempIndex + 1

        else:
            index = self.handle_evaluation(tokenTable, index + 1)
        formula = quaternion()
        formula.no = self.index
        self.index += 1
        formula.op = 'j'
        formula.result = str(beg)
        self.structure.append(formula)

        self.wanreplace(beg, 0, self.index)

        return index

    def wanreplace(self, beg, flag, value):
        """
        完成四元式回读
        :param beg:
        :param falg:
        :param value:
        :return:
        """
        index = 0
        while 1:
            if index == beg:
                break
            elif index >= len(self.structure):
                break
            index += 1
        index += 1
        if flag == 1:
            while 1:
                if index >= len(self.structure):
                    break
                elif self.structure[index].result == '#':
                    self.structure[index].result = str(value)
                index += 1
        elif flag == 0:
            while 1:
                if index >= len(self.structure):
                    break
                elif self.structure[index].result == '-1':
                    self.structure[index].result = str(value)
                index += 1
        else:
            while 1:
                if index >= len(self.structure):
                    break
                elif self.structure[index].result == '$':
                    self.structure[index].result = str(value)
                index += 1

    def replace(self, beg, flag):
        """
        四元式回读
        :param beg:
        :param flag:
        :return:
        """
        index = 0
        while 1:
            if index == beg:
                break
            elif index >= len(self.structure):
                break
            index += 1
        index += 1
        if flag == 1:
            while 1:
                if index >= len(self.structure):
                    break
                elif self.structure[index].result == '#':
                    self.structure[index].result = str(self.index)
                index += 1
        elif flag == 0:
            while 1:
                if index >= len(self.structure):
                    break
                elif self.structure[index].result == '-1':
                    self.structure[index].result = str(self.index)
                index += 1
        else:
            while 1:
                if index >= len(self.structure):
                    break
                elif self.structure[index].result == '$':
                    self.structure[index].result = str(self.index)
                index += 1
