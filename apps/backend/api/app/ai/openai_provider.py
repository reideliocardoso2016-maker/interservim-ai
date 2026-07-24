from openai import AsyncOpenAI
from app.ai.provider import AIProvider
from app.ai.prompts import SALES_AGENT_SYSTEM_PROMPT, INTENT_CLASSIFICATION_PROMPT, MARKETING_PROMPTS


class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def generate_response(
        self,
        system_prompt: str,
        messages: list,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                *messages,
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    async def classify_intent(self, message: str, context: str = "") -> dict:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": INTENT_CLASSIFICATION_PROMPT},
                {"role": "user", "content": f"Mensaje: {message}\n\nContexto: {context}"},
            ],
            temperature=0.1,
            max_tokens=50,
        )
        intent = response.choices[0].message.content.strip()
        return {"intent": intent}

    async def generate_marketing_content(self, params: dict) -> dict:
        content_type = params.get("content_type", "WHATSAPP_STATUS")
        prompt_template = MARKETING_PROMPTS.get(content_type, MARKETING_PROMPTS["WHATSAPP_STATUS"])
        product_info = params.get("product_description", "")
        tone = params.get("tone", "PROFESSIONAL")
        audience = params.get("audience", "general")
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"{prompt_template}\n\nTono: {tone}\nAudiencia: {audience}\n\nGenera título, texto, y llamada a la acción."},
                {"role": "user", "content": f"Producto: {product_info}"},
            ],
            temperature=0.8,
            max_tokens=500,
        )
        content = response.choices[0].message.content
        return {"content": content, "content_type": content_type}
