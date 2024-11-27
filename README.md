
## Quickstart
```
uv venv
source .venv/bin/activate
uv sync
uv run -- spacy download en_core_web_sm   
```

Commands:
```
uv run test_nlp.py # my eval script here currently -- temporary
uv run pytest # run pytests
uv run phenoxtractors.py # a few demo strings here currently -- temporary
```

instead of `python phenoxtractor.py` use `uv` run instead. 

### Pip

```
python -m pip install -r requirements.txt
```

## TODO

- Explore using dataclass-inspired DataFrameModel instead of object-oriented DataFrameSclshema
-- Reference: https://pandera.readthedocs.io/en/stable/index.html


## Dev quickstart
```
uv venv --python 3.11.5
source .venv/bin/activate
uv python pin 3.11.5 
uv add [some dependency]
uv sync
git add uv.lock
git commit -m "update dependencies"
uv pip compile pyproject.toml -o requirements.txt
```
