app_style = """
/* Панель заголовка */
TitleBar {
    background-color: rgb(54, 157, 180);
}"""


lineEdit_light = '''
 QLineEdit {	
	border: 2px solid rgb(212, 215, 255);
	border-radius: 10px;
	padding-left: 5px;
	padding-right: 5px;
	background-color: rgb(243, 244, 255);
}

 QLineEdit:hover {
	border: 2px solid rgb(194, 194, 255);
}

 QLineEdit:focus {
	border: 2px solid rgb(140, 146, 255);
}
'''

lineEdit_dark = '''
 QLineEdit {	
	border: 2px solid rgb(212, 215, 255);
	border-color: rgb(123, 125, 148);
	border-radius: 10px;
	padding-left: 5px;
	padding-right: 5px;
	background-color: rgb(51, 51, 54);
	color: rgb(231, 231, 231);
}

 QLineEdit:hover {
	border-color: rgb(141, 141, 185);
}

 QLineEdit:focus {
	border: 2px solid rgb(140, 146, 255);
}  
'''

lineEdit_0_light = '''
 QLineEdit {	
	border: 2px solid rgb(212, 215, 255);
	border-radius: 10px;
	padding-left: 5px;
	padding-right: 5px;
	background-color: rgb(243, 244, 255);
}
'''

lineEdit_0_dark = '''
 QLineEdit {	
	border: 2px solid rgb(212, 215, 255);
	border-color: rgb(123, 125, 148);
	border-radius: 10px;
	padding-left: 5px;
	padding-right: 5px;
	background-color: rgb(51, 51, 54);
	color: rgb(231, 231, 231);
} 
'''

tabWidget_light = '''
 QTabBar::tab {	
	border: 2px solid rgb(212, 215, 255);
	border-radius: 10px;
	margin-left: 10px;
	padding-left: 5px;
	padding-right: 5px;
	background-color: rgb(243, 244, 255);
}

 QTabBar::tab:hover {
	border: 2px solid rgb(194, 194, 255);
}

 QTabBar::tab:selected {
    background: rgb(129, 135, 255);
	color: rgb(248, 246, 255);
	border: 2px solid rgb(129, 135, 255);
}

 QTabWidget::pane{
	border: 1px;
	background: rgb(129, 135, 255);
}
'''

tabWidget_dark = '''
 QTabBar::tab {	
	border: 2px solid rgb(212, 215, 255);
	border-color: rgb(123, 125, 148);
	border-radius: 10px;
	margin-left: 10px;
	padding-left: 5px;
	padding-right: 5px;
	background-color: rgb(51, 51, 54);
	color: rgb(231, 231, 231);
}

QTabBar::tab:hover {
	border-color: rgb(141, 141, 185);
}

 QTabBar::tab:selected {
    background: rgb(129, 135, 255);
	color: rgb(248, 246, 255);
	border: 2px solid rgb(129, 135, 255);
}

 QTabWidget::pane{
	border: 1px;
	background: rgb(129, 135, 255);
}
'''

mainWindow_light = '''background-color: rgb(255, 255, 255);'''

mainWindow_dark = '''background-color: rgb(68, 70, 79);'''

label_light = ''''''

label_dark = '''color: rgb(231, 231, 231);'''

comboBox_light = '''
 QComboBox {
	border: 2px solid rgb(212, 215, 255);
	border-radius: 10px;
	padding-left: 5px;
	padding-right: 5px;
	background-color: rgb(243, 244, 255);
 }

 QComboBox:hover {
	border: 2px solid rgb(194, 194, 255);
}


 QComboBox::drop-down {
    width: 0px;
    height: 0px;
    border: 0px;
}


 QComboBox QAbstractItemView {
    color: rgb(0, 0, 0);
    background-color: rgb(243, 244, 255);
    padding: 5px;
  	border: 2px solid rgb(212, 215, 255);
	border-radius: 10px;
	padding-left: 0px;
	padding-right: 0px;
	selection-background-color: rgb(140, 146, 255);
	margin-top: 8px;
	outline: 0px;
}


/* ===================== QScrollBar ======================= */
 QScrollBar:vertical {
	border: none;
	background-color: rgb(243, 244, 255);
    width: 10px;
}

 QScrollBar::handle:vertical {
    background-color: rgb(194, 194, 255);       
    min-height: 5px;
    border-radius: 4px;
}

 QScrollBar::handle:vertical:hover{
    background-color: rgb(140, 146, 255);
    min-height: 5px;
    border-radius: 4px;
}

 QScrollBar::handle:vertical:pressed{
    background-color: rgb(115, 115, 255);
    min-height: 5px;
    border-radius: 4px;
}

 QScrollBar::sub-line:vertical {
    margin: 3px 0px 3px 0px; 
    border-image: url(./images/up_arrow.png); 
    height: 10px;
    width: 0px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

 QScrollBar::add-line:vertical {
    margin: 3px 0px 3px 0px; 
    border-image: url(./images/up_arrow_disabled.png);      
    height: 10px;
    width: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

 QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {
    border-image: url(./images/up_arrow.png);                 
    height: 10px;
    width: 10px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

 QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
    background: none;
}
 QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
'''

comboBox_dark = '''
 QComboBox {
	border: 2px solid rgb(212, 215, 255);
	border-color: rgb(123, 125, 148);
	border-radius: 10px;
	padding-left: 5px;
	padding-right: 5px;
	background-color: rgb(51, 51, 54);
	color: rgb(231, 231, 231);
 }

 QComboBox:hover {
	border-color: rgb(141, 141, 185);
}

 QComboBox::drop-down {
    width: 0px;
    height: 0px;
    border: 0px;
}

 QComboBox QAbstractItemView {
    background-color: rgb(51, 51, 54);
	color: rgb(231, 231, 231);
    padding: 5px;
  	border: 2px solid rgb(212, 215, 255);
	border-color: rgb(141, 141, 185);
	border-radius: 10px;
	padding-left: 0px;
	padding-right: 0px;
	selection-color: rgb(231, 231, 231);
	selection-background-color: rgb(140, 146, 255);
	margin-top: 8px;
	outline: 0px;
}

/*
    QComboBox QListView {
        outline: 2px solid rgb(141, 141, 185);     
        color: rgb(231, 231, 231);
        selection-background-color: rgb(51, 51, 54);  
        outline-radius: 5px;    
    }
*/


/* ===================== QScrollBar ======================= */
 QScrollBar:vertical {
	border: none;
	background-color: rgb(243, 244, 255);
	background-color: rgb(51, 51, 54);
    width: 10px;
}
 QScrollBar::handle:vertical {
    background-color: rgb(194, 194, 255);       
    min-height: 5px;
    border-radius: 4px;
}

 QScrollBar::handle:vertical:hover {
    background-color: rgb(140, 146, 255);
    min-height: 5px;
    border-radius: 4px;
}

 QScrollBar::handle:vertical:pressed {
    background-color: rgb(115, 115, 255);
    min-height: 5px;
    border-radius: 4px;
}

 QScrollBar::sub-line:vertical {
    margin: 3px 0px 3px 0px; 
    border-image: url(./images/up_arrow.png); 
    height: 10px;
    width: 0px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

 QScrollBar::add-line:vertical {
    margin: 3px 0px 3px 0px; 
    border-image: url(./images/up_arrow_disabled.png);      
    height: 10px;
    width: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

 QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {
    border-image: url(./images/up_arrow.png);                 
    height: 10px;
    width: 10px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

 QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
    background: none;
}

 QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
'''

radioButton_light = ''''''

radioButton_dark = '''color: rgb(231, 231, 231);'''

textBrowser_light = '''
 QTextBrowser {
	border: 2px solid rgb(212, 215, 255);
	border-radius: 10px;
	padding-left: 5px;
	padding-right: 5px;
 }
 '''

textBrowser_dark = '''
 QTextBrowser {
	border: 2px solid rgb(212, 215, 255);
	border-color: rgb(123, 125, 148);
	border-radius: 10px;
	padding-left: 5px;
	padding-right: 5px;
    color: rgb(231, 231, 231);
 }
'''
