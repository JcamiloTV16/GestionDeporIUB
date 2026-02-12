import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append("c:/GestionDeporIUB")

try:
    print("Testing Imports...")
    from app.controllers.user_controller import user_controller
    print("✅ Configured Imports work (app.controllers.user_controller).")
except ImportError as e:
    print(f"❌ Import Error: {e}")

try:
    print("Testing Models...")
    from app.models.all_models import Horario, Inscripcion
    from datetime import datetime, time
    
    h = Horario(deporte_id=1, entrenador_id=1, dia_semana="Lunes", hora_inicio=time(8,0), hora_fin=time(10,0))
    print(f"✅ Horario Model instantiated: {h}")
    
    i = Inscripcion(usuario_id=1, horario_id=1)
    print(f"✅ Inscripcion Model instantiated: {i}")

except Exception as e:
    print(f"❌ Model Error: {e}")

print("\n(Permission logic requires a running DB connection to fully test, avoiding strict DB dependency here to prevent test crash if DB is unreachable)")
