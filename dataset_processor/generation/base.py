from abc import ABC, abstractmethod


class BaseRAGGenerator(ABC):
    """
    Abstract base class for RAG (Retrieval-Augmented Generation) systems.

    This class defines the blueprint for a system that can:
    1. Generate questions from a given context.
    2. Provide answers to questions based on the same context.
    """

    @abstractmethod
    def generate_questions(self, context: str, num_generations: int) -> dict:
        """
        Generate questions based on the provided context.

        Parameters:
        ----------
        context : str
            The text or information from which questions are to be generated.
            Typically a passage, article, or document.

        num_generations : int
            The number of questions to generate from the given context.

        Returns:
        -------
        dict
            A dictionary containing generated questions.
        """
        pass

    @abstractmethod
    def generate_answers(self, context: str, questions: list[str]) -> list:
        """
        Generate answers for a list of questions based on the provided context.

        Parameters:
        ----------
        context : str
            The text or information from which answers are to be derived.
            Typically a passage, article, or document.

        questions : list
            A list of questions for which answers are to be generated. Each
            question is a string.

        Returns:
        -------
        list
            A list of pairs (question, answer).
        """
        pass
