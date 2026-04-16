from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto

def listar_productos(request):
    productos = Producto.objects.all()
    # Fíjate que aquí usamos 'lista.html' porque así se llama tu archivo en templates
    return render(request, 'lista.html', {'productos': productos})

def crear_producto(request):
    if request.method == "POST":
        Producto.objects.create(
            nombre=request.POST['nombre'],
            precio=request.POST['precio'],
            stock=request.POST['stock']
        )
        return redirect('listar')
    return render(request, 'form.html')

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    return redirect('listar')
