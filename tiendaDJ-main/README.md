# Tienda DJ — Instrucciones rápidas

paso 1
Instalacion base:

dentro de la terminal o consola debes ingresar lo siguiente:

```powershell
pip install django pillow
# si hay problemas, prueba con:
python -m pip install django pillow
```

paso 2
configuracion de settings:

1) agregar app:

```py
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	# ⬇️ AGREGAR AQUÍ:
	'mainApp', 
]
```

2) import os (si no está ya en el archivo):

```py
import os
```

3) agregar media a settings:

```py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

4) agregar templates a settings (corregir nombre de la variable y la ruta):

```py
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [TEMPLATE_DIR],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]
```

5) agregar static:

```py
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

paso 3
hacer las migraciones y crear ADMIN:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

paso 4
correr programa

```powershell
python manage.py runserver
```

-direccion y contexto de los datos-

Gestión Inicial de Contenido (Administrador)
Accede al panel de administración: http://127.0.0.1:8000/admin/.

Carga Mínima: Utiliza el panel para crear y cargar:

- Varias Categorías.
- Al menos dos o tres Productos (incluyendo sus imágenes).

El flujo público se centra en tres acciones principales:

- Navegación por el Catálogo (Ruta: /)
- Muestra el listado de productos con opciones de búsqueda y filtrado.
- Solicitud de Pedido (Rutas: /solicitar/ o /solicitar/<id>/)
  - El cliente accede a /solicitar/ o hace clic en "Solicitar este producto" desde la vista de detalle.
  - Llena el Formulario de Pedido (PedidoForm).
  - Sube Imágenes: Utiliza el campo de archivos múltiples para subir las imágenes de referencia.

Confirmación y Token:
- Al enviar el formulario, el sistema:
  - Guarda los datos y las imágenes.
  - Genera un Token Único de Seguimiento.
  - Muestra el token y un enlace directo a la página de seguimiento.

Seguimiento del Pedido (Ruta: /seguimiento/<token>/)
- El cliente usa el token generado para acceder a esta URL.
- El sistema muestra el Estado Actual del pedido (e.g., Solicitado, En Proceso, Entregado), el estado de pago, y las imágenes subidas como referencia.

Tareas del Administrador:
El administrador gestiona el flujo de trabajo a través del panel de Django Admin
Recepción y Revisión:
- Revisa los nuevos pedidos entrantes.
Actualización:
- Actualiza el campo estado y estado_pago del modelo Pedido. Estos cambios se reflejan inmediatamente en la vista de seguimiento del cliente.

