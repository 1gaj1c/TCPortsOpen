# TCPortsOpen
'TCPortsOpen' es un módulo creado para la herramienta 'Spiderfoot' que realiza un ataque pasivo de tal forma que busca todos los puertos TCP abiertos en una máquina, dada su IP.

Spiderfoot es una herramienta muy usada para OSINT que automatiza la recopilación de información a través de diferentes recursos como fuentes públicas o herramientas privadas. Esta herramienta, que cuenta con licencia libre, está desarrollada en Python y sigue una estructura de clases. Su versión gratuita cuenta con más de 200 módulos categorizados según la información que extraen o el dato que solicitan.

Para este análisis de puertos utiliza la llamada 'nmap' con los siguientes parámetros:
		-n  => no realiza resolución de nombres (inversa) para ahorrar tiempo
		-Pn => no hace discovery host
		-sT => para saber si el puerto está abierto o cerrado - Técnica TCP Scan
		-p- => indica todos los puertos
		--min-rate => número de paquetes por segundo

Un ejemplo sería:
	~$nmap -n -Pn -sT -p- --min-rate 4000 192.168.1.100

La aplicación necesitará como dato de entrada tan solo una dirección IP y como salida listará todos los puertos TCP abiertos para esa IP.

En el caso en que la máquina no tenga puertos TCP abiertos o la máquina esté caída, se lanzará un evento que mostrará por salida el mensaje 'The ports list is not available on IP'.
