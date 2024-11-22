from langchain_ollama import ChatOllama, OllamaLLM

model = OllamaLLM(model="llama3.2")

for content in model.stream("Come up with 10 names for a song about parrots"):
    print(content, end="", flush=True)
