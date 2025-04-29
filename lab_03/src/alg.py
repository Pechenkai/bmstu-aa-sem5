def search_linear(arr, elem):
    length = len(arr)

    if length == 0:
        return -1, 0

    cmp = 0

    for i in range(length):
        cmp += 1

        if arr[i] == elem:
            return i, cmp

    return -1, cmp


def search_binary(arr, elem):
    length = len(arr)

    if length == 0:
        return -1, 0

    cmp = 0
    left = 0
    right = len(arr) - 1
    while left <= right:
        cmp += 1
        mid = (left + right) // 2

        if arr[mid] == elem:
            return mid, cmp
        elif arr[mid] < elem:
            left = mid + 1
        else:
            right = mid - 1

    return -1, cmp


if __name__ == '__main__':
    arr = [1, 2, 3, 4]
    print(search_binary(arr, 1))
