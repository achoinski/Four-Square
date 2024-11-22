import numpy as np
import itertools
import xlsxwriter

#The purpose of this code is to produce a list of the natural numbers next to every of their decompositions into the sum of four perfect squares. 


# we will only consider partitions that include a highest perfect square of N**2
N = 10
numbers = np.arange(1, N+1, dtype = int)
#Here are said square numbers
squares = numbers**2


#These four lines produce every combination of length 1, 2, 3 and 4 (respectively) of the square numbers!
one_square = list(itertools.combinations_with_replacement(squares, 1))
print("One_square done")
two_squares = list(itertools.combinations_with_replacement(squares, 2))
print("Two_squares done")
three_squares = list(itertools.combinations_with_replacement(squares, 3))
print("Three_squares done")
four_squares = list(itertools.combinations_with_replacement(squares, 4))
print("Four_squares done")

# Here we define a function to replace these lists of combinations (*combo,) with a list of (SUM_OF_COMBO,*combo,); i.e. we inject the sum of the combination as the first element of each combination. I.e. we "sum-tag" it!

def sum_tag(x):
    #x is list of tuples
    for i in range(len(x)):
        x[i] = (np.sum(x[i]),) + x[i]
    return x
    
# Now I make a superlist of tagged combos
square_partitions = sum_tag(one_square) + sum_tag(two_squares) + sum_tag(three_squares)+sum_tag(four_squares)


#Finally: combine everything such that they are ordered by sum (i.e. for each integer we have all the combos that sum to it), and also whip into the data type shapey thing I wanted
A = []
for j in range(int(N**2)+1):
    print(f"{j}/{int(N**2)+1}")
    A.append([[j]])
    for i in range(len(square_partitions)):
        if square_partitions[i][0] == j:
            A[j].append(list(square_partitions[i][1:]))



#Testing ground/filters! Here we can select which we want to see given some criterion. 

# A is a list of lists; element in A is [n, [1,4,4,9],[4,9,1],[9,9]] or whatever. 

def irreducable_n(n):
    for i in range(N**2+1):
        ticker = 0
        for j in range(len(A[i])):
            if j > 0 and len(A[i][j]) == n:
                ticker += 1
        if ticker == len(A[i])-1:
            print(A[i][0])
#x = input("Identify numbers whose square partitions are all of length ____:")

#for i in range(4):
#    print()
#    print((i+1))
#    print()
#    irreducable_n(int(i+1))
#for i in A:
#    print(i)


workbook = xlsxwriter.Workbook('irreducible_spartitions.xlsx')
worksheet = workbook.add_worksheet("Data")
worksheet2 = workbook.add_worksheet("Minbreaks")

n=0
n_1 = 0
n_2 = 0
n_3 = 0
n_4 = 0
ir = 0
for i in range(len(A)-1):
    #print("i",i)
    format = workbook.add_format()
    format.set_bg_color(False)

    ###########################################################################
    #      GENERATING IRREDUCIBLE 3s
    ###########################################################################
    spars = A[i+1][1:]
    m=0
    for spar in spars:
        print("SPar",spar,"len spar",len(spar))
        if len(spar) == 3:
            m+=1
    if m == len(spars):
        worksheet.write(ir,12,A[i+1][0][0])
        ir += 1
    ###########################################################################
    
    lower_square = int(np.floor(np.sqrt(i+1))**2)
    
    #find irreducible spartition (square partition)
    mindices = [n for n, x in enumerate(A[i+1][1:]) if len(x) == len(min(A[i+1][1:],key=len))]
    
    windex = 0 #winning index. lol
    #print(i+1,lower_square,A[i+1][1:],len(min(A[i+1][1:],key=len)))
    for mindex in mindices:
        if lower_square in A[i+1][1:][mindex]:
            #print("IN!",mindex)
            windex = mindex
            
    
    
    ir_spar = A[i+1][1:][windex]
    
    if lower_square not in ir_spar:
        format.set_bg_color('#87CEFA')
        worksheet2.write(n,0,A[i+1][0][0])
        n+=1
        
    if i+1 == lower_square:
        format.set_bg_color('#FF6347')
    worksheet.write(i,0,A[i+1][0][0],format)
    worksheet.write(i,1,len(ir_spar),format)
    worksheet.write(i,2,','.join(str(x) for x in ir_spar),format)
    
    
    if len(ir_spar) == 1:
        worksheet.write(n_1,7,A[i+1][0][0])
        n_1 += 1
    
    if len(ir_spar) == 2:
        worksheet.write(n_2,8,A[i+1][0][0])
        n_2 += 1
    
    if len(ir_spar) == 3:
        worksheet.write(n_3,9,A[i+1][0][0])
        n_3 += 1
    
    if len(ir_spar) == 4:
        worksheet.write(n_4,10,A[i+1][0][0])
        n_4 += 1

#workbook = xlsxwriter.Workbook('foursquare_breaks.xlsx')
#worksheet = workbook.add_worksheet("Breaks")
#print("BREAKS")
n = 0
format.set_bg_color('#FFD700')
for j in numbers[:-1]:
    for i in np.arange(j**2 + 1, (j+1)**2,dtype=int):
        print("len of A",len(A),"i",i)  
        if sum(x.count(j**2) for x in A[i])==0:
            n+=1
            worksheet.write(int(A[i][0][0])-1,3,A[i][0][0],format)
            worksheet.write(int(A[i][0][0])-1,4,''.join(str(x) for x in A[i][1:]),format)

workbook.close()            
print("Done")
#workbook.close()
            
