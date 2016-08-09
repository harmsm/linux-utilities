#!/usr/bin/env python3

import itertools, string

class PasswordIterator:

    def __init__(self,base_password):
        """
        """

        self._base_password = base_password
        self._is_letter = [p in string.ascii_letters for p in self._base_password]

        self._to_recombine = [p for i,p in enumerate(self._base_password)
                              if self._is_letter[i]]
        self._recombine_map = [i for i in range(len(self._base_password)) 
                               if self._is_letter[i]]
        self._base_out = list(self._base_password)
        
        lowers = list("".join(self._to_recombine).lower())
        uppers = list("".join(self._to_recombine).upper())

        self._choices = [lowers,uppers]

        self._password_iterator = itertools.product([0, 1], repeat=len(uppers))

    @property
    def next_password(self):
        """
        """

        try:
            password_indexes = next(self._password_iterator)
        except StopIteration:
            return None
 
        for j, i in enumerate(password_indexes):
            self._base_out[self._recombine_map[j]] = self._choices[i][j]
 
        return "".join(self._base_out)           
 

        
   
if __name__ == "__main__":

    import sys
    password_base = sys.argv[1]

    p = PasswordIterator(password_base)

    while True:

        out = p.next_password

        if out is None:
            break
        else:
            print(out)
     
