d = ['aa','a','aaa','aaab','aaaaaaaaaaaaaaaaaaaaaaaa','aax','v']
sent = 'aaavvaaaaaaaaaaaaabaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaax'

import non_space_split

res = non_space_split.non_space_split(d,sent,False)
print(len(sent))
print(len(res))
print(res)








