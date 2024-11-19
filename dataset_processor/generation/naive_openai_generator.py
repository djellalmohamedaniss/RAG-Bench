import json
import os

from openai import OpenAI

from generation import BaseRAGGenerator


class RAGGeneratorOpenAI(BaseRAGGenerator):
    """
    Implementation of RAG system using OpenAI API.
    """

    def __init__(self) -> None:
        super().__init__()
        self.client = self._initialize_client()

    def _initialize_client(self):
        """
        Initialize the OpenAI client.
        """
        self.api_key = os.environ.get("OPENAI_API_KEY")
        return OpenAI(api_key=self.api_key)

    def generate_questions(self, context: str, num_generations: int) -> dict:
        """
        Generate a list of questions in JSON format using OpenAI's API.
        """
        prompt_template = """
        Here is some context:
        <context>
        {}
        </context>

        Your task is to generate {} questions in FRENCH that can be answered using the provided context and return a JSON object of a list of questions, following these rules:

        <rules>
        1. The question should make sense to humans even when read without the given context.
        2. The question should be fully answered from the given context.
        3. The question should be framed from a part of context that contains important information. It can also be from tables, code, etc.
        4. The answer to the question should not contain any links.
        5. The question should be of moderate difficulty.
        6. The question must be reasonable and must be understood and responded by humans.
        7. Avoid phrases like 'provided context' in the question.
        8. Avoid framing questions using the word "and" that can be decomposed into more than one question.
        9. Questions should not exceed 10 words.
        </rules>
        """
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt_template.format(context, num_generations),
                }
            ],
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)

    def generate_answers(self, context: str, questions: list) -> list:
        """
        Generate answers to the provided questions using OpenAI's API.
        """
        answers = []
        generation_template = """
        It is your task to generate an answer to the following questions <questions>{}</questions> only based on the <context>{}</context></task>
        The output should be only the answer generated from the context.
        <rules>
        1. Only use the given context as a source for generating the answer.
        2. Be as precise as possible with answering the question.
        3. Be concise in answering the question and only answer the question at hand rather than adding extra information.
        </rules>
        """
        for question in questions:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": generation_template.format(context, question),
                    }
                ],
                model="gpt-4o-mini",
            )
            answers.append(
                {
                    "question": question,
                    "answer": response.choices[0].message.content.strip(),
                }
            )
        return answers
