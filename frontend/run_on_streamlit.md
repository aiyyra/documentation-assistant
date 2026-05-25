this code is only useful if run from backend dir

## intialize data/ chunks
```
python -m app.ingestion.processor
python -m app.retrieval.indexer
```

## start streamlit
```
streamlit run ../frontend/streamlit_app.py
```
> will run on port 8501