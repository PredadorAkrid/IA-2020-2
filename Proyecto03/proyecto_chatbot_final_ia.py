#!/usr/bin/python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------
#  chatbot.py
#
#  Proyecto 3: Implementación de un chatbot para un restaurante
#  Inteligencia Artificial 2020-2
#  Elaborado por el equipo La Orden de Turing
#  Integrantes:
#       Amaya López Dulce Fernanda
#       López Arias Víctor Ulises
#       Navarrete Puebla Alexis
#       Rosado Cabrera Diego
#       Sainz Takata Izumi María
#----------------------------------------------------------------------

import string
import re
import random

class chatbot:
    def __init__(self):
        '''
        El chatbot consta de una base de conocimiento representada como una lista de casos o intents
        '''
        self.nombre_usuario = ""
        self.platillo = ""
        self.ingrediente = ""
        self.categoria = ""
        self.tipo_de_pago = ""
        self.conocimiento = [] # la base de conocimiento, representan los diferentes casos o intents
        for caso in conocimiento:
            caso['regex'] = list(map(lambda x:re.compile(x, re.IGNORECASE), caso['regex'])) # compilar las expresiones regulares es óptimo cuando se usan varias veces
            self.conocimiento.append(caso)

    def responder(self, user_input):
        '''
        Flujo básico para identificar coincidencias de intents para responder 
        al usuario. Con el texto del usuario como parámetro, los paso a 
        realizarse son:
            1. Encontrar el caso de la base de conocimiento usando expresiones 
               regulares
            2. Si es necesario, realizar acciones asociadas al intent (por 
               ejemplo: consultar información adicional)
            3. Seleccionar una respuesta de la lista de respuestas según el caso
               del intent
            4. Si es necesario, identificar los parámetros o entidades del texto
               para dar formato a la respuesta seleccionada
            5. Devolver la respuesta
        :param str user_input: El texto escrito por el usuario
        :return Un texto de respuesta al usuario
        :rtype: str
        '''
        caso = self.encontrar_intent(user_input)
        if not caso:
            return 'No puedo responder a eso'
        respuesta = self.convertir_respuesta(random.choice(caso['respuesta']), caso, user_input)
        informacion_adicional = self.acciones(caso)
        
        respuesta_final = (respuesta  + informacion_adicional).strip() # Strip quita espacios en blanco al inicio y final del texto
        return respuesta_final

    def encontrar_intent(self, user_input):
        '''
        Encuentra el caso o intent asociado en la base de conocimiento

        :param str user_input: El texto escrito por el usuario
        :return El diccionario que representa el caso o intent deseado
        :rtype: str
        '''
        for caso in self.conocimiento:
            for regularexp in caso['regex']:
                match = regularexp.match(user_input)
                if match:
                    self.regexp_selected = regularexp # Asignar esta propiedad es útil para acceder rápidamente a la expresión regular del match
                    return caso
        return {}

    def convertir_respuesta(self, respuesta, caso, user_input):
        '''
        Cambia los textos del tipo %1, %2, %3, etc., por su correspondiente 
        propiedad identificada en los grupos parentizados de la expresión 
        regular asociada.

        :param str respuesta: Una respuesta que desea convertirse
        :param dict caso: El caso o intent asociado a la respuesta
        :param str user_input: El texto escrito por el usuario
        :return La respuesta con el cambio de parámetros
        :rtype: str
        '''
        respuesta_cambiada = respuesta
        intent = caso['intent']
        match = self.regexp_selected.match(user_input)
        
        if intent == 'nombre':
            self.nombre_usuario = ""
            respuesta_cambiada = respuesta_cambiada.replace('%1', match.group(1))
            self.nombre_usuario = match.group(1)
        elif intent == 'categoria filtrada menú':
            cat = match.group(1)
            if(not cat.endswith("s")):
              cat = cat + "s"
              respuesta_cambiada = respuesta_cambiada.replace('%1', cat)
              self.categoria = cat
            else:
              respuesta_cambiada = respuesta_cambiada.replace('%1', match.group(1))
              self.categoria = match.group(1)
        elif intent == 'información platillo':
            respuesta_cambiada = respuesta_cambiada.replace('%5', match.group(5))
            self.platillo = match.group(5)
        elif intent == 'precio platillo':
            if(self.valida_platillo(match.group(4))):
                self.platillo = match.group(4)
                respuesta_cambiada = respuesta_cambiada.replace('%4', match.group(4))
            else:
                self.platillo = ""
                respuesta_cambiada = "No existe ese platillo en nuestro menú :("
        elif intent == 'chiste':
            respuesta_cambiada = respuesta_cambiada.replace('%1', self.nombre_usuario)
        elif intent == 'dar recomendación bebida':
            respuesta_cambiada = respuesta_cambiada.replace('%3', match.group(3))
            self.platillo = match.group(3)
        elif intent == 'acciones chatbot':
            respuesta_cambiada = respuesta_cambiada.replace('%1', self.nombre_usuario)
        elif intent == 'no busqueda categoria':
            respuesta_cambiada = respuesta_cambiada.replace('%1', self.nombre_usuario)
        elif intent == 'tipos de pago':
            self.tipo_de_pago = ""
            respuesta_cambiada = respuesta_cambiada.replace('%2', self.nombre_usuario)
            metodo_pago = match.group(1).lower()
            if "sí," in metodo_pago or "si," in metodo_pago:
                metodo_pago = metodo_pago.replace("sí,", "")
                metodo_pago = metodo_pago.replace("si,", "") 
                metodo_pago = metodo_pago.strip()
                self.tipo_de_pago = metodo_pago
                respuesta_cambiada = respuesta_cambiada.replace('%1', metodo_pago)

            else:
                self.tipo_de_pago = metodo_pago.strip()
                respuesta_cambiada = respuesta_cambiada.replace('%1', metodo_pago)

                

        return respuesta_cambiada

    def acciones(self, caso):
        '''
        Obtiene información adicional necesaria para dar una respuesta coherente al usuario.
        El tipo de acciones puede ser una consulta de información, revisar base de datos, generar
        un código, etc. y el resultado final es expresado como una cadena de texto

        :param dict caso: El caso o intent asociado a la respuesta
        :return Texto que representa información adicional para complementar la respuesta al usuario
        :rtype: str
        '''
        intent = caso['intent']
        if intent == 'categoria filtrada menú':
            return self.get_categoria(self.categoria)
        elif intent == 'información platillo':
            return self.get_ingredientes_platillo(self.platillo)
        elif intent == 'precio platillo':
            return self.get_costo_platillo(self.platillo)
        elif intent == 'dar recomendación bebida':
            return self.get_bebida_platillo(self.platillo)
        elif intent == 'no busqueda categoria':
            return self.get_menu()
        elif intent == 'tipos de pago':
            return self.get_estado_tipo_pago(self.tipo_de_pago)  
        return ''

    def get_menu(self):
        '''
        Devuelve el menú del día, i.e. el nombre de los platillos del menú.
        Representa un ejemplo de consulta de información o acciones en el flujo
        para construir una respuesta del chatbot
        :return Texto de los platillos en el menú
        :rtype str
        '''
        lista_platillos = []
        for platillo in menu:
            lista_platillos.append(platillo['nombre'].title())
        respuesta = ' , \n'.join(lista_platillos)
        if not respuesta:
            return 'Por el momento no tenemos platillos disponibles'
        return respuesta

    def get_categoria(self, categ):
        '''
        Devuelve el menú del día, i.e. el nombre de los platillos del menú.
        Representa un ejemplo de consulta de información o acciones en el flujo
        para construir una respuesta del chatbot
        :return Texto de los platillos en el menú
        :rtype str
        '''
        lista_platillos = []
        for platillo in menu:
          if(platillo['categoria'].lower() == categ.lower()):
            lista_platillos.append(platillo['nombre'].title() + ",")
        respuesta = '\n'.join(lista_platillos)
        if not respuesta:
            return 'Por el momento no tenemos disponibles platillos para esa categoría'
        return respuesta

    def get_ingredientes_platillo(self, plat):
        '''
        Devuelve los ingredientes del platillo.
        :param str plat: el platillo del cual se quieren sus ingredientes
        :return cadena con los ingredientes del platillo
        :rtype str
        '''
        lista_platillos = []
        respuesta = ""
        for elem in menu:
            if(elem['nombre'].title().lower() == plat.lower()):
                lista_platillos.append(elem['ingredientes'])
                for i in lista_platillos:
                    respuesta += '\n'.join(i)
                            
        if not respuesta:
            return 'No dispongo de esa información en éste momento'
        return respuesta

  
    def get_costo_platillo(self, plat):
        '''
        Devuelve el costo del platillo.
        :param str plat: platillo del que se quiere el costo
        :return cadena con el costo del platillo
        :rtype str
        '''
        lista_platillos = []
        for elem in menu:
            if(elem['nombre'].lower() == plat.lower()):
                lista_platillos.append(elem['precio'])
                break;

        respuesta = ""
        if(len(lista_platillos) == 0):
            pass
        else:
          respuesta = str(lista_platillos[0]) + " mxn"
        if not respuesta:
            return ""
        return respuesta

    def get_bebida_platillo(self, plat):
        '''
        Devuelve la bebida recomendada para el platillo.
        :param str plat: el platillo del cual se quiere su bebida recomendada
        :return cadena con la bebida recomendada del platillo
        :rtype str
        '''
        bebida = ""
        for elem in menu:
            if(elem['nombre'].lower() == plat.lower()):
                bebida = elem['bebida']     
        
        if not bebida:
            rand = random.choice(menu)
            return rand['bebida'] + " aunque ese platillo no está dentro de nuestro menú :("
        return bebida
    def get_estado_tipo_pago(self, pago):
        if(pago == "debito" or pago == "débito" ):
          pago = "tarjeta de débito"
        elif(pago == "credito" or pago == "crédito"):
          pago = "tarjeta de crédito"
        for elem in tipo_pagos:
            if(elem[0].lower() == pago.lower() and elem[1] == True):
                 return "sí se encuentra disponible, pregunta en sucursal por promociones."
            else:
                 continue
        return "no se encuentra disponible, intenta más tarde mientras busco una solución :)"
        
    def valida_platillo(self, platillo_buscado):
        '''
        Valida si el platillo que recibe se encuentra en el menú
        :param str platillo_buscado: el platillo
        :return true si el platillo se encuentra en el menú, false si no
        :rtype bool
        '''
        for elem in menu:
            if(elem['nombre'].title().lower() == platillo_buscado.lower()):
                return True
            else:
                pass
        return False
        
        

#----------------------------------------------------------------------
# Basse de conocimiento
# La base de conocimiento representa una lista de todos los casos o intents
# que el chatbot será capaz de identificar.
#
# Cada caso o intent es un diccionario que incluye los siguientes keys 
# (propiedades):
# - intent: Nombre para identificar el intent
# - regex: Lista de posibles expresiones regulares asociadas al intent, 
#          donde los parámetros se obtienen del texto parentizado en la 
#          expresión regular
# - respuesta: Lista de posibles respuestas al usuario, indicando los parámetros
#              obtenidos con la notación %1, %2, %3, etc. para cada parámetro.
#----------------------------------------------------------------------
conocimiento = [
    
    # El intent nombre nos ayuda a obtener el nombre del usuario y guardarlo en 
    # una bandera, con lo cual, podemos dar respuestas más particulares incluyendo
    # en las mismas el nombre del usuario para que éste se sienta más cómodo
    # hablando con el chatbot.
    {
        'intent': 'nombre',
        'regex': [
            r'Me llamo (.*)',
            r'Hola, me llamo (.*)',
            r'hola, me llamo (.*)',
            r'me llamo (.*)',
            r'mi nombre es (.*)',
            r'Mi nombre es (.*)',
            r'Soy (.*)',
        ],
        'respuesta': [
            'Hola %1, actualmente te puedo ayudar con: \n' + 
            '   Dar menú \n'+
            '   Ingredientes de tu platillo \n'+
            '   Costo de tu platillo \n' +
            '   Recomendarte una bebida \n' +
            '   Otras acciones \n',
            '%1 un gusto, ¿en qué te puedo servir? Dispongo de lo siguiente: \n' + 
            '   Dar menú \n'+
            '   Ingredientes de tu platillo \n'+
            '   Costo de tu platillo \n' +
            '   Recomendarte una bebida \n'+
            '   Otras acciones \n',
            '%1, ¿qué se te antoja hoy? \nPuedo ayudarte con: \n' +  
            '   Dar menú \n'+
            '   Ingredientes de tu platillo \n'+
            '   Costo de tu platillo \n' +
            '   Recomendarte una bebida \n' +
            '   Otras acciones \n', 
        ]
    },
    # El intent información platillo está pensado para responder por preguntas
    # o requerimientos hechas por el usuario respecto a consulta de  ingredientes.
    
    {
        'intent': 'información platillo',
        'regex': [
            r'(.*)(Cuáles|Qué|que|Cuáles son los|qué|cuales|cuáles son los|Cuales|cuáles|Que) ingredientes (llevan|lleva|en|contienen|contiene|tienen|hay en|hay|tiene|de) (las|la|los|en la|en los|en las|de las|de la) (.*)\?',
            r'(.*)(Cuáles|Qué|que|Cuáles son los|qué|cuales|cuáles son los|Cuales|cuáles|Que) (llevan|lleva|en|contienen|contiene|tienen|hay en|hay|tiene|de) (las|la|los|en la|en los|en las|de las|de la) (.*)\?',
            r'(.*)(I|i)ngredientes (lleva|en|de|contienen|contiene|lleva|tienen|hay en|hay|tiene) (las|los|la|en los|en las|de) (.*)',
            r'¿?(.*)(C|c)ontenido (de|en) (las|la) (.*)\?',
            r'(.*)(C|c)ontenido (de|en) (las|la) (.*)',

        ],
        'respuesta': [
            'Los ingredientes de (la|los) %5 son: ',
            'L(a|os) %5 contiene(n): ',
        ]
    },
    # El intent precio de platillo está pensado para indicarle al usuario el precio
    # del platillo del menú que desea consultar. 
    {
        'intent': 'precio platillo',
        'regex': [
            r'¿?(Qué|qué|Que|que|Cuál|cuál|Cual|cual) es el (precio|costo) de(l platillo| el platillo| laCosto de | las| los) (.*)\?',
            r'¿?(Qué|qué|Que|que|Cuál|cuál|Cual|cual) es el (precio|costo) de(l platillo| el platillo| la| las| los) (.*)',
            r'¿?(Qué|qué|Que|que) costo tiene(n)? (el platillo|los|las|la) (.*)\?',
            r'¿?(Qué|qué|Que|que) costo tiene(n)? (el platillo|los|las|la) (.*)',
            r'¿?(Qué|qué|Que|que) precio tiene(n)? (el platillo|los|las|la) (.*)\?',
            r'¿?(Qué|qué|Que|que) precio tiene(n)? (el platillo|los|las|la) (.*)',
            r'¿?((C|c)osto) de (el|las|los|la) (.*)\?',
            r'¿?((C|c)osto) de (el|las|los|la) (.*)',
            r'¿?((P|p)recio) de (el|las|los|la) (.*)\?',
            r'¿?((P|p)recio) de (el|las|los|la) (.*)',
        ],
        'respuesta': [
            'El costo  de %4 es: ',
            '%4 tiene(n) un costo de: ',
            'Actualmente l@s %4 tienen un costo de: '

        ]
    },
    # Información de pago está pensada para que le informe al usuario del estado
    # de disponibilidad de su tipo de pago favorito para ello espera recibir una
    # respuesta válida dentro de la lista de métodos pago, i.e, débito, crédito ó
    # efectivo.

    {
        'intent': 'información de pago',
        'regex': [
            r'¿?(Q|q)ué metodos de pago aceptan\?',
            r'(.*)pago(.*)',
            r'(.*)metodos de pago(.*)',
        ],
        'respuesta': [
            '¿Qué tipo de pago buscas? Efectivo, débito o crédito',
            '¿Qué tipo de pago buscas? Efectivo, tarjeta de débito o tarjeta de crédito',
            'Indícame tu tipo de pago para consultarlo (efectivo, débido o crédito)',
            'Indícame tu tipo de pago para consultarlo (efectivo, tarjeta de débido o tarjeta de crédito)',
        ]
    },
    # El intent tipos de pago devuelve el estado actual del método de pago indicado
    # por el usuario.
    {
        'intent': 'tipos de pago',
        'regex': [
            r'(Efectivo|Sí, efectivo|Si, efectivo|sí, efectivo|si, efectivo|efectivo)',
            r'(Tarjeta de crédito|Sí, cr.dito|Si, cr.dito|sí, cr.dito|si, cr.dito|Sí, tarjeta de cr.dito|tarjeta de cr.dito|cr.dito|credito)',
            r'(Tarjeta de débito|Sí, d.bito|Si, d.bito|sí, d.bito|si, d.bito|Sí, tarjeta de débito|tarjeta de débito|débito|debito)',
        ],
        'respuesta': [
            'Estimad@ %2, actualmente el método de pago %1 ',
            'Estimad@ %2, el método de pago %1 '

        ]
    },

    # Acciones chatbot  nos permite informar al usuario todo el alcance del chatbot
    # para que pueda ejecutar cualquiera de éstas acciones por medio el chat.
    {
        'intent': 'acciones chatbot',
        'regex': [
            r'¿?(e|E)n (qué|que) (.*) ayudar\?',
            r'¿?(e|E)n (qué|que) (.*) ayudar',
            r'¿?(Q|q)u(é|e) (más)? puedes hacer\?',
            r'¿?(Q|q)u(é|e) (más)? puedes hacer',
            r'(O|o)tras acciones(.*)',
            r'(.*) puedes hacer(.*)',
            r'(.*)acciones(.*)',
            r'¿?(.*)(P|p)ara qu(é|e) sirves(.*)\?',
            r'¿?(.*)(P|p)ara qu(é|e) sirves(.*)',
            

        ],
        'respuesta': [
            'Hola %1, actualmente te puedo ayudar con: \n' + 
            '   Dar menú \n'+
            '   Ingredientes de tu platillo \n'+
            '   Costo de tu platillo \n' +
            '   Recomendarte una bebida para tu platillo \n' +       
            'Además puedo ayudarte con cualquiera de las siguientes acciones: \n'+
            '   Consultar los tipos de pago \n'+
            '   Contar un chiste \n' +
            '   Hacer tu tarea \n',
        ] 
    },

    # El intent quién eres está pensado solo para indicar que es una IA desarrollada
    # por La Orden De Turing
    {
        'intent': 'quién eres',
        'regex': [
            r'¿?(.*)(Q|q)ui(e|é)n eres\?',
            r'¿?(.*)(Q|q)ui(e|é)n eres',
           

        ],
        'respuesta': [
            'Soy una inteligencia artificial desarrollada por la Orden de Turing y estoy para ayudarte :)',
        ] 
    },

    # El intent dar menú está pensado para filtrar por tipo platillos para el usuario
    # , para ello pregunta si le gusta alguna categoría en especial, de no ser el caso
    # le indica todo el menu, está preparado para recibir el sustantivo en plurar
    # o en singular según sea el caso.
    {
        'intent': 'dar menú',
        'regex': [
            r'¿?(Qué|qué|que|Que|Cuáles|cuáles|cuales) .*platillos (hay|tienen|venden)*.*',
            r'¿?(Qué|qué|que|Que|Cuáles|cuáles|cuales) .*platillos (hay|tienen|venden)*.*\?',
            r'(.*)(Menú|menú|menu|Menu)(.*)',
            r'(.*)platillo me recomiendas(.*)',
            
        ],
        'respuesta': [
            '¿Te gustaría alguna categoría en especial hoy?' +
            ' Tenemos lo siguiente:\n' + 'Pizzas|Enchiladas|Ensaladas|Hamburguesas|Sopas|Pastas|Chilaquiles',
            '¿Buscas alguna categoría? \n' + 'Tenemos las siguiente:\n  Pizzas|Enchiladas|Ensaladas|Hamburguesas|Sopas|Pastas|Chilaquiles',
            '¿Se te antoja un tipo de comida en especial hoy? Disponemos de: \n' + 'Tenemos lo siguiente: Pizzas|Enchiladas|Ensaladas|Hamburguesas|Sopas|Pastas|Chilaquiles',
        ]
    },
    # El intent categoría filtrado es el que recibe por parte del usuario cualquiera
    # de los platillos del menú, en otro caso no es capaz de entender la petición.
    {
        'intent': 'categoria filtrada menú',
        'regex': [
            r'(Pizzas?|pizzas?|Enchiladas?|enchiladas?|Ensaladas?|ensaladas?|Hamburguesas?|hamburguesas?|Sopas?|sopas?|Pastas?|pastas?|Chilaquiles|chilaquiles)(.*)',
            r'S.,(Pizzas|pizzas|Enchiladas?|enchiladas?|Ensaladas?|ensaladas?|Hamburguesas?|hamburguesas?|Sopas?|sopas?|Pastas?|pastas?|Chilaquiles|chilaquiles)(.*)',
            r's.,(Pizzas?|pizzas?|Enchiladas?|enchiladas?|Ensaladas?|ensaladas?|Hamburguesas?|hamburguesas?|Sopas?|sopas?|Pastas?|pastas?|Chilaquiles|chilaquiles)(.*)',
            r'S.,\s(Pizzas|pizzas|Enchiladas?|enchiladas?|Ensaladas?|ensaladas?|Hamburguesas?|hamburguesas?|Sopas?|sopas?|Pastas?|pastas?|Chilaquiles|chilaquiles)(.*)',
            r's.,\s(Pizzas?|pizzas?|Enchiladas?|enchiladas?|Ensaladas?|ensaladas?|Hamburguesas?|hamburguesas?|Sopas?|sopas?|Pastas?|pastas?|Chilaquiles|chilaquiles)(.*)',
           
        ],
        'respuesta': [
            '¿Te gusta(n) la(s) %1? Tenemos ést(a|o) disponible para ti: ',
            'Con que %1 eh, sabia elección tenemos ést(a|o)s en nuestro menú: ',
        ]
    },
    
    # El intent recomendación bebida está preparado para tomar el platillo del usuario
    # y darle una recomendación de bebida, para ello el restaurante asocia una 
    # bebida particular para cada platillo basándose en cuál es la más solicitada
    # para dicho platillo, si el usuario no introduce un platillo del menú el chatbot
    # le indicará una bebida aleatoria de todo el menú con el fin de hacer más "natural"
    # o humanizar la respuesta
   
    {
        'intent': 'dar recomendación bebida',
        'regex': [
            r'¿?(.*) bebida me recomiendas con (mis|el|mi) platillo (.*)\?',
            r'(.*) bebida me recomiendas con (mis|el|mi) platillo (.*)',
            r'¿?(.*) bebida me recomiendas con (mis|la|el|las|los|mi) (.*)\?',
            r'¿?(.*) bebida me recomiendas con (mis|la|el|las|los|mi) (.*)\?',
            r'¿?(Q|q)ué puedo beber con (mis|la|el|las|los|mi) (.*)\?',
            r'(Q|q)ué puedo beber con (mis|la|el|las|los|mi) (.*)',
            r'¿?(Qué|Que|que|qué) me recomiendas para beber con (mis|la|el|las|los|mi) (.*)\?',
            r'(Qué|Que|que|qué) me recomiendas para beber con (mis|la|el|las|los|mi) (.*)',
            r'¿?(Qué|Que|que|qué) me recomiendas de beber con (mis|la|el|las|los|mi) (.*)\?',
            r'(Qué|Que|que|qué) me recomiendas de beber con (mis|la|el|las|los|mi) (.*)',
            r'¿?(qué|Qué|que|qué) es lo más solicitado para beber (para mi|para|con los|con mis|con la|con) (.*)\?',
            r'(qué|Qué|que|qué) es lo más solicitado para beber (para mi|para|con los|con mis|con la|con) (.*)',
            r'¿?(qué|Qué|que|qué) es lo más solicitado de beber (para mi|para|con los|con mis|con la|con) (.*)\?',
            r'(qué|Qué|que|qué) es lo más solicitado de beber (para mi|para|con los|con mis|con la|con) (.*)',
            r'¿?(.*) bebida más solicitada (para mi|para|con los|con mis|con la|con) (.*)\?',
            r'(.*) bebida más solicitada (para mi|para|con los|con mis|con la|con) (.*)',
            r'¿?(qué|Qué|que|qué) es lo más solicitado de beber (para mi|para|con los||con mis|con la|con) (.*)\?',
            r'(qué|Qué|que|qué) es lo más solicitado de beber (para|con los||con mis|con la|con) (.*)',
            r'¿?(.*) me recomiendas (para mi|para|con los|mis|con mis|con la|con) (.*)\?',
            r'(.*) me recomiendas (para mi|para|con los|con mi|con mis|con la|con) (.*)',
           
        ],
        'respuesta': [
            'Con que %3, te recomiendo lo siguiente para saciar tu sed de hoy: ',
            'Interesante, a mi también me gusta(n) (l@s) %3 ¿qué te parece lo siguiente para ti? ',
            'Me gusta (el|la) %3,  te sugiero lo siguiente: ',
            '(La|los) %3 (es|son) bastante solicitad(a|os), para ello te recomiendo: ',

        ]
    },
    # El intent chiste solo cubre el caso de que un usuario pida un chiste a un chatbot
    # o asistente virtual, es muy común.
    {
        'intent': 'chiste',
        'regex': [
            r'(.*)(c|C)histe(.*)',
            r'.*(D|d)ime un chiste',
            r'.*(C|c)uéntame un chiste',
            r'¿(M|m)e cuentas chiste?',
        ],
        'respuesta': [
            'No creí que hablaras en serio %1',
            '%1 estoy empezando mi negocio de reparto de alcohol \n' + 
            'lo llamaré Ubeer',
            'Hardware: Lo que puedes partir con un hacha \n' + 
            'Software: Aquello que sólo puedes maldecir \n' + 
            'Chatbot: Aquello que nunca te va a entender \n',
            '- ¿Hace cuánto que espera? \n' +  
            'Y responde la pera: \n' + 
            '- Desde que nací. \n' + 
            '¿Qué esperabas? Si fuera comediante no estaría aquí :(', 
            'Me gustan mi relación como me gusta mi código, abierto',
            


        ]
    },
    # El intent ayuda tarea no va más allá de lo que hace chiste.
    {
        'intent': 'ayuda tarea',
        'regex': [
            r'(.*)(tarea|Tarea)(.*)',
        ],
        'respuesta': [
            'Es broma, no puedo ayudarte con eso :(',
            'Lo siento, era broma, no puedo ayudarte con eso ¿pero qué te parece \n' +
            'algo de nuestro menú ;)?',
            'Está bien son 1000 pesos'

        ]
    },
    # El intent no busqueda categoría es la negación del intent ver menu donde el 
    # el usuario indica que no se le antoja ninguna categoría en especial y por ende
    # se le enseña todo el menú disponible.
    {
        'intent': 'no busqueda categoria',
        'regex': [
            r'(.*)(N|n)o(.*)',
        ],
        'respuesta': [
            'Okay %1, te mostraré todo nuestro menú: \n',
        ]
    },
    # El intent desconocido es si el chatbot recibe una respuesta por parte del usuario
    # para la que no está preparado.
    {
        'intent': 'desconocido',
        'regex': [
            r'.*'
        ],
        'respuesta': [
            'No te entendí ¿Puedes repetirlo con otras palabras por favor? ',
            'Disculpa, no comprendí lo que dices ¿puedes repetirlo?',
            'Me parece que no nos estamos entendiendo ¿podrías repetir eso último de diferente forma?',
        ]
    }
]

#----------------------------------------------------------------------
# Diccionario que representa el menú
# Ejemplo de información que podría consultarse de manera externa,
# ser generada, o auxiliar en la redacción de una respuesta del chatbot.
#----------------------------------------------------------------------
menu = [
    {
        'nombre': 'Pizza Hawaiana',
        'ingredientes': ['jamón', 'piña'],
        'precio': 100,
        'categoria': 'Pizzas',
        'bebida': 'Limonada'
    },
    {
        'nombre': 'Pizza De Pepperoni',
        'ingredientes': ['pepperoni', 'queso extra'],
        'precio': 120,
        'categoria': 'Pizzas',
        'bebida': 'Naranjada'
    },
    {
        'nombre': 'Pizza Mexicana',
        'ingredientes': ['chile', 'chorizo', 'frijoles'],
        'precio': 125,
        'categoria': 'Pizzas',
        'bebida': 'Coca cola'
    },
    {
        'nombre': 'Enchiladas suizas',
        'ingredientes': ['tortilla maíz', 'salsa verde', 'queso manchego', 'crema', 'pollo'],
        'precio': 70,
        'categoria': 'Enchiladas',
        'bebida': 'Manzanita'
    },
    {
        'nombre': 'Enchiladas verdes',
        'ingredientes': ['tortilla maíz', 'salsa verde', 'crema', 'pollo', 'cebolla'],
        'precio': 60,
        'categoria': 'Enchiladas',
        'bebida': 'Agua de jamaica'
    },
    {
        'nombre': 'Enchiladas rojas',
        'ingredientes': ['tortilla maíz', 'salsa roja', 'crema', 'pollo', 'cebolla'],
        'precio': 60,
        'categoria': 'Enchiladas',
        'bebida': 'Agua de tamarindo'
    },
    {
        'nombre': 'Ensalada campestre',
        'ingredientes': ['pollo empanizado', 'lechuga', 'queso panela', 'jitomate', 'manzana'],
        'precio': 100,
        'categoria': 'Ensaladas',
        'bebida': 'Naranjada'
    },
    {
        'nombre': 'Ensalada caribeña',
        'ingredientes': ['pollo a la parilla', 'lechuga', 'durazno', 'fresa'],
        'precio': 90,
        'categoria': 'Ensaladas',
        'bebida': 'Té helado'
    },
    {
        'nombre': 'Ensalada griega',
        'ingredientes': ['lechuga', 'queso de cabra', 'aceitunas negras', 'pepino', 'jitomate'],
        'precio': 110,
        'categoria': 'Ensaladas',
        'bebida': 'Agua de limón y pepino'
    },
    {
        'nombre': 'Ensalada paraíso',
        'ingredientes': ['mango', 'manzana', 'espinaca', 'nuez'],
        'precio': 80,
        'categoria': 'Ensaladas',
        'bebida': 'Té helado'
    },
    {
        'nombre': 'Hamburguesa con queso',
        'ingredientes': ['carne de res', 'queso americano', 'jitomate', 'lechuga', 'pepinillos'],
        'precio': 80,
        'categoria': 'Hamburguesas',
        'bebida': 'Manzanita'
    },
    {
        'nombre': 'Hamburguesa hawaiana',
        'ingredientes': ['carne de res', 'queso americano', 'jamón', 'piña', 'jitomate', 'lechuga', 'pepinillos'],
        'precio': 90,
        'categoria': 'Hamburguesas',
        'bebida': 'Coca cola'
    },
    {
        'nombre': 'Hamburguesa BBQ',
        'ingredientes': ['carne de res', 'queso americano', 'tocino', 'jitomate', 'lechuga', 'salsa BBQ'],
        'precio': 120,
        'categoria': 'Hamburguesas',
        'bebida': '7up'
    },
    {
        'nombre': 'Hamburguesa vegetariana',
        'ingredientes': ['carne de quinoa', 'queso cheddar', 'jitomate', 'lechuga', 'champiñones'],
        'precio': 100,
        'categoria': 'Hamburguesas',
        'bebida': 'Coca cola'
    },
    {
        'nombre': 'Sopa de verduras',
        'ingredientes': ['caldo de pollo', 'zanahoria', 'calabaza', 'brocolí', 'papa', 'chayote'],
        'precio': 40,
        'categoria': 'Sopas',
        'bebida': 'Agua de jamaica'
    },
    {
        'nombre': 'Sopa de tortilla',
        'ingredientes': ['tortilla de maíz', 'queso oaxaca', 'aguacate', 'chile pasilla'],
        'precio': 60,
        'categoria': 'Sopas',
        'bebida': 'Limonada'
    },
    {
        'nombre': 'Chilaquiles verdes',
        'ingredientes': ['tortilla de maíz', 'salsa verde', 'pollo', 'crema', 'queso panela'],
        'precio': 60,
        'categoria': 'Chilaquiles',
        'bebida': 'Naranjada'
    },
    {
        'nombre': 'Chilaquiles rojos',
        'ingredientes': ['tortilla de maíz', 'salsa roja', 'pollo', 'crema', 'queso panela'],
        'precio': 60,
        'categoria': 'Chilaquiles',
        'bebida': 'Agua de tamarindo'
    },
    {
        'nombre': 'Chilaquiles suizos',
        'ingredientes': ['tortilla de maíz', 'salsa verde', 'pollo', 'crema', 'queso manchego', 'cebolla'],
        'precio': 70,
        'categoria': 'Chilaquiles',
        'bebida': 'Coca cola'
    },
    {
        'nombre': 'Chilaquiles yucatecos',
        'ingredientes': ['tortilla de maíz', 'salsa pibil', 'pollo', 'crema', 'frijoles refritos', 'aguacate'],
        'precio': 80,
        'categoria': 'Chilaquiles',
        'bebida': 'Sprite'
    },
    {
        'nombre': 'Pasta alfredo',
        'ingredientes': ['fettuccini', 'salsa de queso', 'queso parmesano', 'jamón', 'champiñones'],
        'precio': 90,
        'categoria': 'Pastas',
        'bebida': 'Naranjada'
    },
    {
        'nombre': 'Pasta arrabiata',
        'ingredientes': ['spaguetti', 'salsa de jitomate', 'mantequilla', 'chile de árbol', 'queso parmesano', 'jamón'],
        'precio': 100,
        'categoria': 'Pastas',
        'bebida': 'Agua de sandía y limón'
    },
    {
        'nombre': 'Pasta carbonara',
        'ingredientes': ['fusilli', 'salsa de queso', 'tocino', 'queso parmesano'],
        'precio': 90,
        'categoria': 'Pastas',
        'bebida': 'Limonada'
    },
    {
        'nombre': 'Pasta bolognesa',
        'ingredientes': ['spaguetti', 'salsa de jitomate', 'carne de res', 'queso parmesano'],
        'precio': 100,
        'categoria': 'Pastas',
        'bebida': 'Agua de naranja'
    }
]
#----------------------------------------------------------------------
# Lista que representa los medios de pago y su estado 
#----------------------------------------------------------------------

tipo_pagos = [("efectivo", True),("tarjeta de débito", False),("tarjeta de crédito", True)]


#----------------------------------------------------------------------
#  Interfaz de texto
#----------------------------------------------------------------------
def command_interface():
    print('Delivery&Eats\n---------')
    print('='*72)
    print('¡Bienvenido! ¿cuál es tu nombre? \n Mi nombre es ________')


    input_usuario = ''
    asistente = chatbot();
    while input_usuario != 'salir':
        try:
            input_usuario = input('> ')
        except EOFError:
            print('Ocurrio un problema, abortando :(')
        else:            
            print(asistente.responder(input_usuario))

if __name__ == "__main__":
    command_interface()