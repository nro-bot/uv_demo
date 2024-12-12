
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

## Tips n Tricks

Can preview rules and see tokens using this site;
https://demos.explosion.ai/matcher?text=gleason%20score%207%20(3%20%2B%204)&model=en_core_web_sm&pattern=[{"id"%3A0%2C"attrs"%3A[{"name"%3A"IS_DIGIT"%2C"value"%3Atrue}]}%2C{"id"%3A3%2C"attrs"%3A[{"name"%3A"IS_PUNCT"%2C"value"%3Atrue}]}%2C{"id"%3A4%2C"attrs"%3A[{"name"%3A"IS_DIGIT"%2C"value"%3Afalse}]}]