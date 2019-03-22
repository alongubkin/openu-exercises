def partition(A, p, r):
  x = A[r]
  i = p-1

  for j in range(p, r): 
    if A[j] <= x:
      i += 1
      A[j],A[i] = A[i],A[j]
      # print 'swap ', A[j], ' <=> ', A[i], ' ==> ', A


  A[i+1],A[r] = A[r],A[i+1] 
  # print 'swap2 ', A[i+1], ' <=> ', A[r], ' ==> ', A

  return i+1

def quick_sort_recursive(A, p, r, first):
  print 'Quicksort(A={}, p={}, r={}, x={}, first={})'.format(A, p, r, A[r], first)

  if p < r: 
    q = partition(A, p, r)
    quick_sort_recursive(A, p, q - 1, True)
    quick_sort_recursive(A, q + 1, r, False)



  

data = [1,3,5,7,9,11,13,2,4,6,8,10,12,14]
print len(data)
quick_sort_recursive(data, 0, len(data) - 1, None)

print data