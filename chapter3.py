import time


class Password:
    next_rising_number = None  # actually it is next_non_decreasing_number

    def __init__(self, num: int):
        self.number = num
        self.int_list = self.create_int_list()

    def create_int_list(self):
        # turns int into list of ints: 123 -> [1, 2, 3]
        return [int(n) for n in list(str(self.number))]

    def is_valid(self):
        return self.is_rising() and self.has_two_clusters()

    def is_rising(self):
        # is_non_decreasing doesn't roll of the tongue quite as well
        previous_val = 0

        for i, n in enumerate(self.int_list):
            if n < previous_val:
                self.set_next_rising_number(i, previous_val)
                return False
            previous_val = n
        return True

    def set_next_rising_number(self, index, value):
        # 'calculates' next rising number (ex: 12000 -> 12222)
        str_list = [str(n) for n in self.int_list]
        for i in range(index, len(str_list)):
            str_list[i] = str(value)
        string_num = ''.join(str_list)

        self.next_rising_number = int(string_num)

    def has_two_clusters(self):
        int_list = self.int_list.copy()
        int_list.append(-1)  # 'hack' solution to force the last cluster check
        cluster_count = 0
        cluster_start_index = 0

        for i in range(1, len(int_list)):
            if int_list[i] != int_list[i-1]:
                if i - cluster_start_index > 1:
                    cluster_count += 1
                    if cluster_count > 1:
                        return True
                cluster_start_index = i
        return False


def main(start, end):
    start_time = time.time()
    counter = 0

    n = start
    while n <= end:
        password = Password(n)
        counter += 1 if password.is_valid() else 0
        if password.next_rising_number:
            n = password.next_rising_number
        else:
            n += 1

    print(f"Passwords to check: {counter}")
    print(f"Runtime: {time.time() - start_time}s")


if __name__ == "__main__":
    main(372**2, 809**2)
