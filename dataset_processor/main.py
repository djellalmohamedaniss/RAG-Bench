import argparse
import importlib
import random
from os import listdir
from os.path import isfile, join
from typing import Type

from dotenv import load_dotenv
from splitter import BaseSplitter
from tqdm import tqdm

from datasets import Dataset
from generation import BaseRAGGenerator


def load_class(module_name: str, class_name: str, base_class: Type) -> Type:
    """Load and validate a class from a module."""
    try:
        module = importlib.import_module(module_name)
        loaded_class = getattr(module, class_name)
        if not issubclass(loaded_class, base_class):
            raise TypeError(f"{class_name} must inherit from {base_class.__name__}")
        return loaded_class
    except ModuleNotFoundError as e:
        raise ImportError(f"Module {module_name} not found.") from e
    except AttributeError as e:
        raise ImportError(f"Class {class_name} not found in {module_name}.") from e


def process_file(
    file_path: str,
    splitter: BaseSplitter,
    generator: BaseRAGGenerator,
    num_generations: int,
    split_sample: int,
):
    """Process a single file and generate Q&A dataset."""
    content = splitter.read(file_path)
    elements = splitter.split(content)
    if split_sample != -1:
        elements = random.sample(elements, split_sample)

    qa_dataset = []
    for element in tqdm(elements, desc=f"Processing {file_path}"):
        questions = generator.generate_questions(element, num_generations)
        answers = generator.generate_answers(element, questions["questions"])
        qa_dataset.extend(answers)
    return qa_dataset


def main(
    splitter_class_name: str,
    generator_class_name: str,
    num_generations: int,
    data_path: str,
    split_sample: int,
):
    """Main function to orchestrate the pipeline."""
    load_dotenv("../.env")

    try:
        SplitterClass = load_class("splitter", splitter_class_name, BaseSplitter)
        GeneratorClass = load_class(
            "generation", generator_class_name, BaseRAGGenerator
        )

        splitter = SplitterClass()
        generator = GeneratorClass()

        data_files = [
            join(data_path, f) for f in listdir(data_path) if isfile(join(data_path, f))
        ]

        all_qa_data = []
        for file_path in data_files:
            all_qa_data.extend(
                process_file(
                    file_path, splitter, generator, num_generations, split_sample
                )
            )

        # Save the processed dataset
        output_path = join(data_path, "processed")
        dataset = Dataset.from_list(all_qa_data)
        dataset.save_to_disk(output_path)
        print(f"Dataset saved to {output_path}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process Splitter and Generator classes"
    )
    parser.add_argument(
        "--splitter", required=True, help="The name of the Splitter class"
    )
    parser.add_argument(
        "--generator", required=True, help="The name of the Generator class"
    )
    parser.add_argument(
        "--num-generations",
        type=int,
        default=3,
        help="The number of questions generated",
    )
    parser.add_argument("--data", required=True, help="The data path")
    parser.add_argument(
        "--split-sample",
        required=False,
        default=-1,
        help="Number of splits to process, by default, all splits are processed",
    )
    args = parser.parse_args()

    main(
        args.splitter,
        args.generator,
        int(args.num_generations),
        args.data,
        int(args.split_sample),
    )
