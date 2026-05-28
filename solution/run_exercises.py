from solution import call_openai


prompt = "Hãy kể cho tôi một sự thật thú vị về Việt Nam."

temperatures = [0.0, 0.5, 1.0, 1.5]

for temperature in temperatures:
    print("=" * 70)
    print(f"Temperature: {temperature}")
    print("-" * 70)

    response, latency = call_openai(
        prompt=prompt,
        temperature=temperature,
        top_p=0.9,
        max_tokens=200,
    )

    print(response)
    print(f"\nLatency: {latency:.3f}s")
    print()