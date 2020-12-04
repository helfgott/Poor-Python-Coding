#!/usr/bin/env python3

"""
Lanzamos subprocesos y devolvemos la salida de su ejecucion
"""

import os.path, subprocess, logging, time, re,sys

def runSubprocess(subProc):
    # https://docs.python.org/2.6/library/subprocess.html

    logging.info('Subproceso recibido para ejecutar: {}'.format(subProc))
    try:
        runProc = subprocess.Popen(
                                   subProc.split(), 
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, 
                                 )
        pid_ = runProc.pid
        output_ = runProc.stdout

        # CustomTomcatPid = Proviene del script: /opt/mygroup/bin/iniciar-tomcat.sh
        # Esperamos un string del estilo: TomcatPID:<PID>, unicamente aplica si el proceso que hemos lanzado es Tomcat
        customTomcatPid_ = str(output_.read())
        customTomcatPid_ = re.search(r'TomcatPID:\d+',customTomcatPid_)
        if customTomcatPid_ and customTomcatPid_ != None :
            customTomcatPid_ = customTomcatPid_.group(0)
            # Realizo un slice del string pues ya sabemos la longitud del valor esperado
            customTomcatPid_ = customTomcatPid_[10:] 
            logging.info('Proceso ejecutado con PID:{}'.format(str(customTomcatPid_)))
        else :
            # Cualquier otro proceso accede a su PID a traves del metodo PID de Popen
            logging.info('Proceso ejecutado con PID:{}, {}'.format(str(pid_),str(output_.read())))

        return runProc 
    except OSError as e :
        exceptOSerror = {
                         'ReturnCode': 413,
                         'ReturnError': e,
                         'ReturnMessage': 'Error de OS lanzando subproceso: {}'.format(e)
                        }       
        logging.error(exceptOSerror)
        return exceptOSerror 
    except Exception as e :
        unknownException = {
                            'ReturnCode': 415,
                            'ReturnValue': None,
                            'ReturnMessage': 'Error lanzando subproceso: Error desconocido - GRAVE {} '.format(e)
                           }
        logging.error(unknownException)
        return unknownException 
