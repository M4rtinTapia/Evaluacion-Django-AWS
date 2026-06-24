from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Producto

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('username', '').strip()
        clave = request.POST.get('password', '')
        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            login(request, user)
            return redirect('listar')
        else:
            messages.error(request, "Credenciales incorrectas.")
            return render(request, 'login.html')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def listar(request):
    productos = Producto.objects.all()
    return render(request, 'lista.html', {'productos': productos})

def crear(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre', '').strip()
        try:
            precio = float(request.POST.get('precio', 0))
            stock = int(request.POST.get('stock', 0))
        except (ValueError, TypeError):
            return render(request, 'form.html', {'error': 'Datos numéricos inválidos.'})
        
        imagen = request.FILES.get('imagen')

        if not nombre or precio < 0 or stock < 0:
            return render(request, 'form.html', {'error': 'Por favor, rellena los campos con datos válidos.'})

        Producto.objects.create(nombre=nombre, precio=precio, stock=stock, imagen=imagen)
        return redirect('listar')
    return render(request, 'form.html')

def eliminar(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    return redirect('listar')

def editar(request, id):
    try:
        producto = Producto.objects.get(id=id)
    except Producto.DoesNotExist:
        return redirect('listar')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio_raw = request.POST.get('precio')
        stock_raw = request.POST.get('stock')
        imagen_nueva = request.FILES.get('imagen') 

        try:
            precio = int(precio_raw)
            stock = int(stock_raw)
            if precio < 0 or stock < 0:
                raise ValueError
            
            producto.nombre = nombre
            producto.precio = precio
            producto.stock = stock
            if imagen_nueva:
                producto.imagen = imagen_nueva
            producto.save()
            return redirect('listar')
        except (ValueError, TypeError):
            return render(request, 'form.html', {'error': 'Datos numéricos inválidos en la edición.', 'producto': producto})
    return render(request, 'form.html', {'producto': producto})