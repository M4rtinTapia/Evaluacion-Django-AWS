from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Producto

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('username', '').strip()
        clave = request.POST.get('password', '')

        # PROGRAMACIÓN SEGURA: authenticate() usa consultas parametrizadas internamente contra SQLi
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

# CORREGIDO: Se renombró a 'listar' para hacer match con urls.py y {% url 'listar' %}
def listar(request):
    productos = Producto.objects.all()
    return render(request, 'lista.html', {'productos': productos})

# CORREGIDO: Se renombró a 'crear' para hacer match con urls.py y {% url 'crear' %}
def crear(request):
    if request.method == "POST":
        # Sanitización en el origen: eliminamos espacios maliciosos en los extremos
        nombre = request.POST.get('nombre', '').strip()
        
        # Validación estricta de tipos para evitar inyección de texto en campos numéricos
        try:
            precio = float(request.POST.get('precio', 0))
            stock = int(request.POST.get('stock', 0))
        except (ValueError, TypeError):
            return render(request, 'form.html', {'error': 'Datos numéricos inválidos.'})

        # Control de datos vacíos o incoherentes
        if not nombre or precio < 0 or stock < 0:
            return render(request, 'form.html', {'error': 'Por favor, rellena los campos con datos válidos.'})

        # Inserción segura en la base de datos de Oracle Cloud mediante el ORM
        Producto.objects.create(nombre=nombre, precio=precio, stock=stock)
        return redirect('listar')
        
    return render(request, 'form.html')

# CORREGIDO: Se renombró a 'eliminar' para hacer match con urls.py y {% url 'eliminar' %}
def eliminar(request, id):
    # El convertidor <int:id> de la URL ya bloquea ataques de texto directo aquí
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    return redirect('listar')

def editar(request, id):
    # 1. Rescatamos el producto por su ID desde Oracle Cloud OCI
    try:
        producto = Producto.objects.get(id=id)
    except Producto.DoesNotExist:
        return redirect('listar')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio_raw = request.POST.get('precio')
        stock_raw = request.POST.get('stock')

        # 2. Validación y sanitización estricta de tipos
        try:
            precio = int(precio_raw)
            stock = int(stock_raw)
            
            if precio < 0 or stock < 0:
                raise ValueError

            # 3. Guardado seguro parametrizado mediante el ORM
            producto.nombre = nombre
            producto.precio = precio
            producto.stock = stock
            producto.save()
            return redirect('listar')

        except (ValueError, TypeError):
            # Si meten letras con F12, recargamos el formulario con la alerta visual
            return render(request, 'form.html', {
                'error': 'Datos numéricos inválidos en la edición.',
                'producto': producto
            })

    # Si entran por primera vez (GET), cargamos el formulario con los datos actuales
    return render(request, 'form.html', {'producto': producto})