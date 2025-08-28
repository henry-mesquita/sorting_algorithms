def bubble_sort_gen(sizes, comparisons):
        n = len(sizes)
        for i in range(n):
            for j in range(0, n - i - 1):
                if sizes[j] > sizes[j + 1]:
                    comparisons += 1
                    sizes[j], sizes[j + 1] = sizes[j + 1], sizes[j]
                    yield j, j + 1, comparisons

def quick_sort_gen(arr, left, right, comparisons):
    if left >= right:
        return
    
    i = left
    pivot = arr[right]
    
    for j in range(left, right):
        if arr[j] <= pivot:
            comparisons += 1
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            yield j, i, comparisons

    arr[i], arr[right] = arr[right], arr[i]

    yield from quick_sort_gen(arr, left, i - 1, comparisons)
    yield from quick_sort_gen(arr, i + 1, right, comparisons)

def merge_sort_gen(arr, left, right, comparisons):
    if left >= right:
        comparisons += 1
        return
    
    mid = (left + right) // 2

    yield from merge_sort_gen(arr, left, mid, comparisons)
    yield from merge_sort_gen(arr, mid + 1, right, comparisons)

    left_copy = arr[left:mid + 1]
    right_copy = arr[mid + 1:right + 1]

    i = j = 0
    k = left

    while i < len(left_copy) and j < len(right_copy):
        comparisons += 1
        left_i = left + i
        right_i = mid + 1 + j

        yield left_i, right_i, comparisons

        if left_copy[i] <= right_copy[j]:
            comparisons += 1
            arr[k] = left_copy[i]
            i += 1
        else:
            comparisons += 1
            arr[k] = right_copy[j]
            j += 1
        k += 1
    
    while i < len(left_copy):
        comparisons += 1
        arr[k] = left_copy[i]
        i += 1
        k += 1
    while j < len(right_copy):
        comparisons += 1
        arr[k] = right_copy[j]
        j += 1
        k += 1
