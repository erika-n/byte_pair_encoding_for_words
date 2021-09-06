
# Byte pair encoding for word separation



### Byte pair encoding 

From Wikipedia (https://en.wikipedia.org/wiki/Byte_pair_encoding):

> Suppose the data to be encoded is
>
> aaabdaaabac
>
> The byte pair "aa" occurs most often, so it will be replaced by a byte that is not used in the data, "Z". Now there is the following data and replacement table:
>
> ZabdZabac
> Z=aa
> 
> Then the process is repeated with byte pair "ab", replacing it with Y:
>
> ZYdZYac
> Y=ab
> Z=aa


Byte pair encoding is used for data compression, notably 
as a first pass step in the GPT-2 natural language model (https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)

### Byte pair encoding for word segmentation 

This program creates output with brackets representing the higher level symbols at one or more levels. Spaces are removed from the text before processing, creating a word segmentation task.

It demonstrates that byte pair encoding alone is enough to gather some language structure, e.g. finding the pattern 
>   [ < kellynch >< hall > ] 

which accurately splits the words "kellynch" and "hall", and accurately associates them in a larger structure. 

Another example is 

> [ < precise >< ly > ]

which accurately splits the word "precisely" into parts and joins them as a larger unit.

The purpose of this project is to demonstrate the power of this very simple technique to find word-like patterns in text. 

### Usage
python byte_pair_encoding_for_words.py

The files under output show the output of this program.



