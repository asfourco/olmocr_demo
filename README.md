# Demo project for using [olmOCR](https://github.com/allenai/olmocr)

## Requirements
1. LM-Studio running on a local machine with olmOCR model 
2. Python 3.11
3. [uv](https://docs.astral.sh/uv)

## Setup
1. Clone the repository and change to the directory
2. Install the requirements
```bash
# create a virtual environment
uv venv --python 3.11

# activate the virtual environment
source .venv/bin/activate

# install the requirements
uv pip install -r pyproject.toml
```

## Usage
1. Start the LM-Studio server
2. update `.envrc` with the correct LM-Studio server URL, e.g. `http://localhost:12345/v1`
3. get a sample pdf of handwritten text and place it in the `samples` directory
3. Run the demo
```bash
uv run main.py samples/sample.pdf
```