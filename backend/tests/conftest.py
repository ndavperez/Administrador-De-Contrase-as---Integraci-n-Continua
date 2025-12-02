"""Configuración de fixtures para tests"""
import sys
from pathlib import Path

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    """Fixture que proporciona un cliente de test sin conectar a BD real"""
    # Importar DESPUÉS de agregar al path
    from main import app
    
    return TestClient(app)
