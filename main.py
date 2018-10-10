from simpleai.search import astar, SearchProblem

# Membuat kelas Astar solver
class PuzzleSolver(SearchProblem):
    # Membuat fungsi untuk mencari kemungkinan" ketika ada slot yang kosong
    def actions(self, cur_state):
        rows = string_to_list(cur_state)
        row_empty, col_empty = get_location(rows, 'x')

        actions = []
        if row_empty > 0:
            actions.append(rows[row_empty - 1][col_empty])
        if row_empty < 2:
            actions.append(rows[row_empty + 1][col_empty])
        if col_empty > 0:
            actions.append(rows[row_empty][col_empty - 1])
        if col_empty < 2:
            actions.append(rows[row_empty][col_empty + 1])

        return actions

    # Mengembalikan hasil setelah terjadi perpindahan untuk mengisi slot yang kosong
    def result(self, state, action):
        rows = string_to_list(state)
        row_empty, col_empty = get_location(rows, 'x')
        row_new, col_new = get_location(rows, action)

        rows[row_empty][col_empty], rows[row_new][col_new] = \
                rows[row_new][col_new], rows[row_empty][col_empty]

        return list_to_string(rows)

    # Proses berhenti jika urutan angka tercapai
    def is_goal(self, state):
        return state == puzzle_sorted

    # Mengestimasi jarak dengan menggunakan metode heuristik manhattan distance
    def manhattan(self, state):
        rows = string_to_list(state)
        distance = 0

        for number in '12345678x':
            row_new, col_new = get_location(rows, number)
            row_new_goal, col_new_goal = goal_positions[number]

            distance += abs(row_new - row_new_goal) + abs(col_new - col_new_goal)

        return distance

# merubah list menjadi string
def list_to_string(input_list):
    return '\n'.join(['-'.join(x) for x in input_list])

# merubah string menjadi list
def string_to_list(input_string):
    return [x.split('-') for x in input_string.split('\n')]

# Mencari lokasi input elemen
def get_location(rows, input_element):
    for i, row in enumerate(rows):
        for j, item in enumerate(row):
            if item == input_element:
                return i, j  

# Hasil yang ingin dicapai
puzzle_sorted = '''1-2-3
4-5-6
7-8-x'''

# Letak awal
initial_space = '''1-2-x
6-3-4
7-5-8'''

# Menyimpan posisi hasil yang ingin dicapai
goal_positions = {}
rows_goal = string_to_list(puzzle_sorted)
for number in '12345678x':
    goal_positions[number] = get_location(rows_goal, number)

# Create the solver object
result = astar(PuzzleSolver(initial_space))

# Mencetak hasil
for i, (action, state) in enumerate(result.path()):
    print()
    if action == None:
        print('Letak awal')
    else:
        print('Memindahkan ', action, ' ke kotak kosong')

    print(state)
