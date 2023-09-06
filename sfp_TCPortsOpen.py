# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         sfp_TCPortsOpen
# Purpose:      SpiderFoot plug-in for creating new modules.
#
# Author:     MCarmen García Jiménez
# Based on the template:    Daniel García Baameiro <dagaba13@gmail.com>
#
# Created:     26/08/2022
# Copyright:   (c) MCarmen García Jiménez 2023
# Licence:     GPL
# -------------------------------------------------------------------------------

from spiderfoot import SpiderFootEvent, SpiderFootPlugin #Librerías propias de spiderfoot
import subprocess #Este módulo permite ejecutar órdenes en paralelo a la ejecución de nuestro código

class sfp_TCPortsOpen(SpiderFootPlugin):

    # Diccionario que tiene la información acerca del módulo
    meta = {
        'name': "TCPortsOpen_EIP",
        'summary': "Busca puertos TCP abiertos en una máquina, dada su IP",
        'flags': [""],
        'useCases': [""],
        'categories': ["Passive DNS"]
    }

    # Default options
    opts = {
    }

    # Option descriptions
    optdescs = {
    }

    results = None

    def setup(self, sfc, userOpts=dict()):
        self.sf = sfc
        self.results = self.tempStorage()

        for opt in list(userOpts.keys()):
            self.opts[opt] = userOpts[opt]
            
    # Datos de entrada que va a recibir el módulo
    # What events is this module interested in for input
    def watchedEvents(self):
        return ["IP_ADDRESS"]

    # Datos de salida del módulo
    # What events this module produces
    # This is to support the end user in selecting modules based on events
    # produced.
    def producedEvents(self):
        return ["TCP_PORT_OPEN"]

    # Handle events sent to this module
    def handleEvent(self, event):
        eventName = event.eventType
        srcModuleName = event.module
        eventData = event.data

        if eventData in self.results:
            return

        self.results[eventData] = True

        self.sf.debug(f"Received event, {eventName}, from {srcModuleName}")

        try:

            # Log
            self.sf.debug(f"We use the data: {eventData}")
            print(f"We use the data: {eventData}")

            ########################
            data = subprocess.run("nmap -n -Pn -sT -p- --min-rate 4000 "+eventData, text=True, shell=True, capture_output= True) # 'eventData' dato de entrada
            out = data.stdout
            outLines = out.split('\n') # Divide la salida en líneas
            
            encontrado = False
            allPorts = list()
            for linea in outLines: # Recorre todas las líneas
                if "PORT" in linea:
                    encontrado = True
                if encontrado:
                    trozosLinea = linea.split('/') # Divide por '/' si ha encontrado la cadena "PORT" en la salida
                    if len(trozosLinea) > 1:
                        allPorts.append(trozosLinea[0]) # Añade a una lista el puerto
            ########################
            
            # Si está vacío, puede que la máquina esté apagada o tenga los puertos cerrados 
            # if not data:
            if len(allPorts) == 0:
                # self.sf.error("Unable to perform <ACTION MODULE> on " + eventData)
                self.sf.info("The ports list is not available on  " + eventData)
                evt = SpiderFootEvent("TCP_PORT_OPEN", "The ports list is not available on " + eventData, self.__name__, event)
                self.notifyListeners(evt)
                return
                
        except Exception as e:
            self.sf.error("Unable to perform the <ACTION MODULE> on " + eventData + ": " + str(e))
            evt = SpiderFootEvent("TCP_PORT_OPEN", "Unable to perform the <ACTION MODULE> on  " + eventData, self.__name__, event)
            self.notifyListeners(evt)
            return

        # Devuelve el contenido para que lo lance la interfaz web
        for port in allPorts:
            evt = SpiderFootEvent("TCP_PORT_OPEN", port, self.__name__, event)
            self.notifyListeners(evt)

# End of sfp_TCPortsOpen class