# Config Folder

This folder contains configuration files for managing model, database, and benchmarking settings in the poetry RAG project. Modify these files to customize different aspects of the pipeline without changing code.

### Files

- **model_config.yaml**: Settings for embedding and generation models, including model paths, fine-tuning options, and generation parameters.
- **database_config.yaml**: Database configurations for indexing and retrieval, such as database type, index type, similarity metric, and batch size.
- **benchmark_config.yaml**: Parameters for evaluating model performance, with options for datasets, metrics (e.g., thematic relevance, stylistic accuracy), and logging.

### Usage

1. **Edit Parameters**: Adjust any settings here to fit the poetry dataset or retrieval needs.
2. **Add New Configs**: Create new YAML files as needed, ensuring they follow a similar structure for easy integration.
