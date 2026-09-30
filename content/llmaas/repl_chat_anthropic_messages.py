import os
from anthropic import Anthropic


base_url = os.environ.get("ANTHROPIC_BASE_URL", "http://localhost:11434")
api_key = os.environ.get("ANTHROPIC_API_KEY", "ollama")
model = os.environ.get("ANTHROPIC_MODEL", "gemma4:e2b")

client = Anthropic(base_url=base_url, api_key=api_key)
system = "Just chat with the user, be friendly and helpful. Do not think. Just answer."
messages = []

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
            response = client.messages.create(model=model, system=system, messages=messages, max_tokens=2048)
        except Exception as exc:
            print(f"error> {exc}")
            continue
        answer = "".join(block.text for block in response.content if block.type == "text")
        print(f"assistant> {answer}")
        messages.append(dict(role="assistant", content=answer))
except (EOFError, KeyboardInterrupt):
    pass
print("Goodbye!")
exit(0)
