"""Day 1 — LLM API Foundation"""

import os
import time
from typing import Any, Callable


def using_openrouter() -> bool:
    return bool(os.getenv("OPENROUTER_API_KEY"))


OPENAI_MODEL = "openai/gpt-4o" if using_openrouter() else "gpt-4o"
OPENAI_MINI_MODEL = "openai/gpt-4o-mini" if using_openrouter() else "gpt-4o-mini"

COST_PER_1K_OUTPUT_TOKENS = {
    "gpt-4o": 0.010,
    "gpt-4o-mini": 0.0006,
    "openai/gpt-4o": 0.010,
    "openai/gpt-4o-mini": 0.0006,
}


def create_client():
    from openai import OpenAI

    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if openrouter_key:
        return OpenAI(
            api_key=openrouter_key,
            base_url="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "http://localhost",
                "X-Title": "Day01 Lab Assignment",
            },
        )

    return OpenAI(api_key=openai_key)


def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    client = create_client()

    start = time.perf_counter()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )

    end = time.perf_counter()
    latency = max(end - start, 1e-9)

    response_text = response.choices[0].message.content or ""

    return response_text, latency


def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    return call_openai(
        prompt=prompt,
        model=OPENAI_MINI_MODEL,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )


def compare_models(prompt: str) -> dict:
    gpt4o_response, gpt4o_latency = call_openai(prompt)
    mini_response, mini_latency = call_openai_mini(prompt)

    estimated_tokens = len(gpt4o_response.split()) / 0.75
    gpt4o_cost_estimate = (
        estimated_tokens / 1000
    ) * COST_PER_1K_OUTPUT_TOKENS.get(OPENAI_MODEL, 0.010)

    return {
        "gpt4o_response": gpt4o_response,
        "mini_response": mini_response,
        "gpt4o_latency": gpt4o_latency,
        "mini_latency": mini_latency,
        "gpt4o_cost_estimate": gpt4o_cost_estimate,
    }


def streaming_chatbot() -> None:
    client = create_client()
    history = []

    print("Streaming chatbot started. Type 'quit' or 'exit' to stop.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break

        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})

        messages = history[-6:]

        stream = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=0.7,
            top_p=0.9,
            max_tokens=256,
            stream=True,
        )

        assistant_reply = ""

        print("Assistant: ", end="", flush=True)

        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            print(delta, end="", flush=True)
            assistant_reply += delta

        print()

        history.append({"role": "assistant", "content": assistant_reply})
        history = history[-6:]


def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as error:
            last_error = error

            if attempt == max_retries:
                raise last_error

            delay = base_delay * (2 ** attempt)
            time.sleep(delay)

    raise last_error


def batch_compare(prompts: list[str]) -> list[dict]:
    results = []

    for prompt in prompts:
        result = compare_models(prompt)
        result["prompt"] = prompt
        results.append(result)

    return results


def format_comparison_table(results: list[dict]) -> str:
    def short(text: str, max_len: int = 40) -> str:
        text = str(text).replace("\n", " ")

        if len(text) <= max_len:
            return text

        return text[:max_len - 3] + "..."

    headers = [
        "Prompt",
        "GPT-4o Response",
        "Mini Response",
        "GPT-4o Latency",
        "Mini Latency",
    ]

    rows = []

    for item in results:
        rows.append([
            short(item.get("prompt", "")),
            short(item.get("gpt4o_response", "")),
            short(item.get("mini_response", "")),
            f"{item.get('gpt4o_latency', 0):.3f}s",
            f"{item.get('mini_latency', 0):.3f}s",
        ])

    all_rows = [headers] + rows

    widths = [
        max(len(str(row[i])) for row in all_rows)
        for i in range(len(headers))
    ]

    def make_row(row: list[str]) -> str:
        return " | ".join(
            str(row[i]).ljust(widths[i])
            for i in range(len(row))
        )

    table = []
    table.append(make_row(headers))
    table.append("-+-".join("-" * width for width in widths))

    for row in rows:
        table.append(make_row(row))

    return "\n".join(table)


if __name__ == "__main__":
    test_prompt = "Explain the difference between temperature and top_p in one sentence."

    print("=== Comparing models ===")
    result = compare_models(test_prompt)

    for key, value in result.items():
        print(f"{key}: {value}")

    print("\n=== Starting chatbot (type 'quit' to exit) ===")
    streaming_chatbot()
