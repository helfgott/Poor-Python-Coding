#!/usr/bin/env python3

import logging
import flask
from flask import Flask, render_template, request
app = Flask(__name__)


import gsdRecordRCstatus
import gsdRCstatusDisplay 

@app.route("/")
def hello():
    return "Nothing to see here!"

@app.route("/get/deployedrc")
def template_test():
        return render_template('template.html', foundRC=gsdRCstatusDisplay.displayRC())

@app.route('/post/rcstatus/', methods = ['POST'])
def RCStatus():
    """
    Actualiza los RC de los equipos
    """
    logging.info('Notificamos stauts de un RC: /post/rcstatus/')
    updateRCstatus = request.get_json()
    
    # Obtenemos el servidor
    callingServer = updateRCstatus['server']

    # Agregamos el dict en mongo
    updateRCstatus = gsdRecordRCstatus.updateMongo( callingServer, updateRCstatus ) 
    return str(updateRCstatus)


if __name__ == "__main__":
    app.run()
