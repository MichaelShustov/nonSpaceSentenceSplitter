# nonSpaceSentenceSplitter
the Matlab function to split sentence without spaces between words into the list of words using the pre-given dictionary

For example, you have a string "helloiamrobotihaveatask"
And we want to split it into separated words using the dictionary ["hello" "i" "am" "robot" "have" "task" "mask" "gun" "a"]

as a result we want to get a separated string as a list of words ["hello" "i" "am" "robot" "i" "have" "a" "task"]

the function's parameter 'weighted' allows to prefer smaller words, i.e. if in the dictionary we also have a word "iam" and weighted=true, than the algorithm prefers to split the above sentence to ["hello" "i" "am" "robot" "i" "have" "a" "task"] instead of ["hello" "iam" "robot" "i" "have" "a" "task"]
