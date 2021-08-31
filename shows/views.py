from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from shows.models import Shows,Channels, Users
from django.http import HttpResponseRedirect
import bcrypt
from .decorators import login_required



@login_required
def index(request):
    if 'counter' not in request.session:
        request.session['counter'] = 0
    
    return redirect('/shows')

@login_required
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
@login_required
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

@login_required
def shows (request):
    shows = Shows.objects.all()
    networks = Channels.objects.all()
    
    context = {
        'shows' : shows,
        'networks' : networks

    }

    return render(request,'shows.html', context)
@login_required
def showinfo(request,id):
    print(id)

    show = Shows.objects.get(id=id)
    
    context = {
        'show' : show,
        
    }

    return render(request,'show_info.html',context)

@login_required
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

@login_required
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

@login_required
def destroy(request,id):
    show = Shows.objects.get(id=id)
    print(show)
    show.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def register(request):
    #si llega un get, renderizamos la pagina del registro
    if request.method =='GET':
        return render(request,'register.html')
    else:
        #si llega un POST tomamos los valores del formulario
        #y creamos un nuevo usuario
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        #validar que el formulario este correcto

        errors = Users.objects.basic_validator(request.POST)
        if len(errors) > 0:
            #se es mayor a cero, hay al menos un error
            #entonces le mostramos los errores al usuario
            for llave,mensaje_de_error in errors.items():
                messages.error(request,mensaje_de_error)

            return redirect('/register')

    users = Users.objects.create(
        name = name,
        email = email,
        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    )

    request.session['user'] = {
        'id' : users.id,
        'name' : users.name,
        'email' : users.email,
        'avatar' : users.avatar,
    }
    messages.success(request,'Usuario creado con exito')
    return redirect('/shows')

def login(request):
    #si llega un get, renderizamos la pagina del registro
    if request.method =='GET':
        return render(request,'register.html')
    else:
        email = request.POST['email']
        password = request.POST['password']

    try:
        user = Users.objects.get(email=email)
    except Users.DoesNotExist:
        messages.error(request,'Usuario inexistente o contraseña incorrecta')
        return redirect('/register')

    #si llegamos aca, estamos seguro que el usuario existe 
    if not bcrypt.checkpw(password.encode(), user.password.encode()):
        messages.error(request,'Usuario inexistente o contraseña incorrecta')
        return redirect('/register')

    #si llegamos hasta aca, estamos seguros que el usuario existe y la contraseña es correcta
    request.session['user'] = {
        'id' : user.id,
        'name' : user.name,
        'email' : user.email,
        'avatar' : user.avatar
    }
    messages.success(request, f'Hola {user.name}')
    return redirect('/shows')

@login_required
def logout(request):
    del request.session['user']
    return redirect('/register')