import sys
from PyQt5.QtWidgets import QPlainTextEdit, QAction, QApplication, QMainWindow, qApp, QTabWidget, QGridLayout, QWidget \
    , QFileDialog, QMessageBox, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QTableWidget, \
    QTableWidgetItem
from PyQt5.QtGui import QIcon
from analyze.lexicalAnalyze import participle, creatToken, isRepate, token
from analyze.grammaticalAnalyze import gramma
from analyze.middleProduce import middle
from analyze.ll1 import ll1
from analyze.nfatodfa import nfatodfa
from analyze.nfatodfa import nfa


class exp(QMainWindow):
    fileName = ''
    content = []
    error = 1

    def __init__(self):
        super().__init__()
        self.initUI()
        self.tokenTable = []

    def initUI(self):
        # 定义动作
        exitAct = QAction(QIcon('//Volumes//Transcend//Python//fundamentalsOfCompiling//3.png'), 'Open', self)
        exitAct.setShortcut('Ctrl+O')
        exitAct.setStatusTip('Open a file')
        exitAct.triggered.connect(self.openFile)

        exitAct7 = QAction(QIcon('//Volumes//Transcend//Python//fundamentalsOfCompiling//8.png'), 'New', self)
        exitAct7.setShortcut('Ctrl+N')
        exitAct7.setStatusTip('Create a new file')
        exitAct7.triggered.connect(self.newFile)

        exitAct1 = QAction(QIcon('//Volumes//Transcend//Python//fundamentalsOfCompiling//1.png'), 'Save', self)
        exitAct1.setShortcut('Ctrl+S')
        exitAct1.setStatusTip('Save')
        exitAct1.triggered.connect(self.saveFile)

        exitAct2 = QAction(QIcon('//Volumes//Transcend//Python//fundamentalsOfCompiling//4.png'), 'Revocation', self)
        exitAct2.setShortcut('Ctrl+Z')
        exitAct2.setStatusTip('Back to the previous step')
        exitAct2.triggered.connect(qApp.quit)

        exitAct3 = QAction(QIcon('//Volumes//Transcend//Python//fundamentalsOfCompiling//5.png'), 'Copy', self)
        exitAct3.setShortcut('Ctrl+C')
        exitAct3.setStatusTip('Copy')
        exitAct3.triggered.connect(self.copyText)

        exitAct4 = QAction(QIcon('//Volumes//Transcend//Python//fundamentalsOfCompiling//6.png'), 'Cut', self)
        exitAct4.setShortcut('Ctrl+X')
        exitAct4.setStatusTip('Cut')
        exitAct4.triggered.connect(qApp.quit)

        exitAct5 = QAction(QIcon('//Volumes//Transcend//Python//fundamentalsOfCompiling//2.png'), 'Help', self)
        exitAct5.setShortcut('Ctrl+H')
        exitAct5.setStatusTip('Help')
        exitAct5.triggered.connect(qApp.quit)

        exitAct6 = QAction(QIcon('//Volumes//Transcend//Python//fundamentalsOfCompiling//7.png'), 'Exit', self)
        exitAct6.setShortcut('Ctrl+Q')
        exitAct6.setStatusTip('Press to quit')
        exitAct6.triggered.connect(qApp.quit)

        exitAct8 = QAction('LexicalAnalyze', self)
        exitAct8.setShortcut('Ctrl+L')
        exitAct8.triggered.connect(self.lexianlyze)

        exitAct9 = QAction('GrammaticAnalyze', self)
        exitAct9.setShortcut('Ctrl+G')
        exitAct9.triggered.connect(self.grammaAnalyze)

        exitAct10 = QAction('MiddleCode', self)
        exitAct10.setShortcut('Ctrl+M')
        exitAct10.triggered.connect(self.middle)

        exitAct11 = QAction('LL1', self)
        exitAct11.setShortcut('Ctrl+L')
        exitAct11.triggered.connect(self.ll1)

        exitAct12 = QAction('NFA-DFA-MFA', self)
        exitAct12.setShortcut('Ctrl+T')
        exitAct12.triggered.connect(self.nfadfa)

        # 设置菜单栏
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&文件')
        fileMenu.addAction(exitAct)
        fileMenu.addAction(exitAct7)
        fileMenu.addAction(exitAct1)
        fileMenu.addAction(exitAct5)
        fileMenu.addAction(exitAct6)

        editMenu = menuBar.addMenu('&编辑')
        editMenu.addAction(exitAct1)

        morophologyMenu = menuBar.addMenu('&词法分析')
        morophologyMenu.addAction(exitAct8)
        morophologyMenu.addAction(exitAct12)

        grammaMenu = menuBar.addMenu('&语法分析')
        grammaMenu.addAction(exitAct9)
        grammaMenu.addAction(exitAct11)

        middleMenu = menuBar.addMenu('&中间代码')
        middleMenu.addAction(exitAct10)

        targetMenu = menuBar.addMenu('&目标代码生成')
        targetMenu.addAction(exitAct)

        checkMenu = menuBar.addMenu('&查看')
        checkMenu.addAction(exitAct)

        helpMenu = menuBar.addMenu('&帮助')
        helpMenu.addAction(exitAct5)

        self.statusBar()

        tbar = self.addToolBar('Open')
        tbar.addAction(exitAct)

        tbar7 = self.addToolBar('New')
        tbar7.addAction(exitAct7)

        tbar1 = self.addToolBar('Save')
        tbar1.addAction(exitAct1)

        tbar2 = self.addToolBar('Revocation')
        tbar2.addAction(exitAct2)

        tbar3 = self.addToolBar('Copy')
        tbar3.addAction(exitAct3)

        tbar4 = self.addToolBar('Cut')
        tbar4.addAction(exitAct4)

        tbar5 = self.addToolBar('Help')
        tbar5.addAction(exitAct5)

        tbar6 = self.addToolBar('Exit')
        tbar6.addAction(exitAct6)

        # 文本框
        self.result = QPlainTextEdit()
        self.result.setReadOnly(False)

        # 选项卡
        tabWidget = QTabWidget(self)
        tabWidget.setTabPosition(QTabWidget.South)
        self.w1 = QPlainTextEdit()
        self.w1.setReadOnly(True)

        self.w2 = QPlainTextEdit()
        self.w2.setReadOnly(True)

        self.w3 = QPlainTextEdit()
        self.w3.setReadOnly(True)

        self.w4 = QPlainTextEdit()
        self.w4.setReadOnly(True)

        tabWidget.addTab(self.w1, "Token表")
        tabWidget.addTab(self.w2, "符号表")
        tabWidget.addTab(self.w3, "错误列表")
        tabWidget.addTab(self.w4, "程序结构")

        btnLayout = QGridLayout()
        btnLayout.addWidget(self.result, 1, 0)
        btnLayout.addWidget(tabWidget, 1, 1)

        back = QWidget()
        back.setLayout(btnLayout)
        self.setCentralWidget(back)

        # rightMenu = QMenu()
        # rightMenu.addAction(exitAct)
        # rightMenu.exec_(QCursor.pos())

        self.setGeometry(200, 200, 1000, 800)
        self.setWindowTitle('编译原理分析系统')
        self.show()

    def openFile(self):
        """
        打开文件
        :return:
        """
        try:
            name = self.fileName
            self.fileName, filetype = QFileDialog.getOpenFileName(self, "选取文件", "/Volumes/Transcend", "All Files (*);"
                                                                                                      ";Text Files (*.txt);"
                                                                                                      ";C Files (*.c);"
                                                                                                      ";JAVA Files (*.java);"
                                                                                                      ";Python Files(*.py)")
            self.result.clear()
            # 设置文件扩展名过滤,注意用双分号间隔
            self.fileName = '//Volumes//Transcend//文件//编译原理//sample2的副本 2.txt'
            file = open(self.fileName)
            n = 0
            while 1:
                lines = file.readlines(100000)
                if not lines:
                    break
                for line in lines:
                    n += 1
                    self.content.append(line.replace("\n", ""))  # 去掉每一行的换行符
                    self.result.appendPlainText(line.replace("\n", ""))
        except Exception as e:
            print(e)
            self.fileName = name

    def saveFile(self):
        """
        保存文件
        :return:
        """
        try:
            if self.fileName == '':
                name = self.fileName
                self.fileName, ok2 = QFileDialog.getSaveFileName(self, "文件保存", "C:/", "All Files (*);"
                                                                                      ";Text Files (*.txt);"
                                                                                      ";C Files (*.c);"
                                                                                      ";JAVA Files (*.java);"
                                                                                      ";Python Files (*.py)")
            fileContent = self.result.toPlainText()
            file = open(self.fileName, "w+")
            file.write(fileContent)
            file = open(self.fileName)
            self.content = []
            while 1:
                lines = file.readlines(100000)
                if not lines:
                    break
                for line in lines:
                    self.content.append(line.replace("\n", ""))
        except Exception as e:
            print(e)
            self.fileName = name

    def newFile(self):
        """
        新建文件
        :return:
        """
        self.saveFile()
        self.content = []
        self.fileName = ''
        self.result.clear()
        self.w1.clear()
        self.w2.clear()
        self.w3.clear()

    def copyText(self):
        clipboard = QApplication.clipboard()

    def lexianlyze(self):
        """
        词法分析
        :return:
        """
        self.tokenTable = []
        self.w1.clear()
        self.w2.clear()
        self.w3.clear()
        self.w4.clear()
        try:
            if len(self.content) == 0:
                QMessageBox.warning(self, "Warning", "程序为空", QMessageBox.Yes)  # 弹出警告框
            else:
                self.w1.appendPlainText("---------------------------------Token表-------------------------------")
                self.w2.appendPlainText("---------------------------------符号表---------------------------- ----")
                self.w3.appendPlainText("---------------------------------错误列表-------------------------------")
                self.w4.appendPlainText("---------------------------------程序结构-------------------------------")
                remark = 0
                remarkContent = []
                name = []
                for i in range(len(self.content)):
                    flag1 = 0
                    flag2 = 0
                    flag3 = 0
                    words, exceptData, remark, self.remarkContent = participle(self.content[i], remark, remarkContent)
                    for j in range(len(words)):
                        temp = token()
                        if words[j] == '(':
                            flag1 = 1
                            data = creatToken(words[j])
                            self.w1.appendPlainText(words[j] + '\t' + str(data.index))
                            temp.word = words[j]
                            temp.tokenValue = data.index
                            temp.line = i
                            temp.wordtype = data.wordtype
                            self.tokenTable.append(temp)
                        elif words[j] == ')':
                            if flag1 == 1:
                                data = creatToken(words[j])
                                self.w1.appendPlainText(words[j] + '\t' + str(data.index))
                                temp.word = words[j]
                                temp.tokenValue = data.index
                                temp.line = i
                                temp.wordtype = data.wordtype
                                self.tokenTable.append(temp)
                            else:
                                self.w3.appendPlainText(
                                        "Error:\t\" " + words[j] + " \" can't match,\tline" + str(i + 1))
                        elif words[j] == '/*':
                            flag2 = 1
                        elif words[j] == '*/':
                            if flag2 == 0:
                                self.w3.appendPlainText(
                                        "Error:\t\" " + words[j] + " \" can't match,\tline" + str(i + 1))
                        else:
                            data = creatToken(words[j])
                            if (words[j][0] == '\'') & (len(words[j]) == 3):
                                self.w1.appendPlainText(words[j][1] + '\t' + str(data.index))
                                temp.word = words[j][1]
                                temp.tokenValue = data.index
                                temp.line = i
                                temp.wordtype = data.wordtype
                                self.tokenTable.append(temp)
                            else:
                                self.w1.appendPlainText(words[j] + '\t' + str(data.index))
                                temp.word = words[j]
                                temp.tokenValue = data.index
                                temp.line = i
                                temp.wordtype = data.wordtype
                                self.tokenTable.append(temp)
                                if ((data.wordtype == 'identifier') | (data.wordtype == 'const')) & (
                                            isRepate(name, words[j]) == 0):
                                    self.w2.appendPlainText(
                                            words[j] + '\t' + str(len(words[j])) + '\t' + str(
                                                    data.index) + '\t' + data.wordtype)
                    for j in range(len(exceptData)):
                        self.w3.appendPlainText("Error:\t\" " + exceptData[j] + " \" is Unknown,\tline" + str(i + 1))
                    if len(exceptData) != 0:
                        flag3 = 1
                if flag3 == 0:
                    self.w3.appendPlainText("Warining 0\tError 0.")
        except Exception as e:
            print(e)

    def grammaAnalyze(self):
        """
        语法分析
        :return:
        """
        if (len(self.tokenTable) == 0) & (len(self.remarkContent) == 0):
            QMessageBox.warning(self, "Warning", "请先完成词法分析", QMessageBox.Yes)  # 弹出警告框
        else:
            deal = gramma()
            tempToken = []
            for i in range(len(self.tokenTable)):
                temp = token()
                temp.word = self.tokenTable[i].word
                temp.line = self.tokenTable[i].line
                temp.tokenValue = self.tokenTable[i].tokenValue
                temp.wordtype = self.tokenTable[i].wordtype
                tempToken.append(temp)

            deal.grammaDeal(tempToken)
            self.w2.clear()
            self.w3.clear()
            self.w4.clear()
            self.w2.appendPlainText("---------------------------------符号表---------------------------- ----")
            self.w3.appendPlainText("---------------------------------错误列表-------------------------------")
            self.w4.appendPlainText("---------------------------------程序结构-------------------------------")
            if len(deal.errorList) == 0:
                self.w3.appendPlainText("Warining 0\tError 0.")
                self.error = 0
            else:
                for i in range(len(deal.errorList)):
                    self.w3.appendPlainText(
                            'Error:\t' + deal.errorList[i].errorType + '  \"' + deal.errorList[i].word + '\",\tline' +
                            str(deal.errorList[i].line))
            for i in range(len(deal.constantList)):
                temp = deal.constantList[i].word + '\t' + deal.constantList[i].value + '\t' + deal.constantList[
                    i].signType + '\tconstant'
                self.w2.appendPlainText(temp)
            for i in range(len(deal.variateList)):
                temp = deal.variateList[i].word + '\t' + deal.variateList[i].value + '\t' + deal.variateList[
                    i].signType + '\tvariate'
                self.w2.appendPlainText(temp)
            for i in range(len(deal.structure)):
                self.w4.appendPlainText(deal.structure[i])

    def middle(self):
        """
        中间代码生成
        :return:
        """
        # if self.error == 1:
        #     QMessageBox.warning(self, "Warning", "代码存在错误", QMessageBox.Yes)  # 弹出警告框
        # else:
        self.w4.clear()
        self.w4.appendPlainText("No\top\targ1\targs2\tresult")
        deal = middle()

        tempToken = []
        for i in range(len(self.tokenTable)):
            temp = token()
            temp.word = self.tokenTable[i].word
            temp.line = self.tokenTable[i].line
            temp.tokenValue = self.tokenTable[i].tokenValue
            temp.wordtype = self.tokenTable[i].wordtype
            tempToken.append(temp)

        deal.middleDeal(tempToken)
        for i in range(len(deal.structure)):
            self.w4.appendPlainText(
                    str(deal.structure[i].no) + "\t" + deal.structure[i].op + "\t" + deal.structure[
                        i].args1 + "\t" + deal.structure[i].args2 + "\t" + deal.structure[i].result)

    def ll1(self):
        """
        ll1算法
        :return:
        """
        self.llwindow = slaveWindow()
        self.llwindow.show()

    def nfadfa(self):
        self.nfawindow = nfaWindow()
        self.nfawindow.show()


class slaveWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.fileName = ''
        self.content = []
        self.index = 0
        self.pro = []

    def initUI(self):
        self.openButton = QPushButton(self)
        self.openButton.setText("Open File")
        self.openButton.clicked.connect(self.openFile)

        self.result = QPlainTextEdit()
        self.result.setReadOnly(False)

        self.fristButton = QPushButton(self)
        self.fristButton.setText("First")
        self.fristButton.clicked.connect(self.first)

        self.firstText = QTableWidget()

        self.followButton = QPushButton(self)
        self.followButton.setText("Follow")
        self.followButton.clicked.connect(self.follow)

        self.followText = QTableWidget()

        btnLayout = QVBoxLayout()
        btnLayout.addWidget(self.openButton)
        btnLayout.addWidget(self.result)
        btnLayout.addWidget(self.fristButton)
        btnLayout.addWidget(self.firstText)
        btnLayout.addWidget(self.followButton)
        btnLayout.addWidget(self.followText)

        self.formButton = QPushButton(self)
        self.formButton.setText("Form")
        self.formButton.clicked.connect(self.createform)

        self.formText = QTableWidget()

        nameLabel = QLabel("Sentence")
        self.inputText = QLineEdit()
        self.inputText.setReadOnly(False)

        self.resultButton = QPushButton(self)
        self.resultButton.setText("Result")
        self.resultButton.clicked.connect(self.process)

        self.singleButton = QPushButton(self)
        self.singleButton.setText("Single Step")
        self.singleButton.clicked.connect(self.process_single)

        self.resultText = QTableWidget()

        sentence = QHBoxLayout()
        sentence.addWidget(nameLabel)
        sentence.addWidget(self.inputText)

        qhbtn = QHBoxLayout()
        qhbtn.addWidget(self.resultButton)
        qhbtn.addWidget(self.singleButton)

        qvbtn = QVBoxLayout()
        qvbtn.addWidget(self.formButton)
        qvbtn.addWidget(self.formText)
        inp = QWidget()
        inp.setLayout(sentence)
        qvbtn.addWidget(inp)
        select = QWidget()
        select.setLayout(qhbtn)
        qvbtn.addWidget(select)
        qvbtn.addWidget(self.resultText)

        left = QWidget()
        left.setLayout(btnLayout)
        right = QWidget()
        right.setLayout(qvbtn)

        backbtn = QHBoxLayout()
        backbtn.addWidget(left)
        backbtn.addWidget(right)

        back = QWidget()
        back.setLayout(backbtn)
        self.setCentralWidget(back)
        self.setGeometry(300, 200, 800, 600)
        self.setWindowTitle('LL1算法')
        self.show()

    def openFile(self):
        """
        打开文件
        :return:
        """
        try:
            name = self.fileName
            self.fileName, filetype = QFileDialog.getOpenFileName(self, "选取文件", "/Volumes/Transcend", "All Files (*);"
                                                                                                      ";Text Files (*.txt);"
                                                                                                      ";C Files (*.c);"
                                                                                                      ";JAVA Files (*.java);"
                                                                                                      ";Python Files(*.py)")
            self.result.clear()
            # 设置文件扩展名过滤,注意用双分号间隔
            self.fileName = '//Volumes//Transcend//文件//编译原理//LL1_1.TXT'
            file = open(self.fileName)
            n = 0
            while 1:
                lines = file.readlines(100000)
                if not lines:
                    break
                for line in lines:
                    n += 1
                    self.content.append(line.replace("\n", ""))  # 去掉每一行的换行符
                    self.result.appendPlainText(line.replace("\n", ""))
        except Exception as e:
            print(e)
            self.fileName = name

    def getIndex(self, group, ele):
        """
        获得元素的序号
        :param group:
        :param ele:
        :return:
        """
        for i in range(len(group)):
            if group[i] == ele:
                return i
        return -1

    def first(self):
        """
        first集
        :return:
        """
        if len(self.content) == 0:
            QMessageBox.warning(self, "Warning", "请先打开文件", QMessageBox.Yes)  # 弹出警告框
        else:
            deal = ll1()
            deal.first(self.content)
            self.firstText.setColumnCount(len(deal.vt))
            self.firstText.setRowCount(len(deal.vn))
            for i in range(len(deal.vt)):
                self.firstText.setColumnWidth(i, 40)
            for i in range(len(deal.vn)):
                self.firstText.setRowHeight(i, 20)
            self.firstText.setHorizontalHeaderLabels(deal.vt)
            self.firstText.setVerticalHeaderLabels(deal.vn)
            for i in range(len(deal.firstGroup)):
                for j in range(len(deal.firstGroup[i].result)):
                    index = self.getIndex(deal.vt, deal.firstGroup[i].result[j])
                    self.firstText.setItem(i, index, QTableWidgetItem("1"))

    def follow(self):
        """
        follow集
        :return:
        """
        if len(self.content) == 0:
            QMessageBox.warning(self, "Warning", "请先打开文件", QMessageBox.Yes)  # 弹出警告框
        else:
            deal = ll1()
            deal.follow(self.content)
            t = []
            for m in deal.vt:
                if m == '$':
                    t.append("#")
                else:
                    t.append(m)
            self.followText.setColumnCount(len(deal.vt))
            self.followText.setRowCount(len(deal.vn))
            for i in range(len(t)):
                self.followText.setColumnWidth(i, 40)
            for i in range(len(deal.vn)):
                self.followText.setRowHeight(i, 20)
            self.followText.setHorizontalHeaderLabels(t)
            self.followText.setVerticalHeaderLabels(deal.vn)
            for i in range(len(deal.followGroup)):
                for j in range(len(deal.followGroup[i].result)):
                    index = self.getIndex(t, deal.followGroup[i].result[j])
                    self.followText.setItem(i, index, QTableWidgetItem("1"))

    def createform(self):
        """
        分析表
        :return:
        """
        if len(self.content) == 0:
            QMessageBox.warning(self, "Warning", "请先打开文件", QMessageBox.Yes)  # 弹出警告框
        else:
            deal = ll1()
            deal.createform(self.content)
            t = []
            for m in deal.vt:
                if m == '$':
                    t.append("#")
                else:
                    t.append(m)
            self.formText.setColumnCount(len(deal.vt))
            self.formText.setRowCount(len(deal.vn))
            for i in range(len(t)):
                self.formText.setColumnWidth(i, 60)
            for i in range(len(deal.vn)):
                self.formText.setRowHeight(i, 20)
            self.formText.setHorizontalHeaderLabels(t)
            self.formText.setVerticalHeaderLabels(deal.vn)
            for i in range(len(deal.form)):
                for j in range(len(deal.form[i].result)):
                    index = self.getIndex(t, deal.form[i].result[j])
                    m = self.getIndex(deal.vn, deal.form[i].word)
                    self.formText.setItem(m, index, QTableWidgetItem(deal.form[i].formula))

    def analzell1(self):
        """
        通过分析表进行句子分析
        :return:
        """
        fileContent = self.inputText.text()
        # print(fileContent[::-1])
        # print(fileContent[:-1])
        if len(self.content) == 0:
            QMessageBox.warning(self, "Warning", "请先打开文件", QMessageBox.Yes)  # 弹出警告框
        else:
            deal = ll1()
            self.pro = deal.analyze(self.content, fileContent)
            t = []
            for m in deal.vt:
                if m == '$':
                    t.append("#")
                else:
                    t.append(m)
            self.resultText.setColumnCount(4)
            self.resultText.setRowCount(len(self.pro))
            for i in range(4):
                self.resultText.setColumnWidth(i, 120)
            for i in range(len(self.pro)):
                self.resultText.setRowHeight(i, 20)
            self.resultText.setHorizontalHeaderLabels(['编号', '分析栈', '剩余输入串', '推导所用产生式'])

    def process(self):
        """
        输出分析表过程
        :param content:
        :return:
        """
        self.analzell1()
        i = self.index
        while 1:
            if i >= len(self.pro):
                break
            self.resultText.setItem(i, 0, QTableWidgetItem(str(self.pro[i].no)))
            self.resultText.setItem(i, 1, QTableWidgetItem(self.pro[i].ana))
            self.resultText.setItem(i, 2, QTableWidgetItem(self.pro[i].input))
            self.resultText.setItem(i, 3, QTableWidgetItem(self.pro[i].formula))
            i += 1
        self.index = 0

    def process_single(self):
        """
        单步输出分析表过程
        :return:
        """
        if self.index == 0:
            self.analzell1()
            self.resultText.clear()
        elif self.index >= len(self.pro):
            self.resultText.clear()
            self.index = 0
        self.resultText.setItem(self.index, 0, QTableWidgetItem(str(self.pro[self.index].no)))
        self.resultText.setItem(self.index, 1, QTableWidgetItem(self.pro[self.index].ana))
        self.resultText.setItem(self.index, 2, QTableWidgetItem(self.pro[self.index].input))
        self.resultText.setItem(self.index, 3, QTableWidgetItem(self.pro[self.index].formula))
        self.index += 1


class nfaWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.fileName = ''
        self.fileName1 = ''
        self.flag = 0
        self.content = ''
        self.nfafile = []
        self.dfafile = []
        self.start = 0
        self.end = 0
        self.nfafor = []
        self.dfafor = []
        self.dfaend = []

    def initUI(self):
        nameLabel = QLabel("请输入正规式")
        self.inputText = QLineEdit()
        self.inputText.setReadOnly(False)
        self.openButton = QPushButton(self)
        self.openButton.setText("验证正规式")
        self.openButton.clicked.connect(self.verify)

        back1 = QHBoxLayout()
        back1.addWidget(nameLabel)
        back1.addWidget(self.inputText)
        back1.addWidget(self.openButton)

        btn1 = QWidget()
        btn1.setLayout(back1)

        title1 = QLabel("正规式->NFA")
        self.nfaText = QTableWidget()
        label1_1 = QLabel("开始状态集")
        self.label_1 = QLabel()
        back2_1 = QHBoxLayout()
        back2_1.addWidget(label1_1)
        back2_1.addWidget(self.label_1)

        btn2_1 = QWidget()
        btn2_1.setLayout(back2_1)

        label1_2 = QLabel("终结状态集")
        self.label_2 = QLabel()
        back2_2 = QHBoxLayout()
        back2_2.addWidget(label1_2)
        back2_2.addWidget(self.label_2)
        btn2_2 = QWidget()
        btn2_2.setLayout(back2_2)

        self.opennfa = QPushButton(self)
        self.opennfa.setText("打开NFA文件")
        self.opennfa.clicked.connect(self.openNfa)

        self.createnfa = QPushButton(self)
        self.createnfa.setText("生成NFA")
        self.createnfa.clicked.connect(self.formulatonfa)

        back2_3 = QHBoxLayout()
        back2_3.addWidget(self.opennfa)
        back2_3.addWidget(self.createnfa)
        btn2_3 = QWidget()
        btn2_3.setLayout(back2_3)

        nfabtn = QVBoxLayout()
        nfabtn.addWidget(title1)
        nfabtn.addWidget(self.nfaText)
        nfabtn.addWidget(btn2_1)
        nfabtn.addWidget(btn2_2)
        nfabtn.addWidget(btn2_3)

        nfaback = QWidget()
        nfaback.setLayout(nfabtn)

        title2 = QLabel("NFA->DFA")
        self.dfaText = QTableWidget()
        label2_1 = QLabel("开始状态集")
        self.label_3 = QLabel()
        back3_1 = QHBoxLayout()
        back3_1.addWidget(label2_1)
        back3_1.addWidget(self.label_3)

        btn3_1 = QWidget()
        btn3_1.setLayout(back3_1)

        label2_2 = QLabel("终结状态集")
        self.label_4 = QLabel()
        # self.label.setText(u"这个标签的长裤可以变化吗aaaaaaaa东西南北？")
        back3_2 = QHBoxLayout()
        back3_2.addWidget(label2_2)
        back3_2.addWidget(self.label_4)
        btn3_2 = QWidget()
        btn3_2.setLayout(back3_2)

        self.opendfa = QPushButton(self)
        self.opendfa.setText("打开DFA文件")
        self.opendfa.clicked.connect(self.openDfa)

        self.createdfa = QPushButton(self)
        self.createdfa.setText("生成DFA")
        self.createdfa.clicked.connect(self.nfatodfa)

        back3_3 = QHBoxLayout()
        back3_3.addWidget(self.opendfa)
        back3_3.addWidget(self.createdfa)
        btn3_3 = QWidget()
        btn3_3.setLayout(back3_3)

        dfabtn = QVBoxLayout()
        dfabtn.addWidget(title2)
        dfabtn.addWidget(self.dfaText)
        dfabtn.addWidget(btn3_1)
        dfabtn.addWidget(btn3_2)
        dfabtn.addWidget(btn3_3)

        dfaback = QWidget()
        dfaback.setLayout(dfabtn)

        title3 = QLabel("DFA->MFA")
        self.mfaText = QTableWidget()
        label3_1 = QLabel("开始状态集")
        self.label_5 = QLabel()
        back4_1 = QHBoxLayout()
        back4_1.addWidget(label3_1)
        back4_1.addWidget(self.label_5)

        btn4_1 = QWidget()
        btn4_1.setLayout(back4_1)

        label3_2 = QLabel("终结状态集")
        self.label_6 = QLabel()
        # self.label.setText(u"这个标签的长裤可以变化吗aaaaaaaa东西南北？")
        back4_2 = QHBoxLayout()
        back4_2.addWidget(label3_2)
        back4_2.addWidget(self.label_6)
        btn4_2 = QWidget()
        btn4_2.setLayout(back4_2)

        self.createmfa = QPushButton(self)
        self.createmfa.setText("生成MFA")
        self.createmfa.clicked.connect(self.dfatomfa)

        mfabtn = QVBoxLayout()
        mfabtn.addWidget(title3)
        mfabtn.addWidget(self.mfaText)
        mfabtn.addWidget(btn4_1)
        mfabtn.addWidget(btn4_2)
        mfabtn.addWidget(self.createmfa)

        mfaback = QWidget()
        mfaback.setLayout(mfabtn)

        output = QHBoxLayout()
        output.addWidget(nfaback)
        output.addWidget(dfaback)
        output.addWidget(mfaback)

        bottom = QWidget()
        bottom.setLayout(output)

        backbtn = QVBoxLayout()
        backbtn.addWidget(btn1)
        backbtn.addWidget(bottom)

        back = QWidget()
        back.setLayout(backbtn)
        self.setCentralWidget(back)
        self.setGeometry(300, 200, 800, 600)
        self.setWindowTitle('NFA-DFA-MFA')
        self.show()

    def verify(self):
        """
        验证正则式
        :return:
        """
        self.content = self.inputText.text()
        if self.content == '':
            QMessageBox.warning(self, "Warning", "请先输入正则式", QMessageBox.Yes)  # 弹出警告框
        else:
            deal = nfatodfa()
            self.flag = deal.verify(self.content)
            if self.flag == 1:
                QMessageBox.warning(self, "Warning", "正则式表达正确", QMessageBox.Yes)  # 弹出警告框
            else:
                QMessageBox.warning(self, "Warning", "正则式表达错误", QMessageBox.Yes)  # 弹出警告框

    def formulatonfa(self):
        """
        正则式转nfa
        :return:
        """
        if (self.fileName == '') & (self.content == ''):
            QMessageBox.warning(self, "Warning", "请先输入或验证正则式", QMessageBox.Yes)  # 弹出警告框
        elif self.content != '':
            self.nfaText.clear()
            deal = nfatodfa()
            deal.formulatonfa(self.content)
            start = deal.start
            end = deal.end
            nfa = deal.nfaformula

            self.nfaText.setColumnCount(3)
            self.nfaText.setRowCount(len(nfa))
            for i in range(3):
                self.nfaText.setColumnWidth(i, 60)
            for i in range(len(nfa)):
                self.nfaText.setRowHeight(i, 20)
            self.nfaText.setHorizontalHeaderLabels(['起始状态', '接受符号', '到达状态'])
            for i in range(len(nfa)):
                self.nfaText.setItem(i, 0, QTableWidgetItem(str(nfa[i].start)))
                self.nfaText.setItem(i, 1, QTableWidgetItem(nfa[i].operation))
                self.nfaText.setItem(i, 2, QTableWidgetItem(str(nfa[i].end)))
            self.label_1.setText(str(start))
            self.label_2.setText(str(end))

    def openNfa(self):
        """
        打开nfa
        :return:
        """
        try:
            name = self.fileName
            self.fileName, filetype = QFileDialog.getOpenFileName(self, "选取文件", "/Volumes/Transcend", "All Files (*);"
                                                                                                      ";Text Files (*.txt);"
                                                                                                      ";C Files (*.c);"
                                                                                                      ";JAVA Files (*.java);"
                                                                                                      ";Python Files(*.py)")
            self.nfaText.clear()
            # 设置文件扩展名过滤,注意用双分号间隔
            self.fileName = '//Volumes//Transcend//文件//编译原理//nfa_3.txt'
            file = open(self.fileName)
            while 1:
                lines = file.readlines(100000)
                if not lines:
                    break
                for line in lines:
                    self.nfafile.append(line.split('\n')[0])

            self.nfaText.setColumnCount(3)
            self.nfaText.setRowCount(len(self.nfafile) - 3)
            for i in range(3):
                self.nfaText.setColumnWidth(i, 60)
            for i in range(len(self.nfafile) - 3):
                self.nfaText.setRowHeight(i, 20)
            self.nfaText.setHorizontalHeaderLabels(['起始状态', '接受符号', '到达状态'])
            start = self.nfafile[0].split(':')[1]
            end = self.nfafile[1].split(':')[1]
            n = 3
            self.nfafor = []
            while 1:
                if n >= len(self.nfafile):
                    break
                content = self.nfafile[n].split("\t")
                temp = nfa()
                temp.start = content[0]
                temp.operation = content[1]
                temp.end = content[2]
                self.nfafor.append(temp)
                self.nfaText.setItem(n - 3, 0, QTableWidgetItem(content[0]))
                self.nfaText.setItem(n - 3, 1, QTableWidgetItem(content[1]))
                self.nfaText.setItem(n - 3, 2, QTableWidgetItem(content[2]))
                n += 1

            self.label_1.setText(start)
            self.label_2.setText(end)
            self.nfastart = start
            self.nfaend = end

        except Exception as e:
            print(e)
            self.fileName = name

    def nfatodfa(self):
        if (self.fileName == '') & (self.content == ''):
            QMessageBox.warning(self, "Warning", "请先输入或验证正则式", QMessageBox.Yes)  # 弹出警告框
        elif self.content != '':
            self.dfaText.clear()
            deal = nfatodfa()
            deal.createform(self.content)

            start = deal.dfastart
            end = deal.dfaend
            dfa = deal.dfaformula

            self.dfaText.setColumnCount(3)
            self.dfaText.setRowCount(len(dfa))
            for i in range(3):
                self.dfaText.setColumnWidth(i, 60)
            for i in range(len(dfa)):
                self.dfaText.setRowHeight(i, 20)
            self.dfaText.setHorizontalHeaderLabels(['起始状态', '接受符号', '到达状态'])
            for i in range(len(dfa)):
                self.dfaText.setItem(i, 0, QTableWidgetItem(str(dfa[i].start)))
                self.dfaText.setItem(i, 1, QTableWidgetItem(dfa[i].operation))
                self.dfaText.setItem(i, 2, QTableWidgetItem(str(dfa[i].end)))
            self.label_3.setText(str(start))

            endc = str(end[0])
            i = 1
            while 1:
                if i >= len(end):
                    break
                endc = endc + "," + str(end[i])
                i += 1
            self.label_4.setText(endc)
        elif self.fileName != '':
            self.dfaText.clear()
            deal = nfatodfa()
            deal.createform1(self.nfafor, self.nfastart, self.nfaend)

            start = deal.dfastart
            end = deal.dfaend
            dfa = deal.dfaformula

            self.dfaText.setColumnCount(3)
            self.dfaText.setRowCount(len(dfa))
            for i in range(3):
                self.dfaText.setColumnWidth(i, 60)
            for i in range(len(dfa)):
                self.dfaText.setRowHeight(i, 20)
            self.dfaText.setHorizontalHeaderLabels(['起始状态', '接受符号', '到达状态'])
            for i in range(len(dfa)):
                self.dfaText.setItem(i, 0, QTableWidgetItem(str(dfa[i].start)))
                self.dfaText.setItem(i, 1, QTableWidgetItem(dfa[i].operation))
                self.dfaText.setItem(i, 2, QTableWidgetItem(str(dfa[i].end)))
            self.label_3.setText(str(start))

            endc = ''
            if len(end) != 0:
                endc = str(end[0])
            i = 1
            while 1:
                if i >= len(end):
                    break
                endc = endc + "," + str(end[i])
                i += 1
            self.label_4.setText(endc)

    def openDfa(self):
        """
        打开nfa
        :return:
        """
        try:
            name = self.fileName
            self.fileName1, filetype = QFileDialog.getOpenFileName(self, "选取文件", "/Volumes/Transcend", "All Files (*);"
                                                                                                       ";Text Files (*.txt);"
                                                                                                       ";C Files (*.c);"
                                                                                                       ";JAVA Files (*.java);"
                                                                                                       ";Python Files(*.py)")
            self.nfaText.clear()
            # 设置文件扩展名过滤,注意用双分号间隔
            self.fileName1 = '//Volumes//Transcend//文件//编译原理//dfa_4.txt'
            file = open(self.fileName1)
            while 1:
                lines = file.readlines(100000)
                if not lines:
                    break
                for line in lines:
                    self.dfafile.append(line.split('\n')[0])

            self.dfaText.setColumnCount(3)
            self.dfaText.setRowCount(len(self.dfafile) - 3)
            for i in range(3):
                self.dfaText.setColumnWidth(i, 60)
            for i in range(len(self.dfafile) - 3):
                self.dfaText.setRowHeight(i, 20)
            self.dfaText.setHorizontalHeaderLabels(['起始状态', '接受符号', '到达状态'])
            start = self.dfafile[0].split(':')[1]
            end = self.dfafile[1].split(':')[1]
            print(str(start))
            print(str(end))
            endg = end.split(',')
            n = 3

            self.dfafor = []
            while 1:
                if n >= len(self.dfafile):
                    break
                content = self.dfafile[n].split("\t")
                temp = nfa()
                temp.start = content[0]
                temp.operation = content[1]
                temp.end = content[2]
                self.dfafor.append(temp)
                self.dfaText.setItem(n - 3, 0, QTableWidgetItem(content[0]))
                self.dfaText.setItem(n - 3, 1, QTableWidgetItem(content[1]))
                self.dfaText.setItem(n - 3, 2, QTableWidgetItem(content[2]))
                n += 1

            self.label_3.setText(start)
            self.label_4.setText(end)
            self.dfastart = start
            self.dfaend = endg

        except Exception as e:
            print(e)
            self.fileName = name

    def dfatomfa(self):
        """
        dfa->mfa
        :return:
        """
        # if (self.fileName == '') & (len(self.dfafor) == 0):
        #     QMessageBox.warning(self, "Warning", "请先输入或验证正则式", QMessageBox.Yes)  # 弹出警告框
        if False:
            print(1)
        elif self.content != '':
            self.mfaText.clear()
            deal = nfatodfa()
            deal.dfatomfa(self.content)

            start = deal.dfastart
            end = deal.dfaend
            mfa = deal.mfaformula

            self.mfaText.setColumnCount(3)
            self.mfaText.setRowCount(len(mfa))
            for i in range(3):
                self.mfaText.setColumnWidth(i, 60)
            for i in range(len(mfa)):
                self.mfaText.setRowHeight(i, 20)
            self.mfaText.setHorizontalHeaderLabels(['起始状态', '接受符号', '到达状态'])
            for i in range(len(mfa)):
                self.mfaText.setItem(i, 0, QTableWidgetItem(str(mfa[i].start)))
                self.mfaText.setItem(i, 1, QTableWidgetItem(mfa[i].operation))
                self.mfaText.setItem(i, 2, QTableWidgetItem(str(mfa[i].end)))
            self.label_5.setText(str(start))

            endc = str(end[0])
            i = 1
            while 1:
                if i >= len(end):
                    break
                endc = endc + "," + str(end[i])
                i += 1
            self.label_6.setText(endc)
        elif len(self.dfafor) != 0:
            self.mfaText.clear()
            deal = nfatodfa()
            deal.dfatomfa1(self.dfafor, self.dfastart, self.dfaend)

            start = deal.dfastart
            end = deal.dfaend
            mfa = deal.mfaformula

            self.mfaText.setColumnCount(3)
            self.mfaText.setRowCount(len(mfa))
            for i in range(3):
                self.mfaText.setColumnWidth(i, 60)
            for i in range(len(mfa)):
                self.mfaText.setRowHeight(i, 20)
            self.mfaText.setHorizontalHeaderLabels(['起始状态', '接受符号', '到达状态'])
            for i in range(len(mfa)):
                self.mfaText.setItem(i, 0, QTableWidgetItem(str(mfa[i].start)))
                self.mfaText.setItem(i, 1, QTableWidgetItem(mfa[i].operation))
                self.mfaText.setItem(i, 2, QTableWidgetItem(str(mfa[i].end)))
            self.label_5.setText(str(start))

            endc = str(end[0])
            i = 1
            while 1:
                if i >= len(end):
                    break
                endc = endc + "," + str(end[i])
                i += 1
            self.label_6.setText(endc)


def show():
    app = QApplication(sys.argv)
    ex = exp()
    sys.exit(app.exec_())
