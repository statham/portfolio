##You are given the size n of an array A that contains only zeros. You are also given
##a list of n ordered pairs of integers (ai bi) such that 0 <= ai < bi <= (n-1). For each
##pair (ai, bi), you change the bit in position k of the array (for every integer k such that
##ai <= k <= bi) from 0 to 1 or from 1 to 0

#runs in O(n)

def find_array(N, B):
    #start with hash table of all zeros
    hash_table = [0]*N
    summation = 0
    #for each pair, add one to the x position in hash table, subtract one from y+1 position
    for (x,y) in B:
        hash_table[x] += 1
        if y < (N-1):
            hash_table[y+1] -= 1
    for x in range(len(hash_table)):
        #summation will only take values 0 or 1
        summation = (summation + hash_table[x])%2
        hash_table[x] = summation
    return hash_table
