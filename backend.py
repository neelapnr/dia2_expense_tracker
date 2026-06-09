import os
import json
import base64

from dotenv import load_dotenv
from groq import Groq


class ExpenseAgent:
    def __init__(self):
        load_dotenv()

        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        base_dir = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(base_dir, "context.txt"), encoding="utf-8") as f:
            self.system_prompt = f.read()

        with open(os.path.join(base_dir, "prompt.txt"), encoding="utf-8") as f:
            self.user_prompt = f.read()

        self.expected_fields = [
            "type_document",
            "fournisseur",
            "date",
            "montant_ttc",
            "tva",
            "devise",
            "description",
            "confiance"
        ]

    def extract_from_bytes(self, image_bytes, media_type):
        image_b64 = base64.b64encode(image_bytes).decode()

        completion = self.client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": self.system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": self.user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{media_type};base64,{image_b64}"
                            },
                        },
                    ],
                },
            ],
        )

        data = json.loads(completion.choices[0].message.content)

        for field in self.expected_fields:
            data.setdefault(field, None)

        return data


if __name__ == "__main__":
    agent = ExpenseAgent()

    with open("ticket.jpg", "rb") as f:
        image = f.read()

    result = agent.extract_from_bytes(image, "image/jpeg")

    print(json.dumps(result, indent=2, ensure_ascii=False))                
     
                   
