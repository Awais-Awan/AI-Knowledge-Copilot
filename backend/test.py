from app.utils.chunking import chunk_text

text = "This is a test document. " * 100
chunks = chunk_text(text)

print(len(chunks))
print(chunks[0][:100])

