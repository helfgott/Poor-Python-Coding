#!/usr/bin/python
# -------------------- Este script es entregado por puppet (role_base)
# Documentacion: 

import gsdHTTPRequests
import gsdRCtoJson 
from gsdVariables import rcStatusEndpoint, postTimeout

gsdRCStatus = gsdRCtoJson.transformar_data_to_json()

print gsdHTTPRequests.httpPostRequest( rcStatusEndpoint, gsdRCStatus, postTimeout )

