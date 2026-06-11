import asyncio
import subprocess

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination

from team import pm, architect, developer, qa
from executor import apply_dev_output


team = RoundRobinGroupChat(
    participants=[pm, architect, developer, qa],
    termination_condition=MaxMessageTermination(20)
)

task = "Crear función sum en JavaScript dentro de workspace y corregir bugs si existen"


def run_tests():
    """
    Ejecuta tests del proyecto.
    Ajusta este comando a tu stack real.
    """
    try:
        result = subprocess.run(
            "npm test",
            shell=True,
            capture_output=True,
            text=True
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e)
        }


async def main():

    iteration = 0
    max_iterations = 5

    while iteration < max_iterations:

        print(f"\n\n🔁 ITERATION {iteration + 1}\n")

        stream = team.run_stream(task=task)

        seen = set()
        last_dev_output = None

        async for message in stream:

            content = str(message)

            if content in seen:
                continue
            seen.add(content)

            print("\n🧠 MESSAGE:\n")
            print(content)

            # Capturar output del Developer
            if "Developer" in content and "FILE:" in content and "CODE:" in content:

                print("\n⚙️ APPLYING CODE...\n")
                last_dev_output = content
                apply_dev_output(content)

        # 🧪 EJECUTAR TESTS DESPUÉS DEL CICLO COMPLETO
        print("\n🧪 RUNNING TESTS...\n")
        test_result = run_tests()

        print("\n📊 TEST RESULT:\n")
        print(test_result)

        # 🧠 SI TODO OK → FIN
        if test_result["success"]:
            print("\n🎉 PROJECT COMPLETED SUCCESSFULLY")
            break

        # 🔥 SI FALLA → REPARACIÓN AUTOMÁTICA
        print("\n⚠️ TEST FAILED → REPAIRING...\n")

        task = f"""
El proyecto sigue fallando.

ERRORES:
{test_result["stderr"]}

OUTPUT:
{test_result["stdout"]}

Debes corregir el problema manteniendo el diseño del Architect.
"""

        iteration += 1

    print("\n🏁 FINAL STATE REACHED")


if __name__ == "__main__":
    asyncio.run(main())