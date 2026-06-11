import asyncio
import json

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination

from team import pm, architect, developer, qa
from executor import apply_dev_output


team = RoundRobinGroupChat(
    participants=[pm, architect, developer, qa],
    termination_condition=MaxMessageTermination(12)
)

task = "Crea una app que convierte imágenes JPG a ASCII"


def handle_output(raw: str):
    try:
        return json.loads(raw)
    except Exception:
        return None


async def main():

    stream = team.run_stream(task=task)

    seen = set()

    async for message in stream:

        raw = getattr(message, "content", None)

        if not raw:
            continue

        print("\n🧠 RAW CONTENT:\n", raw)

        # ✅ SOLO UN PARSER
        data = handle_output(raw)

        if not data:
            print("\n⚠️ SKIPPED NON-JSON MESSAGE")
            continue

        role = data.get("role")
        msg_type = data.get("type")

        print(f"\n📦 ROLE: {role} | TYPE: {msg_type}\n")

        # 🟢 APPLY SOLO DEVELOPER
        if role == "Developer" and "files" in data:

            print("\n⚙️ APPLYING FILE CHANGES...\n")

            result = apply_dev_output(json.dumps(data))

            for r in result:
                print(r)

        # 🟢 QA DECIDE FINAL STATE
        if role == "QA" and data.get("status") == "ok":
            print("\n🎉 PROJECT COMPLETED SUCCESSFULLY")
            return


if __name__ == "__main__":
    asyncio.run(main())