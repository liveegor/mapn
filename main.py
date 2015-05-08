#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt4 import QtCore
import os
from MainWindow import *
import sys
import subprocess
import cPickle as pickle




class Window (QtGui.QMainWindow, Ui_mainWindow):

    cmd = {}
    commandText = ''
    nmapPath = ''

    # Constructor
    def __init__ (self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        # initial state of cmd
        # Tab 1
        self.cmd['address'] = QtCore.QString('')
        self.cmd['OS']      = QtCore.QString('')
        self.cmd['short']   = QtCore.QString('')
        self.cmd['versions']= QtCore.QString('')
        self.cmd['speed']   = QtCore.QString('')
        self.cmd['tcp']     = QtCore.QString('')
        self.cmd['nontcp']  = QtCore.QString('')
        # Tab 2
        self.cmd['noping']  = QtCore.QString('')
        self.cmd['icmp']    = QtCore.QString('')
        self.cmd['icmp_time']  = QtCore.QString('')
        self.cmd['icmp_mask']  = QtCore.QString('')
        self.cmd['ack']  = QtCore.QString('')
        self.cmd['syn']  = QtCore.QString('')
        self.cmd['udp']  = QtCore.QString('')
        # Tab 3
        self.cmd['verbose']  = QtCore.QString('')
        self.cmd['ports']  = QtCore.QString('')
        # Connections init
        # Common
        self.scanPushButton.clicked.connect(self.execute)
        self.ipLineEdit.textChanged.connect(self.onAddressChanged)
        # Tab 1
        self.aboutAuthorAction.triggered.connect(self.showAuthor)
        self.OSCheckBox.stateChanged.connect(self.onOsStateChanged)
        self.shortCheckBox.stateChanged.connect(self.onShortStateChanged)
        self.versionsCheckBox.stateChanged.connect(self.onVersionsStateChanged)
        self.speedSpinBox.valueChanged.connect(self.onSpeedChanged)
        self.tcpComboBox.activated.connect(self.onTcpActivated)
        self.nonTcpComboBox.activated.connect(self.onNonTcpActivated)
        # Tab 2
        self.noPingCheckBox.stateChanged.connect(self.onNoPingStateChanged)
        self.icmpCheckBox.stateChanged.connect(self.onIcmpStateChanged)
        self.icmpTimeLableCheckBox.stateChanged.connect(self.onIcmpTimeLableStateChanged)
        self.icmpNetmaskCheckBox.stateChanged.connect(self.onIcmpNetmaskStateChanged)
        self.ackCheckBox.stateChanged.connect(self.onAckStateChanged)
        self.synCheckBox.stateChanged.connect(self.onSynStateChanged)
        self.udpCheckBox.stateChanged.connect(self.onUdpStateChanged)
        self.ackLineEdit.textChanged.connect(self.onAckStateChanged)
        self.synLineEdit.textChanged.connect(self.onSynStateChanged)
        self.udpLineEdit.textChanged.connect(self.onUdpStateChanged)
        # Tab 2
        self.verboseCheckBox.stateChanged.connect(self.onVerboseChanged)
        self.portsCheckBox.stateChanged.connect(self.onPortsStateChanged)
        self.portsLineEdit.textChanged.connect(self.onPortsStateChanged)
        # Path (for windows version
        self.nmapPathAction.triggered.connect(self.addNmapPath)
        f = 0
        try:
            f = open('nmapPath.bin', 'rb')
        except IOError, e:
            print e
            title = QtGui.QApplication.translate("self", "Ошибка", None, QtGui.QApplication.UnicodeUTF8)
            text  = QtGui.QApplication.translate("self", "Добавьте путь к исполняемому файлу nmap.exe", None, QtGui.QApplication.UnicodeUTF8)
            QtGui.QMessageBox.warning(self, title, text)
            f = 0
        if f != 0:
            self.nmapPath = pickle.load(f)
            f.close()
        # lol
        self.updateCommandText()

    def showAuthor(self):
        title = QtGui.QApplication.translate("self", "Автор", None, QtGui.QApplication.UnicodeUTF8)
        text  = QtGui.QApplication.translate("self", "Copyright ©2014 Литвинов Егор Викторович", None, QtGui.QApplication.UnicodeUTF8)
        QtGui.QMessageBox.about(self, title, text)

    def execute(self):
        # Execute command
        self.outputTableWidget.setRowCount(0)
        PIPE = subprocess.PIPE
        p = subprocess.Popen(self.commandText , shell=True, stdin=PIPE, stdout=PIPE,
        stderr=subprocess.STDOUT, close_fds=False)
        outString = ''
        while True:
            s = p.stdout.readline()
            if not s:
                break
            outString += s
        # Output to text edit
        self.outputTextEdit.setText(outString)
        # Output to table widget
        outText = outString.split('\n')
        currentIp = ''
        for line in outText:
            if 'Nmap scan report for ' in line:
                begin = line.find('(') + 1
                end   = line.find(')')
                currentIp = line[begin:end]
                if begin == 0:
                    currentIp = line.replace('Nmap scan report for ', '')
            if '/tcp' in line or '/udp' in line:
                # Parse string
                line = line.split()
                tmp = line[0].split('/')
                tmp.extend(line[1:])
                line = tmp
                # Insert into table
                rowIndex = self.outputTableWidget.rowCount()
                self.outputTableWidget.insertRow(rowIndex)
                item = QtGui.QTableWidgetItem(currentIp)
                self.outputTableWidget.setItem(rowIndex, 0, item)
                colsN = self.outputTableWidget.columnCount()
                elementsN = len(line)
                for i in range(1, min([colsN, elementsN])):
                    item = QtGui.QTableWidgetItem(line[i - 1])
                    self.outputTableWidget.setItem(rowIndex, i, item)

    def updateCommandText(self):
        self.commandText = self.nmapPath +  \
            self.cmd['tcp'].toUtf8().data() + \
            self.cmd['nontcp'].toUtf8().data() + \
            self.cmd['versions'].toUtf8().data() + \
            self.cmd['speed'].toUtf8().data() + \
            self.cmd['ports'].toUtf8().data() + \
            self.cmd['OS'].toUtf8().data() + \
            self.cmd['verbose'].toUtf8().data() + \
            self.cmd['short'].toUtf8().data() + \
            self.cmd['noping'].toUtf8().data() + \
            self.cmd['icmp'].toUtf8().data() + \
            self.cmd['icmp_time'].toUtf8().data() + \
            self.cmd['icmp_mask'].toUtf8().data() + \
            self.cmd['ack'].toUtf8().data() + \
            self.cmd['syn'].toUtf8().data() + \
            self.cmd['udp'].toUtf8().data() + \
            self.cmd['address'].toUtf8().data()
        self.commandLineEdit.setText(self.commandText)

    def onAddressChanged(self, address):
        self.cmd['address'] = ' ' + address
        self.updateCommandText()

    def onOsStateChanged (self, unused):
        if self.OSCheckBox.isChecked():
            self.cmd['OS'] = QtCore.QString(' -O')
        else:
            self.cmd['OS'] = QtCore.QString('')
        self.updateCommandText()

    def onShortStateChanged (self, unused):
        if self.shortCheckBox.isChecked():
            self.cmd['short'] = QtCore.QString(' -F')
        else:
            self.cmd['short'] = QtCore.QString('')
        self.updateCommandText()

    def onVersionsStateChanged (self, unused):
        if self.versionsCheckBox.isChecked():
            self.cmd['versions'] = QtCore.QString(' -sV')
        else:
            self.cmd['versions'] = QtCore.QString('')
        self.updateCommandText()

    def onSpeedChanged (self, value):
        if value == 0:
            self.cmd['speed'] = QtCore.QString('')
        else:
            self.cmd['speed'] = QtCore.QString(' -T') + QtCore.QString.number(value)
        self.updateCommandText()

    def onTcpActivated (self, index):
        opts = {0: '',
                1: ' -sS',
                2: ' -sT',
                3: ' -sF',
                4: ' -sA',
                5: ' -sW',
                6: ' -sM',
                7: ' -sN', 
                8: ' -sX'}
        self.cmd['tcp'] = QtCore.QString(opts[index])
        self.updateCommandText()

    def onNonTcpActivated (self, index):
        opts = {0: '',
                1: ' -sU',
                2: ' -sO',
                3: ' -sP'}
        self.cmd['nontcp'] = QtCore.QString(opts[index])
        self.updateCommandText()

    def onNoPingStateChanged (self, unused):
        if self.noPingCheckBox.isChecked():
            self.cmd['noping'] = QtCore.QString(' -PN')
        else:
            self.cmd['noping'] = QtCore.QString('')
        self.updateCommandText()

    def onIcmpStateChanged (self, unused):
        if self.icmpCheckBox.isChecked():
            self.cmd['icmp'] = QtCore.QString(' -PE')
        else:
            self.cmd['icmp'] = QtCore.QString('')
        self.updateCommandText()

    def onIcmpTimeLableStateChanged (self, unused):
        if self.icmpTimeLableCheckBox.isChecked():
            self.cmd['icmp_time'] = QtCore.QString(' -PP')
        else:
            self.cmd['icmp_time'] = QtCore.QString('')
        self.updateCommandText()

    def onIcmpNetmaskStateChanged (self, unused):
        if self.icmpNetmaskCheckBox.isChecked():
            self.cmd['icmp_mask'] = QtCore.QString(' -PM')
        else:
            self.cmd['icmp_mask'] = QtCore.QString('')
        self.updateCommandText()

    def onAckStateChanged (self, unused):
        if self.ackCheckBox.isChecked():
            self.cmd['ack'] = QtCore.QString(' -PA') + self.ackLineEdit.text()
        else:
            self.cmd['ack'] = QtCore.QString('')
        self.updateCommandText()

    def onSynStateChanged (self, unused):
        if self.synCheckBox.isChecked():
            self.cmd['syn'] = QtCore.QString(' -PS') + self.synLineEdit.text()
        else:
            self.cmd['syn'] = QtCore.QString('')
        self.updateCommandText()

    def onUdpStateChanged (self, unused):
        if self.udpCheckBox.isChecked():
            self.cmd['udp'] = QtCore.QString(' -PU') + self.udpLineEdit.text()
        else:
            self.cmd['udp'] = QtCore.QString('')
        self.updateCommandText()

    def onVerboseChanged (self, unused):
        if self.verboseCheckBox.isChecked():
            self.cmd['verbose'] = QtCore.QString(' -v')
        else:
            self.cmd['verbose'] = QtCore.QString('')
        self.updateCommandText()

    def onPortsStateChanged (self, unused):
        if self.portsCheckBox.isChecked():
            self.cmd['ports'] = QtCore.QString(' -p') + self.portsLineEdit.text()
        else:
            self.cmd['ports'] = QtCore.QString('')
        self.updateCommandText()

    def addNmapPath (self):
        # Ask path
        path = QtGui.QFileDialog.getOpenFileName(self, 'Open')
        if not path:
            return
        path = path.toUtf8().data()
        self.nmapPath = path
        self.updateCommandText()
        # Load path to file
        f = open('nmapPath.bin', 'wb')
        pickle.dump(path, f, 2)
        f.close()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
