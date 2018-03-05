from analyze.lexicalAnalyze import token


class error:
    """
    错误信息
    """

    def __init__(self):
        self.word = ''  # 错误名称
        self.line = 0  # 错误位置
        self.errorType = ''  # 错误类型


class sign:
    """
    符号信息
    """

    def __init__(self):
        self.word = ''  # 符号名称
        self.value = ''  # 符号值
        self.signType = ''  # 符号类型


class gramma:
    def __init__(self):
        self.errorList = []  # 错误列表
        self.constantList = []  # 常量列表
        self.variateList = []  # 变量列表
        self.structure = []  # 程序结构

    def grammaDeal(self, tokenTable):
        """
        语法总控程序
        :param tokenTable:
        :return:
        """
        try:
            flag = 0
            i = 0
            if i >= len(tokenTable):
                flag = 1
            elif tokenTable[i].word != 'program':
                temp = error()
                temp.word = 'program'
                temp.line = 1
                temp.errorType = 'lack'
                self.errorList.append(temp)
            else:
                i += 1
            if flag == 0:
                if i >= len(tokenTable):
                    temp = error()
                    temp.word = 'identifier'
                    temp.line = 1
                    temp.errorType = 'lack'
                    self.errorList.append(temp)
                    flag = 1
                elif (i < len(tokenTable)) & (tokenTable[i].wordtype != 'identifier'):
                    temp = error()
                    temp.word = 'identifier'
                    temp.line = tokenTable[i].line
                    temp.errorType = 'lack'
                    self.errorList.append(temp)
                else:
                    i += 1
                if flag == 0:
                    if i >= len(tokenTable):
                        temp = error()
                        temp.word = ';'
                        temp.errorType = 'lack'
                        temp.line = tokenTable[i - 1].line
                        self.errorList.append(temp)
                    elif (i < len(tokenTable)) & (tokenTable[i].word != ';'):
                        temp = error()
                        temp.word = ';'
                        temp.line = tokenTable[i].line
                        temp.errorType = 'lack'
                        self.errorList.append(temp)
                    else:
                        self.structure.append("---" + tokenTable[i - 2].word + " " + tokenTable[i - 1].word)
                        i += 1
                    while 1:
                        if i >= len(tokenTable):
                            break
                        elif tokenTable[i].word == 'begin':
                            break
                        elif tokenTable[i].word == 'const':
                            i = self.handle_constant(tokenTable, i + 1)
                            self.structure.append("     ---const")
                        elif tokenTable[i].word == 'var':
                            i = self.handle_variate(tokenTable, i + 1)
                            self.structure.append("     ---var")
                        else:
                            temp = error()
                            line = tokenTable[i].line
                            temp.line = line
                            temp.errorType = 'Unknown'
                            while 1:
                                if i >= len(tokenTable):
                                    self.errorList.append(temp)
                                    break
                                elif (tokenTable[i].word == 'const') | (tokenTable[i].word == 'var') | (
                                            tokenTable[i].word == 'begin'):
                                    self.errorList.append(temp)
                                    break
                                else:
                                    temp.word += tokenTable[i].word + ' '
                                i += 1
                    if i < len(tokenTable):
                        self.structure.append("     ---begin")
                        i = self.handle_mainfunction(tokenTable, i + 1, self.structure)
                        if i < len(tokenTable):
                            temp = error()
                            temp.line = tokenTable[i].line
                            temp.errorType = 'Illegal operation'
                            while 1:
                                if i >= len(tokenTable):
                                    break
                                else:
                                    temp.word += tokenTable[i].word + ' '
                                i += 1
                            self.errorList.append(temp)
        except Exception as e:
            print(e)

    def handle_constant(self, tokenTable, start):
        """
        处理常数定义
        :param tokenTable:
        :param start:
        :return:
        """
        flag = 1
        while 1:
            if start >= len(tokenTable):
                if tokenTable[start - 1].word == 'const':
                    temp = error()
                    temp.word = 'constant' + '\t' + 'identifier'
                    temp.line = tokenTable[start - 1].line
                    temp.errorType = 'lack'
                    self.errorList.append(temp)
                return start
            elif (tokenTable[start].word == 'var') | (tokenTable[start].word == 'begin'):
                return start
            else:
                start = self.handle_evaluation(tokenTable, start, flag)

    def handle_evaluation(self, tokenTable, start, flag):
        """
        处理赋值语句
        :param tokenTable:
        :param start:
        :param flag:
        :return:
        """
        line = tokenTable[start].line
        if (flag == 0) & (self.match(self.constantList, tokenTable[start].word) != -1):
            temp = error()
            temp.word = 'constant'
            temp.line = line
            temp.errorType = 'Illegal operation'
            self.errorList.append(temp)
            while 1:
                if start >= len(tokenTable):
                    return start
                elif tokenTable[start].word == ';':
                    return start + 1
                elif tokenTable[start].line != line:
                    return start
                start += 1

        elif (flag == 1) & ((self.match(self.constantList, tokenTable[start].word) != -1) | (
                    self.match(self.variateList, tokenTable[start].word) != -1)):
            temp = error()
            temp.word = 'constant'
            temp.line = line
            temp.errorType = 'Illegal operation'
            self.errorList.append(temp)
            while 1:
                if start >= len(tokenTable):
                    return start
                elif tokenTable[start].word == ';':
                    return start + 1
                elif tokenTable[start].line != line:
                    return start
                start += 1

        elif tokenTable[start].wordtype != 'identifier':
            temp = error()
            while 1:
                if start >= len(tokenTable):
                    return start

                elif tokenTable[start].word == ';':
                    temp.word += '\tidentifier'
                    temp.line = line
                    temp.errorType = 'lack'
                    self.errorList.append(temp)
                    return start + 1

                elif tokenTable[start].line != line:
                    temp.word += '\tidentifier'
                    temp.line = line
                    temp.errorType = 'lack'
                    self.errorList.append(temp)
                    return start

                temp.word += tokenTable[start].word + ' '
                start += 1
        else:
            if (flag == 0) & (self.match(self.variateList, tokenTable[start].word) == -1):
                temp = error()
                temp.word += tokenTable[start].word
                temp.line = line
                temp.errorType = 'No defined '
                self.errorList.append(temp)
                while 1:
                    if start >= len(tokenTable):
                        return start
                    elif tokenTable[start].word == ';':
                        return start + 1
                    elif tokenTable[start].line != line:
                        return start
                    start += 1
            data = sign()
            data.word = tokenTable[start].word
            start += 1

            if start >= len(tokenTable):
                temp = error()
                temp.word = ':'
                temp.line = line
                temp.errorType = 'lack'
                self.errorList.append(temp)
                return start

            elif (tokenTable[start].line != line) | (tokenTable[start].word != ':'):
                temp = error()
                while 1:
                    if start >= len(tokenTable):
                        return start

                    elif tokenTable[start].word == ';':
                        temp.word += '\t\":\"'
                        temp.line = line
                        temp.errorType = 'lack'
                        self.errorList.append(temp)
                        return start + 1

                    elif tokenTable[start].line != line:
                        temp.word += '\t\":\"'
                        temp.line = line
                        temp.errorType = 'lack'
                        self.errorList.append(temp)
                        return start

                    temp.word += tokenTable[start].word + ' '
                    start += 1
            else:
                start += 1
                if start >= len(tokenTable):
                    temp = error()
                    temp.word = '='
                    temp.line = line
                    temp.errorType = 'lack'
                    self.errorList.append(temp)
                    return start

                elif (tokenTable[start].line != line) | (tokenTable[start].word != '='):
                    temp = error()
                    while 1:
                        if start >= len(tokenTable):
                            return start + 1

                        elif tokenTable[start].word == ';':
                            temp.word += '\t\"=\"'
                            temp.line = line
                            temp.errorType = 'lack'
                            self.errorList.append(temp)
                            return start + 1

                        elif tokenTable[start].line != line:
                            temp.word += '\t\"=\"'
                            temp.line = line
                            temp.errorType = 'lack'
                            self.errorList.append(temp)
                            return start

                        temp.word += tokenTable[start].word + ' '
                        start += 1
                else:
                    start += 1
                    if flag == 1:
                        if start >= len(tokenTable):
                            temp = error()
                            temp.word = 'constant'
                            temp.line = line
                            temp.errorType = 'lack'
                            self.errorList.append(temp)
                            return start
                        elif tokenTable[start].word == '\'':
                            start += 1
                            if start >= len(tokenTable):
                                temp = error()
                                while 1:
                                    if start >= len(tokenTable):
                                        return start

                                    elif tokenTable[start].word == ';':
                                        temp.word += '\tconstant'
                                        temp.line = line
                                        temp.errorType = 'lack'
                                        self.errorList.append(temp)
                                        return start + 1

                                    elif tokenTable[start].line != line:
                                        temp.word += '\tconstant'
                                        temp.line = line
                                        temp.errorType = 'lack'
                                        self.errorList.append(temp)
                                        return start

                                    temp.word += tokenTable[start].word + ' '
                                    start += 1

                        if (tokenTable[start].line != line) | (tokenTable[start].wordtype != 'const'):
                            temp = error()
                            while 1:
                                if start >= len(tokenTable):
                                    return start

                                elif tokenTable[start].word == ';':
                                    temp.word += '\tconstant'
                                    temp.line = line
                                    temp.errorType = 'lack'
                                    self.errorList.append(temp)
                                    return start + 1

                                elif tokenTable[start].line != line:
                                    temp.word += '\tconstant'
                                    temp.line = line
                                    temp.errorType = 'lack'
                                    self.errorList.append(temp)
                                    return start

                                temp.word += tokenTable[start].word + ' '
                                start += 1
                        else:
                            data.value = tokenTable[start].word
                            if tokenTable[start].tokenValue == 35:
                                if tokenTable[start - 1] == '\'':
                                    temp = error()
                                    while 1:
                                        if start >= len(tokenTable):
                                            return start

                                        elif tokenTable[start].word == ';':
                                            temp.word += '\tconstant'
                                            temp.line = line
                                            temp.errorType = 'lack'
                                            self.errorList.append(temp)
                                            return start + 1

                                        elif tokenTable[start].line != line:
                                            temp.word += '\tconstant'
                                            temp.line = line
                                            temp.errorType = 'lack'
                                            self.errorList.append(temp)
                                            return start

                                    temp.word += tokenTable[start].word + ' '
                                    start += 1
                                else:
                                    data.signType = 'integer'
                            elif tokenTable[start].tokenValue == 36:
                                if tokenTable[start - 1] == '\'':
                                    temp = error()
                                    while 1:
                                        if start >= len(tokenTable):
                                            return start

                                        elif tokenTable[start].word == ';':
                                            temp.word += '\tconstant'
                                            temp.line = line
                                            temp.errorType = 'lack'
                                            self.errorList.append(temp)
                                            return start + 1

                                        elif tokenTable[start].line != line:
                                            temp.word += '\tconstant'
                                            temp.line = line
                                            temp.errorType = 'lack'
                                            self.errorList.append(temp)
                                            return start

                                    temp.word += tokenTable[start].word + ' '
                                    start += 1
                                else:
                                    data.signType = 'real'

                            elif tokenTable[start].tokenValue == 37:
                                data.signType = 'char'
                                start += 1
                            elif tokenTable[start].tokenValue == 38:
                                if tokenTable[start - 1] == '\'':
                                    temp = error()
                                    while 1:
                                        if start >= len(tokenTable):
                                            return start

                                        elif tokenTable[start].word == ';':
                                            temp.word += '\tconstant'
                                            temp.line = line
                                            temp.errorType = 'lack'
                                            self.errorList.append(temp)
                                            return start + 1

                                        elif tokenTable[start].line != line:
                                            temp.word += '\tconstant'
                                            temp.line = line
                                            temp.errorType = 'lack'
                                            self.errorList.append(temp)
                                            return start

                                    temp.word += tokenTable[start].word + ' '
                                    start += 1
                                else:
                                    data.signType = 'bool'

                            start += 1
                            if start >= len(tokenTable):
                                temp = error()
                                temp.word = ';'
                                temp.line = line
                                temp.errorType = 'lack'
                                self.errorList.append(temp)
                                return start
                            elif tokenTable[start].word != ';':
                                temp = error()
                                while 1:
                                    if start >= len(tokenTable):
                                        return start

                                    elif tokenTable[start].word == ';':
                                        temp.word += '\t";"'
                                        temp.line = line
                                        temp.errorType = 'lack'
                                        self.errorList.append(temp)
                                        return start + 1

                                    elif tokenTable[start].line != line:
                                        temp.word += '\t";"'
                                        temp.line = line
                                        temp.errorType = 'lack'
                                        self.errorList.append(temp)
                                        return start

                                    temp.word += tokenTable[start].word + ' '
                                    start += 1
                            else:
                                self.constantList.append(data)
                                return start + 1

                    elif flag == 0:
                        if start >= len(tokenTable):
                            temp = error()
                            temp.word = 'value'
                            temp.line = line
                            temp.errorType = 'lack'
                            self.errorList.append(temp)
                            return start
                        elif tokenTable[start].word == '\'':
                            start += 1
                            if start >= len(tokenTable):
                                temp = error()
                                while 1:
                                    if start >= len(tokenTable):
                                        return start

                                    elif tokenTable[start].word == ';':
                                        temp.word += '\tvalue'
                                        temp.line = line
                                        temp.errorType = 'lack'
                                        self.errorList.append(temp)
                                        return start + 1

                                    elif tokenTable[start].line != line:
                                        temp.word += '\tvalue'
                                        temp.line = line
                                        temp.errorType = 'lack'
                                        self.errorList.append(temp)
                                        return start

                                    temp.word += tokenTable[start].word + ' '
                                    start += 1
                            elif tokenTable[start].line != line:
                                temp = error()
                                temp.word += '\tvalue'
                                temp.line = line
                                temp.errorType = 'lack'
                                self.errorList.append(temp)
                                return start
                            elif tokenTable[start].tokenValue != 37:
                                temp = error()
                                while 1:
                                    if start >= len(tokenTable):
                                        return start

                                    elif tokenTable[start].word == ';':
                                        temp.word += '\tvalue'
                                        temp.line = line
                                        temp.errorType = 'lack'
                                        self.errorList.append(temp)
                                        return start + 1

                                    elif tokenTable[start].line != line:
                                        temp.word += '\tvalue'
                                        temp.line = line
                                        temp.errorType = 'lack'
                                        self.errorList.append(temp)
                                        return start

                                    temp.word += tokenTable[start].word + ' '
                                    start += 1
                            else:
                                if self.getVar(data.word) != 'char':
                                    temp = error()
                                    temp.line = line
                                    temp.word = data.word
                                    temp.errorType = 'is ' + self.getVar(data.word)
                                    self.errorList.append(temp)
                                    while 1:
                                        if start >= len(tokenTable):
                                            return start
                                        elif tokenTable[start].line != line:
                                            return start
                                        elif tokenTable[start].word == ';':
                                            return start + 1
                                        start += 1
                                else:
                                    data.value = tokenTable[start].word
                                    start += 2
                                    if start >= len(tokenTable):
                                        temp = error()
                                        temp.word = ';'
                                        temp.line = line
                                        temp.errorType = 'lack'
                                        self.errorList.append(temp)
                                        return start
                                    elif tokenTable[start].word != ';':
                                        temp = error()
                                        while 1:
                                            if start >= len(tokenTable):
                                                return start

                                            elif tokenTable[start].word == ';':
                                                temp.word += '\t";"'
                                                temp.line = line
                                                temp.errorType = 'lack'
                                                self.errorList.append(temp)
                                                return start + 1

                                            elif tokenTable[start].line != line:
                                                temp.word += '\t";"'
                                                temp.line = line
                                                temp.errorType = 'lack'
                                                self.errorList.append(temp)
                                                return start

                                            temp.word += tokenTable[start].word + ' '
                                            start += 1
                                    else:
                                        index = self.match(self.variateList, data.word)
                                        self.variateList[index].signType = 'char'
                                        self.variateList[index].value = data.value
                                        return start + 1

                        elif tokenTable[start].line != line:
                            temp = error()
                            temp.word = "express"
                            temp.line = line
                            temp.errorType = 'lack'
                            self.errorList(temp)
                            return start

                        # elif tokenTable[start].wordtype == 'const':
                        # elif tokenTable[start].wordtype == ''
                        else:
                            if tokenTable[start].tokenValue == 38:
                                if self.getVar(data.word) != 'bool':
                                    temp = error()
                                    temp.line = line
                                    temp.word = data.word
                                    temp.errorType = 'is ' + self.getVar(data.word)
                                    self.errorList.append(temp)
                                    while 1:
                                        if start >= len(tokenTable):
                                            return start
                                        elif tokenTable[start].line != line:
                                            return start
                                        elif tokenTable[start].word == ';':
                                            return start + 1
                                        start += 1
                                else:
                                    data.value = tokenTable[start].word
                                    start += 1
                                    if start >= len(tokenTable):
                                        temp = error()
                                        temp.word = ';'
                                        temp.line = line
                                        temp.errorType = 'lack'
                                        self.errorList.append(temp)
                                        return start
                                    elif tokenTable[start].word != ';':
                                        temp = error()
                                        while 1:
                                            if start >= len(tokenTable):
                                                return start

                                            elif tokenTable[start].word == ';':
                                                temp.word += '\t";"'
                                                temp.line = line
                                                temp.errorType = 'lack'
                                                self.errorList.append(temp)
                                                return start + 1

                                            elif tokenTable[start].line != line:
                                                temp.word += '\t";"'
                                                temp.line = line
                                                temp.errorType = 'lack'
                                                self.errorList.append(temp)
                                                return start

                                            temp.word += tokenTable[start].word + ' '
                                            start += 1
                                    else:
                                        index = self.match(self.variateList, data.word)
                                        self.variateList[index].signType = 'bool'
                                        self.variateList[index].value = data.value
                                        return start + 1

                            elif tokenTable[start].tokenValue == 34:
                                tempExpress = []
                                while 1:
                                    if start >= len(tokenTable):
                                        temp = error()
                                        temp.line = line
                                        temp.word = ';'
                                        temp.errorType = 'lack'
                                        self.errorList.append(temp)
                                        return start

                                    elif tokenTable[start].line != line:
                                        temp = error()
                                        temp.line = line
                                        temp.word = ';'
                                        temp.errorType = 'lack'
                                        self.errorList.append(temp)
                                        return start

                                    elif tokenTable[start].word == ';':
                                        start += 1
                                        break
                                    tempExpress.append(tokenTable[start])
                                    start += 1
                                tempExpress = self.replace(tempExpress)
                                if len(tempExpress) == 0:
                                    return start
                                if self.isFloat(tempExpress, 0) == 1:
                                    if self.getVar(data.word) != 'real':
                                        temp = error()
                                        temp.line = line
                                        temp.word = data.word
                                        temp.errorType = 'is ' + self.getVar(data.word)
                                        self.errorList.append(temp)
                                    else:
                                        flag, value = self.calExpressFloat(tempExpress, 0, 0)
                                        if flag == 0:
                                            index = self.match(self.variateList, data.word)
                                            self.variateList[index].signType = 'real'
                                            self.variateList[index].value = str(value)
                                            return start
                                        else:
                                            temp = error()
                                            temp.word = 'express'
                                            temp.line = line
                                            temp.errorType = 'error'
                                            self.errorList.append(temp)
                                            return start
                                elif tempExpress[0].tokenValue == 35:
                                    if self.getVar(data.word) != 'integer':
                                        temp = error()
                                        temp.line = line
                                        temp.word = data.word
                                        temp.errorType = 'is ' + self.getVar(data.word)
                                        self.errorList.append(temp)
                                    else:
                                        flag, value = self.calExpressInt(tempExpress, 0, 0)
                                        if flag == 0:
                                            index = self.match(self.variateList, data.word)
                                            self.variateList[index].signType = 'integer'
                                            self.variateList[index].value = str(value)
                                            return start
                                        else:
                                            temp = error()
                                            temp.word = 'express'
                                            temp.line = line
                                            temp.errorType = 'error'
                                            self.errorList.append(temp)
                                            return start
                                else:
                                    temp = error()
                                    temp.word += '\tvalue'
                                    temp.line = line
                                    temp.errorType = 'lack'
                                    self.errorList.append(temp)





                            elif self.isFloat(tokenTable, start) == 1:
                                if self.getVar(data.word) != 'real':
                                    temp = error()
                                    temp.line = line
                                    temp.word = data.word
                                    temp.errorType = 'is ' + self.getVar(data.word)
                                    self.errorList.append(temp)
                                    while 1:
                                        if start >= len(tokenTable):
                                            return start
                                        elif tokenTable[start].line != line:
                                            return start
                                        elif tokenTable[start].word == ';':
                                            return start + 1
                                        start += 1
                                else:
                                    tempExpress = []
                                    while 1:
                                        if start >= len(tokenTable):
                                            temp = error()
                                            temp.line = line
                                            temp.word = ';'
                                            temp.errorType = 'lack'
                                            self.errorList.append(temp)
                                            return start

                                        elif tokenTable[start].line != line:
                                            temp = error()
                                            temp.line = line
                                            temp.word = ';'
                                            temp.errorType = 'lack'
                                            self.errorList.append(temp)
                                            return start

                                        elif tokenTable[start].word == ';':
                                            start += 1
                                            break
                                        tempExpress.append(tokenTable[start])
                                        start += 1
                                    tempExpress = self.replace(tempExpress)
                                    if len(tempExpress) == 0:
                                        return start
                                    else:
                                        flag, value = self.calExpressFloat(tempExpress, 0, 0)
                                        if flag == 0:
                                            index = self.match(self.variateList, data.word)
                                            self.variateList[index].signType = 'real'
                                            self.variateList[index].value = str(value)
                                            return start
                                        else:
                                            temp = error()
                                            temp.word = 'express'
                                            temp.line = line
                                            temp.errorType = 'error'
                                            self.errorList.append(temp)
                                            return start

                            elif tokenTable[start].tokenValue == 35:
                                if self.getVar(data.word) != 'integer':
                                    temp = error()
                                    temp.line = line
                                    temp.word = data.word
                                    temp.errorType = 'is ' + self.getVar(data.word)
                                    self.errorList.append(temp)
                                    while 1:
                                        if start >= len(tokenTable):
                                            return start
                                        elif tokenTable[start].line != line:
                                            return start
                                        elif tokenTable[start].word == ';':
                                            return start + 1
                                        start += 1
                                else:
                                    tempExpress = []
                                    while 1:
                                        if start >= len(tokenTable):
                                            temp = error()
                                            temp.line = line
                                            temp.word = ';'
                                            temp.errorType = 'lack'
                                            self.errorList.append(temp)
                                            return start

                                        elif tokenTable[start].line != line:
                                            temp = error()
                                            temp.line = line
                                            temp.word = ';'
                                            temp.errorType = 'lack'
                                            self.errorList.append(temp)
                                            return start

                                        elif tokenTable[start].word == ';':
                                            start += 1
                                            break
                                        tempExpress.append(tokenTable[start])
                                        start += 1
                                    tempExpress = self.replace(tempExpress)
                                    if len(tempExpress) == 0:
                                        return start
                                    else:
                                        flag, value = self.calExpressInt(tempExpress, 0, 0)
                                        if flag == 0:
                                            index = self.match(self.variateList, data.word)
                                            self.variateList[index].signType = 'integer'
                                            self.variateList[index].value = str(value)
                                            return start
                                        else:
                                            temp = error()
                                            temp.word = 'express'
                                            temp.line = line
                                            temp.errorType = 'error'
                                            self.errorList.append(temp)
                                            return start

                            elif tokenTable[start].word == "(":
                                if start >= len(tokenTable) - 1:
                                    temp = error()
                                    while 1:
                                        if start >= len(tokenTable):
                                            return start

                                        elif tokenTable[start].word == ';':
                                            temp.word += '\tvalue'
                                            temp.line = line
                                            temp.errorType = 'lack'
                                            self.errorList.append(temp)
                                            return start + 1

                                        elif tokenTable[start].line != line:
                                            temp.word += '\tvalue'
                                            temp.line = line
                                            temp.errorType = 'lack'
                                            self.errorList.append(temp)
                                            return start

                                        temp.word += tokenTable[start].word + ' '
                                        start += 1

                                elif self.isFloat(tokenTable, start) == 1:
                                    if self.getVar(data.word) != 'real':
                                        temp = error()
                                        temp.line = line
                                        temp.word = data.word
                                        temp.errorType = 'is ' + self.getVar(data.word)
                                        self.errorList.append(temp)
                                        while 1:
                                            if start >= len(tokenTable):
                                                return start
                                            elif tokenTable[start].line != line:
                                                return start
                                            elif tokenTable[start].word == ';':
                                                return start + 1
                                            start += 1
                                    else:
                                        tempExpress = []
                                        while 1:
                                            if start >= len(tokenTable):
                                                temp = error()
                                                temp.line = line
                                                temp.word = ';'
                                                temp.errorType = 'lack'
                                                self.errorList.append(temp)
                                                return start

                                            elif tokenTable[start].line != line:
                                                temp = error()
                                                temp.line = line
                                                temp.word = ';'
                                                temp.errorType = 'lack'
                                                self.errorList.append(temp)
                                                return start

                                            elif tokenTable[start].word == ';':
                                                start += 1
                                                break
                                            tempExpress.append(tokenTable[start])
                                            start += 1
                                        tempExpress = self.replace(tempExpress)
                                        if len(tempExpress) == 0:
                                            return start
                                        else:
                                            flag, value = self.calExpressFloat(tempExpress, 0, 0)
                                            if flag == 0:
                                                index = self.match(self.variateList, data.word)
                                                self.variateList[index].signType = 'real'
                                                self.variateList[index].value = str(value)
                                                return start
                                            else:
                                                temp = error()
                                                temp.word = 'express'
                                                temp.line = line
                                                temp.errorType = 'error'
                                                self.errorList.append(temp)
                                                return start

                                elif tokenTable[start + 1].tokenValue == 35:
                                    if self.getVar(data.word) != 'integer':
                                        temp = error()
                                        temp.line = line
                                        temp.word = data.word
                                        temp.errorType = 'is ' + self.getVar(data.word)
                                        self.errorList.append(temp)
                                        while 1:
                                            if start >= len(tokenTable):
                                                return start
                                            elif tokenTable[start].line != line:
                                                return start
                                            elif tokenTable[start].word == ';':
                                                return start + 1
                                            start += 1
                                    else:
                                        tempExpress = []
                                        while 1:
                                            if start >= len(tokenTable):
                                                temp = error()
                                                temp.line = line
                                                temp.word = ';'
                                                temp.errorType = 'lack'
                                                self.errorList.append(temp)
                                                return start

                                            elif tokenTable[start].line != line:
                                                temp = error()
                                                temp.line = line
                                                temp.word = ';'
                                                temp.errorType = 'lack'
                                                self.errorList.append(temp)
                                                return start

                                            elif tokenTable[start].word == ';':
                                                start += 1
                                                break
                                            tempExpress.append(tokenTable[start])
                                            start += 1
                                        tempExpress = self.replace(tempExpress)
                                        if len(tempExpress) == 0:
                                            return start
                                        else:
                                            flag, value = self.calExpressInt(tempExpress, 0, 0)
                                            if flag == 0:
                                                index = self.match(self.variateList, data.word)
                                                self.variateList[index].signType = 'integer'
                                                self.variateList[index].value = str(value)
                                                return start
                                            else:
                                                temp = error()
                                                temp.word = 'express'
                                                temp.line = line
                                                temp.errorType = 'error'
                                                self.errorList.append(temp)
                                                return start



                            elif tokenTable[start].word == '-':
                                if start >= len(tokenTable) - 1:
                                    temp = error()
                                    while 1:
                                        if start >= len(tokenTable):
                                            return start

                                        elif tokenTable[start].word == ';':
                                            temp.word += '\tvalue'
                                            temp.line = line
                                            temp.errorType = 'lack'
                                            self.errorList.append(temp)
                                            return start + 1

                                        elif tokenTable[start].line != line:
                                            temp.word += '\tvalue'
                                            temp.line = line
                                            temp.errorType = 'lack'
                                            self.errorList.append(temp)
                                            return start

                                        temp.word += tokenTable[start].word + ' '
                                        start += 1

                                elif self.isFloat(tokenTable, start) == 1:
                                    if self.getVar(data.word) != 'real':
                                        temp = error()
                                        temp.line = line
                                        temp.word = data.word
                                        temp.errorType = 'is ' + self.getVar(data.word)
                                        self.errorList.append(temp)
                                        while 1:
                                            if start >= len(tokenTable):
                                                return start
                                            elif tokenTable[start].line != line:
                                                return start
                                            elif tokenTable[start].word == ';':
                                                return start + 1
                                            start += 1
                                    else:
                                        tempExpress = []
                                        while 1:
                                            if start >= len(tokenTable):
                                                temp = error()
                                                temp.line = line
                                                temp.word = ';'
                                                temp.errorType = 'lack'
                                                self.errorList.append(temp)
                                                return start

                                            elif tokenTable[start].line != line:
                                                temp = error()
                                                temp.line = line
                                                temp.word = ';'
                                                temp.errorType = 'lack'
                                                self.errorList.append(temp)
                                                return start

                                            elif tokenTable[start].word == ';':
                                                start += 1
                                                break
                                            tempExpress.append(tokenTable[start])
                                            start += 1
                                        tempExpress = self.replace(tempExpress)
                                        if len(tempExpress) == 0:
                                            return start
                                        else:
                                            flag, value = self.calExpressFloat(tempExpress, 0, 0)
                                            if flag == 0:
                                                index = self.match(self.variateList, data.word)
                                                self.variateList[index].signType = 'real'
                                                self.variateList[index].value = str(value)
                                                return start
                                            else:
                                                temp = error()
                                                temp.word = 'express'
                                                temp.line = line
                                                temp.errorType = 'error'
                                                self.errorList.append(temp)
                                                return start

                                elif tokenTable[start + 1].tokenValue == 35:
                                    if self.getVar(data.word) != 'integer':
                                        temp = error()
                                        temp.line = line
                                        temp.word = data.word
                                        temp.errorType = 'is ' + self.getVar(data.word)
                                        self.errorList.append(temp)
                                        while 1:
                                            if start >= len(tokenTable):
                                                return start
                                            elif tokenTable[start].line != line:
                                                return start
                                            elif tokenTable[start].word == ';':
                                                return start + 1
                                            start += 1
                                    else:
                                        tempExpress = []
                                        while 1:
                                            if start >= len(tokenTable):
                                                temp = error()
                                                temp.line = line
                                                temp.word = ';'
                                                temp.errorType = 'lack'
                                                self.errorList.append(temp)
                                                return start

                                            elif tokenTable[start].line != line:
                                                temp = error()
                                                temp.line = line
                                                temp.word = ';'
                                                temp.errorType = 'lack'
                                                self.errorList.append(temp)
                                                return start

                                            elif tokenTable[start].word == ';':
                                                start += 1
                                                break
                                            tempExpress.append(tokenTable[start])
                                            start += 1
                                        tempExpress = self.replace(tempExpress)
                                        if len(tempExpress) == 0:
                                            return start
                                        else:
                                            flag, value = self.calExpressInt(tempExpress, 0, 0)
                                            if flag == 0:
                                                index = self.match(self.variateList, data.word)
                                                self.variateList[index].signType = 'integer'
                                                self.variateList[index].value = str(value)
                                                return start
                                            else:
                                                temp = error()
                                                temp.word = 'express'
                                                temp.line = line
                                                temp.errorType = 'error'
                                                self.errorList.append(temp)
                                                return start





                            else:
                                temp = error()
                                while 1:
                                    if start >= len(tokenTable):
                                        return start

                                    elif tokenTable[start].word == ';':
                                        temp.word += '\tvalue'
                                        temp.line = line
                                        temp.errorType = 'lack'
                                        self.errorList.append(temp)
                                        return start + 1

                                    elif tokenTable[start].line != line:
                                        temp.word += '\tvalue'
                                        temp.line = line
                                        temp.errorType = 'lack'
                                        self.errorList.append(temp)
                                        return start

                                    temp.word += tokenTable[start].word + ' '
                                    start += 1

    def match(self, list, word):
        """
        判断存在
        :param list:
        :param word:
        :return:
        """
        i = 0
        flag = -1
        while 1:
            if i >= len(list):
                break
            elif word == list[i].word:
                flag = i
                break
            i += 1
        return flag

    def getVar(self, word):
        """
        获得定义的变量的类型
        :param word:
        :return:
        """
        for i in range(len(self.variateList)):
            if word == self.variateList[i].word:
                return self.variateList[i].signType
        for i in range(len(self.constantList)):
            if word == self.constantList[i].word:
                return self.constantList[i].signType
        return ''

    def getValue(self, word):
        """
        获得变量的值
        :param word:
        :return:
        """
        for i in range(len(self.variateList)):
            if word == self.variateList[i].word:
                return self.variateList[i].value
        for i in range(len(self.constantList)):
            if word == self.constantList[i].word:
                return self.constantList[i].value
        return ''

    def calExpressInt(self, express, index, flag):
        """
        判定算数表达式(整数)
        :param express:
        :return:
        """
        while 1:
            if len(express) == 1:
                return 0, int(express[0].word)
            elif flag == 1:
                return 1, 0
            elif express[index].word == '(':
                i = index + 1
                temp = []
                sum = 1
                e = error()
                while 1:
                    if i >= len(express):
                        e.word = ')'
                        e.errorType = 'not match'
                        e.line = express[i - 1].line
                        self.errorList.append(e)
                        return 1, 0
                    elif express[i].word == ')':
                        sum -= 1
                    elif express[i].word == '(':
                        sum += 1
                    if sum == 0:
                        break
                    temp.append(express[i])
                    i += 1
                flag, express[index].word = self.calExpressInt(temp, 0, flag)
                if flag == 0:
                    self.remove(express, index + 1, i)
                    express[index].tokenValue = 35
            elif (express[index].word == '*') | (express[index].word == '/'):
                if (index >= len(express) - 1) | (index < 1):
                    return 1, 0
                elif express[index - 1].tokenValue != 35:
                    return 1, 0
                elif express[index + 1].word == '(':
                    i = index + 2
                    temp = []
                    sum = 1
                    e = error()
                    while 1:
                        if i >= len(express):
                            e.word = ')'
                            e.errorType = 'not match'
                            e.line = express[i - 1].line
                            self.errorList.append(e)
                            return 1, 0
                        elif express[i].word == ')':
                            sum -= 1
                        elif express[i].word == '(':
                            sum += 1
                        if sum == 0:
                            break
                        temp.append(express[i])
                        i += 1
                    flag, express[index + 1].word = self.calExpressInt(temp, 0, flag)
                    if flag == 0:
                        self.remove(express, index + 2, i)
                        express[index + 1].tokenValue = 35

                elif express[index + 1].tokenValue != 35:
                    return 1, 0

                if express[index].word == '*':
                    express[index - 1].word = int(express[index - 1].word) * int(express[index + 1].word)
                else:
                    express[index - 1].word = int(express[index - 1].word) / int(express[index + 1].word)
                self.remove(express, index, index + 1)
            elif express[index].word == '+':
                if (index >= len(express) - 1) | (index < 1):
                    return 1, 0
                elif express[index - 1].tokenValue != 35:
                    return 1, 0
                elif express[index + 1].tokenValue == 35:
                    if index < len(express) - 3:
                        if (express[index + 2].word == '*') | (express[index + 2].word == '/'):
                            temp = []
                            temp.append(express[index + 1])
                            temp.append(express[index + 2])
                            temp.append(express[index + 3])
                            flag, express[index + 1].word = self.calExpressInt(temp, 0, flag)
                            if flag == 0:
                                express[index + 1].tokenValue = 35
                                self.remove(express, index + 2, index + 3)

                elif express[index + 1].word == '(':
                    i = index + 2
                    temp = []
                    sum = 1
                    e = error()
                    while 1:
                        if i >= len(express):
                            e.word = ')'
                            e.errorType = 'not match'
                            e.line = express[i - 1].line
                            self.errorList.append(e)
                            return 1, 0
                        elif express[i].word == ')':
                            sum -= 1
                        elif express[i].word == '(':
                            sum += 1
                        if sum == 0:
                            break
                        temp.append(express[i])
                        i += 1
                    flag, express[index + 1].word = self.calExpressInt(temp, 0, flag)
                    if flag == 0:
                        self.remove(express, index + 2, i)
                        express[index + 1].tokenValue = 35

                else:
                    return 1, 0

                express[index - 1].word = int(express[index - 1].word) + int(express[index + 1].word)
                self.remove(express, index, index + 1)
            elif express[index].word == '-':
                if index >= len(express) - 1:
                    return 1, 0
                elif index == 0:
                    express[index].word = int(express[index + 1].word) * (-1)
                    self.remove(express, index + 1, index + 1)
                    express[index].tokenValue = 35
                else:
                    if (index >= len(express) - 1) | (index < 1):
                        return 1, 0
                    elif express[index - 1].tokenValue != 35:
                        return 1, 0
                    elif express[index + 1].tokenValue == 35:
                        if index < len(express) - 3:
                            if (express[index + 2].word == '*') | (express[index + 2].word == '/'):
                                temp = []
                                temp.append(express[index + 1])
                                temp.append(express[index + 2])
                                temp.append(express[index + 3])
                                flag, express[index + 1].word = self.calExpressInt(temp, 0, flag)
                                if flag == 0:
                                    express[index + 1].tokenValue = 35
                                    self.remove(express, index + 2, index + 3)

                    elif express[index + 1].word == '(':
                        i = index + 2
                        temp = []
                        sum = 1
                        e = error()
                        while 1:
                            if i >= len(express):
                                e.word = ')'
                                e.errorType = 'not match'
                                e.line = express[i - 1].line
                                self.errorList.append(e)
                                return 1, 0
                            elif express[i].word == ')':
                                sum -= 1
                            elif express[i].word == '(':
                                sum += 1
                            if sum == 0:
                                break
                            temp.append(express[i])
                            i += 1
                        flag, express[index + 1].word = self.calExpressInt(temp, 0, flag)
                        if flag == 0:
                            self.remove(express, index + 2, i)
                            express[index + 1].tokenValue = 35

                    else:
                        return 1, 0

                    express[index - 1].word = int(express[index - 1].word) - int(express[index + 1].word)
                    self.remove(express, index, index + 1)

            elif express[index].tokenValue == 35:
                index += 1
            else:
                return 1, 0

    def calExpressFloat(self, express, index, flag):
        """
        判别算数表达式(实数)
        :param express:
        :param index:
        :param flag:
        :return:
        """
        while 1:
            if len(express) == 1:
                return 0, float(express[0].word)
            elif flag == 1:
                return 1, 0
            elif express[index].word == '(':
                i = index + 1
                temp = []
                sum = 1
                e = error()
                while 1:
                    if i >= len(express):
                        e.word = ')'
                        e.errorType = 'not match'
                        e.line = express[i - 1].line
                        self.errorList.append(e)
                        return 1, 0
                    elif express[i].word == ')':
                        sum -= 1
                    elif express[i].word == '(':
                        sum += 1
                    if sum == 0:
                        break
                    temp.append(express[i])
                    i += 1
                flag, express[index].word = self.calExpressFloat(temp, 0, flag)
                if flag == 0:
                    self.remove(express, index + 1, i)
                    express[index].tokenValue = 36
            elif (express[index].word == '*') | (express[index].word == '/'):
                if (index >= len(express) - 1) | (index < 1):
                    return 1, 0
                elif (express[index - 1].tokenValue != 35) & (express[index - 1].tokenValue != 36):
                    return 1, 0
                elif express[index + 1].word == '(':
                    i = index + 2
                    temp = []
                    sum = 1
                    e = error()
                    while 1:
                        if i >= len(express):
                            e.word = ')'
                            e.errorType = 'not match'
                            e.line = express[i - 1].line
                            self.errorList.append(e)
                            return 1, 0
                        elif express[i].word == '(':
                            sum += 1
                        elif express[i].word == ')':
                            sum -= 1
                        if sum == 0:
                            break
                        temp.append(express[i])
                        i += 1
                    flag, express[index + 1].word = self.calExpressFloat(temp, 0, flag)
                    if flag == 0:
                        self.remove(express, index + 2, i)
                        express[index + 1].tokenValue = 36

                elif (express[index + 1].tokenValue != 35) & (express[index + 1].tokenValue != 36):
                    return 1, 0

                if express[index].word == '*':
                    express[index - 1].word = float(express[index - 1].word) * float(express[index + 1].word)
                else:
                    express[index - 1].word = float(express[index - 1].word) / float(express[index + 1].word)
                self.remove(express, index, index + 1)
            elif express[index].word == '+':
                if (index >= len(express) - 1) | (index < 1):
                    return 1, 0
                elif (express[index - 1].tokenValue != 35) & (express[index - 1].tokenValue != 36):
                    return 1, 0
                elif (express[index + 1].tokenValue == 35) | (express[index + 1].tokenValue == 36):
                    if index < len(express) - 3:
                        if (express[index + 2].word == '*') | (express[index + 2].word == '/'):
                            temp = []
                            temp.append(express[index + 1])
                            temp.append(express[index + 2])
                            temp.append(express[index + 3])
                            flag, express[index + 1].word = self.calExpressFloat(temp, 0, flag)
                            if flag == 0:
                                express[index + 1].tokenValue = 36
                                self.remove(express, index + 2, index + 3)

                elif express[index + 1].word == '(':
                    i = index + 2
                    temp = []
                    sum = 1
                    e = error()
                    while 1:
                        if i >= len(express):
                            e.word = ')'
                            e.errorType = 'not match'
                            e.line = express[i - 1].line
                            self.errorList.append(e)
                            return 1, 0
                        elif express[i].word == ')':
                            sum -= 1
                        elif express[i].word == '(':
                            sum += 1
                        if sum == 0:
                            break
                        temp.append(express[i])
                        i += 1
                    flag, express[index + 1].word = self.calExpressFloat(temp, 0, flag)
                    if flag == 0:
                        self.remove(express, index + 2, i)
                        express[index + 1].tokenValue = 36

                else:
                    return 1, 0

                express[index - 1].word = float(express[index - 1].word) + float(express[index + 1].word)
                self.remove(express, index, index + 1)
            elif express[index].word == '-':
                if index >= len(express) - 1:
                    return 1, 0
                elif index == 0:
                    express[index].word = float(express[index + 1].word) * (-1)
                    self.remove(express, index + 1, index + 1)
                    express[index].tokenValue = 36
                else:
                    if (index >= len(express) - 1) | (index < 1):
                        return 1, 0
                    elif (express[index - 1].tokenValue != 35) & (express[index - 1].tokenValue != 36):
                        return 1, 0
                    elif (express[index + 1].tokenValue == 35) | (express[index + 1].tokenValue == 36):
                        if index < len(express) - 3:
                            if (express[index + 2].word == '*') | (express[index + 2].word == '/'):
                                temp = []
                                temp.append(express[index + 1])
                                temp.append(express[index + 2])
                                temp.append(express[index + 3])
                                flag, express[index + 1].word = self.calExpressFloat(temp, 0, flag)
                                if flag == 0:
                                    express[index + 1].tokenValue = 36
                                    self.remove(express, index + 2, index + 3)

                    elif express[index + 1].word == '(':
                        i = index + 2
                        temp = []
                        sum = 1
                        e = error()
                        while 1:
                            if i >= len(express):
                                e.word = ')'
                                e.errorType = 'not match'
                                e.line = express[i - 1].line
                                self.errorList.append(e)
                                return 1, 0
                            elif express[i].word == ')':
                                sum -= 1
                            elif express[i].word == '(':
                                sum += 1
                            if sum == 0:
                                break
                            temp.append(express[i])
                            i += 1
                        flag, express[index + 1].word = self.calExpressInt(temp, 0, flag)
                        if flag == 0:
                            self.remove(express, index + 2, i)
                            express[index + 1].tokenValue = 36

                    else:
                        return 1, 0

                    express[index - 1].word = float(express[index - 1].word) - float(express[index + 1].word)
                    self.remove(express, index, index + 1)

            elif (express[index].tokenValue == 35) | (express[index].tokenValue == 36):
                index += 1
            else:
                return 1, 0

    def simplifyBoolExpress(self, express):
        """
        简化布尔表达式
        :param express:
        :return:
        """
        i = 0
        data = []
        while 1:
            if i >= len(express):
                return express
            elif express[i].word == '=':
                temp = error()
                temp.word = '='
                temp.line = express[i].line
                temp.errorType = 'can\'t exist in boolExpress'
                self.errorList.append(temp)
                return data
            elif (express[i].word == '>') | (express[i].word == '<') | (express[i].word == '==') | (
                        express[i].word == '!='):
                symbol = express[i].word
                if (i == 0) | (i == len(express) - 1):
                    temp = error()
                    temp.word = 'boolExpress'
                    temp.line = express[i].line
                    temp.errorType = 'error'
                    return data
                elif express[i - 1].word == ')':
                    index = i - 1
                    sum = 0
                    tempExpress = []
                    while 1:
                        if index == -1:
                            temp = error()
                            temp.word = '('
                            temp.line = express[i].line
                            temp.errorType = 'not match'
                            self.errorList.append(temp)
                            return data
                        elif express[index].word == ')':
                            sum += 1
                        elif express[index].word == '(':
                            sum -= 1
                        tempExpress.append(express[index])
                        if sum == 0:
                            break
                        index -= 1
                    tempExpress = self.reverse(tempExpress)
                    if self.isFloat(tempExpress, 0) == 1:
                        flag, express[index].word = self.calExpressFloat(tempExpress, 0, 0)
                        express[index].tokenValue = 36
                    else:
                        flag, express[index].word = self.calExpressInt(tempExpress, 0, 0)
                        express[index].tokenValue = 35
                    if flag == 1:
                        temp = error()
                        temp.word = 'express'
                        temp.line = tempExpress[index].line
                        temp.errorType = 'error'
                        self.errorList.append(temp)
                        return data
                    else:
                        self.remove(express, index + 1, i - 1)
                        i = index + 1
                elif express[i + 1].word == '(':
                    index = i + 1
                    sum = 0
                    tempExpress = []
                    while 1:
                        if index == len(express):
                            temp = error()
                            temp.word = ')'
                            temp.line = express[i].line
                            temp.errorType = 'not match'
                            self.errorList.append(temp)
                            return data
                        elif express[index].word == '(':
                            sum += 1
                        elif express[index].word == ')':
                            sum -= 1
                        tempExpress.append(express[index])

                        if sum == 0:
                            break
                        index += 1

                    if self.isFloat(tempExpress, 0) == 1:
                        flag, express[i + 1].word = self.calExpressFloat(tempExpress, 0, 0)
                        express[i + 1].tokenValue = 36
                    else:
                        flag, express[i + 1].word = self.calExpressInt(tempExpress, 0, 0)
                        express[i + 1].tokenValue = 35
                    if flag == 1:
                        temp = error()
                        temp.word = 'express'
                        temp.line = tempExpress[index].line
                        temp.errorType = 'error'
                        self.errorList.append(temp)
                        return data
                    else:
                        self.remove(express, i + 2, index)
                elif ((express[i - 1].tokenValue == 35) | (express[i - 1].tokenValue == 36) & (
                            express[i + 1].tokenValue == 35) | (express[i + 1].tokenValue == 36)):
                    if express[i - 1].tokenValue == 35:
                        a = int(express[i - 1].word)
                    else:
                        a = float(express[i - 1].word)
                    if express[i + 1].tokenValue == 35:
                        b = int(express[i + 1].word)
                    else:
                        b = float(express[i + 1].word)
                    if symbol == '>':
                        express[i - 1].word = a > b
                    elif symbol == '<':
                        express[i - 1].word = a < b
                    elif symbol == '==':
                        express[i - 1].word = a == b
                    elif symbol == '!=':
                        express[i - 1].word = a != b
                    self.remove(express, i, i + 1)
                    express[i - 1].tokenValue = 38
                else:
                    temp = error()
                    temp.word = 'express'
                    temp.line = express[i].line
                    temp.errorType = 'error'
                    self.errorList.append(temp)
                    return data

            elif (express[i].tokenValue == 35) | (express[i].tokenValue == 36) | (express[i].tokenValue == 38) | (
                        express[i].word == '(') | (express[i].word == ')') | (express[i].word == '+') | (
                        express[i].word == '-') | (express[i].word == '*') | (express[i].word == '/') | (
                        express[i].word == 'and') | (express[i].word == 'or') | (express[i].word == 'not'):
                i += 1
            else:
                temp = error()
                temp.word = 'express'
                temp.line = express[i].line
                temp.errorType = 'error'
                self.errorList.append(temp)
                return data

    def reverse(self, list):
        """
        反转数组元素
        :param list:
        :return:
        """
        i = len(list) - 1
        tempList = []
        while 1:
            if i < 0:
                break
            else:
                tempList.append(list[i])
            i -= 1
        return tempList

    def boolExpress(self, express, index, flag):
        """
        判别布尔表达式
        :param express:
        :param index:
        :param flag:
        :return:
        """
        while 1:
            if len(express) == 1:
                return 0, express[0].word
            elif flag == 1:
                return 1, 0
            elif express[index].word == '(':
                i = index + 1
                temp = []
                sum = 1
                e = error()
                while 1:
                    if i >= len(express):
                        e.word = ')'
                        e.errorType = 'not match'
                        e.line = express[i - 1].line
                        self.errorList.append(e)
                        return 1, 0
                    elif express[i].word == ')':
                        sum -= 1
                    elif express[i].word == '(':
                        sum += 1
                    if sum == 0:
                        break
                    temp.append(express[i])
                    i += 1
                flag, express[index].word = self.boolExpress(temp, 0, flag)
                if flag == 0:
                    self.remove(express, index + 1, i)
                    express[index].tokenValue = 38
            elif express[index].word == 'and':
                if (index >= len(express) - 1) | (index < 1):
                    return 1, 0
                elif express[index - 1].tokenValue != 38:
                    return 1, 0
                elif express[index + 1].word == '(':
                    i = index + 2
                    temp = []
                    sum = 1
                    e = error()
                    while 1:
                        if i >= len(express):
                            e.word = ')'
                            e.errorType = 'not match'
                            e.line = express[i - 1].line
                            self.errorList.append(e)
                            return 1, 0
                        elif express[i].word == ')':
                            sum -= 1
                        elif express[i].word == '(':
                            sum += 1
                        if sum == 0:
                            break
                        temp.append(express[i])
                        i += 1
                    flag, express[index + 1].word = self.boolExpress(temp, 0, flag)
                    if flag == 0:
                        self.remove(express, index + 2, i)
                        express[index + 1].tokenValue = 38

                elif express[index + 1].tokenValue != 38:
                    return 1, 0

                express[index - 1].word = bool(express[index - 1].word) & bool(express[index + 1].word)
                self.remove(express, index, index + 1)
            elif express[index].word == 'or':
                if (index >= len(express) - 1) | (index < 1):
                    return 1, 0
                elif express[index - 1].tokenValue != 38:
                    return 1, 0
                elif express[index + 1].tokenValue == 38:
                    if index < len(express) - 3:
                        if express[index + 2].word == 'and':
                            temp = []
                            temp.append(express[index + 1])
                            temp.append(express[index + 2])
                            temp.append(express[index + 3])
                            flag, express[index + 1].word = self.boolExpress(temp, 0, flag)
                            if flag == 0:
                                express[index + 1].tokenValue = 38
                                self.remove(express, index + 2, index + 3)

                elif express[index + 1].word == '(':
                    i = index + 2
                    temp = []
                    sum = 1
                    e = error()
                    while 1:
                        if i >= len(express):
                            e.word = ')'
                            e.errorType = 'not match'
                            e.line = express[i - 1].line
                            self.errorList.append(e)
                            return 1, 0
                        elif express[i].word == ')':
                            sum -= 1
                        elif express[i].word == '(':
                            sum += 1
                        if sum == 0:
                            break
                        temp.append(express[i])
                        i += 1
                    flag, express[index + 1].word = self.boolExpress(temp, 0, flag)
                    if flag == 0:
                        self.remove(express, index + 2, i)
                        express[index + 1].tokenValue = 38

                else:
                    return 1, 0

                express[index - 1].word = bool(express[index - 1].word) | bool(express[index + 1].word)
                self.remove(express, index, index + 1)
            elif express[index].word == 'not':
                if index >= len(express) - 1:
                    return 1, 0
                elif index == 0:
                    if express[index + 1].word != '(':
                        express[index].word = not (bool(express[index + 1].word))
                        self.remove(express, index + 1, index + 1)
                        express[index].tokenValue = 38
                    else:
                        i = index + 2
                        temp = []
                        sum = 1
                        e = error()
                        while 1:
                            if i >= len(express):
                                e.word = ')'
                                e.errorType = 'not match'
                                e.line = express[i - 1].line
                                self.errorList.append(e)
                                return 1, 0
                            elif express[i].word == ')':
                                sum -= 1
                            elif express[i].word == '(':
                                sum += 1
                            if sum == 0:
                                break
                            temp.append(express[i])
                            i += 1
                        flag, express[index + 1].word = self.boolExpress(temp, 0, flag)
                        if flag == 0:
                            self.remove(express, index + 2, i)
                            express[index + 1].tokenValue = 38

            elif express[index].tokenValue == 38:
                index += 1
            else:
                return 1, 0

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

    def replace(self, list):
        """
        根据符号表替换变量
        :param list:
        :return:
        """
        data = []
        line = list[0].line
        for i in range(len(list)):
            if list[i].tokenValue == 34:
                if self.getValue(list[i].word) == '':
                    temp = error()
                    temp.line = line
                    temp.word = list[i].word
                    temp.errorType = 'have not value'
                    self.errorList.append(temp)
                    return data
                else:
                    if self.getVar(list[i].word) == 'integer':
                        list[i].tokenValue = 35
                    elif self.getVar(list[i].word) == 'real':
                        list[i].tokenValue = 36
                    list[i].word = self.getValue(list[i].word)
        return list

    def isFloat(self, list, start):
        """
        判定是否为实数算数表达式
        :param list:
        :param start:
        :return:
        """
        i = start
        line = list[start].line
        while 1:
            if i >= len(list):
                break
            elif (list[i].line != line) | (list[i].word == ';'):
                break
            if list[i].tokenValue == 36:
                return 1
            elif (list[i].tokenValue == 34) & (self.getVar(list[i].word) == 'real'):
                return 1

            i += 1
        return 0

    def handle_variate(self, tokenTable, start):
        """
        处理变量定义
        :param tokenTable:
        :param start:
        :return:
        """
        while 1:
            if start >= len(tokenTable):
                if tokenTable[start - 1].word == 'var':
                    temp = error()
                    temp.word = 'variate' + '\t' + 'identifier'
                    temp.line = tokenTable[start - 1].line
                    temp.errorType = 'lack'
                    self.errorList.append(temp)
                return start
            elif (tokenTable[start].word == 'const') | (tokenTable[start].word == 'begin'):
                return start
            else:
                start = self.handle_defination(tokenTable, start)

    def handle_defination(self, tokenTable, start):
        """
        处理变量定义语句
        :param tokenTable:
        :param start:
        :return:
        """
        line = tokenTable[start].line
        temp = error()
        flag = 0
        tempVariate = []
        while 1:
            if start >= len(tokenTable):
                temp.word += ':'
                temp.errorType = 'lack'
                temp.line = line
                self.errorList.append(temp)
                return start

            elif tokenTable[start].line != line:
                temp.word += ':'
                temp.errorType = 'lack'
                temp.line = line
                self.errorList.append(temp)
                return start

            elif tokenTable[start].word == ';':
                temp.word += ':'
                temp.errorType = 'lack'
                temp.line = line
                self.errorList.append(temp)
                return start + 1

            elif tokenTable[start].word == ':':
                if flag == 1:
                    if (self.match(self.constantList, tokenTable[start - 1].word) != -1) | (
                                self.isReplace(tempVariate, tokenTable[start - 1].word) == 1) | (
                                self.match(self.variateList, tokenTable[start - 1].word) != -1):
                        temp = error()
                        temp.word = tokenTable[start - 1].word
                        temp.line = line
                        temp.errorType = 'Rename'
                        self.errorList.append(temp)
                    else:
                        tempVariate.append(tokenTable[start - 1].word)
                    break
                else:
                    temp = error()
                    while 1:
                        if start >= len(tokenTable):
                            return start

                        elif tokenTable[start].word == ';':
                            temp.word += '\tidentifier'
                            temp.line = line
                            temp.errorType = 'lack'
                            self.errorList.append(temp)
                            return start + 1

                        elif tokenTable[start].line != line:
                            temp.word += '\tidentifier'
                            temp.line = line
                            temp.errorType = 'lack'
                            self.errorList.append(temp)
                            return start
                        temp.word += tokenTable[start].word + ' '
                        start += 1

            elif flag == 0:
                if tokenTable[start].wordtype != 'identifier':
                    temp = error()
                    while 1:
                        if start >= len(tokenTable):
                            return start

                        elif tokenTable[start].word == ';':
                            temp.word += '\tidentifier'
                            temp.line = line
                            temp.errorType = 'lack'
                            self.errorList.append(temp)
                            return start + 1

                        elif tokenTable[start].line != line:
                            temp.word += '\tidentifier'
                            temp.line = line
                            temp.errorType = 'lack'
                            self.errorList.append(temp)
                            return start
                        temp.word += tokenTable[start].word + ' '
                        start += 1
                else:
                    flag = 1

            elif flag == 1:
                if tokenTable[start].word != ',':
                    temp = error()
                    while 1:
                        if start >= len(tokenTable):
                            return start

                        elif tokenTable[start].word == ';':
                            temp.word += '\t","'
                            temp.line = line
                            temp.errorType = 'lack'
                            self.errorList.append(temp)
                            return start + 1

                        elif tokenTable[start].line != line:
                            temp.word += '\t","'
                            temp.line = line
                            temp.errorType = 'lack'
                            self.errorList.append(temp)
                            return start
                        temp.word += tokenTable[start].word + ' '
                        start += 1
                else:
                    flag = 0
                    if (self.match(self.constantList, tokenTable[start - 1].word) == 1) | (
                                self.isReplace(tempVariate, tokenTable[start - 1].word) == 1) | (
                                self.match(self.variateList, tokenTable[start - 1].word) == 1):
                        temp = error()
                        temp.word = tokenTable[start - 1].word
                        temp.line = line
                        temp.errorType = 'Rename'
                        self.errorList.append(temp)

                    else:
                        tempVariate.append(tokenTable[start - 1].word)
            start += 1

        start += 1
        if start >= len(tokenTable):
            temp = error()
            temp.word = 'wordkey'
            temp.line = line
            temp.errorType = 'lack'
            self.errorList.append(temp)
            return start

        elif tokenTable[start].line != line:
            temp = error()
            temp.word = 'wordkey'
            temp.line = line
            temp.errorType = 'lack'
            self.errorList.append(temp)
            return start

        elif (tokenTable[start].tokenValue != 3) & (tokenTable[start].tokenValue != 4) & (
                    tokenTable[start].tokenValue != 5) & (tokenTable[start].tokenValue != 6):
            temp = error()
            while 1:
                if start >= len(tokenTable):
                    return start

                elif tokenTable[start].word == ';':
                    temp.word += '\tidentifier'
                    temp.line = line
                    temp.errorType = 'lack'
                    self.errorList.append(temp)
                    return start + 1

                elif tokenTable[start].line != line:
                    temp.word += '\tidentifier'
                    temp.line = line
                    temp.errorType = 'lack'
                    self.errorList.append(temp)
                    return start
                temp.word += tokenTable[start].word + ' '
                start += 1
        else:
            start += 1
            if start >= len(tokenTable):
                temp = error()
                temp.word = ';'
                temp.line = line
                temp.errorType = 'lack'
                self.errorList.append(temp)
                return start

            elif tokenTable[start].line != line:
                temp = error()
                temp.word = ';'
                temp.line = line
                temp.errorType = 'lack'
                self.errorList.append(temp)
                return start
            elif tokenTable[start].word != ';':
                temp = error()
                while 1:
                    if start >= len(tokenTable):
                        return start

                    elif tokenTable[start].word == ';':
                        temp.word += '\t";"'
                        temp.line = line
                        temp.errorType = 'lack'
                        self.errorList.append(temp)
                        return start + 1

                    elif tokenTable[start].line != line:
                        temp.word += '\t";"'
                        temp.line = line
                        temp.errorType = 'lack'
                        self.errorList.append(temp)
                        return start
                    temp.word += tokenTable[start].word + ' '
                    start += 1
            else:
                for j in range(len(tempVariate)):
                    data = sign()
                    data.word = tempVariate[j]
                    data.signType = tokenTable[start - 1].word
                    self.variateList.append(data)
                return start + 1

    def isReplace(self, list, word):
        """
        判断是否重复
        :param list:
        :param word:
        :return:
        """
        for i in range(len(list)):
            if list[i] == word:
                return 1
        return 0

    def handle_mainfunction(self, tokenTable, start, structure):
        """
        处理主函数
        :param tokenTable:
        :param start:
        :param structure:
        :return:
        """
        while 1:
            if start >= len(tokenTable):
                temp = error()
                temp.word = 'end'
                temp.line = tokenTable[start - 1].line
                temp.errorType = 'lack'
                self.errorList.append(temp)
                return start
            elif tokenTable[start].word == 'end':
                start += 1
                if start >= len(tokenTable):
                    temp = error()
                    temp.word = '"."'
                    temp.line = tokenTable[start - 1].line
                    temp.errorType = 'lack'
                    self.errorList.append(temp)
                structure.append("     ---end.")
                return start + 1
            elif tokenTable[start].word == 'if':
                structure.append("     -----if")
                start = self.handle_if(tokenTable, start, structure)
            elif tokenTable[start].word == 'repeat':
                structure.append("     -----repeat")
                start = self.handle_repeat(tokenTable, start, structure)
            elif tokenTable[start].word == 'for':
                structure.append("     -----for")
                start = self.handle_for(tokenTable, start, structure)
            elif tokenTable[start].word == 'while':
                structure.append("     -----while")
                start = self.handle_while(tokenTable, start, structure)
            else:
                structure.append("     -----calExpress")
                start = self.handle_evaluation(tokenTable, start, 0)
        return start

    def handle_if(self, tokenTable, start, structure):
        """
        处理if语句
        :param tokenTable:
        :param start:
        :return:
        """
        index = start + 1
        line = tokenTable[index].line
        tempExpress = []
        while 1:
            if index >= len(tokenTable):
                temp = error()
                temp.word = 'then'
                temp.line = line
                temp.errorType = 'lack'
                return index
            elif tokenTable[index].word == ';':
                temp = error()
                temp.word = 'then'
                temp.line = line
                temp.errorType = 'lack'
                return index + 1
            elif (tokenTable[index].word == 'then') | (tokenTable[index].line != line):
                break
            tempExpress.append(tokenTable[index])
            index += 1
        if tokenTable[index].word != 'then':
            temp = error()
            temp.word = 'then'
            temp.line = line
            temp.errorType = 'lack'
            return index
        else:
            tempExpress = self.replace(tempExpress)
            if len(tempExpress) == 0:

                while 1:
                    if index >= len(tokenTable):
                        return index
                    elif tokenTable[index].line != line:
                        return index
                    elif tokenTable[index].word == ';':
                        return index + 1
                    index += 1
            else:
                tempExpress = self.simplifyBoolExpress(tempExpress)
                if len(tempExpress) == 0:
                    while 1:
                        if index >= len(tokenTable):
                            return index
                        elif tokenTable[index].line != line:
                            return index
                        elif tokenTable[index].word == ';':
                            return index + 1
                        index += 1
                else:
                    flag, value = self.boolExpress(tempExpress, 0, 0)
                    if flag == 1:
                        temp = error()
                        temp.word = 'express'
                        temp.line = line
                        temp.errorType = 'error'
                        self.errorList.append(temp)
                        while 1:
                            if index >= len(tokenTable):
                                return index
                            elif tokenTable[index].line != line:
                                return index
                            elif tokenTable[index].word == ';':
                                return index + 1
                            index += 1
                    else:
                        if str(value) == 'True':
                            if index > len(tokenTable) - 1:
                                temp = error()
                                temp.word = 'express'
                                temp.line = tokenTable[index].line
                                temp.errorType = 'lack'
                                self.errorList.append(temp)
                                return index
                            elif tokenTable[index + 1].word == 'begin':
                                structure.append("     -------begin")
                                tempIndex = index + 2
                                while 1:
                                    if tempIndex >= len(tokenTable):
                                        temp = error()
                                        temp.word = 'end'
                                        temp.line = tokenTable[tempIndex - 1].line
                                        temp.errorType = 'lack'
                                        self.errorList.append(temp)
                                        return tempIndex

                                    elif tokenTable[tempIndex].word == 'end':
                                        tempIndex += 1
                                        if tempIndex >= len(tokenTable):
                                            temp = error()
                                            temp.word = '"."'
                                            temp.line = tokenTable[tempIndex - 1].line
                                            temp.errorType = 'lack'
                                            self.errorList.append(temp)
                                        elif tokenTable[tempIndex].word == '.':
                                            structure.append("     -------end.")
                                            break
                                        else:
                                            temp = error()
                                            temp.word = '"."'
                                            temp.line = tokenTable[tempIndex - 1].line
                                            temp.errorType = 'lack'
                                            self.errorList.append(temp)
                                            while 1:
                                                if tempIndex >= len(tokenTable):
                                                    return tempIndex
                                                elif tokenTable[tempIndex].line != line:
                                                    return tempIndex
                                                elif tokenTable[tempIndex].word == ';':
                                                    return tempIndex + 1
                                                tempIndex += 1
                                    elif tokenTable[tempIndex].word == 'if':
                                        structure.append("     ---------if")
                                        tempIndex = self.handle_if(tokenTable, tempIndex, structure)
                                    elif tokenTable[tempIndex].word == 'repeat':
                                        structure.append("     ---------repeat")
                                        tempIndex = self.handle_repeat(tokenTable, tempIndex, structure)
                                    elif tokenTable[tempIndex].word == 'for':
                                        structure.append("     ---------for")
                                        tempIndex = self.handle_for(tokenTable, tempIndex, structure)
                                    elif tokenTable[tempIndex].word == 'while':
                                        structure.append("     ---------while")
                                        tempIndex = self.handle_while(tokenTable, tempIndex, structure)
                                    else:
                                        structure.append("     ---------calExpress")
                                        tempIndex = self.handle_evaluation(tokenTable, tempIndex, 0)
                                index = tempIndex + 1

                            else:
                                structure.append("     -------calExpress")
                                index = self.handle_evaluation(tokenTable, index + 1, 0)
                            if index >= len(tokenTable):
                                return index
                            else:
                                if tokenTable[index].word == 'else':
                                    if index > len(tokenTable) - 1:
                                        temp = error()
                                        temp.word = 'express'
                                        temp.line = tokenTable[index].line
                                        temp.errorType = 'lack'
                                        self.errorList.append(temp)
                                        return index
                                    elif tokenTable[index + 1].word == 'begin':
                                        tempIndex = index + 2
                                        tempList = []
                                        tempList = self.copyList(self.variateList)
                                        while 1:
                                            if tempIndex >= len(tokenTable):
                                                temp = error()
                                                temp.word = 'end'
                                                temp.line = tokenTable[tempIndex - 1].line
                                                temp.errorType = 'lack'
                                                self.errorList.append(temp)
                                                return tempIndex

                                            elif tokenTable[tempIndex].word == 'end':
                                                tempIndex += 1
                                                if tempIndex >= len(tokenTable):
                                                    temp = error()
                                                    temp.word = '"."'
                                                    temp.line = tokenTable[tempIndex - 1].line
                                                    temp.errorType = 'lack'
                                                    self.errorList.append(temp)
                                                elif tokenTable[tempIndex].word == '.':
                                                    break
                                                else:
                                                    temp = error()
                                                    temp.word = '"."'
                                                    temp.line = tokenTable[tempIndex - 1].line
                                                    temp.errorType = 'lack'
                                                    self.errorList.append(temp)
                                                    while 1:
                                                        if tempIndex >= len(tokenTable):
                                                            return tempIndex
                                                        elif tokenTable[tempIndex].line != line:
                                                            return tempIndex
                                                        elif tokenTable[tempIndex].word == ';':
                                                            return tempIndex + 1
                                                        tempIndex += 1
                                            elif tokenTable[tempIndex].word == 'if':
                                                tempIndex = self.handle_if(tokenTable, tempIndex, structure)
                                            elif tokenTable[tempIndex].word == 'repeat':
                                                tempIndex = self.handle_repeat(tokenTable, tempIndex, structure)
                                            elif tokenTable[tempIndex].word == 'for':
                                                tempIndex = self.handle_for(tokenTable, tempIndex, structure)
                                            elif tokenTable[tempIndex].word == 'while':
                                                tempIndex = self.handle_while(tokenTable, tempIndex, structure)
                                            else:
                                                tempIndex = self.handle_evaluation(tokenTable, tempIndex, 0)
                                        index = tempIndex + 1
                                        self.variateList = []
                                        self.variateList = self.copyList(tempList)

                                    else:
                                        tempList = []
                                        tempList = self.copyList(self.variateList)
                                        index = self.handle_evaluation(tokenTable, index + 1, 0)
                                        self.variateList = []
                                        self.variateList = self.copyList(tempList)
                                return index
                        elif str(value) == 'False':
                            if index > len(tokenTable) - 1:
                                temp = error()
                                temp.word = 'express'
                                temp.line = tokenTable[index].line
                                temp.errorType = 'lack'
                                self.errorList.append(temp)
                                return index
                            elif tokenTable[index + 1].word == 'begin':
                                tempIndex = index + 2
                                tempList = []
                                tempList = self.copyList(self.variateList)
                                while 1:
                                    if tempIndex >= len(tokenTable):
                                        temp = error()
                                        temp.word = 'end'
                                        temp.line = tokenTable[tempIndex - 1].line
                                        temp.errorType = 'lack'
                                        self.errorList.append(temp)
                                        return tempIndex

                                    elif tokenTable[tempIndex].word == 'end':
                                        tempIndex += 1
                                        if tempIndex >= len(tokenTable):
                                            temp = error()
                                            temp.word = '"."'
                                            temp.line = tokenTable[tempIndex - 1].line
                                            temp.errorType = 'lack'
                                            self.errorList.append(temp)
                                        elif tokenTable[tempIndex].word == '.':
                                            break
                                        else:
                                            temp = error()
                                            temp.word = '"."'
                                            temp.line = tokenTable[tempIndex - 1].line
                                            temp.errorType = 'lack'
                                            self.errorList.append(temp)
                                            while 1:
                                                if tempIndex >= len(tokenTable):
                                                    return tempIndex
                                                elif tokenTable[tempIndex].line != line:
                                                    return tempIndex
                                                elif tokenTable[tempIndex].word == ';':
                                                    return tempIndex + 1
                                                tempIndex += 1
                                    elif tokenTable[tempIndex].word == 'if':
                                        tempIndex = self.handle_if(tokenTable, tempIndex, structure)
                                    elif tokenTable[tempIndex].word == 'repeat':
                                        tempIndex = self.handle_repeat(tokenTable, tempIndex, structure)
                                    elif tokenTable[tempIndex].word == 'for':
                                        tempIndex = self.handle_for(tokenTable, tempIndex, structure)
                                    elif tokenTable[tempIndex].word == 'while':
                                        tempIndex = self.handle_while(tokenTable, tempIndex, structure)
                                    else:
                                        tempIndex = self.handle_evaluation(tokenTable, tempIndex, 0)
                                self.variateList = []
                                self.variateList = self.copyList(tempList)
                                index = tempIndex + 1

                            else:
                                tempList = []
                                tempList = self.copyList(self.variateList)
                                index = self.handle_evaluation(tokenTable, index + 1, 0)
                                self.variateList = []
                                self.variateList = self.copyList(tempList)

                            if index >= len(tokenTable):
                                return index
                            else:
                                if tokenTable[index].word == 'else':
                                    if tokenTable[index + 1].word == 'begin':
                                        structure.append("     -------begin")
                                        tempIndex = index + 2
                                        while 1:
                                            if tempIndex >= len(tokenTable):
                                                temp = error()
                                                temp.word = 'end'
                                                temp.line = tokenTable[tempIndex - 1].line
                                                temp.errorType = 'lack'
                                                self.errorList.append(temp)
                                                return tempIndex

                                            elif tokenTable[tempIndex].word == 'end':
                                                tempIndex += 1
                                                if tempIndex >= len(tokenTable):
                                                    temp = error()
                                                    temp.word = '"."'
                                                    temp.line = tokenTable[tempIndex - 1].line
                                                    temp.errorType = 'lack'
                                                    self.errorList.append(temp)
                                                elif tokenTable[tempIndex].word == '.':
                                                    structure.append("     -------end.")
                                                    break
                                                else:
                                                    temp = error()
                                                    temp.word = '"."'
                                                    temp.line = tokenTable[tempIndex - 1].line
                                                    temp.errorType = 'lack'
                                                    self.errorList.append(temp)
                                                    while 1:
                                                        if tempIndex >= len(tokenTable):
                                                            return tempIndex
                                                        elif tokenTable[tempIndex].line != line:
                                                            return tempIndex
                                                        elif tokenTable[tempIndex].word == ';':
                                                            return tempIndex + 1
                                                        tempIndex += 1
                                            elif tokenTable[tempIndex].word == 'if':
                                                structure.append("     ---------if")
                                                tempIndex = self.handle_if(tokenTable, tempIndex, structure)
                                            elif tokenTable[tempIndex].word == 'repeat':
                                                structure.append("     ---------repeat")
                                                tempIndex = self.handle_repeat(tokenTable, tempIndex, structure)
                                            elif tokenTable[tempIndex].word == 'for':
                                                structure.append("     ---------for")
                                                tempIndex = self.handle_for(tokenTable, tempIndex, structure)
                                            elif tokenTable[tempIndex].word == 'while':
                                                structure.append("     ---------while")
                                                tempIndex = self.handle_while(tokenTable, tempIndex, structure)
                                            else:
                                                structure.append("     ---------calExpress")
                                                tempIndex = self.handle_evaluation(tokenTable, tempIndex, 0)
                                        index = tempIndex + 1

                                    else:
                                        structure.append("     -------calExpress")
                                        index = self.handle_evaluation(tokenTable, index + 1, 0)
                                return index

    def handle_repeat(self, tokenTable, start, structure):
        """
        处理repeat语句
        :param tokenTable:
        :param start:
        :return:
        """
        index = start + 1
        line = tokenTable[index].line
        tempExpress = []
        while 1:
            if index >= len(tokenTable):
                temp = error()
                temp.word = 'util'
                temp.line = line
                temp.errorType = 'lack'
                return index
            elif (tokenTable[index].word == 'util') | (tokenTable[index].line != line):
                break
            tempExpress.append(tokenTable[index])
            index += 1
        if tokenTable[index].word != 'util':
            temp = error()
            temp.word = 'util'
            temp.line = line
            temp.errorType = 'lack'
            return index
        else:
            sum = index
            tempExpress1 = []
            tempToken = []
            tempData = index + 1
            while 1:
                if tempData >= len(tokenTable):
                    break
                t = token()
                t.word = tokenTable[tempData].word
                t.line = tokenTable[tempData].line
                t.tokenValue = tokenTable[tempData].tokenValue
                t.wordtype = tokenTable[tempData].wordtype
                tempToken.append(t)
                tempData += 1
            for i in range(len(tempExpress)):
                temp = token()
                temp.word = tempExpress[i].word
                temp.tokenValue = tempExpress[i].tokenValue
                temp.line = tempExpress[i].line
                temp.wordtype = tempExpress[i].wordtype
                tempExpress1.append(temp)
            while 1:
                index = sum
                tempExpress = []
                for i in range(len(tempExpress1)):
                    temp = token()
                    temp.word = tempExpress1[i].word
                    temp.tokenValue = tempExpress1[i].tokenValue
                    temp.line = tempExpress1[i].line
                    temp.wordtype = tempExpress1[i].wordtype
                    tempExpress.append(temp)
                if len(tempExpress) == 0:

                    while 1:
                        if index >= len(tokenTable):
                            return index
                        elif tokenTable[index].line != line:
                            return index
                        elif tokenTable[index].word == ';':
                            return index + 1
                        index += 1
                else:
                    if tempExpress[0].word == 'begin':
                        structure.append("     -------begin")
                        tempIndex = 1
                        while 1:
                            if tempIndex >= len(tempExpress):
                                temp = error()
                                temp.word = 'end'
                                temp.line = tempExpress[tempIndex - 1].line
                                temp.errorType = 'lack'
                                self.errorList.append(temp)
                                return tempIndex

                            elif tempExpress[tempIndex].word == 'end':
                                tempIndex += 1
                                if tempIndex >= len(tempExpress):
                                    temp = error()
                                    temp.word = '"."'
                                    temp.line = tempExpress[tempIndex - 1].line
                                    temp.errorType = 'lack'
                                    self.errorList.append(temp)
                                    return tempIndex
                                elif tempExpress[tempIndex].word == '.':
                                    structure.append("     -------end.")
                                    break
                                else:
                                    temp = error()
                                    temp.word = '"."'
                                    temp.line = tokenTable[tempIndex - 1].line
                                    temp.errorType = 'lack'
                                    self.errorList.append(temp)
                            elif tempExpress[tempIndex].word == 'if':
                                structure.append("     ---------if")
                                tempIndex = self.handle_if(tempExpress, tempIndex, structure)
                            elif tokenTable[tempIndex].word == 'repeat':
                                structure.append("     ---------repeat")
                                tempIndex = self.handle_repeat(tempExpress, tempIndex, structure)
                            elif tokenTable[tempIndex].word == 'for':
                                structure.append("     ---------for")
                                tempIndex = self.handle_for(tempExpress, tempIndex, structure)
                            elif tokenTable[tempIndex].word == 'while':
                                structure.append("     ---------while")
                                tempIndex = self.handle_while(tempExpress, tempIndex, structure)
                            else:
                                structure.append("     ---------calExpress")
                                tempIndex = self.handle_evaluation(tempExpress, tempIndex, 0)

                    else:
                        structure.append("     -------calExpress")
                        tempIndex = self.handle_evaluation(tempExpress, 0, 0)
                        if tempIndex != len(tempExpress):
                            temp = error()
                            temp.word = 'express'
                            temp.line = tokenTable[index].line
                            temp.errorType = 'error'
                            self.errorList.append(temp)
                tempData = index + 1
                if tempData >= len(tokenTable):
                    temp = error()
                    temp.word = 'express'
                    temp.line = tokenTable[index].line
                    temp.errorType = 'lack'
                    self.errorList.append(temp)
                    return index
                n = 0
                while 1:
                    if n >= len(tempToken):
                        break
                    del tokenTable[tempData]
                    n += 1
                tempData = index + 1
                n = 0
                while 1:
                    if n >= len(tempToken):
                        break
                    t = token()
                    t.word = tempToken[n].word
                    t.line = tempToken[n].line
                    t.tokenValue = tempToken[n].tokenValue
                    t.wordtype = tempToken[n].wordtype
                    tokenTable.append(t)
                    n += 1
                tempData = index + 1
                tempBool = []
                while 1:
                    if tempData >= len(tokenTable):
                        temp = error()
                        temp.word = 'express'
                        temp.line = tokenTable[tempData - 1].line
                        temp.errorType = 'lack'
                        self.errorList.append(temp)
                        return index
                    elif tokenTable[tempData].line != line:
                        temp = error()
                        temp.word = 'express'
                        temp.line = tokenTable[tempData - 1].line
                        temp.errorType = 'lack'
                        self.errorList.append(temp)
                        return index
                    elif tokenTable[tempData].word == ';':
                        break
                    tempBool.append(tokenTable[tempData])
                    tempData += 1

                tempBool = self.replace(tempBool)
                if len(tempBool) == 0:

                    while 1:
                        if tempData >= len(tokenTable):
                            return tempData
                        elif tokenTable[tempData].line != line:
                            return tempData
                        elif tokenTable[tempData].word == ';':
                            return tempData + 1
                        tempData += 1
                else:
                    tempBool = self.simplifyBoolExpress(tempBool)
                    if len(tempBool) == 0:
                        while 1:
                            if tempData >= len(tokenTable):
                                return tempData
                            elif tokenTable[tempData].line != line:
                                return tempData
                            elif tokenTable[tempData].word == ';':
                                return tempData + 1
                            tempData += 1
                    else:
                        flag, value = self.boolExpress(tempBool, 0, 0)
                        if flag == 1:
                            temp = error()
                            temp.word = 'express'
                            temp.line = line
                            temp.errorType = 'error'
                            self.errorList.append(temp)
                            while 1:
                                if tempData >= len(tokenTable):
                                    return tempData
                                elif tokenTable[tempData].line != line:
                                    return tempData
                                elif tokenTable[tempData].word == ';':
                                    return tempData + 1
                                index += 1
                        else:
                            if str(value) == 'True':
                                return tempData + 1

    def handle_for(self, tokenTable, start, structure):
        """
        处理for语句
        :param tokenTable:
        :param start:
        :return:
        """
        index = start + 1
        line = tokenTable[index].line
        tempExpress = []
        while 1:
            if index >= len(tokenTable):
                temp = error()
                temp.word = 'do'
                temp.line = line
                temp.errorType = 'lack'
                return index
            elif tokenTable[index].word == ';':
                temp = error()
                temp.word = 'do'
                temp.line = line
                temp.errorType = 'lack'
                return index + 1
            elif (tokenTable[index].word == 'do') | (tokenTable[index].line != line):
                break
            tempExpress.append(tokenTable[index])
            index += 1
        if tokenTable[index].word != 'do':
            temp = error()
            temp.word = 'do'
            temp.line = line
            temp.errorType = 'lack'
            return index
        else:
            sum = index
            tempExpress1 = []
            tempToken = []
            tempData = index + 1
            while 1:
                if tempData >= len(tokenTable):
                    break
                t = token()
                t.word = tokenTable[tempData].word
                t.line = tokenTable[tempData].line
                t.tokenValue = tokenTable[tempData].tokenValue
                t.wordtype = tokenTable[tempData].wordtype
                tempToken.append(t)
                tempData += 1
            for i in range(len(tempExpress)):
                temp = token()
                temp.word = tempExpress[i].word
                temp.tokenValue = tempExpress[i].tokenValue
                temp.line = tempExpress[i].line
                temp.wordtype = tempExpress[i].wordtype
                tempExpress1.append(temp)
            tempExpress2 = []
            tempExpress3 = []
            tempExpress2, tempExpress3 = self.splitByTo(tempExpress)
            if len(tempExpress3) == 0:
                temp = error()
                temp.word = 'to'
                temp.line = line
                temp.errorType = 'lack'
                while 1:
                    if index >= len(tokenTable):
                        return index
                    elif tokenTable[index].line != line:
                        return index
                    elif tokenTable[index].word == ';':
                        return index + 1
                    index += 1
            else:
                x = token()
                x.word = ';'
                x.line = tempExpress1[0].line
                x.tokenValue = 40
                x.wordtype = 'delimiter'
                tempExpress2.append(x)
                tempIndex = self.handle_evaluation(tempExpress2, 0, 0)
                if tempIndex != len(tempExpress2):
                    temp = error()
                    temp.word = 'express'
                    temp.line = line
                    temp.errorType = 'error'
                    while 1:
                        if index >= len(tokenTable):
                            return index
                        elif tokenTable[index].line != line:
                            return index
                        elif tokenTable[index].word == ';':
                            return index + 1
                        index += 1
            while 1:
                index = sum
                tempExpress = []
                for i in range(len(tempExpress1)):
                    temp = token()
                    temp.word = tempExpress1[i].word
                    temp.tokenValue = tempExpress1[i].tokenValue
                    temp.line = tempExpress1[i].line
                    temp.wordtype = tempExpress1[i].wordtype
                    tempExpress.append(temp)
                tempExpress2 = []
                tempExpress3 = []
                tempExpress2, tempExpress3 = self.splitByTo(tempExpress)
                if len(tempExpress3) == 0:
                    temp = error()
                    temp.word = 'to'
                    temp.line = line
                    temp.errorType = 'lack'
                    while 1:
                        if index >= len(tokenTable):
                            return index
                        elif tokenTable[index].line != line:
                            return index
                        elif tokenTable[index].word == ';':
                            return index + 1
                        index += 1
                else:
                    tempExpress3=self.replace(tempExpress3)
                    flag, value = self.calExpressFloat(tempExpress3, 0, 0)
                    if flag == 1:
                        temp = error()
                        temp.word = 'express'
                        temp.line = line
                        temp.errorType = 'error'
                        while 1:
                            if index >= len(tokenTable):
                                return index
                            elif tokenTable[index].line != line:
                                return index
                            elif tokenTable[index].word == ';':
                                return index + 1
                            index += 1
                    else:
                        if float(self.getValue(tempExpress[0].word)) <= value:
                            tempData = index + 1
                            n = 0
                            while 1:
                                if n >= len(tempToken):
                                    break
                                del tokenTable[tempData]
                                n += 1
                            tempData = index + 1
                            n = 0
                            while 1:
                                if n >= len(tempToken):
                                    break
                                t = token()
                                t.word = tempToken[n].word
                                t.line = tempToken[n].line
                                t.tokenValue = tempToken[n].tokenValue
                                t.wordtype = tempToken[n].wordtype
                                tokenTable.append(t)
                                n += 1
                            if index > len(tokenTable) - 1:
                                temp = error()
                                temp.word = 'express'
                                temp.line = tokenTable[index].line
                                temp.errorType = 'lack'
                                self.errorList.append(temp)
                                return index

                            elif tokenTable[index + 1].word == 'begin':
                                structure.append("     -------begin")
                                tempIndex = index + 2
                                while 1:
                                    if tempIndex >= len(tokenTable):
                                        temp = error()
                                        temp.word = 'end'
                                        temp.line = tokenTable[tempIndex - 1].line
                                        temp.errorType = 'lack'
                                        self.errorList.append(temp)
                                        return tempIndex

                                    elif tokenTable[tempIndex].word == 'end':
                                        tempIndex += 1
                                        if tempIndex >= len(tokenTable):
                                            temp = error()
                                            temp.word = '"."'
                                            temp.line = tokenTable[tempIndex - 1].line
                                            temp.errorType = 'lack'
                                            self.errorList.append(temp)
                                        elif tokenTable[tempIndex].word == '.':
                                            structure.append("     -------end.")
                                            break
                                        else:
                                            temp = error()
                                            temp.word = '"."'
                                            temp.line = tokenTable[tempIndex - 1].line
                                            temp.errorType = 'lack'
                                            self.errorList.append(temp)
                                            while 1:
                                                if tempIndex >= len(tokenTable):
                                                    return tempIndex
                                                elif tokenTable[tempIndex].line != line:
                                                    return tempIndex
                                                elif tokenTable[tempIndex].word == ';':
                                                    return tempIndex + 1
                                                tempIndex += 1
                                    elif tokenTable[tempIndex].word == 'if':
                                        structure.append("     ---------if")
                                        tempIndex = self.handle_if(tokenTable, tempIndex, structure)
                                    elif tokenTable[tempIndex].word == 'repeat':
                                        structure.append("     ---------repeat")
                                        tempIndex = self.handle_repeat(tokenTable, tempIndex, structure)
                                    elif tokenTable[tempIndex].word == 'for':
                                        structure.append("     ---------for")
                                        tempIndex = self.handle_for(tokenTable, tempIndex, structure)
                                    elif tokenTable[tempIndex].word == 'while':
                                        structure.append("     ---------while")
                                        tempIndex = self.handle_while(tokenTable, tempIndex, structure)
                                    else:
                                        structure.append("     ---------calExpress")
                                        tempIndex = self.handle_evaluation(tokenTable, tempIndex, 0)
                                tempIndex1 = tempIndex + 1

                            else:
                                structure.append("     -------calExpress")
                                index = self.handle_evaluation(tokenTable, index + 1, 0)
                                tempIndex1 = index
                            n = self.match(self.variateList, tempExpress[0].word)
                            number = 1 + float(self.variateList[n].value)
                            self.variateList[n].value = str(number)
                        else:
                            break
            return tempIndex1

    def handle_while(self, tokenTable, start, structure):
        """
        处理while语句
        :param tokenTable:
        :param start:
        :return:
        """
        index = start + 1
        line = tokenTable[index].line
        tempExpress = []
        while 1:
            if index >= len(tokenTable):
                temp = error()
                temp.word = 'do'
                temp.line = line
                temp.errorType = 'lack'
                return index
            elif tokenTable[index].word == ';':
                temp = error()
                temp.word = 'do'
                temp.line = line
                temp.errorType = 'lack'
                return index + 1
            elif (tokenTable[index].word == 'do') | (tokenTable[index].line != line):
                break
            tempExpress.append(tokenTable[index])
            index += 1
        if tokenTable[index].word != 'do':
            temp = error()
            temp.word = 'do'
            temp.line = line
            temp.errorType = 'lack'
            return index
        else:
            sum = index
            tempExpress1 = []
            tempToken = []
            tempData = index + 1
            while 1:
                if tempData >= len(tokenTable):
                    break
                t = token()
                t.word = tokenTable[tempData].word
                t.line = tokenTable[tempData].line
                t.tokenValue = tokenTable[tempData].tokenValue
                t.wordtype = tokenTable[tempData].wordtype
                tempToken.append(t)
                tempData += 1
            for i in range(len(tempExpress)):
                temp = token()
                temp.word = tempExpress[i].word
                temp.tokenValue = tempExpress[i].tokenValue
                temp.line = tempExpress[i].line
                temp.wordtype = tempExpress[i].wordtype
                tempExpress1.append(temp)
            tempIndex1 = 0
            while 1:
                index = sum
                tempExpress = []
                for i in range(len(tempExpress1)):
                    temp = token()
                    temp.word = tempExpress1[i].word
                    temp.tokenValue = tempExpress1[i].tokenValue
                    temp.line = tempExpress1[i].line
                    temp.wordtype = tempExpress1[i].wordtype
                    tempExpress.append(temp)
                tempExpress = self.replace(tempExpress)
                if len(tempExpress) == 0:

                    while 1:
                        if index >= len(tokenTable):
                            return index
                        elif tokenTable[index].line != line:
                            return index
                        elif tokenTable[index].word == ';':
                            return index + 1
                        index += 1
                else:
                    tempExpress = self.simplifyBoolExpress(tempExpress)
                    if len(tempExpress) == 0:
                        while 1:
                            if index >= len(tokenTable):
                                return index
                            elif tokenTable[index].line != line:
                                return index
                            elif tokenTable[index].word == ';':
                                return index + 1
                            index += 1
                    else:
                        flag, value = self.boolExpress(tempExpress, 0, 0)
                        if flag == 1:
                            temp = error()
                            temp.word = 'express'
                            temp.line = line
                            temp.errorType = 'error'
                            self.errorList.append(temp)
                            while 1:
                                if index >= len(tokenTable):
                                    return index
                                elif tokenTable[index].line != line:
                                    return index
                                elif tokenTable[index].word == ';':
                                    return index + 1
                                index += 1
                        else:
                            if str(value) == 'True':
                                tempData = index + 1
                                n = 0
                                while 1:
                                    if n >= len(tempToken):
                                        break
                                    del tokenTable[tempData]
                                    n += 1
                                tempData = index + 1
                                n = 0
                                while 1:
                                    if n >= len(tempToken):
                                        break
                                    t = token()
                                    t.word = tempToken[n].word
                                    t.line = tempToken[n].line
                                    t.tokenValue = tempToken[n].tokenValue
                                    t.wordtype = tempToken[n].wordtype
                                    tokenTable.append(t)
                                    n += 1
                                if index > len(tokenTable) - 1:
                                    temp = error()
                                    temp.word = 'express'
                                    temp.line = tokenTable[index].line
                                    temp.errorType = 'lack'
                                    self.errorList.append(temp)
                                    return index

                                elif tokenTable[index + 1].word == 'begin':
                                    structure.append("     -------begin")
                                    tempIndex = index + 2
                                    while 1:
                                        if tempIndex >= len(tokenTable):
                                            temp = error()
                                            temp.word = 'end'
                                            temp.line = tokenTable[tempIndex - 1].line
                                            temp.errorType = 'lack'
                                            self.errorList.append(temp)
                                            return tempIndex

                                        elif tokenTable[tempIndex].word == 'end':
                                            tempIndex += 1
                                            if tempIndex >= len(tokenTable):
                                                temp = error()
                                                temp.word = '"."'
                                                temp.line = tokenTable[tempIndex - 1].line
                                                temp.errorType = 'lack'
                                                self.errorList.append(temp)
                                            elif tokenTable[tempIndex].word == '.':
                                                structure.append("     -------end.")
                                                break
                                            else:
                                                temp = error()
                                                temp.word = '"."'
                                                temp.line = tokenTable[tempIndex - 1].line
                                                temp.errorType = 'lack'
                                                self.errorList.append(temp)
                                                while 1:
                                                    if tempIndex >= len(tokenTable):
                                                        return tempIndex
                                                    elif tokenTable[tempIndex].line != line:
                                                        return tempIndex
                                                    elif tokenTable[tempIndex].word == ';':
                                                        return tempIndex + 1
                                                    tempIndex += 1
                                        elif tokenTable[tempIndex].word == 'if':
                                            structure.append("     ---------if")
                                            tempIndex = self.handle_if(tokenTable, tempIndex, structure)
                                        elif tokenTable[tempIndex].word == 'repeat':
                                            structure.append("     ---------repeat")
                                            tempIndex = self.handle_repeat(tokenTable, tempIndex, structure)
                                        elif tokenTable[tempIndex].word == 'for':
                                            structure.append("     ---------for")
                                            tempIndex = self.handle_for(tokenTable, tempIndex, structure)
                                        elif tokenTable[tempIndex].word == 'while':
                                            structure.append("     ---------while")
                                            tempIndex = self.handle_while(tokenTable, tempIndex, structure)
                                        else:
                                            structure.append("     ---------calExpress")
                                            tempIndex = self.handle_evaluation(tokenTable, tempIndex, 0)
                                    tempIndex1 = tempIndex + 1

                                else:
                                    structure.append("     -------calExpress")
                                    index = self.handle_evaluation(tokenTable, index + 1, 0)
                                    tempIndex1 = index
                            elif str(value) == 'False':
                                break
            return tempIndex1

    def copyList(self, list):
        """
        复制数组
        :param list1:
        :param list2:
        :return:
        """
        tempList = []
        for i in range(len(list)):
            temp = sign()
            temp.word = list[i].word
            temp.value = list[i].value
            temp.signType = list[i].signType
            tempList.append(temp)
        return tempList

    def splitByTo(self, list):
        """
        根据to将数组切分
        :param list:
        :return:
        """
        list1 = []
        list2 = []
        i = 0
        while 1:
            if i >= len(list):
                break
            elif list[i].word == 'to':
                break
            list1.append(list[i])
            i += 1
        if i == len(list):
            return list1, list2
        else:
            i += 1
            while 1:
                if i >= len(list):
                    break
                elif list[i].word == 'to':
                    break
                list2.append(list[i])
                i += 1
            return list1, list2
