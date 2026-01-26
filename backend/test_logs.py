# backend/test_logs.py

from logger_config import logger

def test_logging():
    try:
        logger.info("Mensaje de INFO de prueba")
        logger.warning("Mensaje de WARNING de prueba")
        logger.error("Mensaje de ERROR de prueba")
        print("Logging ejecutado correctamente. Revisa backend/logs/app.log")
    except Exception as e:
        print(f"Error inesperado al probar logging: {e}")

if __name__ == "__main__":
    test_logging()
