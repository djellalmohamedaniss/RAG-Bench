
# QA Dataset Generation Guide

Follow this guide to create a QA dataset based on your documents.

## Steps to Implement Classes

### 1. **Create a Generation Class**
- **Base Class:** Inherit from `generation/base.py`.
- **Purpose:** Implement the following methods:
  - `generate_questions`: Define the logic for generating questions.
  - `generate_answers`: Define the logic for generating answers.

### 2. **Create a Splitter Class**
- **Base Class:** Inherit from `splitter/base.py`.
- **Purpose:** Implement the following methods:
  - `read`: Define how the data is read from the source.
  - `split`: Define how the data is split into smaller chunks for processing.

### 3. **Organize Your Dataset**
- Place your dataset in the following directory:
  `datasets/your_dataset`

## Generating the QA Dataset

Run the following command to process and generate your QA dataset:

```bash
./scripts/run_processing.sh --splitter SplitterClassName \
--generator GenerationClassName \
--num-generations 5 \
--data datasets/your_dataset_path \
--split-sample 10 \
```

### **Command Parameters**
- `--splitter`: Name of the splitter class you implemented (e.g., `MyCustomSplitter`).
- `--generator`: Name of the generator class you implemented (e.g., `MyCustomGenerator`).
- `--num-generations` *(optional)*: Number of QA pairs to generate per chunk. Default is 5 if omitted.
- `--data`: Path to your dataset directory or file (e.g., `datasets/your_dataset_path`).
- `--split-sample` *(optional)*: Number of chunks to pick from a document. By default, all chunks are used if this parameter is omitted.

### Example Command

To generate a dataset for the `tableau-historique-paris` dataset, use:

```bash
./scripts/run_processing.sh --splitter HistoireParisSplitter \
--generator RAGGeneratorOpenAI \
--data datasets/tableau-historique-paris
```

In this example:
- `HistoireParisSplitter` is the splitter class used to preprocess and split the data.
- `RAGGeneratorOpenAI` is the generator class used to create QA pairs.
- `datasets/tableau-historique-paris` is the dataset to be processed.
