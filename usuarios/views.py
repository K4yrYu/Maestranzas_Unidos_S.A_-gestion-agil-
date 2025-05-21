from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'usuarios/login.html')

@login_required
def logout_usuario(request):
    logout(request)
    return redirect('login_usuario')

def es_admin(user):
    return user.is_superuser or user.is_staff

@user_passes_test(es_admin)
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

@user_passes_test(es_admin)
def crear_usuario(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        is_active = 'activo' in request.POST
        rol = request.POST.get('rol', 'usuario')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ya existe un usuario con ese nombre.")
            return redirect('crear_usuario')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = is_active

        if rol == 'admin':
            user.is_superuser = True
            user.is_staff = True
        elif rol == 'operario':
            user.is_staff = True
            user.is_superuser = False
        else:
            user.is_staff = False
            user.is_superuser = False

        user.save()
        messages.success(request, "Usuario creado correctamente.")
        return redirect('lista_usuarios')

    return render(request, 'usuarios/formulario_usuario.html', {'modo': 'crear'})


@user_passes_test(es_admin)
def editar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)

    if request.method == "POST":
        usuario.username = request.POST['username']
        usuario.email = request.POST['email']
        usuario.is_active = 'activo' in request.POST
        rol = request.POST.get('rol', 'usuario')

        if request.POST['password']:
            usuario.set_password(request.POST['password'])

        if rol == 'admin':
            usuario.is_superuser = True
            usuario.is_staff = True
        elif rol == 'operario':
            usuario.is_staff = True
            usuario.is_superuser = False
        else:
            usuario.is_staff = False
            usuario.is_superuser = False

        usuario.save()
        messages.success(request, "Usuario actualizado correctamente.")
        return redirect('lista_usuarios')

    return render(request, 'usuarios/formulario_usuario.html', {'modo': 'editar', 'usuario': usuario})