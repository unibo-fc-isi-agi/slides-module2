import asyncio
import os
from openai import AsyncOpenAI


base_url = os.environ.get("OPENAI_BASE_URL", "https://openrouter.ai/api/v1/")
api_key = os.environ.get("OPENAI_API_KEY") or input(f"Enter your API key for {base_url}: ")
model = os.environ.get("OPENAI_MODEL", "openrouter/auto")

client = AsyncOpenAI(base_url=base_url, api_key=api_key)
messages = [dict(role="system", content="Just chat with the user, be friendly and helpful. Do not think. Just answer.")]

print(f"Using model: {model}")


async def main() -> int:
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
                stream = await client.chat.completions.create(model=model, messages=messages, stream=True)
            except Exception as exc:
                print(f"\nerror> {exc}")
                continue
            answer_parts = []
            print("assistant> ", end="", flush=True)
            try:
                async for item in stream:
                    if not item.choices:
                        continue
                    chunk = item.choices[0].delta.content or ""
                    if not chunk:
                        continue
                    chunk = chunk.replace("\n", "\nassistant> ")
                    print(chunk, end="", flush=True)
                    answer_parts.append(chunk)
            except Exception as exc:
                print(f"\nerror> {exc}", flush=True)
                continue
            print(flush=True)
            answer = "".join(answer_parts)
            messages.append(dict(role="assistant", content=answer))
    except (EOFError, KeyboardInterrupt):
        pass
    print("Goodbye!")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
