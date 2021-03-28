
def non_space_split(dictlist, sentence, weighted = False):

    import numpy
    from scipy.linalg import qr


    '''
    This is the function, which splits the sentence without spaces
    :param dictlist: type - list, a list of possible words (dictionary)
    :param sentence: type - str, the sentence to be splitted
    :param weighted: type - bool, an optional parameter to use length-weight
    :return: type - list, a list of splitted words of the sentence
    '''

    def find_subs(pattern, bigstring):

        '''
        Nested function to find all positions of a pattern in a bigstring
        :param pattern:
        :param bigstring:
        :return: list of positions
        '''

        lastpos = len(bigstring) - len(pattern) + 1     # the last possible position of the word in the sentence
        reslist = list()
        i = 0

        while (i <= lastpos):
            nextpos = bigstring.find(pattern, i, len(bigstring))
            if nextpos != -1:
                i = nextpos + 1
                reslist.append(nextpos)
            else:
                break
        return reslist

    def build_words_matr():

        '''
        Nested function to build the matrix of possible words positions (left side of the system)
        :return:
        '''

        # First we need to find all positions of all words of the dictionary in the sentence
        wordpos = list()
        for word in dictlist:
            wordpos.append(find_subs(word, sentence))

        # Now we need to build a matrix of 0 and 1. Number of rows = number of letters in the
        # Sentence, number of cols = number of words in the dictionary.
        # For example we have a sentence "mymanywordsmy". Our dictionary = ["a" "many"
        # "words" "m" "my" ]
        # So we build the Matrix in the next way:
        # Search the first word from a dictionary "a", it occupies the 4th
        # position in the sentence. So the first column in Matr will be [0 0 0 1 0 0 0 0 0 0 0 0 0]
        #
        # The word "m" stays in 3 different positions in the Sentence: 1, 3 and 12th, so it gives us
        # 3 columns in the Matr:
        # [1 0 0 0 0 0 0 0 ....]
        # [0 0 1 0 0 0 0 0 ....]
        # [0 0 0 0 0 0 0 0 0 0 0 1 0]
        #
        # The word "my" stays in 2 places and each time it occupies 2 positions
        # (because it has 2 letters), so columns of the Matr will be:
        # [1 1 0 0 0 0 0 0 0 0 0....]
        # [0 0 0 ..............  1 1]
        #
        # So we build this matrix for all the found words for all their probable positions
        i = 0
        wordarr = list()  # this is the list of lists wich will be transformed to matrix to solve the system
        wordarrpos = list()  # this is the list of (word, position_in_wordarr) to match the final result
        for word in dictlist:
            wordleng = len(word)
            sentleng = len(sentence)

            if wordpos[i] != []:

                if (len(word) != 0) and (weighted == True):
                    weight = 1 / (len(word)**2)
                else:
                    weight = 1

                k = 0
                for j in wordpos[i]:
                    wordcol = [0] * sentleng
                    wordcol[j:j + wordleng] = [weight] * wordleng
                    wordarr.append(wordcol)
                    wordarrpos.append((dictlist.index(word), wordpos[i][k]))
                    k = k + 1
            i = i + 1

        # transform list of lists to array of numpy. This is the left side matrix of the system
        matr = numpy.asarray(wordarr)
        # wordarrpos = numpy.asarray(wordarrpos)
        return (matr,wordarrpos)

    def lin_solve_qr_underdet(a,b):

        '''
        Solver for underdetermined systems (rows<cols) using the QR decomposition
        :param a: left-side matrix, N rows < N cols
        :param b: right-side column-vector
        :return: solution vector. returns -1 if the matrix is not underdetermined
        '''

        rows,cols = a.shape

        if rows<cols:
            a_t = a.transpose()
            q,r,p = qr(a_t,pivoting = True, mode='economic')

            rt = r.transpose()
            rt1 = numpy.linalg.inv(rt)
            rt1b = numpy.matmul(rt1,b)
            res = numpy.matmul(q,rt1b)
            return res
        else:
            return -1

     # Now we need to solve the system of equations matr*sol=univect
    # right side vector
    univect1 = [1]*len(sentence)
    univect = (numpy.asmatrix(univect1)).transpose()

    # left side matrix
    (matr,wordarrpos) = build_words_matr()
    matr = matr.transpose()

    rows, cols = matr.shape

    if rows < cols:         # if system is underdetermined
        sol = lin_solve_qr_underdet(matr, univect)
    else:                   # if system is square or overdetermined
        sol = numpy.linalg.lstsq(matr,univect, rcond=100)[0]


    # normalize the solution with a treshold. All what is less than
    # treshold becomes equal to 0, all what is more than treshold becomes 1
    treshold = 0.5
    normsol = list()
    for s in sol:
        if s>treshold:
            normsol.append(1)
        else:
            normsol.append(0)

    # sort words in the dictionary of probable positions (sort by their position in the sentence)
    respos = list()
    ind = 0
    for i in normsol:
        if i != 0:
            respos.append(wordarrpos[ind])
        ind = ind + 1
    respos = sorted(respos, key=lambda x: x[1])

    # buils the resulting list of words in a correct order
    res = list()
    for i in respos:
        wordnum,pos = i
        res.append(dictlist[wordnum])

    return res


# Reminder if the script was ran directly
if __name__ == '__main__':
    # the function ran directly
    dictlist = ['this', 'function', 'must', 'be', 'ran', 'remotely']
    sentence = 'thisfunctionmustberanremotely'
    r = non_space_split(dictlist, sentence, weighted=False)
    print(r)


