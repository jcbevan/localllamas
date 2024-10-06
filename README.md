### Setup Ollama Container
`docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama`  

`docker exec -it ollama ollama run llama3.2`

### Setup Python venv
`python3.12 -m venv .venv`

`.venv\Scripts\activate`

`pip install -r .\requirements.txt`

`streamlit run src/main.py`
