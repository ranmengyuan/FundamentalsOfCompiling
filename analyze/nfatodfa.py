class nfa:
    """
    nfa
    """

    def __init__(self):
        self.start = 0
        self.end = 0
        self.operation = ''


class nfatodfa:
    """
    nfa->dfa
    """

    def __init__(self):
        self.index = 0
        self.start = 0
        self.end = 0
        self.nfaformula = []  # nfa
        self.element = []  # 元素
        self.dfastart = 0
        self.dfaend = []
        self.dfaformula = []  # dfa
        self.mfaformula = []  # mfa

    def verify(self, content):
        """
        验证正则式
        :return:
        """
        flag = 0
        index = 0
        if (content[index] != '(') & (content[index].isalpha() != 1) & (content[index].isdigit() != 1):
            return 0
        else:
            if content[index] == '(':
                flag += 1
            index += 1
            while 1:
                if flag < 0:
                    return 0
                elif index >= len(content) - 1:
                    return 1
                elif index == len(content) - 1:
                    if content[index] == ')':
                        flag -= 1
                    if flag != 0:
                        return 0
                    elif (content[index] != '*') & (content[index].isalpha() != 1) & (content[index].isdigit() != 1):
                        return 0
                    else:
                        return 1
                else:
                    if content[index] == '|':
                        if (content[index - 1] != '*') & (content[index - 1] != ')') & (
                                    content[index - 1].isalpha() != 1) & (content[index - 1].isdigit() != 1):
                            return 0
                        elif content[index - 1] == ')':
                            flag -= 1
                        elif (content[index + 1] != '(') & (content[index + 1].isalpha() != 1) & (
                                    content[index + 1].isdigit() != 1):
                            return 0
                        elif content[index + 1] == '(':
                            flag += 1
                    elif content[index] == '*':
                        if (content[index - 1] != ')') & (content[index - 1].isalpha() != 1) & (
                                    content[index - 1].isdigit() != 1):
                            return 0
                        elif content[index - 1] == ')':
                            flag -= 1
                        elif (content[index + 1] != '|') & (content[index + 1] != '(') & (
                                    content[index + 1].isalpha() != 1) & (
                                    content[index + 1].isdigit() != 1):
                            return 0
                        elif content[index + 1] == '(':
                            flag += 1
                    elif (content[index] != ')') & (content[index] != '(') & (content[index].isalpha() != 1) & (
                                content[index].isdigit() != 1):
                        return 0
                    index += 1

    def getindex(self, oper):
        """
        获得可以到达该点的点
        :return:
        """
        node = []
        for i in range(len(self.nfaformula)):
            if self.nfaformula[i].operation == oper:
                node.append(self.nfaformula[i].start)
        return node

    def calnfa(self, content):
        """
        计算nfa
        :param content:
        :return:
        """
        i = 0
        constart = 0
        conend = 0
        if (content[i].isalpha() == 1) | (content[i].isdigit() == 1):
            temp = nfa()
            temp.start = self.index
            self.index += 1
            temp.end = self.index
            temp.operation = content[i]
            self.nfaformula.append(temp)
            start = temp.start
            end = temp.end
            self.index += 1
        elif content[i] == '(':
            flag = 1
            i += 1
            formula = []
            while 1:
                if flag == 0:
                    break
                elif content[i] == ')':
                    flag -= 1
                elif content[i] == '(':
                    flag += 1
                else:
                    formula.append(content[i])
                i += 1
            i -= 1
            constart, conend = self.calnfa(formula)
            print(str(constart) + "\t" + str(conend))
            start = constart
            end = constart

        i += 1

        while 1:
            if i >= len(content):
                break
            elif (content[i].isalpha() == 1) | (content[i].isdigit() == 1):
                if (content[i - 1].isalpha() == 1) | (content[i - 1].isdigit() == 1):
                    temp = nfa()
                    temp.start = self.index - 1
                    temp.end = self.index
                    temp.operation = '#'
                    self.nfaformula.append(temp)
                elif (content[i - 1] == ')') | (content[i - 1] == '*'):
                    temp = nfa()
                    temp.start = conend
                    temp.end = self.index
                    temp.operation = '#'
                    self.nfaformula.append(temp)
                temp = nfa()
                temp.start = self.index
                self.index += 1
                temp.end = self.index
                temp.operation = content[i]
                self.nfaformula.append(temp)
                self.index += 1
                end = temp.end
            elif content[i] == '|':
                xuhao = i
                if (content[i + 1].isalpha() == 1) | (content[i + 1].isdigit() == 1):
                    n = self.nfaformula[-1].start
                    m = self.nfaformula[-1].end

                    temp = nfa()
                    temp.start = self.index
                    self.index += 1
                    temp.end = self.index
                    self.index += 1
                    temp.operation = content[i + 1]
                    self.nfaformula.append(temp)

                elif content[i + 1] == '(':
                    flag = 1
                    i += 2
                    formula = []
                    while 1:
                        if flag == 0:
                            break
                        elif content[i] == ')':
                            flag -= 1
                        elif content[i] == '(':
                            flag += 1
                        else:
                            formula.append(content[i])
                        i += 1
                    i -= 1
                    constart1, conend1 = self.calnfa(formula)

                if (content[xuhao - 1].isalpha() == 1) | (content[xuhao - 1].isdigit() == 1):
                    s = n
                    e = m
                elif (content[xuhao - 1] == ')') | (content[xuhao - 1] == '*'):
                    s = constart
                    e = conend

                if (content[xuhao + 1].isalpha() == 1) | (content[xuhao + 1].isdigit() == 1):

                    ss = self.nfaformula[-1].start
                    ee = self.nfaformula[-1].end
                elif content[xuhao + 1] == '(':
                    ss = constart1
                    ee = conend1

                temp = nfa()
                temp.start = self.index
                temp.end = s
                temp.operation = '#'
                self.nfaformula.append(temp)

                temp = nfa()
                temp.start = self.index
                self.index += 1
                start = temp.start
                temp.end = ss
                temp.operation = '#'
                self.nfaformula.append(temp)

                temp = nfa()
                temp.start = e
                temp.end = self.index
                end = temp.end
                temp.operation = '#'
                self.nfaformula.append(temp)

                temp = nfa()
                temp.start = ee
                temp.end = self.index
                self.index += 1
                temp.operation = '#'
                self.nfaformula.append(temp)
                i += 1
            elif content[i] == '*':
                if (content[i - 1].isalpha() == 1) | (content[i - 1].isdigit() == 1):
                    temp = nfa()
                    temp.start = self.index - 1
                    temp.end = self.index - 2
                    temp.operation = '#'
                    self.nfaformula.append(temp)

                    node = self.getindex(content[i - 1])
                    for k in range(len(node)):
                        temp = nfa()
                        temp.start = node[k]
                        temp.end = self.index
                        temp.operation = '#'
                        self.nfaformula.append(temp)
                    end = self.index
                    self.index += 1
                elif content[i - 1] == ')':
                    temp = nfa()
                    temp.start = conend
                    temp.end = constart
                    temp.operation = '#'
                    self.nfaformula.append(temp)

                    temp = nfa()
                    temp.start = self.index
                    start = temp.start
                    self.index += 1
                    temp.end = constart
                    temp.operation = '#'
                    self.nfaformula.append(temp)

                    temp = nfa()
                    temp.end = self.index
                    self.index += 1
                    temp.start = conend
                    end = temp.end
                    temp.operation = '#'
                    self.nfaformula.append(temp)

                    temp = nfa()
                    temp.start = self.index - 2
                    temp.end = self.index - 1
                    temp.operation = '#'
                    self.nfaformula.append(temp)
                    constart = self.index - 2
                    conend = self.index - 1
            i += 1
        return start, end

    def getElement(self, content):
        """
        获得正则式中的元素
        :param content:
        :return:
        """
        for i in range(len(content)):
            if (content[i].isdigit() == 1) | (content[i].isalpha() == 1):
                self.element.append(content[i])

    def formulatonfa(self, content):
        """
        将正则式转nfa
        :return:
        """
        self.index = 0
        self.start = 0
        self.end = 0
        self.nfaformula = []  # nfa
        self.start, self.end = self.calnfa(content)
        self.getElement(content)

    def getformelement(self, oper, ele):
        """
        获得一个元素可以到达的状态
        :param oper:
        :param ele:
        :return:
        """
        end = []
        for i in range(len(self.nfaformula)):
            if (self.nfaformula[i].start == ele) & (self.nfaformula[i].operation == oper):
                position = self.nfaformula[i].end
                end.append(position)
                empty = self.haveempty(position)
                for j in range(len(empty)):
                    end.append(empty[j])
                    temp = self.getformelement("#", empty[j])
                    for k in range(len(temp)):
                        end.append(temp[k])
        return end

    def haveempty(self, ele):
        """
        判断一个状态有没有不需条件就可到达的状态
        :param ele:
        :return:
        """
        end = []
        for i in range(len(self.nfaformula)):
            if (self.nfaformula[i].start == ele) & (self.nfaformula[i].operation == '#'):
                end.append(self.nfaformula[i].end)
        return end

    def isinlist(self, ele, list):
        """
        判断是否在链表中
        :param ele:
        :param list:
        :return:
        """
        for i in range(len(list)):
            if ele == list[i]:
                return 1
        return 0

    def gets(self, formI, form):
        """
        找到下一个结点
        :param formI:
        :param form:
        :return:
        """
        data = []
        for i in range(len(form)):
            for j in range(len(form[i])):
                if (len(form[i][j]) != 0) & (self.isinlist(form[i][j], formI) == 0):
                    return form[i][j]
        return data

    def getx(self, form, ele):
        """
        获得表中序号
        :param form:
        :param ele:
        :return:
        """
        for i in range(len(form)):
            if form[i] == ele:
                return i
        return -1

    def createform(self, content):
        """
        生成表
        :param content:
        :return:
        """
        self.formulatonfa(content)
        form = []
        formI = []
        s = self.getformelement('#', self.start)
        formI.append(s)
        while 1:
            formT = []
            for i in range(len(self.element)):
                formE = []
                for j in range(len(formI[-1])):
                    temp = self.getformelement(self.element[i], formI[-1][j])
                    for k in range(len(temp)):
                        formE.append(temp[k])

                formT.append(formE)
            form.append(formT)
            data = self.gets(formI, form)
            if len(data) == 0:
                break
            else:
                formI.append(data)
        for i in range(len(formI)):
            for j in range(len(formI[i])):
                if formI[i][j] == self.end:
                    self.dfaend.append(i)
            for j in range(len(self.element)):
                data = nfa()
                if len(form[i][j]) != 0:
                    index = self.getx(formI, form[i][j])
                    data.start = i
                    data.end = index
                    data.operation = self.element[j]
                    self.dfaformula.append(data)
        self.dfaend = list(set(self.dfaend))

    def createform1(self, formula, start, end):
        """
        生成表
        :param content:
        :return:
        """
        self.nfaformula = []
        for i in range(len(formula)):
            temp = nfa()
            temp.start = int(formula[i].start)
            temp.end = int(formula[i].end)
            temp.operation = formula[i].operation
            self.nfaformula.append(temp)
        self.start = int(start)
        self.end = int(end)
        for i in range(len(formula)):
            if (formula[i].operation.isdigit() == 1) | (formula[i].operation.isalpha() == 1):
                self.element.append(formula[i].operation)
        self.element = list(set(self.element))
        form = []
        formI = []
        s = self.getformelement('#', self.start)
        formI.append(s)
        s.append(self.start)
        while 1:
            formT = []
            for i in range(len(self.element)):
                formE = []
                for j in range(len(formI[-1])):
                    temp = self.getformelement(self.element[i], formI[-1][j])
                    for k in range(len(temp)):
                        formE.append(temp[k])
                formT.append(formE)
            # print(formI[-1])
            # print(formT)
            # print()
            form.append(formT)
            data = self.gets(formI, form)
            if len(data) == 0:
                break
            else:
                formI.append(data)
        for i in range(len(formI)):
            for j in range(len(formI[i])):
                if formI[i][j] == self.end:
                    self.dfaend.append(i)
            for j in range(len(self.element)):
                data = nfa()
                if len(form[i][j]) != 0:
                    index = self.getx(formI, form[i][j])
                    data.start = i
                    data.end = index
                    data.operation = self.element[j]
                    self.dfaformula.append(data)
        self.dfaend = list(set(self.dfaend))

    def topostion(self, ele, oper):
        """
        获得一个状态通过某条件到的状态
        :param ele:
        :param oper:
        :return:
        """
        temp = []
        for i in range(len(self.dfaformula)):
            if (self.dfaformula[i].start == ele) & (self.dfaformula[i].operation == oper):
                temp.append(self.dfaformula[i].end)
        return temp

    def septeparte(self, block, group, oper):
        """
        将一组的状态分开
        :param block:
        :param group:
        :param ele:
        :return:
        """
        data = []
        to = []
        leave = []
        for i in range(len(block)):
            temp = self.topostion(block[i], oper)
            if len(temp) == 0:
                to.append(block[i])
            else:
                flag = 0
                for j in range(len(temp)):
                    if temp[j] not in block:
                        to.append(block[i])
                        flag = 1
                        break
                if flag == 0:
                    leave.append(block[i])
        if len(to) != 0:
            data.append(to)
        if len(leave) != 0:
            data.append(leave)
        return data

    def dfatomfa(self, content):
        """
        最小化dfa
        :return:
        """
        self.createform(content)
        form = []
        temp = []
        position = []
        for i in range(len(self.dfaformula)):
            position.append(self.dfaformula[i].start)
            position.append(self.dfaformula[i].end)
        position = list(set(position))
        pos = []
        for i in range(len(position)):
            if position[i] not in self.dfaend:
                temp.append(position[i])
            elif position[i] == self.dfastart:
                temp.append(position[i])
        for i in range(len(self.dfaend)):
            if self.dfaend[i] != self.dfastart:
                pos.append(self.dfaend[i])
        if len(temp) != 0:
            form.append(temp)
        if len(pos) != 0:
            form.append(pos)
        while 1:
            flag = 0
            for k in range(len(self.element)):
                tempForm = []
                for i in range(len(form)):
                    if len(form[i]) != 1:
                        dfadata = self.septeparte(form[i], form, self.element[k])
                        if len(dfadata) != 1:
                            flag = 1
                            for j in range(len(dfadata)):
                                tempForm.append(dfadata[j])
                        else:
                            tempForm.append(form[i])
                    else:
                        tempForm.append(form[i])
                form.clear()
                for i in range(len(tempForm)):
                    form.append(tempForm[i])
            if flag == 0:
                break
        for n in range(len(self.dfaformula)):
            self.mfaformula.append(self.dfaformula[n])
        endindex1 = []
        for i in range(len(form)):
            if len(form[i]) == 1:
                if form[i][0] in self.dfaend:
                    endindex1.append(form[i][0])
            else:
                minu = min(form[i])
                for j in range(len(form[i])):
                    if form[i][j] in self.dfaend:
                        endindex1.append(minu)
                for n in range(len(self.mfaformula)):
                    if self.mfaformula[n].start in form[i]:
                        self.mfaformula[n].start = minu
                    if self.mfaformula[n].end in form[i]:
                        self.mfaformula[n].end = minu

        self.dfaend = []
        for i in range(len(endindex1)):
            self.dfaend.append(endindex1[i])
        self.dfaend = list(set(self.dfaend))
        re = []
        for i in range(len(self.mfaformula)):
            if self.isExit(self.mfaformula[i], re) == 0:
                re.append(self.mfaformula[i])
        self.mfaformula = []
        for i in range(len(re)):
            self.mfaformula.append(re[i])

    def dfatomfa1(self, formula, start, end):
        """
        最小化dfa
        :return:
        """
        self.dfaformula = []
        for i in range(len(formula)):
            temp = nfa()
            temp.start = int(formula[i].start)
            temp.end = int(formula[i].end)
            temp.operation = formula[i].operation
            self.dfaformula.append(temp)
        self.dfastart = int(start)
        for i in range(len(end)):
            self.dfaend.append(int(end[i]))
        for i in range(len(formula)):
            if (formula[i].operation.isdigit() == 1) | (formula[i].operation.isalpha() == 1):
                self.element.append(formula[i].operation)
        self.element = list(set(self.element))

        form = []
        temp = []
        position = []
        for i in range(len(self.dfaformula)):
            position.append(self.dfaformula[i].start)
            position.append(self.dfaformula[i].end)
        position = list(set(position))
        pos = []
        for i in range(len(position)):
            if position[i] not in self.dfaend:
                temp.append(position[i])
            elif position[i] == self.dfastart:
                temp.append(position[i])
        for i in range(len(self.dfaend)):
            if self.dfaend[i] != self.dfastart:
                pos.append(self.dfaend[i])
        if len(temp) != 0:
            form.append(temp)
        if len(pos) != 0:
            form.append(pos)
        while 1:
            flag = 0
            for k in range(len(self.element)):
                tempForm = []
                for i in range(len(form)):
                    if len(form[i]) != 1:
                        dfadata = self.septeparte(form[i], form, self.element[k])
                        if len(dfadata) != 1:
                            flag = 1
                            for j in range(len(dfadata)):
                                tempForm.append(dfadata[j])
                        else:
                            tempForm.append(form[i])
                    else:
                        tempForm.append(form[i])
                form.clear()
                for i in range(len(tempForm)):
                    form.append(tempForm[i])
            if flag == 0:
                break
        for n in range(len(self.dfaformula)):
            self.mfaformula.append(self.dfaformula[n])
        endindex1 = []
        # print(form)
        for i in range(len(form)):
            if len(form[i]) == 1:
                if form[i][0] in self.dfaend:
                    endindex1.append(form[i][0])
            else:
                minu = min(form[i])
                for j in range(len(form[i])):
                    if form[i][j] in self.dfaend:
                        endindex1.append(minu)
                for n in range(len(self.mfaformula)):
                    if self.mfaformula[n].start in form[i]:
                        self.mfaformula[n].start = minu
                    if self.mfaformula[n].end in form[i]:
                        self.mfaformula[n].end = minu

        self.dfaend = []
        for i in range(len(endindex1)):
            self.dfaend.append(endindex1[i])
        self.dfaend = list(set(self.dfaend))
        re = []
        for i in range(len(self.mfaformula)):
            if self.isExit(self.mfaformula[i], re) == 0:
                re.append(self.mfaformula[i])
        self.mfaformula = []
        for i in range(len(re)):
            self.mfaformula.append(re[i])

    def isExit(self, data, group):
        """
        判断是否存在
        :param data:
        :return:
        """
        for i in range(len(group)):
            if (data.start == group[i].start) & (data.operation == group[i].operation) & (data.end == group[i].end):
                return 1
        return 0
