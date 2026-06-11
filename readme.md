Perfecto. Si buscas coste 0 €, agentes PM + Developer + QA trabajando entre ellos y que además puedas usar para tus proyectos Vue/Node, te recomiendo esta pila:

Windows / Linux
    │
    ▼
Ollama
    │
    ▼
Qwen3 14B
    │
    ▼
AutoGen
    │
    ▼
PM ↔ Developer ↔ QA

No necesitas GPU dedicada para empezar, aunque ayuda.

Paso 1. Instalar Ollama

Ve a:

Ollama

Instálalo normalmente.

Comprueba que funciona:

ollama --version
Paso 2. Descargar un modelo

Para desarrollo de software recomiendo:

Si tienes 16 GB RAM
ollama pull qwen3:8b
Si tienes 32 GB RAM o más
ollama pull qwen3:14b
Si tienes un equipo potente
ollama pull qwen3:32b

Mi recomendación inicial:

ollama pull qwen3:14b
Paso 3. Probar el modelo
ollama run qwen3:14b

Pregunta:

Escribe una API Express para gestionar productos.

Si responde correctamente, ya está funcionando.

Paso 4. Instalar Python

Descarga:

Python

Marca:

Add Python to PATH

durante la instalación.

Comprueba:

python --version
Paso 5. Crear entorno
mkdir ai-team
cd ai-team

python -m venv venv

Activar:

Windows:

venv\Scripts\activate

Linux/Mac:

source venv/bin/activate
Paso 6. Instalar AutoGen
pip install pyautogen

También:

pip install ollama
Paso 7. Verificar Ollama API

Abre:

http://localhost:11434

Deberías ver algo parecido a:

Ollama is running
Paso 8. Crear primer equipo

Crea:

team.py
from autogen import AssistantAgent

pm = AssistantAgent(
    name="PM",
    system_message="""
    Eres Project Manager.
    Divide el proyecto en tareas pequeñas.
    Revisa entregables.
    """
)

developer = AssistantAgent(
    name="Developer",
    system_message="""
    Eres desarrollador senior Node.js y Vue.
    Implementa exactamente lo pedido.
    """
)

qa = AssistantAgent(
    name="QA",
    system_message="""
    Eres QA.
    Busca errores y mejoras.
    """
)
Paso 9. Configurar Ollama

Añade:

llm_config = {
    "config_list": [
        {
            "model": "qwen3:14b",
            "base_url": "http://localhost:11434/v1",
            "api_key": "ollama"
        }
    ]
}
Paso 10. Conectar agentes
pm.llm_config = llm_config
developer.llm_config = llm_config
qa.llm_config = llm_config
Paso 11. Primera conversación
task = """
Crear una aplicación Vue para gestionar inventario.
"""

reply = pm.generate_reply(
    messages=[
        {"role": "user", "content": task}
    ]
)

print(reply)
Paso 12. Evolucionar a flujo real

Lo ideal es que cada iteración sea:

PM
 ↓
Developer
 ↓
QA
 ↓
PM

Hasta que:

estado = COMPLETADO
Paso 13. Dar acceso a archivos del proyecto

La verdadera potencia aparece cuando el Developer puede leer y modificar tu código.

Estructura:

mi-proyecto
│
├── src
├── backend
├── docs
└── agents

Los agentes:

leen archivos
modifican archivos
generan código
ejecutan tests
crean documentación
Paso 14. Añadir memoria de proyecto

Crea:

project.md

Ejemplo:

Objetivo:
Aplicación web de inventario.

Tecnologías:
- Vue 3
- Node.js
- Express
- SQLite

Estado:
- Login completado
- CRUD pendiente

El PM siempre lo lee antes de planificar.

Esto mejora muchísimo la coherencia.

Paso 15. Siguiente nivel (muy recomendable)

Cuando tengas esto funcionando, añade:

PM
Arquitecto
Developer
QA

y usa un modelo local para cada uno.

PM         -> planifica
Arquitecto -> diseña
Developer  -> programa
QA         -> prueba

Para proyectos como los que has comentado (Vue, Node, Express, Chart.js), esta configuración suele ser suficiente para que los agentes trabajen durante decenas de iteraciones sin coste de tokens. El siguiente paso, cuando tengas Ollama instalado y Qwen funcionando, sería montar un script completo donde el PM genere tareas automáticamente, el Developer escriba archivos reales en tu proyecto y el QA ejecute pruebas antes de devolver el control al PM. Esa versión ya se parece bastante a tener un pequeño equipo de desarrollo autónomo.


EJECUTAR:
.\venv\Scripts\python.exe main.py