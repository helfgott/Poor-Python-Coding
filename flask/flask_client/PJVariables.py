#!/usr/bin/env python3

import os

#____________________________________________________________________ | Settings especificos
USERTYPE = 'notebook'
defaultthistechCLIENT = 'tech'
defaultTSCLIENT = 'techserver.domain'

#____________________________________________________________________ | Template de thistech
THE_TECH_FILE_TEMPLATE='/opt/PJ-Login/thistech/Template.thetechs'
THE_TECH_SESSION_FILE='/opt/PJ-Login/thistech/sucursal.thetechs'

#____________________________________________________________________ | Servidores
THE_TECH_SERVER="thetechserver.domain"
VPNSERVERS = ['SERVER1', 'SERVER2']

#____________________________________________________________________ | TESTING Endpoint API
# ENDPOINTS - TESTING
testingEndpoint = 'http://SERVER1:22134/testingData'                              # URL TESTING, pasa por Proxy Apache en SERVER1 a server TESTING
testingLoginEndpoint = testingEndpoint + '/post/logins/notebooks'               # Testing para login
testingChangePwdEndpoint = testingEndpoint + '/post/notebooks/passwordchange'   # Endpoint para cambio de clave
testingCentralParameters = testingEndpoint + '/post/logins/parameters'          # Testing para variables centralizadas


#____________________________________________________________________ | Productive Endpoint API
# ENDPOINTS - PJLOGIN
pjServer = 'http://pjlogins.igrupocompany'                          # URL productiva
pjLoginEndpoint = pjServer + '/post/logins/notebooks'               # Endpoint para autenticacion de usuarios 
pjChangePwdEndpoint = pjServer + '/post/notebooks/passwordchange'   # Endpoint para cambio de clave
pjCentralParameters = pjServer + '/post/logins/parameters'          # Parametros centralizados en servidor PJLogin
getParametersValue = True                                             # True: Parametros remotos, False: Parametros locales del cliente
postTimeout = 10                                                      # Timeout para POST Requests

#____________________________________________________________________ | Generacion de llaves publicas/privadas
# Ejecutar con companyuser
PRI_KEY = os.environ['HOME'] + '/.ssh/id_rsa-company'
PUB_KEY = PRI_KEY + '.pub'
PRI_KEY_THE_TECH = os.environ['HOME'] + '/.ssh/id_rsa-company_thistech'
PUB_KEY_THE_TECH = PRI_KEY_THE_TECH + '.pub'

#____________________________________________________________________ |  Lanzamiento de subprocesos
# Los procesos se lanzan con Popen, consultar documentacion en xxx!!
subProctech='/usr/thistech/bin/thetechplayer --session ' +  THE_TECH_SESSION_FILE + ' --exit --hide'
subProcTomcat='sudo /opt/mygroup/bin/iniciar-tomcat.sh' 

#___________________________________________________________________ | Lanzamiento de scripts
# Los scripts se lanzan con os.system, consultar documentacion en xxx!!
scriptChangePassword = 'python3 /opt/PJ-Login/PJforChangePasswordUI.py'
scriptIdentifyDevice = 'sudo /opt/mygroup/bin/testingData_notebook.sh'
scriptUpdateNotebook = 'sudo /srv/pjupdater/main.py'
#____________________________________________________________________ |  Logging
LoggingPJ = '/tmp/pjlogin.log'

#____________________________________________________________________  |Identify Device
DEVICEINFORMATION = '/opt/PJ-Login/thistech/device.current'

#___________________________________________________________________  | Comandos locales y remotos
localCmdAuthorizedKeys = ['sed -i "/^ssh-rsa .*','\@company$/d" $HOME/.ssh/authorized_keys ; cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys']
localCmdPrivatethistech = ['echo y | ssh-keygen -m PEM -t dsa -N "secretpass" -P "" -C ', '@company -f ' + PRI_KEY_THE_TECH ]
localCmdPrivateUserKey = ['echo y | ssh-keygen -t rsa -N "" -C ' , '@company -f ' + PRI_KEY ]
remoteCmdSSH = 'rm -rf $HOME/.thetech; mkdir -p $HOME/.thetech/{fonts,config} && cp $HOME/.ssh/id_rsa_thistech.pub $HOME/.thetech/config/authorized.crt'

################################################################################################ [FREE thistech]
techlegacy_SCRIPT = 'startsuc'
techlegacy_START = 'application'
techlegacy_TEMPLATE_FILE = '/opt/PJ-Login/thistech/thislegacy_template.tmpl'
techlegacy_SESSION_FILE = '/opt/PJ-Login/thistech/thislegacy_session_file.thetechs'
subProctechlegacy='/usr/thistechOLD/bin/thetechplayer --session ' +  techlegacy_SESSION_FILE + ' --exit --hide'
