#!/usr/bin/env python3
# mortiz: PJLogin
# parte del codigo fue reciclado de PyLogin de Sebastian Segato
# Revisar la documentacion, todo numero par de las tuplas regresadas por el servidor son codigos exitosos
# Todos los codigos de la aplicacion estan en la documentacion

import logging
import PJVariables 

#------ Set logging level
# According to python: "this function should be called from the main thread before other threads are started"
# mortiz: do not change the position of this line, weird things may happen if you do it.
logFormat = '%(asctime)s : %(levelname)s : %(filename)s : %(message)s'
logging.basicConfig(filename=PJVariables.LoggingPJ,filemode='w', format=logFormat, datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

import sys,os
from PyQt5.QtGui import *
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import * 
import PJforSSH            # Para establecer las llaves FIXME: esto debe ir en el servidor cuando tenga /home
import PJforEncriptarClave # Encriptamos en b64 usuario y password antes de enviar los datos al servidor  
import PJforHTTPRequests   # Modulo que maneja las peticiones HTTP POST 
import PJforTHETECHTemplate     # Se utiliza para la generacion del template de THETECH
import PJforNetworkStatus  # Verifica la conectividad local del equipo y nos da la direccion IP
import PJforAlertUser      # Para mostrarle ventanas al usuario cuando hay errores o eventos
import PJforVPNSRVx        # Nos trae los servidores VPNSRV{SERVER,SERVER1} disponibles luego de evaluarlos con netcat
import PJforSubprocess     # Modulo para el lanzamiento de subprocesos, como Tomcat o THETECH
from subprocess import Popen, PIPE

#------------------------------------------------------------------ Some Vars
# Variables que necesitan inicializacion 
# Sin embargo las variables / parametros van en PJVariables.py
#-------------------------------------------------------------------------

usuario = None 
password = None
challengeLogin = None

#------------------------------------------------------------------ Logging
# Logging de la aplicacion 
# solo si necesitamos un handler especifico 
#-------------------------------------------------------------------------

#log = logging.getLogger(__name__)
#logHandler = logging.FileHandler(filename=PJVariables.LoggingPJ, mode="a", encoding=None, delay=False)
#logFormat = logging.Formatter('%(asctime)s - [ %(levelname)s ]- %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')
#logHandler.setFormatter(logFormat)
#logHandler.setLevel(logging.DEBUG)
#logging.addHandler(logHandler)

#------------------------------------------------------------------ Design
# Diseno de la interfaz grafica, formulario, labels, textbox y botones
#-------------------------------------------------------------------------
# crear ventana
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle ('Acceso a Sucursal')
window.resize(200,100)

#labels
label1 = QLabel(window)
label2 = QLabel(window)
label1.setText("Legajo")
label2.setText('Contrasena')

# button
button = QPushButton('Conectar a Sucursal - THETECH', window)
button.move(20,180)

# crear textbox
# Horiontal | Vertical
usuario = QLineEdit(window)
usuario.setFixedWidth(220)
usuario.setFixedHeight(30)

password = QLineEdit(window)
password.setEchoMode(QLineEdit.Password) 
password.returnPressed.connect(button.click)
password.setFixedWidth(220)
password.setFixedHeight(30)

#Ordenar layout
lbox = QFormLayout()
lbox.addRow(label1, usuario)
lbox.addRow(label2, password)
lbox.addRow(button)
window.setLayout(lbox)

#------------------------------------------------------ Styles
# Funcionan bajo las mimas reglas de CSS
#-------------------------------------------------------------
label1.setStyleSheet("color:#fff;font-size:20px;") 
label2.setStyleSheet("color:#fff;font-size:20px;")

usuario.setStyleSheet("background-color:#fff; color:#000;;")
password.setStyleSheet("background-color:#fff; color:#000;")

button.setStyleSheet("background-color:blue;color:#fff;font-size:22px;font-weight:bold;margin-top:20px;margin-bottom:20px;")

window.setStyleSheet("background-color:#004481;color:#fff")

#----------------------------------------------------------- Acciones
# La interaccion con la parte grafica, como pulsar un boton
#---------------------------------------------------------------------
@pyqtSlot()
def on_click():
    # PJforNetworkStatus, evalua las interfaces de red y obtiene la IP
    logging.info('{}{:^10}{} Obtener IP'.format(str('_')*30,'[STEP]',str('_')*30))
    IPADDR =  PJforNetworkStatus.networkStatus()
    logging.info('Network status devuelve: %s', IPADDR)
    if IPADDR['ReturnCode'] % 2 == 0 :
        IPADDR = IPADDR['ReturnValue']
        logging.info('Se ha asignado correctamente direccion IP: {}'.format(IPADDR))
    else :
        return PJforAlertUser.alertUserWindow(window,IPADDR['ReturnCode'], IPADDR['ReturnError'], IPADDR['ReturnMessage'])
      
    # Con strip eliminamos espacios vacios, Validamos los datos ingresados en el formulario y Limpiamos los campos  
    if str(usuario.text()).strip() == '' or str(password.text()).strip() == '' :
        usuario.setText('')
        password.setText('')
        nullLogin = {'ReturnCode': 3,'ReturnError':'Ingrese usuario y contrasena','ReturnMessage':'Complete los campos'}
        logging.warning(str(nullLogin))
        return PJforAlertUser.alertUserWindow(window,nullLogin['ReturnCode'], nullLogin['ReturnError'], nullLogin['ReturnMessage'])
    else :
        #______________________________________________________________________________ CHECK VPNSRV{SERVER,SERVER1} AVAILABILITY
        # Si hay minimamente uno de los dos servidores disponibles avanzamos, caso contrario avisamos al usuario

        logging.info('{}{:^10}{} Obtener Servidor VPNSRV'.format(str('_')*30,'[STEP]',str('_')*30))
        notValid, validVPNSRVServers = PJforVPNSRVx.validateVPNServers()

        if not validVPNSRVServers :
            return PJforAlertUser.alertUserWindow(window,notValid['ReturnCode'], notValid['ReturnError'], notValid['ReturnMessage'])

#        #______________________________________________________________________________ VARIABLES REMOTAS 
        if PJVariables.getParametersValue == True :
            logging.info('{}{:^10}{} Obtener Parametros Remotos'.format(str('_')*30,'[STEP]',str('_')*30))
            getParameters = {
                            'getParameters':PJVariables.getParametersValue
                            }
#            # Si es <bool:True> entonces hacemos un POST para pedir al server los parametros centralizados
            centralParameters = PJforHTTPRequests.httpPostRequest(PJVariables.pjCentralParameters, PJVariables.getParametersValue, PJVariables.postTimeout)

            # ___________Asignacion de variables remotas________
            if centralParameters['ReturnCode'] % 2  == 0: 
                # Servidor tentativo obtenido remotamente (normalmente esperamos un VPNSRV{SERVER1,SERVER}
#
                REMOTEVALUES = eval(centralParameters['ReturnValue'])
                TENTATIVEVPNSERVER = REMOTEVALUES['VPNSERVER']

                # sobreescribimos las variables locales de PJVariables por las centralizadas
                PJVariables.defaultTSCLIENT = REMOTEVALUES['THETECHTS']
                PJVariables.defaultTHETECHCLIENT = REMOTEVALUES['THETECHCLIENT']
                logging.info('RemoteVariables;{:>3}, PSTHE_TECHTS;{:>3}, THETECHCLIENT:{:>3}'.format(TENTATIVEVPNSERVER,PJVariables.defaultTSCLIENT,PJVariables.defaultTHETECHCLIENT))

               
                # determinar si el servidor elegido remotamente, esta disponible localmente, esto evita que seamos despotas en las decisiones
                # y si lo fueramos, entonces que no erremos :)
                if TENTATIVEVPNSERVER in validVPNSRVServers :
                    VPNSERVER = TENTATIVEVPNSERVER
                else:
                    VPNSERVER = validVPNSRVServers[0]
            else :
                logging.error('Falla al obtener variables remotas, usaremos los valores locales, error:{}'.format(centralParameters))
                # Si no hay valores remotos, entonces usamos lo que devuelve el modulo local
                VPNSERVER = validVPNSRVServers[0]    

        else :
                logging.info('{}{:^10}{} Obtener Parametros Locales'.format(str('_')*30,'[STEP]',str('_')*30))
                logging.info('Se omiten los valores centralizados')
                VPNSERVER = validVPNSRVServers[0]   
                logging.info('Utilizamos: VPNSERVER: {}, PJVariables.defaultTHETECHCLIENT: {}, PJVariables.defaultTSCLIENT: {}'.format(VPNSERVER, PJVariables.defaultTHETECHCLIENT, PJVariables.defaultTSCLIENT))

   
        # Tristemente en pyQt los textbox regresan valorescomo PyQt4.QtCore.QString
        # eso nos obliga a formatear el string con %s % usuario.text() por ejemplo, puede 
        # probar haciendo type(usuario.text()) 
        # Solicitamos autenticarnos ante el servidor testingLogins
        logging.info('{}{:^10}{} Autenticacion'.format(str('_')*30,'[STEP]',str('_')*30))
        logging.info('Autenticamos legajo: {} contra LDAP en pjLogins'.format(usuario.text()))
        
        # armamos un dict() y lo pasamos como parametro a nuestro modulo de POST Requests
        LoginUserData = {
                         'user' : usuario.text(),
                         'password' : password.text(),
                         'usertype' : PJVariables.USERTYPE 
                        }
        challengeLogin = PJforHTTPRequests.httpPostRequest(PJVariables.pjLoginEndpoint, LoginUserData, PJVariables.postTimeout)
        
        # Validamos el codigo de salida de challengeLogin
        if challengeLogin['ReturnCode'] % 2 == 0 :
            logging.info(challengeLogin['ReturnCode'])
        else :
            logging.error(challengeLogin)
            # Informamos al usuario visualmente del problema
            return PJforAlertUser.alertUserWindow(
                                                    window,
                                                    challengeLogin['ReturnCode'], 
                                                    challengeLogin['ReturnError'], 
                                                    challengeLogin['ReturnMessage']
                                                    )
    # [Identify Device]
    logging.info('{}{:^10}{} Script Identify Device'.format(str('_')*30,'[STEP]',str('_')*30))
    # Recuerden el & para no interrumpir este programa
    os.system(PJVariables.scriptIdentifyDevice + ' ' + usuario.text().strip() + '&')

    if challengeLogin['ReturnCode'] % 2 == 0 :
        """
        En caso de login exitoso, cuando el usuario y la password son correctas
        """
        logging.info('Autenticacion exitosa: %s' ,challengeLogin)
        # [get_updates.py] debe manejar su propio timeout, aqui solo devolvemos la salida del script
        # el ampersand garantiza el background del proceso para no interrumpir el login
        # Recuerden el & para no interrumpir este programa
        logging.info('{}{:^10}{} Script PJ Updater'.format(str('_')*30,'[STEP]',str('_')*30))
        os.system(PJVariables.scriptUpdateNotebook + '&')
          
        # PJforEncriptarClave, encripta la contrasena plana en b64
        logging.info('{}{:^10}{} Encriptar Clave'.format(str('_')*30,'[STEP]',str('_')*30))
        PASSCRIPT = PJforEncriptarClave.encriptarClave(password.text())
        
        # [tomcat]
        logging.info('{}{:^10}{} Tomcat'.format(str('_')*30,'[STEP]',str('_')*30))
        PJforSubprocess.runSubprocess(PJVariables.subProcTomcat)

        if PJVariables.defaultTHETECHCLIENT == 'FREETHETECH' :
            # !IMPORTANTE es necesario encriptar con scramble de Perl
            logging.info('{}{:^10}{} Encriptar Clave'.format(str('_')*30,'[STEP]',str('_')*30))
            PASSCRIPT = PJforEncriptarClave.encriptarClaveFreeTHETECH(password.text())           
            generateFreeTHETECHTemplate = PJforTHETECHTemplate.crearTemplateFREETHETECH( str(usuario.text()) , PASSCRIPT , str(VPNSERVER)) 
            if generateFreeTHETECHTemplate['ReturnCode'] % 2 == 0 :
                logging.info('Parece que todo va bien con el template FREETHETECH')
                logging.info('{}{:^10}{} Lanzando legacy FREETHETECH'.format(str('_')*30,'[STEP]',str('_')*30))
                PJforSubprocess.runSubprocess(PJVariables.subProcFREETHETECH)
            else :
                return PJforAlertUser.alertUserWindow(
                                                       window,
                                                        generateFreeTHETECHTemplate['ReturnCode'], 
                                                        generateFreeTHETECHTemplate['ReturnError'], 
                                                        generateFreeTHETECHTemplate['ReturnMessage']
                                                        )
        else :
            # nuevo cliente
            # PJforSSH, genera las llaves locales y las copia a VPNSRVSERVER1 y PSTHE_TECHTS
            logging.info('{}{:^10}{} PJforSSH'.format(str('_')*30,'[STEP]',str('_')*30))
            generateKeys = PJforSSH.create_ssh_keys( VPNSERVER , usuario.text() , password.text() )
            if generateKeys['ReturnCode'] % 2 == 0 :
                logging.info('Proceso SSH/SFTP terminado')
            else :
                return PJforAlertUser.alertUserWindow(
                                                        window,
                                                        generateKeys['ReturnCode'], 
                                                        generateKeys['ReturnError'], 
                                                        generateKeys['ReturnMessage']
                                                        )
 

            # PJforTHETECHTemplate, genera el template de THETECH
            logging.info('{}{:^10}{} Template THETECH'.format(str('_')*30,'[STEP]',str('_')*30))
            generateTHETECHTemplate = PJforTHETECHTemplate.crearTemplateTHETECH(VPNSERVER, usuario.text(), PASSCRIPT, IPADDR)  
            
            if generateTHETECHTemplate['ReturnCode'] % 2 == 0 :
                THETECH_TEMPLATE = generateTHETECHTemplate['ReturnValue'] 
                logging.info('Template generado: {}'.format(THETECH_TEMPLATE))
            else :
                return PJforAlertUser.alertUserWindow(
                                                        window,
                                                        generateTHETECHTemplate['ReturnCode'], 
                                                        generateTHETECHTemplate['ReturnError'], 
                                                        generateTHETECHTemplate['ReturnMessage']
                                                        )
               
            #[thetechplayer], inicia el cliente de THETECH en la notebook
            logging.info('{}{:^10}{} Cliente THETECH'.format(str('_')*30,'[STEP]',str('_')*30))
            PJforSubprocess.runSubprocess(PJVariables.subProcTHETECHTS)
#
    elif challengeLogin[0] == 319 :
        # Iniciar cambio de clave, solicitamos cambio de clave testingLogins
        # Pasamos por parametro el legajo y contrasena suministrados
        # FIXME agregar timeout para el cambio de clave
        logging.warning('Cambio de clave requerido: %s' ,challengeLogin)
        os.system(ChangePassword + " %s %s" % (usuario.text() ,password.text()))
    else :
        # El servidor regresara una tupla con los mensajes de error posibles
        # Se presentara una ventana y se agrega el log en el box del app y en una ventana visible para el usuario
        logging.error('Autenticacion fallida: %s', challengeLogin)
        QMessageBox.about(window, str(challengeLogin[0]), str(challengeLogin) )

button.clicked.connect(on_click)
window.show()
app.exec_()
