import requests


def get_quiz(kahoot_id: str) -> dict:
    """
    Faz request ao endpoint e retorna apenas questions + choices organizados.
    """
    print(kahoot_id)
    progress_url = f"https://kahoot.it/rest/challenges/{kahoot_id}/progress/?upToQuestion=100"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(progress_url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Erro na requisição: {response.status_code}")

    data = response.json()

    questions_data = []

    questions = data.get("questions", [])

    for q in questions:
        questions_data.append({
            "index": q.get("index"),
            "title": q.get("title"),
            "choices": [
                {
                    "text": c.get("answer"),
                    "correct": c.get("correct")
                }
                for c in q.get("choices", [])
            ]
        })

    return {
        "kahootId": data.get("kahootId"),
        "title": data.get("kahootTitle"),
        "questions": questions_data
    }

data = get_quiz("07533d80-c426-4d3d-80a8-3ae49e557d12_1779474250522")

for i, q in enumerate(data["questions"], start=1):
    correct = next(c["text"] for c in q["choices"] if c["correct"])

    print(f"{i}. {q['title']}")
    print(f"   ✔ {correct}")

print("TOTAL DE PERGUNTAS:", len(data["questions"]))
print(data)