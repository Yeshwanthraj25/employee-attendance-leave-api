from huggingface_hub import InferenceClient
from src.setting import settings


class AIModel:
    def __init__(self):
        self.client = None
        self.model_name = "openai/gpt-oss-20b:groq"

    def load(self):
        """Initialize Hugging Face Inference Client"""
        print("Initializing AI Model (HF Inference)...")

        try:
            hf_token = settings.HF_TOKEN

            if not hf_token:
                print("⚠️ Warning: HF_TOKEN not set in .env")
                return

            print(f"Using token: {hf_token[:10]}...")

            self.client = InferenceClient(
                token=hf_token
            )

            print(f"✅ AI Model initialized: {self.model_name}")

        except Exception as e:
            print(f"❌ Error loading AI model: {e}")
            raise

    def generate(self, prompt: str, max_tokens: int = 150) -> str:
        """Generate text using Hugging Face Inference Providers"""

        try:
            if not self.client:
                return "Error: AI Model not initialized"

            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )

            return completion.choices[0].message.content.strip()

        except Exception as e:
            print(f"❌ Error generating response: {e}")
            return f"Error: {str(e)}"


ai_model = AIModel()
