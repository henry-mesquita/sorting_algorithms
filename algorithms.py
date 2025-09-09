def bubble_sort_gen(
    arr:                list[int],
    counts:             dict[str, int]
):
    """
    Generator for bubble sort algorithm.

    Parameters:
        sizes (list[int]): A list of numbers to be sorted.
        comparisons (int): The number of comparisons made in the bubble sort algorithm.
        array_accesses (int): The number of array accesses made in the bubble sort algorithm.

    Yields:
        tuple: A tuple containing the current state of the list and the index of the current element being compared.
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            counts['comparisons'] += 1
            counts['array_accesses'] += 2
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                counts['array_accesses'] += 4
                yield (j, j + 1, counts['comparisons'], counts['array_accesses'])

def quick_sort_gen(
    arr:                list[int],
    left:               int,
    right:              int,
    counts:             dict[str, int]
):
    """
    Generator for quick sort algorithm.

    Parameters:
        sizes (list[int]): A list of numbers to be sorted.
        comparisons (int): The number of comparisons made in the quick sort algorithm.
        array_accesses (int): The number of array accesses made in the quick sort algorithm.

    Yields:
        tuple: A tuple containing the current state of the list and the index of the current element being compared.
    """
    if left >= right:
        return
    
    i = left
    pivot = arr[right]

    counts['array_accesses'] += 1    
    for j in range(left, right):
        counts['comparisons'] += 1
        counts['array_accesses'] += 1
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            counts['array_accesses'] += 4
            i += 1
            yield (j, i, counts['comparisons'], counts['array_accesses'])

    counts['array_accesses'] += 4
    arr[i], arr[right] = arr[right], arr[i]

    yield from quick_sort_gen(arr, left, i - 1, counts)
    yield from quick_sort_gen(arr, i + 1, right, counts)

def merge_sort_gen(
    arr:                list[int],
    left:               int,
    right:              int,
    counts:             dict[str, int]
):
    counts['comparisons'] += 1
    if left >= right:
        return
    
    mid = (left + right) // 2

    yield from merge_sort_gen(arr, left, mid, counts)
    yield from merge_sort_gen(arr, mid + 1, right, counts)

    left_copy = arr[left:mid + 1]
    right_copy = arr[mid + 1:right + 1]
    counts['array_accesses'] += len(left_copy) + len(right_copy)

    i = j = 0
    k = left

    while i < len(left_copy) and j < len(right_copy):
        counts['comparisons'] += 1
        left_i = left + i
        right_i = mid + 1 + j

        yield left_i, right_i, counts['comparisons'], counts['array_accesses']

        counts['comparisons'] += 1
        counts['array_accesses'] += 2
        if left_copy[i] <= right_copy[j]:
            arr[k] = left_copy[i]
            counts['array_accesses'] += 2
            i += 1
        else:
            arr[k] = right_copy[j]
            counts['array_accesses'] += 2
            j += 1
        k += 1
    
    while i < len(left_copy):
        counts['comparisons'] += 1
        arr[k] = left_copy[i]
        counts['array_accesses'] += 2
        i += 1
        k += 1
    while j < len(right_copy):
        counts['comparisons'] += 1
        arr[k] = right_copy[j]
        counts['array_accesses'] += 2
        j += 1
        k += 1

def insertion_sort_gen(
    arr:                list[int],
    counts:             dict[str, int]
):
    for i in range(1, len(arr)):
        for j in range(i, 0, -1):
            counts['comparisons'] += 1
            counts['array_accesses'] += 2
            if arr[j] < arr[j - 1]:
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
                counts['array_accesses'] += 4
                yield i, j, counts['comparisons'], counts['array_accesses']
            else:
                break
