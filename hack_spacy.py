import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span, DocBin
import random
from phenoxtractor import get_test_strs 
import subprocess
from rich.traceback import install
install(show_locals=True)


def HACK_create_spacy_annotations():
    # -- from https://course.spacy.io/en/chapter4 Create training data (1) 
    # TEXTS is a list of strs
    TEXTS = get_test_strs()

    nlp = spacy.blank("en")
    matcher = Matcher(nlp.vocab)
    # Add patterns to the matcher
    total_last_pattern = [
        {"TEXT": {"REGEX": r"[3-6]"}},  
        {"IS_DIGIT": False},  
        {"TEXT": {"REGEX": r"[3-6]"}},  
    ]
    matcher.add("GLEASON_COMPONENT", [total_last_pattern])
    docs = []
    for doc in nlp.pipe(TEXTS):
        print('DOC')
        print(doc)
        # HIPRI TODO: -- HACK -- TO MANUAL REVIEW !!
        matches = matcher(doc)
        spans = []
        seen_tokens = set()

        for match_id, start, end in matches:
            print(doc[start:end])
            # TODO FIX - Check if the tokens in the span are already part of another entity
            # if all(token not in seen_tokens for token in doc[start:end]):
            span = Span(doc, start, end, label=match_id)
            spans.append(span)
            try:
                doc.ents = spans
                docs.append(doc)
            except ValueError:
                pass

    return docs
        # spans = [Span(doc, start, end, label=match_id) for match_id, start, end in matches]

    # docs = []
    # for doc in nlp.pipe(TEXTS):
    #     matches = matcher(doc)
    #     spans = [Span(doc, start, end, label=match_id) for match_id, start, end in matches]
    #     doc.ents = spans
    #     docs.append(doc)
    # return docs


def create_spacy_config():
    subprocess.run(
        [
            "uv", "run", "spacy", "init", "config", "./spacy/config.cfg", 
            "--lang", "en", 
            "--pipeline", "ner",
            "--force"
        ], 
        check=True
    )

# -- CREATE TRAINING CORPUS
# Create test/train split with annotated data
# -- from https://course.spacy.io/en/chapter4 Generating a training corpus (3)
def test_train_split(docs, export=True):
    random.shuffle(docs)
    train_docs = docs[:len(docs) // 2]
    dev_docs = docs[len(docs) // 2:]

    # Create and save a collection of training docs
    if export:
        train_docbin = DocBin(docs=train_docs)
        train_docbin.to_disk("./spacy/train.spacy")
        # Create and save a collection of evaluation docs
        dev_docbin = DocBin(docs=dev_docs)
        dev_docbin.to_disk("./spacy/dev.spacy")


def run_spacy_training():
# !python -m spacy train ./exercises/en/config_gadget.cfg --output ./output --paths.train ./exercises/en/train_gadget.spacy --paths.dev ./exercises/en/dev_gadget.spacy
    command = [
        "uv", "run", "spacy", "train", "./spacy/config.cfg",
        "--output", "./spacy/output",
        "--paths.train", "./spacy/train.spacy",
        "--paths.dev", "./spacy/dev.spacy"
    ]
    subprocess.run(command, check=True)

# Side note: useful util: $ python -m spacy convert ./train.gold.conll ./corpus

def lookatit():
    nlp = spacy.load("./spacy/output/model-best")
    doc = nlp("This is a test of the model performing on 3+4=7.")
    print(doc.ents)

if __name__ == '__main__':
    docs = HACK_create_spacy_annotations() 
    test_train_split(docs, export=True)
    create_spacy_config()
    run_spacy_training()
    lookatit()