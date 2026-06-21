from django.contrib import admin
from django.utils.html import format_html
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # Agregamos 'mostrar_imagen' a la lista de columnas
    list_display = ('nombre', 'precio', 'stock', 'mostrar_imagen')
    # Hacemos que la imagen sea de solo lectura para evitar errores al editar
    readonly_fields = ('mostrar_imagen',)

    def mostrar_imagen(self, obj):
        if obj.imagen:
            # Devuelve una etiqueta HTML con la imagen ajustada a 50px
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />', obj.imagen.url)
        return "Sin imagen"
    
    # Le cambiamos el nombre a la columna para que se vea más ordenado
    mostrar_imagen.short_description = 'Vista Previa'