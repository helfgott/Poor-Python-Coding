#!/usr/bin/python

import json
def requestStartParameters():
    """
    mortiz 23/07/2020
    Controlamos de forma centralizada los parametros de inicio de los clientes
    aunque en el futuro cada cliente tendra su opcion local para 'override' estos valores.
    """
    return json.dumps(
            {
               'MYCLIENT':'THISCLIENT',
               'VPNSERVER':'THISVPNSRV',
               'VIRTUALDESKTOP':'THISONE'
            })
