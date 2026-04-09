import tiktoken
enc  = tiktoken.encoding_for_model("gpt-4o")
text = "Hey There, My name is Subhajit"
tokens = enc.encode(text);

decoded = enc.decode(tokens)

print("Tokens", tokens)
print("Decoded", decoded)