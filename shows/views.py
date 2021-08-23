from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from shows.models import Shows,Channels
from django.http import HttpResponseRedirect


    
def index(request):
    if 'counter' not in request.session:
        request.session['counter'] = 0
    
    return redirect('/shows')


def newshow(request):

    #si llega un GET cargamos el formulario add_shows.html
    if request.method == 'GET':
        shows = Shows.objects.all()
        networks = Channels.objects.all()
        context = {
            'shows' : shows,
            'networks' : networks

        }
        
        return render(request,'add_shows.html',context)

def create_newshow(request):
    # pasar los datos al método que escribimos y guardar la respuesta en una variable llamada errores
    errors = Shows.objects.basic_validator(request.POST)
        # compruebe si el diccionario de errores tiene algo en él
    if len(errors) > 0:
        # si el diccionario de errores contiene algo, recorra cada par clave-valor y cree un mensaje flash
        for key, value in errors.items():
            messages.error(request, value)
        # redirigir al usuario al formulario para corregir los errores
        return redirect('shows/new')
    else:
        # si el objeto de errores está vacío, eso significa que no hubo errores.
        # recuperar el blog para actualizarlo, realizar los cambios y guardar
        
        
        if request.POST['network_id'] == 'other':
            #se crea el nuevo network
            new_network_name = request.POST['new_network']
            network = Channels.objects.create(name = new_network_name)
        else:
            #se toma el network de la lista
            network_id = request.POST['network_id']
            network = Channels.objects.get(id=network_id)

            title = request.POST['title']
            release_date = request.POST['release_date']
            desc = request.POST['desc']
            new_show = Shows.objects.create(title = title, network = network,release_date= release_date,desc = desc)
            print(new_show)
        #messages.success(request, f'El Show {title} ha sido agregado')
        #messages.error(request, 'Ups, ha ocurrido un error')
        #messages.warning(request, f'Su mascota se llama {pet}')
        
        return redirect('/shows')


def shows (request):
    shows = Shows.objects.all()
    networks = Channels.objects.all()
    
    context = {
        'shows' : shows,
        'networks' : networks

    }

    return render(request,'shows.html', context)

def showinfo(request,id):
    print(id)

    show = Shows.objects.get(id=id)
    
    context = {
        'show' : show,
        
    }

    return render(request,'show_info.html',context)

def edit(request,id):
    # Si el metodo es GET, carga el formulario
    if request.method == 'GET':
        show = Shows.objects.get(id=id)
        networks = Channels.objects.all()
        release_date = show.release_date.strftime("%Y-%m-%d")
    
        context = {
            'show' : show,
            'networks' : networks,
            'release_date' : release_date

        }
        return render(request,'edit.html',context)

def update(request,id):
    # pasar los datos al método que escribimos y guardar la respuesta en una variable llamada errores
    errors = Shows.objects.basic_validator(request.POST)
        # compruebe si el diccionario de errores tiene algo en él
    if len(errors) > 0:
        # si el diccionario de errores contiene algo, recorra cada par clave-valor y cree un mensaje flash
        for key, value in errors.items():
            messages.error(request, value)
        # redirigir al usuario al formulario para corregir los errores
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        # si el objeto de errores está vacío, eso significa que no hubo errores.
        # recuperar el blog para actualizarlo, realizar los cambios y guardar
        #si el formulario se envia entonces
        #Si creamos una nueva network hacemos se edita con la nueva netwok
        if request.POST['network_id'] == 'other':
        #se crea el nuevo network
            new_network_name = request.POST['new_network']
            network = Channels.objects.create(name = new_network_name)

            show = Shows.objects.get(id=id)
            print(show.id)
            show.title = request.POST['title']
            show.network = network
            show.desc = request.POST['desc']
            show.release_date = request.POST['release_date']
            #guardamos los cambios
            show.save()
            messages.success(request, "El Show se ha editado Correctamente")
        else:
        #si toma el network de la lista
            network_id = request.POST['network_id']
            network = Channels.objects.get(id=network_id)

            show = Shows.objects.get(id=id)
            print(show.id)
            show.title = request.POST['title']
            show.network_id = request.POST['network_id']
            show.desc = request.POST['desc']
            show.release_date = request.POST['release_date']
            #guardamos los cambios
            show.save()
            messages.success(request, "El Show se ha editado Correctamente")
        # redirigir a la ruta de exito
        return redirect('/shows')

def destroy(request,id):
    show = Shows.objects.get(id=id)
    print(show)
    show.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))