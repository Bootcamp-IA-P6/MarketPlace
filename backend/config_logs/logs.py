import os

# 1. Definir rutas dinámicas
# Esto busca la carpeta padre de 'config_logs', que sería 'backend'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Definimos dónde queremos guardar los archivos físicos
LOG_FILE_DIR = os.path.join(BASE_DIR, 'logs')

# 2. Creamos la carpeta 'logs' automáticamente si no existe
# (Así te evitas crearla manualmente y evitas errores si borras la carpeta)
if not os.path.exists(LOG_FILE_DIR):
    os.makedirs(LOG_FILE_DIR)

# 3. El Diccionario de Configuración (La "Receta")
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            # Aquí usamos la ruta que calculamos arriba + el nombre del archivo
            'filename': os.path.join(LOG_FILE_DIR, 'sistema.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        # Configuración para TUS aplicaciones
        '': { 
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}