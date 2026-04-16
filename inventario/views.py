from django.shortcuts import render, redirect

from .forms import ProductoForm

def crear_producto(request):
    form = ProductoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listar')
    return render(request, 'inventario/form.html', {'form': form})
