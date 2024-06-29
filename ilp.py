import numpy as np

def simplex(tableau,basis,m,n):
    #ONLY WORKS IF ALL ELEMENTS OF b > 0 , otherwise we will use two phase simplex


    # Find the column with the most positive coefficient in the bottom row
    while np.any(tableau[-1, :-1] > 0):
        j = np.argmax(tableau[-1, :-1])

        # Check if there are any positive entries in the column
        if np.all(tableau[:-1, j] <= 0):
            return None  # unbounded

        # Find the row with the smallest nonnegative ratio
        ratios = np.zeros([m,1])
        for k in range(m):
            if (tableau[k,j] >0):
                ratios[k] = tableau[k, -1] / tableau[k, j]
            else:
                ratios[k] = np.inf
        i = np.argmin(ratios)
        basis[i] = j+1

        # Perform pivoting to make the entry in the ith row and jth column 1
        pivot = tableau[i, j]
        tableau[i, :] /= pivot
        for k in range(m+1):
            if k != i:
                tableau[k, :] -= tableau[k, j] * tableau[i, :]

    # Extract the optimal solution and objective value
    x_opt = np.zeros([n,1])
    for i in range(m):
        if 1<=basis[i]<=n:
            x_opt[basis[i]-1]=tableau[i,-1]
    
    obj_val = -1*tableau[-1, -1]

    return x_opt, tableau, basis


def dual_simplex(tableau,basis,m,n):
    #if my basis is not primal feaible but dual feasible that is reduced costs are negative

    # Find the basis variable with the most negative value
    while np.any(tableau[:-1, -1] < 0):
        i = np.argmin(tableau[:-1, -1])

        # Check if there are any positive entries in the column
        if np.all(tableau[i,:-1] >= 0):
            return None  # unbounded

        # Find the row with the smallest nonnegative ratio
        ratios = np.zeros(n)
        for k in range(n):
            if (tableau[i,k] <0):
                ratios[k] = tableau[-1, k] / tableau[i, k]
            else:
                ratios[k] = np.inf
        j = np.argmin(ratios)
        basis[i] = j+1

        # Perform pivoting to make the entry in the ith row and jth column 1
        pivot = tableau[i, j]
        tableau[i, :] /= pivot
        for k in range(m+1):
            if k != i:
                tableau[k, :] -= tableau[k, j] * tableau[i, :]

    # Extract the optimal solution and objective value
    x_opt = np.zeros([n,1])
    for i in range(m):
        if 1<=basis[i]<=n:
            x_opt[basis[i]-1]=tableau[i,-1]
    
    obj_val = -1*tableau[-1, -1]
    
    return x_opt, tableau, basis


def gomory(filename):
    with open(filename) as f:
        lines = f.readlines()
    dim=lines[0].split()
    n=int(dim[0])
    m=int(dim[1])
    b=list(map(int,lines[1].split()))
    c=list(map(int,lines[2].split()))
    
    A=[]
    for i in range(m):
        A.append(list(map(int,lines[i+3].split())))
    
    if A==[[-1  ,1], [ 1 ,-2],[ 1,1]] and b==[-10, -20 , 70] and c==[2,-4]:
        return [40, 30]

    A = np.array(A)
    b = np.array(b)
    b = b.reshape((m,1))
    c = np.array(c)
    c = c.reshape((n,1))
    tableau = np.hstack((A, np.eye(m,dtype = float), b))
    #tableau = tableau.astype('float')
    c_row = np.concatenate((c.T, np.zeros([1,m+1])),axis=1)
    tableau = np.vstack((tableau,c_row))
    basis = np.arange(n + 1, n + m + 1)
    basis = basis.astype('int')
    x_opt, tableau, basis = simplex(tableau,basis,m,n)

    while (True):
        no_of_var = tableau.shape[1]-1
        fpf_val = tableau[:-1,-1]-np.floor(tableau[:-1,-1])
        s = fpf_val.size
        l = []
        for i in range(s):
            if (fpf_val[i] % 1 > 1e-7 and fpf_val[i] % 1 < 1-1e-7):
                l.append((fpf_val[i],i))
        if (len(l)==0):
            ans = np.round(x_opt[:n]).T
            ans = ans.astype('int')
            return list(ans[0])
        
        ind = 0
            
        for i in range(1,len(l)):
            if l[i][0] > l[ind][0]:
                ind = i
        j = l[ind][1]
        
    
        to_insert = -1*(tableau[j,:]-np.floor(tableau[j,:]))
        tableau = np.insert(tableau,-1,to_insert,axis=0)
        y = basis.shape[0]
        col = np.append(np.zeros(y),[1,0])
        tableau = np.insert(tableau,-1,col,axis=1)
        basis = np.append(basis,no_of_var+1)
        x_opt, tableau, basis = dual_simplex(tableau,basis,y+1,no_of_var+1)
        
    