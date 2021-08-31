from django.shortcuts import redirect

#este es un ejemplo de decorador que modifica la funcion cubos hasta, tomando la funcion y los argumentos cubos hasta
def list_html(func):
    def wrapper(argumentos):
        lista = func(argumentos)
        texto = ''
        for item in lista:
            texto += '<li>' + str(item) + '</li>\n'
        return texto
    return wrapper

@list_html
def cubos_hasta(num):
    cubos = [i**3 for i in range(1, num+1)]
    return cubos


def login_required(func):
    
    def wrapper(request, *args, **kwargs):
        if 'user' not in request.session:
            return redirect('/register')
        resp = func(request, *args, **kwargs)
        return resp
    
    return wrapper