# Paper Fetcher for Pharma/Biotech

This is a command-line tool to fetch research papers from PubMed. It filters the results to identify papers with at least one author affiliated with a pharmaceutical or biotech company and outputs the data to a CSV file or the console.

## Code Organization

The project is structured into two main parts as recommended:

1.  **`get_papers_list/`**: A reusable Python module containing all the core logic.
    -   `api.py`: Manages all asynchronous calls to the PubMed API.
    -   `analyzer.py`: Contains heuristics and logic to classify author affiliations as "corporate" or "academic".
    -   `models.py`: Uses Pydantic to define strict data models (`Paper`, `Author`) for type safety.
    -   `processor.py`: Orchestrates the entire workflow from fetching paper IDs to parsing details and filtering results.
    -   `main.py`: The entry point for the command-line application, built using Typer.

2.  **`pyproject.toml`**: The Poetry configuration file. It defines dependencies, project metadata, and the `get-papers-list` command-line script.

## Installation

This project is managed with [Poetry](https://python-poetry.org/).

1.  **Clone the repository:**
    ```bash
    https://github.com/pythoncruz/pubmed_fetcher.git
    ```

2.  **Install dependencies:**
    Ensure you have Poetry installed. Then, run the following command in the project root:
    ```bash
    poetry install
    ```
    This will create a virtual environment and install all necessary libraries.

## How to Execute the Program

You can run the program using the poetry run get-papers-list "crispr therapeutics" -d`.

### Basic Usage

Provide a search query as an argument. The output will be printed to the console as CSV.

```bash
poetry run get-papers-list "crispr gene editing"
```

### Saving to a File

Use the `-f` or `--file` option to save the output to a specified CSV file.

```bash
poetry run get-papers-list "cancer immunotherapy pfizer" --file results.csv
```

### Enabling Debug Mode

Use the `-d` or `--debug` flag to print verbose information about the execution process, which is useful for troubleshooting.

```bash
poetry run get-papers-list "moderna vaccine" -f moderna_papers.csv -d
```

### Getting Help

To see all available options and instructions, use the `--help` flag.

```bash
poetry run get-papers-list --help
```

## Tools and Libraries Used

* **Python 3.9+**
* **[Poetry](https://python-poetry.org/)**: For dependency management and packaging.
* **[Typer](https://typer.tiangolo.com/)**: For creating a clean and robust command-line interface.
* **[HTTPX](https://www.python-httpx.org/)**: As a modern, asynchronous HTTP client for efficient API calls.
* **[Pydantic](https://docs.pydantic.dev/)**: For data validation and settings management using Python type annotations.
* **LLM Assistance**: Gemini was used to structure the project, generate boilerplate code, and refine the logic for identifying non-academic affiliations.
