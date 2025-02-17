# test_import.py
try:
    from langchain_openai import ChatOpenAI
    print("Import successful!")
except ModuleNotFoundError as e:
    print(f"Import failed: {e}")