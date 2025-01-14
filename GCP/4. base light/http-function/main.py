from flask import Request

def my_function(request: Request):
    try:
        # Parsing del JSON (se il payload è JSON)
        if request.is_json:
            data = request.get_json()
            print("Payload JSON ricevuto:", data)
            
            # Accesso ai dati del JSON
            if "name" in data:
                print(f"Nome trovato nel JSON: {data['name']}")
        
        # Parsing di dati form-urlencoded
        #elif request.form:
        #    print("Dati form-urlencoded ricevuti:", request.form)
        #    if "name" in request.form:
        #        print(f"Nome trovato nel form: {request.form['name']}")
        
        # Accesso ai parametri della query string
        #if request.args:
        #    print("Parametri della query string:", request.args)
        #    if "name" in request.args:
         #       print(f"Nome trovato nei parametri della query: {request.args['name']}")
        
        # Risposta HTTP
        return "Richiesta processata con successo", 200
    
    except Exception as e:
        print(f"Errore nel processing della richiesta: {e}")
        return "Errore nel processing della richiesta", 400
