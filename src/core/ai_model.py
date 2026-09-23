from huggingface_hub import InferenceClient
from src.setting import settings


class AIModel:
    def __init__(self):
        self.client = None
        self.model_name = "openai/gpt-oss-20b:groq"

    def load(self):
        try:
            hf_token = settings.HF_TOKEN

            if not hf_token:
                return
            self.client = InferenceClient(
                token=hf_token
            )
        except Exception as e:
            raise

    def generate(self, prompt: str, max_tokens: int = 150) -> str:
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
            return f"Error: {str(e)}"


ai_model = AIModel()
