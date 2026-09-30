import os
from openai import OpenAI


base_url = os.environ.get("OPENAI_BASE_URL", "https://openrouter.ai/api/v1/")
api_key = os.environ.get("OPENAI_API_KEY") or input(f"Enter your API key for {base_url}: ")
model = os.environ.get("OPENAI_MODEL", "openrouter/auto")

client = OpenAI(base_url=base_url, api_key=api_key)
messages = [dict(role="system", content="Just chat with the user, be friendly and helpful. Do not think. Just answer.")]

print(f"Using model: {model}")
print("Type '/exit' or '/quit' to stop. Type '/retry' to retry the last message.")

try:
    while True:
        user_text = input("you> ").strip()
        if not user_text:
            continue
        if (cmd := user_text.lower().strip()) in {"/exit", "/quit"}:
            break
        if cmd not in {"/retry"}:
            messages.append(dict(role="user", content=user_text))
        try:
            response = client.chat.completions.create(model=model, messages=messages)
        except Exception as exc:
            print(f"error> {exc}")
            continue
        answer = response.choices[0].message.content or ""
        print(f"assistant> {answer}")
        messages.append(dict(role="assistant", content=answer))
except (EOFError, KeyboardInterrupt):
    pass
print("Goodbye!")
exit(0)