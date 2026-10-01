import pathlib

LETTERS_DIR = pathlib.Path(__file__).parent.parent.parent / "static"

# Golden set, written by humans (the committee): what a correct scoring of each letter must contain
GOLDEN = [
    dict(letter="letter-mario-rossi.txt", applicant="Mario Rossi", author="Alessandro Bianchi",
         programme="Data Science", has_weaknesses=False, min_score=4),
    dict(letter="letter-jean-dupont.txt", applicant="Jean Dupont", author="Claire Moreau",
         programme="Artificial Intelligence", has_weaknesses=True, max_score=4),
    dict(letter="letter-mohammed-ali.txt", applicant="Mohammed Ali", author="Kareem Al-Haddad",
         programme="Cyber Security", max_score=3),
]


def read_letter(golden: dict) -> str:
    return (LETTERS_DIR / golden["letter"]).read_text()
