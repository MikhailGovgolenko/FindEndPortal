from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QColor
from math import *
import sys
import pyperclip
import sqlite3
import winreg
import styles

click = False


def translate(name, language):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        translation = cursor.execute(f""" SELECT "{language}" FROM language WHERE name = '{name}' """).fetchone()[0]
        return translation


def save(current, label):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(f""" UPDATE current SET {current} = '{label}' """)
        db.commit()


def current(name):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        current = cursor.execute(f""" SELECT {name} FROM current""").fetchone()[0]
        return current


def decart(angle):
    return angle + 90


def condition(angle, coordinate_x, coordinate_z, c_x, c_z):
    sina, cosa = (round(sin(radians(angle)), 10)), (round(cos(radians(angle)), 10))
    cond = None
    if 0 <= cosa <= 1 and 0 <= sina < 1:
        cond = f'{coordinate_x} >= {c_x}'
    if -1 < cosa <= 0 and 0 <= sina <= 1:
        cond = f'{coordinate_z} >= {c_z}'
    if -1 <= cosa <= 0 and -1 < sina <= 0:
        cond = f'{coordinate_x} <= {c_x}'
    if 0 <= cosa < 1 and -1 <= sina <= 0:
        cond = f'{coordinate_z} <= {c_z}'
    return cond


def defend_Theme():
    reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
    try:
        reg_key = winreg.OpenKey(reg, reg_path)
    except FileNotFoundError:
        print('no path')

    for i in range(1024):
        try:
            value_name, value, _ = winreg.EnumValue(reg_key, i)
            if value_name == 'AppsUseLightTheme':
                if value == 1:
                    return 'Light'
                else:
                    return 'Dark'
        except:
            break


class SelectDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if self.parent().currentIndex() == index.row():
            option.backgroundBrush = QColor(194, 194, 255)


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.qwindow = None
        uic.loadUi('design.ui', self)
        if current('theme') == translate('radioButton_light', current("language")):
            self.setLightTheme()
            self.radioButton_light.setChecked(True)
        elif current('theme') == translate('radioButton_dark', current("language")):
            self.setDarkTheme()
            self.radioButton_dark.setChecked(True)
        else:
            self.radioButton_system.setChecked(True)
            if defend_Theme() == 'Light':
                self.setLightTheme()
            else:
                self.setDarkTheme()

        self.currentError = None
        self.current_language2 = None
        self.coordinate_x = None
        self.coordinate_z = None
        QTimer.singleShot(0, self.on_qwindow)

        numbers_regex = QtCore.QRegExp("(^[+-]?0*[0-9]{1,7}(\.[0-9]*)?|\.[0-9]+$)|"
                                       "(^[+-]?0*1[0-9]{7}(\.[0-9]*)?$)|"
                                       "(^[+-]?0*2[0-8][0-9]{6}(\.[0-9]*)?$)|"
                                       "(^[+-]?0*29[0-8][0-9]{5}(\.[0-9]*)?$)|"
                                       "(^[+-]?0*299[0-8][0-9]{4}(\.[0-9]*)?$)|"
                                       "(^[+-]?0*2999[0-8][0-9]{3}(\.[0-9]*)?$)|"
                                       "(^[+-]?0*29999[0-8][0-9]{2}(\.[0-9]*)?$)|"
                                       "(^[+-]?0*299999[0-7][0-9](\.[0-9]*)?$)|"
                                       "(^\-0*2999998[0-3](\.[0-9]*)?$)|"
                                       "(^[+]?0*2999998[0-2](\.[0-9]*)?$)|"
                                       "(^\-0*29999984(\.[0]*)?$)|"
                                       "(^[+]?0*29999983(\.[0]*)?$)")

        angle_regex = QtCore.QRegExp("[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)")

        float_validator = QtGui.QRegExpValidator(numbers_regex)
        angle_validator = QtGui.QRegExpValidator(angle_regex)

        self.x1.setValidator(float_validator)
        self.z1.setValidator(float_validator)
        self.x2.setValidator(float_validator)
        self.z2.setValidator(float_validator)
        self.alpha.setValidator(angle_validator)
        self.beta.setValidator(angle_validator)

        self.clipboard = QtWidgets.QApplication.clipboard()

        self.x1.textChanged.connect(self.calculations_check)
        self.z1.textChanged.connect(self.calculations_check)
        self.x2.textChanged.connect(self.calculations_check)
        self.z2.textChanged.connect(self.calculations_check)
        self.alpha.textChanged.connect(self.calculations_check)
        self.beta.textChanged.connect(self.calculations_check)

        self.btn_command.clicked.connect(self.copy_func)
        self.paste_1.clicked.connect(self.paste1)
        self.paste_2.clicked.connect(self.paste2)
        self.btn_clear.clicked.connect(self.clear)

        self.comboBox.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.comboBox.view().window().setAttribute(Qt.WA_TranslucentBackground)
        self.comboBox.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)

        self.comboBox.view().setAutoScroll(False)
        self.comboBox.currentIndexChanged.connect(self.language)
        # self.comboBox.setItemDelegate(SelectDelegate(self.comboBox))

        with sqlite3.connect('database.db') as db:
            cursor = db.cursor()
            self.current_language = cursor.execute(f""" SELECT language FROM current """).fetchone()[0]
            self.comboBox.setCurrentText(self.current_language)

        self.change_language(self.current_language)

        self.radioButton_light.toggled.connect(self.radioButtonCheck)
        self.radioButton_dark.toggled.connect(self.radioButtonCheck)
        self.radioButton_system.toggled.connect(self.radioButtonCheck)

    def on_qwindow(self):
        self.qwindow = self.windowHandle()
        self.qwindow.activeChanged.connect(self.handle_activeChanged)

    def handle_activeChanged(self):
        if self.qwindow.isActive():
            if current('theme') == translate('radioButton_light', current("language")):
                self.setLightTheme()
                self.radioButton_light.setChecked(True)
            elif current('theme') == translate('radioButton_dark', current("language")):
                self.setDarkTheme()
                self.radioButton_dark.setChecked(True)
            else:
                self.radioButton_system.setChecked(True)
                if defend_Theme() == 'Light':
                    self.setLightTheme()
                else:
                    self.setDarkTheme()

    def setLightTheme(self):
        self.x1.setStyleSheet(styles.lineEdit_light)
        self.z1.setStyleSheet(styles.lineEdit_light)
        self.x2.setStyleSheet(styles.lineEdit_light)
        self.z2.setStyleSheet(styles.lineEdit_light)
        self.alpha.setStyleSheet(styles.lineEdit_light)
        self.beta.setStyleSheet(styles.lineEdit_light)
        self.x0.setStyleSheet(styles.lineEdit_0_light)
        self.z0.setStyleSheet(styles.lineEdit_0_light)
        self.tabWidget.setStyleSheet(styles.tabWidget_light)

        self.setStyleSheet(styles.mainWindow_light)
        self.first_eye.setStyleSheet(styles.label_light)
        self.second_eye.setStyleSheet(styles.label_light)
        self.label_coordinates.setStyleSheet(styles.label_light)
        self.label_mode.setStyleSheet(styles.label_light)
        self.label_language.setStyleSheet(styles.label_light)
        self.comboBox.setStyleSheet(styles.comboBox_light)
        self.radioButton_light.setStyleSheet(styles.radioButton_light)
        self.radioButton_dark.setStyleSheet(styles.radioButton_light)
        self.radioButton_system.setStyleSheet(styles.radioButton_light)
        self.textBrowser.setStyleSheet(styles.textBrowser_light)

    def setDarkTheme(self):
        self.x1.setStyleSheet(styles.lineEdit_dark)
        self.z1.setStyleSheet(styles.lineEdit_dark)
        self.x2.setStyleSheet(styles.lineEdit_dark)
        self.z2.setStyleSheet(styles.lineEdit_dark)
        self.alpha.setStyleSheet(styles.lineEdit_dark)
        self.beta.setStyleSheet(styles.lineEdit_dark)
        self.x0.setStyleSheet(styles.lineEdit_0_dark)
        self.z0.setStyleSheet(styles.lineEdit_0_dark)
        self.tabWidget.setStyleSheet(styles.tabWidget_dark)

        self.setStyleSheet(styles.mainWindow_dark)
        self.first_eye.setStyleSheet(styles.label_dark)
        self.second_eye.setStyleSheet(styles.label_dark)
        self.label_coordinates.setStyleSheet(styles.label_dark)
        self.label_mode.setStyleSheet(styles.label_dark)
        self.label_language.setStyleSheet(styles.label_dark)
        self.comboBox.setStyleSheet(styles.comboBox_dark)
        self.radioButton_light.setStyleSheet(styles.radioButton_dark)
        self.radioButton_dark.setStyleSheet(styles.radioButton_dark)
        self.radioButton_system.setStyleSheet(styles.radioButton_dark)
        self.textBrowser.setStyleSheet(styles.textBrowser_dark)

    def radioButtonCheck(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            save('theme', radioButton.text())
            # setTheme(self)
            if current('theme') == translate('radioButton_light', current("language")):
                self.setLightTheme()
                self.radioButton_light.setChecked(True)
            elif current('theme') == translate('radioButton_dark', current("language")):
                self.setDarkTheme()
                self.radioButton_dark.setChecked(True)
            else:
                self.radioButton_system.setChecked(True)
                if defend_Theme() == 'Light':
                    self.setLightTheme()
                else:
                    self.setDarkTheme()

    def paste1(self):
        coordinates = pyperclip.paste().split()
        try:
            float(coordinates[6]) + float(coordinates[8]) + float(coordinates[9])
            self.x1.setText(coordinates[6])
            self.z1.setText(coordinates[8])
            self.alpha.setText(str(round(round(float(coordinates[9]), 2) % 360, 2)))
        except Exception:
            pass

    def paste2(self):
        coordinates = pyperclip.paste().split()
        try:
            float(coordinates[6]) + float(coordinates[8]) + float(coordinates[9])
            self.x2.setText(coordinates[6])
            self.z2.setText(coordinates[8])
            self.beta.setText(str(round(round(float(coordinates[9]), 2) % 360, 2)))
        except Exception:
            pass

    def clear(self):
        self.x1.setText('')
        self.z1.setText('')
        self.alpha.setText('')
        self.x2.setText('')
        self.z2.setText('')
        self.beta.setText('')
        self.x0.setText('')
        self.z0.setText('')

    def change_language(self, language):
        html = current('html')
        version = current('version')
        text = translate('textBrowser', f'{language}')
        line = html.replace('[version]', version)
        line = line.replace('[text]', text)
        self.textBrowser.setHtml(line)
        self.label_language.setText(translate('label_language', f'{language}'))
        self.first_eye.setText(translate('first_eye', f'{language}'))
        self.second_eye.setText(translate('second_eye', f'{language}'))
        self.label_coordinates.setText(translate('label_coordinates', f'{language}'))
        self.btn_command.setText(translate('btn_command', f'{language}'))
        self.tabWidget.setTabText(0, translate('tabWidget', f'{language}'))
        self.tabWidget.setTabText(1, translate('tabWidget2', f'{language}'))
        self.alpha.setPlaceholderText(translate('alpha', f'{language}'))
        self.beta.setPlaceholderText(translate('beta', f'{language}'))
        self.paste_1.setText(translate('paste_1', f'{language}'))
        self.paste_2.setText(translate('paste_2', f'{language}'))
        self.btn_clear.setText(translate('btn_clear', f'{language}'))
        self.label_mode.setText(translate('label_mode', f'{language}'))
        self.radioButton_light.setText(translate('radioButton_light', f'{language}'))
        self.radioButton_dark.setText(translate('radioButton_dark', f'{language}'))
        self.radioButton_system.setText(translate('radioButton_system', f'{language}'))
        if self.currentError == "error_parallel":
            self.x0.setText(translate('error', f'{language}'))
            self.z0.setText(translate('error_parallel', f'{language}'))
        elif self.currentError == "error_intersection":
            self.x0.setText(translate('error', f'{language}'))
            self.z0.setText(translate('error_intersection', f'{language}'))
        elif self.currentError == "error_out":
            self.x0.setText(translate('error', f'{language}'))
            self.z0.setText(translate('error_out', f'{language}'))
        else:
            pass

    def clickBox(self, state):
        global click
        if state == QtCore.Qt.Checked:
            click = True
        else:
            self.calculations_check()

    def language(self):
        self.change_language(self.comboBox.currentText())
        save(current='language', label=self.comboBox.currentText())
        self.current_language = current('language')

    def calculations_check(self):
        try:
            self.calculations()
        except Exception:
            self.x0.setText("")
            self.z0.setText("")

    def error_parallel(self):
        self.currentError = "error_parallel"
        self.x0.setText(translate('error', self.current_language))
        self.z0.setText(translate('error_parallel', self.current_language))

    def error_intersection(self):
        self.currentError = "error_intersection"
        self.x0.setText(translate('error', self.current_language))
        self.z0.setText(translate('error_intersection', self.current_language))

    def error_out(self):
        self.currentError = "error_out"
        self.x0.setText(translate('error', self.current_language))
        self.z0.setText(translate('error_out', self.current_language))

    def calculations(self):
        self.coordinate_x = None
        self.coordinate_z = None
        qx1 = float(self.x1.text())
        qx2 = float(self.x2.text())
        qz1 = float(self.z1.text())
        qz2 = float(self.z2.text())
        qalpha = float(self.alpha.text())
        qbeta = float(self.beta.text())

        if decart(qalpha) == decart(qbeta):
            self.error_parallel()
        else:
            x = (qz2 - qz1 + tan(radians(decart(qalpha))) * qx1 - tan(radians(decart(qbeta))) * qx2) / (
                    tan(radians(decart(qalpha))) - tan(radians(decart(qbeta))))
            z = ((qx1 - qx2) * tan(radians(decart(qalpha))) * tan(radians(decart(qbeta))) + tan(
                radians(decart(qalpha))) * qz2
                 - tan(radians(decart(qbeta))) * qz1) / (tan(radians(decart(qalpha))) - tan(radians(decart(qbeta))))

            if not (-29999984 <= x <= 29999983 or -29999984 <= z <= 29999983):
                self.error_out()

            elif eval(condition(decart(qalpha), x, z, qx1, qz1)) and \
                    eval(condition(decart(qbeta), x, z, qx2, qz2)):
                self.x0.setText(str(int(x)))
                self.z0.setText(str(int(z)))
                self.coordinate_x = self.x0.text()
                self.coordinate_z = self.z0.text()
                self.currentError = None

            else:
                self.error_intersection()

    def copy_func(self):
        if self.coordinate_x is None and self.coordinate_z is None:
            pass
        else:
            self.clipboard.setText(f'tp @s {self.coordinate_x} ~ {self.coordinate_z}')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon('ender_eye.png'))
    app.setStyleSheet(styles.app_style)
    MainWindow = Ui_MainWindow()
    MainWindow.setWindowIcon(QIcon('ender_eye.png'))
    MainWindow.show()
    sys.exit(app.exec_())
