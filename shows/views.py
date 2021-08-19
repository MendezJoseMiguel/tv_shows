from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from shows.models import Shows,Channels

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