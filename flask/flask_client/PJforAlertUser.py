#!/usr/bin/env python3
# Modulo para enviar avisos en ventanas al usuario
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

def alertUserWindow(window,ReturnCode, ReturnValue, Message) :
    if ReturnCode % 2 == 0:
        return QMessageBox.about(window, "Advertencia: {}".format(Message), "PJ CODIGO: {} \n\n MENSAJE: {} \n\n INFO: {}".format(ReturnCode, ReturnValue, Message))
    else :
        return QMessageBox.about(window, "Advertencia: {}".format(Message), "PJ CODIGO ERROR: {}\n\n MENSAJE: {}\n\n INFO: {}".format(ReturnCode, ReturnValue, Message))
