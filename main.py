import asyncio
import json
import re

from team import pm, architect, developer, qa
from executor import apply_dev_output

STATE_FILE = "project_state.json"

# =========================
# LOAD STATE
# =========================
def load_state():
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

# =========================
# PARSER ROBUSTO (REAL)
# =========================
def parse_json(text: str):
    try:
        # elimina code fences si existen
        text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE).strip()

        matches = re.findall(r"\{[\s\S]*?\}", text)
        if not matches:
            return None

        for candidate in sorted(matches, key=len, reverse=True):
            try:
                return json.loads(candidate)
            except Exception:
                continue

        return None

    except Exception:
        return None


# =========================
# ASK WRAPPER
# =========================
async def ask(agent, prompt: str):

    result = await agent.run(task=prompt)

    raw = result.messages[-1].content

    print("\n🧠 RAW:\n", raw)

    data = parse_json(raw)

    if not data:
        print("\n⚠️ INVALID JSON\n")
        return None

    print(f"\n📦 {data.get('role')} | {data.get('type')}")
    return data


# =========================
# MAIN LOOP
# =========================
async def main():

    state = load_state()

    for i in range(state["number_of_iterations"]):

        print("\n" + "=" * 60)
        print(f"🔁 ITERATION {i+1}")
        print("=" * 60)

        task = state["task"]

        # =========================
        # PM
        # =========================
        pm_result = await pm.run(
            task=f"""
        Objetivo: {state['task']}

        Historial:
        {json.dumps(state['history'][-3:], indent=2)}

        Problemas detectados:
        {state.get('last_error')}
        """
        )
        pm_content = pm_result.messages[-1].content

        pm_data = {
            "role": "PM",
            "type": "design",
            "content": pm_content
        }

        if not pm_data:
            print("⚠️ PM FAILED → regenerating task")
            pm_data = {
                "role": "Project Manager",
                "type": "design",
                "content": task
            }

        # =========================
        # ARCHITECT
        # =========================
        architect_data = await ask(
            architect,
            f"""
        Tarea:
        {pm_data['content']}

        IMPORTANTE:
        Devuelve diseño estructurado con:
        - archivos afectados
        - funciones
        - dependencias
        - cambios concretos
        """
        )

        if not architect_data:
            continue

        # =========================
        # DEVELOPER
        # =========================
        developer_data = await ask(
            developer,
            f"""
                Tarea:
                {pm_data['content']}

                Diseño:
                {architect_data['content']}

                Estado:
                {json.dumps(state)}
                """
        )

        if not developer_data:
            continue

        # =========================
        # APPLY FILES
        # =========================
        if isinstance(developer_data.get("files"), list):

            print("\n⚙️ APPLYING FILES...\n")

            result = apply_dev_output(json.dumps(developer_data))

            for r in result:
                print(r)

        # =========================
        # QA
        # =========================
        qa_data = await ask(
            qa,
            f"""
            Tarea:
            {task}

            Resultado:
            {json.dumps(developer_data)}
            """
        )

        # =========================
        # UPDATE STATE
        # =========================

        state["last_error"] = None

        if qa_data and qa_data.get("status") != "ok":
            state["last_error"] = qa_data.get("content")


        state["history"].append({
            "pm": pm_data,
            "architect": architect_data,
            "developer": developer_data,
            "qa": qa_data
        })

        if qa_data and qa_data.get("status") == "ok":
            state["status"] = "done"
            save_state(state)
            print("\n🎉 PROJECT COMPLETED")
            return

        save_state(state)
        print("💾 STATE SAVED → continuing")


if __name__ == "__main__":
    asyncio.run(main())