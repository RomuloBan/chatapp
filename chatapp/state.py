import reflex as rx
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

class State(rx.State):
    # The current question being asked.
    question: str = ""

    # Keep track of the questions and answers.
    chat_history: list[tuple[str, str]] = []

    def answer(self):
        # Our chatbot has some brains now!
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": self.question},
            ],
            stream=True,
        )
        # Our chatbot is not very smart right now.
        answer = ""
        self.chat_history.append((self.question, answer))

        # Clear the question input.
        self.question = ""
        
        # Yield here to clear the frontend input before continuing.
        yield

        for item in stream:
            if item.choices[0].delta.content is not None:
                answer += item.choices[0].delta.content

                self.chat_history[-1] = (
                    self.chat_history[-1][0],
                    answer,
                )
                yield

