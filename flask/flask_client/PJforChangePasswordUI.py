#!/usr/bin/python

import sys, logging
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PJVariables import LoggingPJ, pjChangePwdEndpoint, postTimeout
import PJforHTTPRequests
#import PJforChangePasswordRequest # Modulo para solicitar cambio de password por HTTP al API
import PJforAlertUser
#________________________________________________________________________________________________________________ Set logging level
# According to python: "this function should be called from the main thread before other threads are started"
# mortiz: do not change the position of this line, weird things may happen if you do it.
logFormat = '%(asctime)s : %(levelname)s : %(filename)s : %(message)s'
logging.basicConfig(filename=LoggingPJ,filemode='w', format=logFormat, datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

#_________________________________required variables
CURRENTUSER=sys.argv[1]
CURRENTPASSWORD=sys.argv[2]

#________________________________ Design
# crear ventana
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle ('Cambiar clave RACFID')
window.resize(420,200)
#window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
window.setGeometry(120,120,80,80)
#labels
label2 = QLabel(window)
label3 = QLabel(window)
label2.setText('Nueva Contrasena')
label3.setText('Confirme nueva contrasena')

# crear textbox
# Horiontal | Vertical

new_pass = QLineEdit(window)
new_pass.setFixedWidth(120)
new_pass.setFixedHeight(30)

new_pass_confirm =  QLineEdit(window)
new_pass_confirm.setFixedWidth(120)
new_pass_confirm.setFixedHeight(30)

# button
button = QPushButton('Cambiar clave', window)
button.move(20,180)

lbox = QFormLayout()
lbox.addRow(label2, new_pass)
lbox.addRow(label3, new_pass_confirm)
lbox.addRow(button)
window.setLayout(lbox)

#------------------------------------------------------ styles
label2.setStyleSheet("color:#135cae;font-size:17px;")
label3.setStyleSheet("color:#135cae;font-size:17px;")

new_pass.setStyleSheet("background-color:#fff")
new_pass_confirm.setStyleSheet("background-color:#fff")

button.setStyleSheet("background-color:#fff;color:#000;font-size:17px;")

window.setStyleSheet("background-color:#fff;")
#--------------------------------------------- Acciones

@pyqtSlot()
def on_click():
       
        logging.info('___________________________________ Comienza aplicacion UI PJforChangePassword')
        NEWPASSWORD = new_pass.text()
        NEWPASSWORDCONFIRM = new_pass_confirm.text()
        # Validamos que las dos nuevas claves se hayan escrito correctamente en las casillas
        if NEWPASSWORD == NEWPASSWORDCONFIRM :
                pjChangePassword = {
                                    'user' : CURRENTUSER,
                                    'currentpassword': CURRENTPASSWORD,
                                    'newpassword' : NEWPASSWORD
                                   }
                reqPwdChange = PJforHTTPRequests .httpPostRequest(pjChangePwdEndpoint, pjChangePassword, postTimeout)
                if  reqPwdChange['ReturnCode'] % 2 == 0 :
                    PJforAlertUser.alertUserWindow(window,reqPwdChange['ReturnCode'],reqPwdChange['ReturnValue'], reqPwdChange['ReturnMessage'])
                    logging.info('Parece que el password se cambio correctamente')
                    logging.info(reqPwdChange)
                    app.exit()
                    return reqPwdChange
                else :
                    logging.error('Hubo algun problema con el cambio de password en el servidor PJLogin')
                    logging.error(reqPwdChange)
                    PJforAlertUser.alertUserWindow(window,reqPwdChange['ReturnCode'],reqPwdChange['ReturnError'], reqPwdChange['ReturnMessage'])
                    app.exit()
        else :
                # FIXME no esta validando si los campos son vacios
                #print "contrasenas no coinciden" 
                PJforAlertUser.alertUserWindow(window, 99,'PASSWORD NO CAMBIADO', 'Los password en las casillas no coinciden, confirme su nuevo password correctamente.')
                logging.info('99, No se puede cambiar la clave, Los password no coinciden en las casillas')

button.clicked.connect(on_click)
window.show()
app.exec_()
