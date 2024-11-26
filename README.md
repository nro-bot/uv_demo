
## Quickstart
```
uv venv
uv sync
source .venv/bin/activate
uv venv --python 3.11.5
uv python pin 3.11.5 #  
uv run -- spacy download en_core_web_sm   
```

Commands:
```
uv run test_nlp.py # my eval script here currently -- temporary
uv run pytest # run pytests
uv run phenoxtractors.py # a few demo strings here currently -- temporary
```


## TODO

- Explore using dataclass-inspired DataFrameModel instead of object-oriented DataFrameSchema
-- Reference: https://pandera.readthedocs.io/en/stable/index.html

uv pip compile pyproject.toml -o requirements.txt
