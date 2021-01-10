#!/usr/bin/env python3
# The purpose of this script is to validate email addresses according company rules primarly and RFC

"""
Disenar como rest api, se envia archivo via rest, se devulve respuesta en archivo via rest
"""
import re       # to analyze each email address

# What is an email address
# \w<chars> @ \w <validchars> . <\w>+ .?<\w>

emailAddress = '.ra..t--on@gogo.xom.ar.ed.uco'

def seems_like_an_email(emailAddress) :
    emailAddress = emailAddress.lower() # estandarizar el input para tener menos regex
    #this = r"([\w.\-_0-9]+)@([-a-z0-9]+.?){3}"
    this = r"([\w.\-_0-9]+)@(([-a-z0-9]+.?){2,3})"
    return re.search(this,emailAddress)

print(seems_like_an_email(emailAddress)[1])
print(seems_like_an_email(emailAddress)[2])

# evaluate root domains TDL accordin IANA
# https://www.iana.org/domains/root/db
# Not valid domain: e.g. www.ab- -cd.com # 3rd and 4th position dashes, rest of dashes and their repetitions seems to be valid

# evaluate maximum dns names resolution (lenght)

## My first step is to normalize the data
#def normalize_email(emailAddress) :
#    """
#    Normalize the email address
#    """
#    return emailAddress.lower()
#
#def split_email_address_provider(emailAddress):
#    """
#    split the address and the provider 
#    """
#    return normalize_email(emailAddress).split("@")
#


# Investigacion:
# - MX record: Primera instancia, dig o nslookup
# - Servidores que soporten - SMTP VRFY 
# - HTTP Requests al API de login: https://github.com/amaurymartiny/check-if-email-exists/blob/5fad57d88ef92d65c7d493cdcb45eff347d6a286/core/src/smtp/yahoo.rs#L107
# - Regex : respeta las reglas de un email, el formato correcto
# - Para <username> y <domain>
# - https://help.returnpath.com/hc/en-us/articles/220560587-What-are-the-rules-for-email-address-syntax-#:~:text=The%20recipient%20name%20may%20be,Special%20characters%20such%20as%20!
# Interesting article:
# - https://www.sparkpost.com/blog/peeking-email-validation-techniques/
#   sending more than 37% of the world’s B2C and B2B email.
#https://stackoverflow.com/questions/386294/what-is-the-maximum-length-of-a-valid-email-address
#   |___http://www.dominicsayers.com/isemail/ <--- really nice, based on RFC
#        |____http://isemail.info/




#
## Known Providers
## send to db
#well_known_public_providers = ['hotmail','gmail','yahoo','']
#well_known_enterprise_providers = ['fibertel','telecentro','google','telefonica']
#america_top_level_domains = ['co','ar','cl','gt','pe']    
#
## specific provider:
#
#"""
#Estas reglas deberian ser validadas segun el dominio, es una etapa de filtro
#puede ser que existan usuarios viejos antes de la implementacion de estas reglas
#por lo tanto se deben marcar "flag" los correos que no cumplan con las mismas y no descartarlos como invalidos inmediatamente.
#"""
## Revisado 2021:
#
#
#
#
#def provider_regex_valid_names(provider):
#    
#    #________________________________________________________________________________ [GOOGLE/GMAIL]
#    if provider == 'google' :
#    # Gmail: (a-z) (0-9) (.)            can start with number           # No permite (..)
#
#        reValidChars = r'([a-zA-Z0-9.])'  # validate characters
#        reRepetition = r'([..]+)'         # validate invalid repetitions
#    if provider  == 'yahoo':
#    # Yahoo: (a-z) (0-9) (.) (_)        must start with letter          # No permite (__)
#
#
#
#    # Hotmail/Outlook: (a-z) (0-9) (.) (-) (_), must start with letter  # No permite (..) , permite (___)
#    # Proton: (a-z) (0-9) (-)           can start with number           # No permite (--) 
#
#
#
#def check_email_provider_rules(username, validChars, reRepetition) :
#    """
#    Verifies if an email is valid according the provider rules in email creation
#        """
#   
#        if re.search(reValidChars, username) :
#            logging.info('Not conflictive characters, now checking format')
#            if re.search(reRepetition): 
#                logging.error('Invalid characters repetition: .., not supported by provider ')
#            else:
#                logging.info('Everything seems ok')
#        else :
#            logging.error('Username has invalid characters for this email provider')
#
#
#
#
#
## Validacion MX
#"""
#Validar que la parte de dominio cuente con registros MX para la resolucion
#-- has mx record: add to table = domains with valid mx records <-- monitoring every 24hs
#"""
#
#
#
## Reglas basicas de un correo <breakdown>
#
#
#
##- Analizar longitud de nombre de usuario
##- Analizar validez de nombre de usuario
#invalid_characters = [':',';', ]
#
#
#valid_characters = [ '+.-_\','    ]
#

#- Analizar longitud de nombre de dominio
"""
:FIXME: Agregar revisiones mensuales sobre este topic en caso de nuevos desarrollos
The maximum number of characters you can have in a website address left of the "." is 63 characters. That's an awfully long URL and we don't recommend choosing such a lengthy domain in any circumstances.
"""
#if len(domainName) > 63 : 
#    print 'The {} is an invalid domain name.'.format(domainName)
#
##- Analizar validez de nombre de dominio
#
