# pip install pyyaml
import pathlib
import yaml

LETTERS_DIR = pathlib.Path(__file__).parent.parent / "data"  # i.e. <root dir>/data/
TEST_DATA_FILE = pathlib.Path(__file__).parent / "test_data.yml"

# list of test cases, each one with an "input" (letter file name) and its "expectations"
TEST_CASES = yaml.safe_load(TEST_DATA_FILE.read_text())


def read_letter(case: dict) -> str:
    return (LETTERS_DIR / case["input"]).read_text()
