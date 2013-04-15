#This function should compute a^(b^c) % p where p is a prime.

#runs in polynomial time in log(a), log(b), log(c), and log(p)

#helper function: computes x^n for large x and n
def exp_by_squaring(x, n):
    if n == 1:
        return x

    #if n is even, recurse on squared x and halved n
    elif (n%2) == 0:
        return exp_by_squaring(x*x, n/2)

    #if n is odd, recurse on squared x and (n-1)/2
    else:
        new_x = exp_by_squaring(x*x, (n-1)/2)
        return x*new_x

def exponent_mod(a, b, c, p):
    d = 1
    
    #use helper function to compute b^c
    b_c = exp_by_squaring(b, c)

    #create binary representation of b^c
    b_c_binary = bin(b_c)[2:]

    #for each digit in b_c_binary, square d and mod p
    for i in b_c_binary:
        d = (d*d)%p
        #for each 1 in b_c_binary, multiply d and a, then mod p
        if i == '1':
            d = (d*a)%p
    return d
