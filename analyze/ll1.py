class relationship:
    """
    关系
    """

    def __init__(self):
        self.word = ''
        self.result = []


class form:
    """
    表格
    """

    def __init__(self):
        self.word = ''
        self.formula = ''
        self.result = []


class process:
    """
    分析过程
    """

    def __init__(self):
        self.no = 1
        self.ana = ''
        self.input = ''
        self.formula = ''


class ll1:
    """
    ll1
    """

    def __init__(self):
        self.vn = []  # 非终结符
        self.vt = []  # 终结符
        self.relation = []  # 关系
        self.firstGroup = []  # first集
        self.followGroup = []  # follow集
        self.form = []  # 分析表

    def sep(self, contents):
        for content in contents:
            temp = relationship()
            result = content.split("->")
            self.vn.append(result[0])
            temp.word = result[0]
            result1 = result[1].split("|")
            for i in range(len(result1)):
                temp.result.append(result1[i])
            self.relation.append(temp)
        self.getvt()

    def getvt(self):
        """
        获得终结符
        :return:
        """
        for i in range(len(self.relation)):
            for j in range(len(self.relation[i].result)):
                data = self.relation[i].result[j]
                for k in range(len(data)):
                    if (self.replace(data[k], self.vt) == 0) & (self.replace(data[k], self.vn) == 0):
                        self.vt.append(data[k])

    def replace(self, c, group):
        """
        判断是否在集合中出现
        :param c:
        :param group:
        :return:
        """
        for i in range(len(group)):
            if c == group[i]:
                return 1
        return 0

    def calfirst(self, ele):
        """
        计算first集
        :param ele:
        :return:
        """
        index = self.getIndex(ele)
        result = []
        for i in range(len(self.relation[index].result)):
            data = self.relation[index].result[i][0]
            if (data == '$') | (self.isVt(data) == 1):
                result.append(data)
            else:
                temp = self.calfirst(data)
                for k in range(len(temp)):
                    result.append(temp[k])
        return result

    def calfollow(self, ele, flag):
        """
        计算follow集
        :param ele:
        :return:
        """
        result = []
        if flag == 0:
            result.append('#')
        temp = self.getFollow(ele)
        for data in temp:
            if data.result == '$':
                if ele != data.word:
                    if data.word == self.vn[0]:
                        val = self.calfollow(data.word, 0)
                    else:
                        val = self.calfollow(data.word, 1)
                    for n in val:
                        result.append(n)
            else:
                if self.isVt(data.result) == 1:
                    result.append(data.result)
                else:
                    flag, leng = self.toEmpty(data.result)
                    if flag == 1:
                        if leng != 1:
                            val = self.calfirst(data.result)
                            for n in val:
                                if n != '$':
                                    result.append(n)
                        if ele != data.word:
                            if data.word == self.vn[0]:
                                val = self.calfollow(data.word, 0)
                            else:
                                val = self.calfollow(data.word, 1)
                            for n in val:
                                result.append(n)

                    else:
                        val = self.calfirst(data.result)
                        for n in val:
                            if n != '$':
                                result.append(n)
        return result

    def toEmpty(self, data):
        """
        判断是否可以退出空
        :param data:
        :return:
        """
        for n in self.relation:
            if n.word == data:
                for m in n.result:
                    if m == '$':
                        return 1, len(n.result)
        return 0, -1

    def getFollow(self, ele):
        """
        根据句子后的元素后面的符号
        :param ele:
        :param sen:
        :return:
        """
        temp = []
        for m in self.relation:
            for n in m.result:
                index = n.find(ele)
                if index != -1:
                    x = relationship()
                    if index == len(n) - 1:
                        x.word = m.word
                        x.result = '$'
                    else:
                        x.word = m.word
                        x.result = n[index + 1]
                    temp.append(x)
        return temp

    def getIndex(self, ele):
        """
        获得符号的序号
        :param ele:
        :return:
        """
        for i in range(len(self.relation)):
            if self.relation[i].word == ele:
                return i
        return 0

    def isVt(self, ele):
        """
        判断是否是终结符
        :param ele:
        :return:
        """
        for con in self.vt:
            if con == ele:
                return 1
        return 0

    def first(self, contents):
        """
        获得first集
        :return:
        """
        self.sep(contents)
        for i in range(len(self.vn)):
            temp = relationship()
            temp.word = self.vn[i]
            temp.result = self.calfirst(self.vn[i])
            self.firstGroup.append(temp)

    def follow(self, contents):
        """
        获得follow集
        :param contents:
        :return:
        """
        self.sep(contents)
        for i in range(len(self.vn)):
            temp = relationship()
            temp.word = self.vn[i]
            if i == 0:
                temp.result = self.calfollow(self.vn[i], 0)
            else:
                temp.result = self.calfollow(self.vn[i], 1)
            temp.result = list(set(temp.result))
            self.followGroup.append(temp)
            print()
            for n in temp.result:
                print(n)
            print()

    def createform(self, contents):
        """
        获得分析表
        :param contetns:
        :return:
        """
        self.sep(contents)
        for i in range(len(self.relation)):
            for j in range(len(self.relation[i].result)):
                temp = form()
                temp.word = self.relation[i].word
                temp.formula = self.relation[i].word + "->" + self.relation[i].result[j]
                if self.relation[i].result[j] == '$':
                    if temp.word == self.vn[0]:
                        temp.result = self.calfollow(self.relation[i].word, 0)
                    else:
                        temp.result = self.calfollow(self.relation[i].word, 1)
                else:
                    if self.isVt(self.relation[i].result[j][0]) == 1:
                        temp.result.append(self.relation[i].result[j][0])
                    else:
                        temp.result = self.calfirst(self.relation[i].word)
                self.form.append(temp)

    def getFormula(self, word, result):
        """
        获得式子
        :param word:
        :param result:
        :return:
        """
        for i in range(len(self.form)):
            if self.form[i].word == word:
                for j in range(len(self.form[i].result)):
                    if self.form[i].result[j] == result:
                        return self.form[i].formula
        return '-1'

    def analyze(self, contents, input):
        """
        进行分析
        :param contents:
        :param input:
        :return:
        """
        self.createform(contents)
        start = '#' + self.vn[0]
        input = input + '#'
        index = 1
        pro = []
        while 1:
            temp = process()
            temp.no = index
            temp.ana = start
            temp.input = input
            if input == '#':
                if start == '#':
                    temp.formula = 'accept'
                    pro.append(temp)
                    return pro
                else:
                    formula = self.getFormula(start[-1], input[0])
                    if formula == '-1':
                        temp.formula = 'refuse'
                        pro.append(temp)
                        return pro
                    else:
                        temp.formula = formula
                        pro.append(temp)
                        start = start[:-1]

            elif start == '#':
                temp.formula = 'refuse'
                pro.append(temp)
                return pro
            elif start[-1] == input[0]:
                temp.formula = start[-1] + ' match'
                pro.append(temp)
                start = start[:-1]
                input = input[:0] + input[1:]
            else:
                formula = self.getFormula(start[-1], input[0])
                if formula == '-1':
                    temp.formula = 'refuse'
                    pro.append(temp)
                    return pro
                else:
                    temp.formula = formula
                    pro.append(temp)
                    n = formula.split('->')
                    start = start[:-1]
                    if n[1] != '$':
                        start = start + n[1][::-1]
            index += 1
