import os
from google import genai
from google.genai import types

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
# It is recommended to set your API key as an environment variable:
#   export GEMINI_API_KEY="your_api_key_here"
# Alternatively, uncomment and replace the line below:
# os.environ["GEMINI_API_KEY"] = "your_api_key_here"

MODEL_ID = "gemini-3.6-flash"   # You can change to gemini-2.0-flash, etc.


def generate_with_temperature(prompt: str, temperature: float) -> str:
    """
    Sends a prompt to Gemini with a specific temperature setting
    and returns the generated text response.
    """
    # The client automatically uses the GEMINI_API_KEY environment variable
    client = genai.Client(
    http_options=types.HttpOptions(timeout=15_000)  # 15 seconds, in milliseconds
)

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
        ),
    )

    # Cleanly close the client to release HTTP resources
    client.close()

    return response.text


def main():
    # ----- Your prompt -----
    prompt = "Explain the concept of temperature in large language models in 3 sentences."

    # ----- Run at temperature 0 (deterministic) -----
    print("=" * 60)
    print("TEMPERATURE = 0  (most deterministic)")
    print("=" * 60)
    try:
        result_0 = generate_with_temperature(prompt, temperature=0.0)
        print(result_0)
    except Exception as e:
        print(f"Error at temperature 0: {e}")

    # ----- Run at temperature 1 (more creative / random) -----
    print("\n" + "=" * 60)
    print("TEMPERATURE = 1  (more diverse output)")
    print("=" * 60)
    try:
        result_1 = generate_with_temperature(prompt, temperature=1.0)
        print(result_1)
    except Exception as e:
        print(f"Error at temperature 1: {e}")


if __name__ == "__main__":
    main()