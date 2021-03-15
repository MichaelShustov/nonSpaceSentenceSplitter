function resStr = nonSpaceSentenceSplit(Dict, SentenceStr, weighted)
%nonSpaceSentenceSplit splits the non-space-sentence into separated words from a
%dictionary Dict. (C) Michael Shustov, 2021.

%Dict - string array of words (dictionary) (["i" "like" "bike" "dive"])
%SentenceStr - string ("ilikebikei")
%resStr - result string array of words of the sentence ["i" "like" "bike"
%"i"]
%weighted - 'true'/'false'. If 'true' - the smaller sized words are
%preferable. Example: in a dictionary ["a" "aa" "aaa" "aaat"] and sentence
%"aaaaaat" the function will find ["a" "a" "a" "aaat"]. 

%%
%The first step - find positions of words from the dictionary in our
%sentence. This can be done using the "suffix tree" of the sentence, but
%Matlab has no internal function to build the tree and I do not want to
%program it now, so we will use internal Matlab functions to find substrings in a
%basic string
%Index in DectPos is the number of the word in our dictionary, elements of
%DictPos- vectors with possible positions of these words in the non-space-Sentence
for i = 1:size(Dict,2)
   DictPos{i}= strfind(SentenceStr,Dict(i));
end

%%

%Now we need to build a matrix of 0 and 1. Number of rows = number of letters in the
%Sentence, number of cols = number of words in the dictionary.
%For example we have a sentence "mymanywordsmy". Our dictionary = ["a" "many"
%"words" "m" "my" ]
%So we build the Matrix in the next way:
%Search the first word from a dictionary "a", it occupies the 4th
%position in the sentence. So the first column in Matr will be [0 0 0 1 0 0 0 0 0 0 0 0 0]
%
% The word "m" stays in 3 different positions in the Sentence: 1, 3 and 12th, so it gives us 
% 3 columns in the Matr:
%[1 0 0 0 0 0 0 0 ....]
%[0 0 1 0 0 0 0 0 ....]
%[0 0 0 0 0 0 0 0 0 0 0 1 0]
%
%The word "my" stays in 2 places and each time it occupies 2 positions
%(because it has 2 letters), so columns of the Matr will be:
%[1 1 0 0 0 0 0 0 0 0 0....]
%[0 0 0 ..............  1 1]
%
%So we build this matrix for all the found words for all their probable
%positions

Matr = [];
k = 1;
for i = 1:size(Dict,2)
   
   %length of i-th word in the dictionary 
   curLength = strlength(Dict(i));
   
   if size(DictPos{i},2) > 0
       for j = 1:size(DictPos{i},2)
          
          %this is our positions matrix
          if weighted == 'true' 
              weight = curLength;
          else weight = 1;
          end
          
          Matr(DictPos{i}(j):DictPos{i}(j)+curLength-1,k) = 1/weight; 
          
          %this is the array who's 1st col contains the number of word in
          %the dictionary and the second col contains related start
          %position of this word in the sentence. We need this array to
          %match our final result with dictionary words and their order int
          %the sentence
          WordsNum(k,1) = i;
          WordsNum(k,2) = DictPos{i}(j);
          k = k + 1;
          
       end
   end
end

%%
%Good! Now we need to solve a system of linear algebraic equations
% Matr * sol1 = vect1. 
%Here vect1 - col-vector of ones with a length of original
%sentence. It means that all positions in the original sentence are
%occupied with letters
% sol1 - col-vector which we are searching for.
% i.e. our sentence is a linear combination of all words from a dictionary
% in all their probable positions with coefficients in sol1

vect1 = [];
vect1(1:strlength(SentenceStr)) = 1;
vect1 = vect1';   %transpose of a row-vector to a column-vector

%and the most satisfying moment of solving the system.....
sol1 = linsolve(Matr,vect1);
%the obtained solution (with a linsolve) is not precize, but our
%coefficients can be only integer 0 or 1, so we round the obtained
%solution. 
%Matlab can also give us -1 in a solution, but because of some features of
%the language we may not filter them, because they do not influence much on
%the solution result (they give 1-2 wrong words in the dictionary)
sol1 = round(sol1);
sol1(sol1>1) = 1;

%%
%sort the words in the dictionary of probable positions
res = sortrows(WordsNum(sol1==1,:),2);

% build the result array of words in the correct order
for i = 1:size(res,1)
    resStr(i) = Dict(res(i,1)); %!!!!!!!!this is the final array of words from the dictionary in a correct order
end


end

