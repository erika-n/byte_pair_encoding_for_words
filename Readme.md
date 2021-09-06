
# Byte pair encoding for word separation

# https://en.wikipedia.org/wiki/Byte_pair_encoding

# From wikipedia:

    # Suppose the data to be encoded is

    # aaabdaaabac
    # The byte pair "aa" occurs most often, so it will be replaced by a byte that is not used in the data, "Z". Now there is the following data and replacement table:

    # ZabdZabac
    # Z=aa
    # Then the process is repeated with byte pair "ab", replacing it with Y:

    # ZYdZYac
    # Y=ab
    # Z=aa

# This program creates output with brackets representing the higher level symbols at one or more levels. 
# It demonstrates that byte pair encoding alone is enough to gather some language structure, e.g. finding the pattern 
#   [ < kellynch >< hall > ] 
# which accurately splits the words "kellynch" and "hall", and accurately associates them in a larger structure. 

# This simple algorithm is limited, but already shows some language segmentation properties. It is used for data compression, notably 
# as a first pass step in the GPT-2 natural language model (https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)

# Note that this is not by any means the most efficient implementation of byte pair encoding and is not intended for production use, it is a demonstration only

