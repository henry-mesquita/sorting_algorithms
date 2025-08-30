def bubble_sort_gen(sizes, comparisons, array_accesses):
    n = len(sizes)
    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons += 1
            array_accesses += 2
            if sizes[j] > sizes[j + 1]:
                sizes[j], sizes[j + 1] = sizes[j + 1], sizes[j]
                array_accesses += 4
                yield j, j + 1, comparisons, array_accesses

def quick_sort_gen(arr, left, right, comparisons, array_accesses):
    if left >= right:
        return
    
    i = left
    pivot = arr[right]

    array_accesses += 1    
    for j in range(left, right):
        comparisons += 1
        array_accesses += 1
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            array_accesses += 4
            i += 1
            yield j, i, comparisons, array_accesses

    array_accesses += 4
    arr[i], arr[right] = arr[right], arr[i]

    yield from quick_sort_gen(arr, left, i - 1, comparisons, array_accesses)
    yield from quick_sort_gen(arr, i + 1, right, comparisons, array_accesses)

def merge_sort_gen(arr, left, right, comparisons, array_accesses):
    comparisons += 1
    if left >= right:
        return
    
    mid = (left + right) // 2

    yield from merge_sort_gen(arr, left, mid, comparisons, array_accesses)
    yield from merge_sort_gen(arr, mid + 1, right, comparisons, array_accesses)

    left_copy = arr[left:mid + 1]
    right_copy = arr[mid + 1:right + 1]
    array_accesses += 2

    i = j = 0
    k = left

    while i < len(left_copy) and j < len(right_copy):
        comparisons += 1
        left_i = left + i
        right_i = mid + 1 + j

        yield left_i, right_i, comparisons, array_accesses

        comparisons += 1
        array_accesses += 2
        if left_copy[i] <= right_copy[j]:
            arr[k] = left_copy[i]
            array_accesses += 2
            i += 1
        else:
            arr[k] = right_copy[j]
            array_accesses += 2
            j += 1
        k += 1
    
    while i < len(left_copy):
        comparisons += 1
        arr[k] = left_copy[i]
        array_accesses += 2
        i += 1
        k += 1
    while j < len(right_copy):
        comparisons += 1
        arr[k] = right_copy[j]
        array_accesses += 2
        j += 1
        k += 1

def insertion_sort_gen(arr, comparisons, array_accesses):
    for i in range(1, len(arr)):
        for j in range(i, 0, -1):
            comparisons += 1
            array_accesses += 2
            if arr[j] < arr[j - 1]:
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
                array_accesses += 4
                yield i, j, comparisons, array_accesses
            else:
                break
