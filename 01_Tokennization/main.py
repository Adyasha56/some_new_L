import tiktoken

# i want to create a encoder for this particular model
enc = tiktoken.encoding_for_model("gpt-4o")

text = "hi i am looking for a job"
tokens = enc.encode(text)

print("Tokens: " , tokens)
# output i got - Tokens [3686, 575, 939, 3778, 395, 261, 3349]

decoder = enc.decode([3686, 575, 939, 3778, 395, 261, 3349])
print("Decoded : ", decoder)
