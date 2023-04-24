import openai
class ChatBot:
    def __init__(self, user_name) -> None:
        self.user = user_name
        self.message = [
            {"role": "user", "content": "Hello!"}
        ]

    async def ask(self, query: str) -> str:
        self.message.append({"role": "user", "content": query})
        rsp = openai.ChatCompletion.create(
            max_tokens = 200,
            user = self.user,
            model="gpt-3.5-turbo",
            messages=self.message
        )
        result = rsp.get("choices")[0]["message"]["content"]
        self.message.append({"role" : "assistant", "content" : result})
        return await result