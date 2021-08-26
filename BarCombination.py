from PyQt5.uic import loadUiType
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import Mabhas6_92
import Mabhas6_98
from pandas import DataFrame
from numpy import all
import sys

import warnings
warnings.filterwarnings("ignore")

# Load GUI template
ui,_ = loadUiType("BarCombination.ui")

class MainApp(QMainWindow , ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("BarCombination")
        self.showMaximized()

        #===========
        #___________SECTION I, ACTIONS
        #===========

        # Warning on enabling 30%Moteamed
        self.chBox_T1_GB1_GB5_5.stateChanged.connect(self.Warning_Moteamed)
        # Warning on enabling Notional Bar
        self.chBox_T1_GB1_GB10_1.toggled.connect(self.Warning_NlBar)
        # Activate grBoxes_T1_GB2[1] if radBut_T1_GB2_GB1_1 enabled.
        self.radBut_T1_GB2_GB1_1.toggled.connect(lambda: self.Enable_grBox_T1_GB2())
        # Show 2800-Warning if I != 0.35 was selected.
        self.coBox_T1_GB2_GB2_2.currentIndexChanged.connect(self.Warning_2800)
        # Select X,Y row from Table
        self.XchkBox = []
        self.YchkBox = []
        for row in range(self.table_T1_GB3_1.rowCount()):
            if row in [0, 8, 17 , 24, 33]:
                self.table_T1_GB3_1.setSpan(row, 0, 1, 3)
            else:
                self.XchkBox.append(self.insertCheckBox(row, x=True))
                self.YchkBox.append(self.insertCheckBox(row, y=True))
        # Set 1st Checkboxe for X and Y to True
        self.XchkBox[0].setChecked(True)
        self.YchkBox[0].setChecked(True)
        # Group CheckBoxes X and Y in Table Separately
        QBG = QtWidgets.QButtonGroup(self)
        for i in self.XchkBox: QBG.addButton(i)
        QBG = QtWidgets.QButtonGroup(self)
        for i in self.YchkBox: QBG.addButton(i)
        # Group CheckBoxes for ETAB format
        QBG = QtWidgets.QButtonGroup(self)
        for i in [self.chBox_T1_GB5_1, self.chBox_T1_GB5_2]: QBG.addButton(i)
        QBG = QtWidgets.QButtonGroup(self)
        for i in [self.chBox_T1_GB5_3, self.chBox_T1_GB5_4]: QBG.addButton(i)        
        # Start Calculating Bar Combinations
        self.puButton_T1_GB5_1.pressed.connect(self.CalBars)

    #===========
    #___________SECTION II, DEFINE FUNCTIONS
    #===========
            
    # Enable grBoxes_T1_GB2
    def Enable_grBox_T1_GB2(self):
        if self.radBut_T1_GB2_GB1_1.isChecked(): self.grBox_T1_GB2_2.setEnabled(True)
        else:
            self.grBox_T1_GB2_2.setEnabled(False)
            self.textEdit_T1_GB4_1.clear()

    # 30% Moteamed
    def Warning_Moteamed(self):
        if not self.chBox_T1_GB1_GB5_5.isChecked():
            msg = "توجه داشته باشید که در صورت عدم انتخاب این گزینه، رفتار ساختمان حتماً باید منظم باشد."
            self.textEdit_T1_GB4_1.setPlainText(msg)
        else: self.textEdit_T1_GB4_1.clear()            

    # Show Waring Message of Notional Bar Selection
    def Warning_NlBar(self):
        if self.chBox_T1_GB1_GB10_1.isChecked():
            msg = "انتخاب بار جانبی فرضی فقط برای ساختمان های فولادی اجباری می باشد."
            self.textEdit_T1_GB4_1.setPlainText(msg)
        else: self.textEdit_T1_GB4_1.clear()
    
    # Show Waring Message of 2800
    def Warning_2800(self):
        if self.coBox_T1_GB2_GB2_2.currentIndex() != 2:
            msg = "در ویرایش چهارم استاندارد 2800، اثر مولفه قائم شتاب زلزله، فقط در پهنه با خطر نسبی خیلی زیاد الزامی می باشد اما در آیین نامه آمریکا، این بار در تمام پهنه ها به کل سازه اعمال می گردد."
            self.textEdit_T1_GB4_1.setPlainText(msg)
        else: self.textEdit_T1_GB4_1.clear()

    # Insert check boxes in Table
    def insertCheckBox(self, row, x=None, y=None):
            cellWidget = QtWidgets.QWidget()
            chkBox = QtWidgets.QCheckBox()
            layOut = QtWidgets.QHBoxLayout(cellWidget)
            layOut.addWidget(chkBox)
            layOut.setAlignment(Qt.AlignHCenter)
            layOut.setContentsMargins(0, 0, 0, 0)
            cellWidget.setLayout(layOut)
            if x: chkBox.setObjectName("chBox_x_T1_GB3_Ta1_%d"%(row)); self.table_T1_GB3_1.setCellWidget(row, 0, cellWidget)
            if y: chkBox.setObjectName("chBox_y_T1_GB3_Ta1_%d"%(row)); self.table_T1_GB3_1.setCellWidget(row, 1, cellWidget)
            return(chkBox)      

    def CalBars(self):
        # Read Bars
        self.readBars()
        # Read Intensity and Acceleration
        self.AI = self.readAI()
        self.omega, self.omega_x_flag, self.omega_y_flag = self.ReadOmega()
        # Calculates Bars
        dfASD = self.ASD()
        dfLRFD = self.LRFD()
        dfLRFD_AMP = self.LRFD_AMP()
        # Show message when calculation is done
        messageBox = QMessageBox()
        msgTrue = '<p style="font-family:B Nazanin;font-size:large"> <b>ترکیبات بار محاسبه گردید.</b> </p>'
        msgFalse = '<p style="font-family:B Nazanin;font-size:large"> <b>هیچ ترکیب باری انتخاب نشده است!</b> </p>'
        if all(dfASD.isnull()) and all(dfLRFD.isnull()) and all(dfLRFD_AMP.isnull()):
            messageBox.information(self, "System Message", msgFalse, QMessageBox.Ok)
        else:
            messageBox.information(self, "System Message", msgTrue, QMessageBox.Ok)

    # Calculate ASD Combinations
    def ASD(self):
        """
        Combinations:
        1 - D
        2 - D + L
        3 - D + (Lr or S or R)
        4 - D + 0.75L + 0.75(Lr or S or R)
        5 - D + [0.6(1.4W) or 0.7E]
        6 - D + 0.75L + 0.75[0.6(1.4W)] + 0.75(Lr or S or R)
        7 - D + 0.75L + 0.75(0.7E) + 0.75S
        8 - 0.6D 0.6(1.4W)
        9 - 0.6D + 0.7E
        10- D + T
        11- D + 0.75[L + (Lr or S) + T]
        """
        orderedBars = []
        for bars in [self.deadBars, self.liveBars, self.soilBars, self.windBars, self.statEarqBars,
                     self.dynaEarqBars, self.snowBars, self.tempBars, self.unexBars]:
            [orderedBars.append(bar) for bar,val in bars.items() if val]
        # Generate Combinations
        apply_30_flag = self.chBox_T1_GB1_GB5_5.isChecked()
        NL_flag = self.chBox_T1_GB1_GB10_1.isChecked()
        AI = self.AI
        df = DataFrame()
        if self.chBox_T1_GB5_3.isChecked(): df = Mabhas6_92.getASD(orderedBars, apply_30_flag, NL_flag, AI)
        if self.chBox_T1_GB5_4.isChecked(): df = Mabhas6_98.getASD(orderedBars, apply_30_flag, NL_flag, AI)
        self.table_T2_GB1_1.setRowCount(0)
        self.plainTextEdit_T2_GB2_1.clear()
        if all(df.isnull()) : return df
        for i in range(len(df)):
            text = " ".join(["%g%s"%(df[j][i], self.renameBar(j)) if _ == 0 else "%+g%s"%(df[j][i], self.renameBar(j)) for _,j in enumerate(df) if df[j][i]])
            rowPos = self.table_T2_GB1_1.rowCount()
            self.table_T2_GB1_1.insertRow(rowPos)
            item = QtWidgets.QTableWidgetItem(text)
            item.setFont(QFont("Times New Roman", 10))
            item.setTextAlignment(4)
            self.table_T2_GB1_1.setItem(rowPos, 0, item)
            # Generate Formatted Text
            self.plainTextEdit_T2_GB2_1.setFont(QFont("Times New Roman", 10))
            self.plainTextEdit_T2_GB2_1.insertPlainText('  COMBO  "LR%s" TYPE "ADD"  DESIGN "CONCRETE" \n'%(df.index[i]))
            for text in ['  COMBO  "LR%s" LOAD "%s" SF %g\n'%(df.index[i], k, v) for k,v in df.iloc[i].items() if v]:
                self.plainTextEdit_T2_GB2_1.insertPlainText(text)
        return df      

    # Calculate LRFD Combinations
    def LRFD(self):
        """
        Combinations:
        
        1 - D
        2 - D + L
        3 - D + (Lr or S or R)
        4 - D + 0.75L + 0.75(Lr or S or R)
        5 - D + [0.6(1.4W) or 0.7E]
        6 - D + 0.75L + 0.75[0.6(1.4W)] + 0.75(Lr or S or R)
        7 - D + 0.75L + 0.75(0.7E) + 0.75S
        8 - 0.6D 0.6(1.4W)
        9 - 0.6D + 0.7E
        10- D + T
        11- D + 0.75[L + (Lr or S) + T]
        """
        orderedBars = []
        for bars in [self.deadBars, self.liveBars, self.soilBars, self.windBars, self.statEarqBars,
                     self.dynaEarqBars, self.snowBars, self.tempBars, self.unexBars]:
            [orderedBars.append(bar) for bar,val in bars.items() if val]
        # Generate Combinations
        apply_30_flag = self.chBox_T1_GB1_GB5_5.isChecked()
        NL_flag = self.chBox_T1_GB1_GB10_1.isChecked()
        AI = self.AI
        df = DataFrame()
        if self.chBox_T1_GB5_3.isChecked(): df = Mabhas6_92.getLRFD(orderedBars, apply_30_flag, NL_flag, AI)
        if self.chBox_T1_GB5_4.isChecked(): df = Mabhas6_98.getLRFD(orderedBars, apply_30_flag, NL_flag, AI)
        self.table_T3_GB1_1.setRowCount(0)
        self.plainTextEdit_T3_GB2_1.clear()
        if all(df.isnull()) : return df
        for i in range(len(df)):
            text = " ".join(["%g%s"%(df[j][i], self.renameBar(j)) if _ == 0 else "%+g%s"%(df[j][i], self.renameBar(j)) for _,j in enumerate(df) if df[j][i]])
            rowPos = self.table_T3_GB1_1.rowCount()
            self.table_T3_GB1_1.insertRow(rowPos)
            item = QtWidgets.QTableWidgetItem(text)
            item.setFont(QFont("Times New Roman", 10))
            item.setTextAlignment(4)
            self.table_T3_GB1_1.setItem(rowPos, 0, item)
            # Generate Formatted Text
            self.plainTextEdit_T3_GB2_1.setFont(QFont("Times New Roman", 10))
            self.plainTextEdit_T3_GB2_1.insertPlainText('  COMBO  "LR%s" TYPE "ADD"  DESIGN "CONCRETE" \n'%(df.index[i]))
            for text in ['  COMBO  "LR%s" LOAD "%s" SF %g\n'%(df.index[i], k, v) for k,v in df.iloc[i].items() if v]:
                self.plainTextEdit_T3_GB2_1.insertPlainText(text)
        return df      

    # Calculate LRFD_AMP Combinations
    def LRFD_AMP(self):
        """
        Combinations:
        
        1 - D
        2 - D + L
        3 - D + (Lr or S or R)
        4 - D + 0.75L + 0.75(Lr or S or R)
        5 - D + [0.6(1.4W) or 0.7E]
        6 - D + 0.75L + 0.75[0.6(1.4W)] + 0.75(Lr or S or R)
        7 - D + 0.75L + 0.75(0.7E) + 0.75S
        8 - 0.6D 0.6(1.4W)
        9 - 0.6D + 0.7E
        10- D + T
        11- D + 0.75[L + (Lr or S) + T]
        """
        orderedBars = []
        for bars in [self.deadBars, self.liveBars, self.soilBars, self.windBars, self.statEarqBars,
                     self.dynaEarqBars, self.snowBars, self.tempBars, self.unexBars]:
            [orderedBars.append(bar) for bar,val in bars.items() if val]
        # Generate Combinations
        apply_30_flag = self.chBox_T1_GB1_GB5_5.isChecked()
        NL_flag = self.chBox_T1_GB1_GB10_1.isChecked()
        AI = self.AI
        df = DataFrame()
        if self.chBox_T1_GB5_3.isChecked(): df = Mabhas6_92.getLRFD_AMP(orderedBars, apply_30_flag, NL_flag, self.omega, self.omega_x_flag, self.omega_y_flag, AI)
        if self.chBox_T1_GB5_4.isChecked(): df = Mabhas6_98.getLRFD_AMP(orderedBars, apply_30_flag, NL_flag, self.omega, self.omega_x_flag, self.omega_y_flag, AI)
        self.table_T4_GB1_1.setRowCount(0)
        self.plainTextEdit_T4_GB2_1.clear()
        if all(df.isnull()) : return df
        for i in range(len(df)):
            text = " ".join(["%g%s"%(df[j][i], self.renameBar(j)) if _ == 0 else "%+g%s"%(df[j][i], self.renameBar(j)) for _,j in enumerate(df) if df[j][i]])
            rowPos = self.table_T4_GB1_1.rowCount()
            self.table_T4_GB1_1.insertRow(rowPos)
            item = QtWidgets.QTableWidgetItem(text)
            item.setFont(QFont("Times New Roman", 10))
            item.setTextAlignment(4)
            self.table_T4_GB1_1.setItem(rowPos, 0, item)
            # Generate Formatted Text
            self.plainTextEdit_T4_GB2_1.setFont(QFont("Times New Roman", 10))
            self.plainTextEdit_T4_GB2_1.insertPlainText('  COMBO  "LR%s" TYPE "ADD"  DESIGN "CONCRETE" \n'%(df.index[i]))
            for text in ['  COMBO  "LR%s" LOAD "%s" SF %g\n'%(df.index[i], k, v) for k,v in df.iloc[i].items() if v]:
                self.plainTextEdit_T4_GB2_1.insertPlainText(text)
        return df      
        
    def readBars(self):
        self.deadBars = {"DL":None, "SDL":None, "WALL":None, "MASS":None}
        self.liveBars = {"LL1":None, "LL2":None, "LLR":None, "LLPAR":None}
        self.soilBars = {"PS0":None, "PSE":None}
        self.windBars = {"WXP":None, "WXN":None,"WYP":None, "WYN":None,"Wi+":None, "Wi-":None}
        self.statEarqBars = {"EX":None, "EY":None,"EXP":None, "EYP":None,"EXN":None, "EYN":None,"EV":None}
        self.dynaEarqBars = {"SPECXX":None, "SPECYY":None,"EDRIFTX":None, "EDRIFTY":None}
        self.snowBars = {"SN":None, "SNM":None, "SNP":None, "SNN":None}
        self.tempBars = {"+T30":None, "-T30":None}
        self.unexBars = {"AK":None}
        self.notiBars = {"NL":None}
        # DeadBars
        lineEdits = [
            self.liEdit_T1_GB1_GB1_1, self.liEdit_T1_GB1_GB1_2,
            self.liEdit_T1_GB1_GB1_3, self.liEdit_T1_GB1_GB1_4
            ]
        checkBoxes = [
            self.chBox_T1_GB1_GB1_1, self.chBox_T1_GB1_GB1_2,
            self.chBox_T1_GB1_GB1_3, self.chBox_T1_GB1_GB1_4
            ]
        c = 0
        for i,j in zip(checkBoxes, lineEdits):
            if i.isChecked():
                k = list(self.deadBars.keys())[c]
                self.deadBars[k] = j.text()
            c+=1
        # LiveBars
        lineEdits = [
            self.liEdit_T1_GB1_GB2_1, self.liEdit_T1_GB1_GB2_2,
            self.liEdit_T1_GB1_GB2_3, self.liEdit_T1_GB1_GB2_4
            ]
        checkBoxes = [
            self.chBox_T1_GB1_GB2_1, self.chBox_T1_GB1_GB2_2,
            self.chBox_T1_GB1_GB2_3, self.chBox_T1_GB1_GB2_4
        ]
        c = 0        
        for i,j in zip(checkBoxes, lineEdits):
            if i.isChecked():
                k = list(self.liveBars.keys())[c]
                self.liveBars[k] = j.text()
            c+=1
        # SoilBars
        lineEdits = [
            self.liEdit_T1_GB1_GB3_1, self.liEdit_T1_GB1_GB3_2
            ]
        checkBoxes = [
            self.chBox_T1_GB1_GB3_1, self.chBox_T1_GB1_GB3_2
        ]        
        c = 0
        for i,j in zip(checkBoxes, lineEdits):
            if i.isChecked():
                k = list(self.soilBars.keys())[c]
                self.soilBars[k] = j.text()
        # WindBars
        lineEdits = [
            self.liEdit_T1_GB1_GB4_1, self.liEdit_T1_GB1_GB4_2,
            self.liEdit_T1_GB1_GB4_3, self.liEdit_T1_GB1_GB4_4,
            self.liEdit_T1_GB1_GB4_5,
            self.liEdit_T1_GB1_GB4_6
            ]
        checkBoxes = [
            self.chBox_T1_GB1_GB4_1,self.chBox_T1_GB1_GB4_1,
            self.chBox_T1_GB1_GB4_2,self.chBox_T1_GB1_GB4_2,
            self.chBox_T1_GB1_GB4_3, 
            self.chBox_T1_GB1_GB4_4
        ]        
        c = 0        
        for i,j in zip(checkBoxes, lineEdits):
            if i.isChecked():
                k = list(self.windBars.keys())[c]
                self.windBars[k] = j.text()
            c+=1
        # StaticEarthquakeBars
        lineEdits = [
            self.liEdit_T1_GB1_GB5_1, self.liEdit_T1_GB1_GB5_2,
            self.liEdit_T1_GB1_GB5_3, self.liEdit_T1_GB1_GB5_4,
            self.liEdit_T1_GB1_GB5_5, self.liEdit_T1_GB1_GB5_6,
            self.liEdit_T1_GB1_GB5_7,
            None
            ]
        checkBoxes = [
            self.chBox_T1_GB1_GB5_1, self.chBox_T1_GB1_GB5_1,
            self.chBox_T1_GB1_GB5_2, self.chBox_T1_GB1_GB5_2,
            self.chBox_T1_GB1_GB5_3, self.chBox_T1_GB1_GB5_3,
            self.chBox_T1_GB1_GB5_4,
            self.chBox_T1_GB1_GB5_5
        ]        
        c = 0         
        for i,j in zip(checkBoxes, lineEdits):
            if i.isChecked() and j != None:
                k = list(self.statEarqBars.keys())[c]
                self.statEarqBars[k] = j.text()
            c+=1
        # DynamicEarthquakeBars
        lineEdits = [
            self.liEdit_T1_GB1_GB6_1, self.liEdit_T1_GB1_GB6_2,
            self.liEdit_T1_GB1_GB6_3, self.liEdit_T1_GB1_GB6_4
            ]
        checkBoxes = [
            self.chBox_T1_GB1_GB6_1, self.chBox_T1_GB1_GB6_2,
            self.chBox_T1_GB1_GB6_3, self.chBox_T1_GB1_GB6_4
        ]
        c = 0         
        for i,j in zip(checkBoxes, lineEdits):
            if i.isChecked():
                k = list(self.dynaEarqBars.keys())[c]
                self.dynaEarqBars[k] = j.text()
            c+=1
        # SnowBars
        lineEdits = [
            self.liEdit_T1_GB1_GB7_1,
            self.liEdit_T1_GB1_GB7_2,
            self.liEdit_T1_GB1_GB7_3, self.liEdit_T1_GB1_GB7_4
            ]
        checkBoxes = [
            self.chBox_T1_GB1_GB7_1,
            self.chBox_T1_GB1_GB7_2,
            self.chBox_T1_GB1_GB7_3, self.chBox_T1_GB1_GB7_3
        ]
        c = 0 
        for i,j in zip(checkBoxes, lineEdits):
            if i.isChecked():
                k = list(self.snowBars.keys())[c]
                self.snowBars[k] = j.text()
            c+=1
        # TempertureBars
        lineEdits = [
            self.liEdit_T1_GB1_GB8_1, self.liEdit_T1_GB1_GB8_2
            ]
        checkBoxes = [
            self.chBox_T1_GB1_GB8_1, self.chBox_T1_GB1_GB8_2
        ]
        c = 0        
        for i,j in zip(checkBoxes, lineEdits):
            if i.isChecked():
                k = list(self.tempBars.keys())[c]
                self.tempBars[k] = j.text()
            c+=1
        # UnexBars
        lineEdits = [
            self.liEdit_T1_GB1_GB9_1
            ]
        checkBoxes = [
            self.chBox_T1_GB1_GB9_1
        ]
        c = 0         
        for i,j in zip(checkBoxes, lineEdits):
            if i.isChecked():
                k = list(self.unexBars.keys())[c]
                self.unexBars[k] = j.text()
            c+=1
        # NotnalBars
        lineEdits = [
            self.liEdit_T1_GB1_GB10_1
            ]
        checkBoxes = [
            self.chBox_T1_GB1_GB10_1
        ]
        c = 0         
        for i,j in zip(checkBoxes, lineEdits):
            if i.isChecked():
                k = list(self.notiBars.keys())[c]
                self.notiBars[k] = j.text()
            c+=1

    # Rename Bars to user specified
    def renameBar(self, bar):
        allBars = {}
        allBars.update(self.deadBars)
        allBars.update(self.liveBars)
        allBars.update(self.soilBars)
        allBars.update(self.windBars)
        allBars.update(self.statEarqBars)
        allBars.update(self.dynaEarqBars)
        allBars.update(self.snowBars)
        allBars.update(self.tempBars)
        allBars.update(self.unexBars)
        allBars.update(self.notiBars)
        if not allBars[bar]: return ""
        return allBars[bar]
    
    def readAI(self):
        I_dic = {0:0.80,
                 1:1.00,
                 2:1.20,
                 3:1.40}
        A_dic = {0:0.20,
                 1:0.25,
                 2:0.30,
                 3:0.35}
        if self.radBut_T1_GB2_GB1_1.isChecked():
            I = I_dic[self.coBox_T1_GB2_GB2_1.currentIndex()]
            A = A_dic[self.coBox_T1_GB2_GB2_2.currentIndex()]
            return 0.6 * A * I
        else:
            return None
    
    def ReadOmega(self):
        c=0; omega, omega_x_flag, omega_y_flag = None, False, False
        for row in range(self.table_T1_GB3_1.rowCount()):
            if row in [0, 8, 17 , 24, 33]:
                continue
            else:
                if self.XchkBox[c].isChecked():
                    omega_x_flag = True
                if self.YchkBox[c].isChecked():
                    omega_y_flag = True                
                if self.XchkBox[c].isChecked() or self.YchkBox[c].isChecked() and self.table_T1_GB3_1.item(row, 2):
                    omega = (self.table_T1_GB3_1.item(row, 2).text())
                    omega = float(omega.replace("/", "."))
                c+=1
        return omega, omega_x_flag, omega_y_flag
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainApp()
    MainWindow.show()
    sys.exit(app.exec_())
