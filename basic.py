import numpy as np
import sys
import time
import psutil
import os

delta = 30
alpha_table = {
    ("A", "C"): 110, ("A", "G"): 48, ("A", "T"): 94, ("A", "A"): 0,
    ("C", "A"): 110, ("G", "A"): 48, ("T", "A"): 94,
    ("C", "G"): 118, ("C", "T"): 48, ("C", "C"): 0,
    ("G", "C"): 118, ("T", "C"): 48,
    ("G", "T"): 110, ("G", "G"): 0,
    ("T", "G"): 110, ("T", "T"): 0,
}


def string_generator(steps, original_string):
    result = original_string
    for index in steps:
        result = result[:index + 1] + result + result[index + 1:]
    return result;


def cal_cost_basic_sequence_alignment(s0, t0, delta, alpha_table, OPT):
    s0_len = len(s0);
    t0_len = len(t0);

    for i in range(1, s0_len + 1):
        OPT[i][0] = i * delta
    for j in range(1, t0_len + 1):
        OPT[0][j] = j * delta

    for i in range(1, s0_len + 1):
        for j in range(1, t0_len + 1):
            mismatch_penalty = OPT[i - 1][j - 1] + alpha_table[(s0[i - 1], t0[j - 1])]
            gap_match_s0 = OPT[i - 1][j] + delta
            gap_match_t0 = OPT[i][j - 1] + delta
            OPT[i][j] = min(mismatch_penalty, gap_match_s0, gap_match_t0)

    total_penalty = OPT[s0_len][t0_len]
    return total_penalty, OPT


def get_memory():
    memory_info = psutil.Process().memory_info()
    return int(memory_info.rss / 1024)  # KB


def show_result_alignment_sequence(OPT, s0, t0):
    i = len(s0)
    j = len(t0)

    new_s0 = []
    new_t0 = []

    while i > 0 or j > 0:
        if i > 0 and OPT[i][j] == OPT[i - 1][j] + delta:
            new_s0.append(s0[i - 1])
            new_t0.append('_')
            i -= 1
        elif j > 0 and OPT[i][j] == OPT[i][j - 1] + delta:
            new_s0.append('_')
            new_t0.append(t0[j - 1])
            j -= 1
        else:
            new_s0.append(s0[i - 1])
            new_t0.append(t0[j - 1])
            i -= 1
            j -= 1

    new_s0.reverse()
    new_t0.reverse()

    return new_s0, new_t0


if len(sys.argv) != 2:  # Updated condition to check for correct number of arguments
    print("Error: Please provide the correct folder path")
    sys.exit(1)

folder_path = sys.argv[1]  # Updated variable name to folder_path

# Traverse the directory and process each file
for file_name in os.listdir(folder_path):
    if "output" not in file_name and file_name.endswith(".txt"):
        input_file = os.path.join(folder_path, file_name)  # Updated input_file path

        with open(input_file, 'r') as file:
            input_data = file.readlines()

        s0 = input_data[0].strip()
        s0_steps = []
        i = 1
        while i < len(input_data) and input_data[i].strip().isdigit():
            s0_steps.append(int(input_data[i].strip()))
            i += 1

    t0 = input_data[i].strip()
    t0_steps = list(map(int, (line.strip() for line in input_data[i + 1:] if line.strip().isdigit())))

    generated_s0 = string_generator(s0_steps, s0)
    generated_t0 = string_generator(t0_steps, t0)

    len1 = len(generated_s0)
    len2 = len(generated_t0)
    OPT = np.zeros((len1 + 1, len2 + 1))
    start = time.time()
    minimum_cost, filled_OPT = cal_cost_basic_sequence_alignment(generated_s0, generated_t0, delta, alpha_table, OPT)
    total_memory = get_memory()
    end = time.time()
    total_time = (end - start) * 1000

    aligned_s0, aligned_t0 = show_result_alignment_sequence(filled_OPT, generated_s0, generated_t0)

    with open(os.path.join(f"{input_file}_output.txt"), 'w') as file:
        file.write(f"Input file: {input_file}\n")
        file.write(f"After aligning s0: {aligned_s0}\n")
        file.write(f"After aligning t0: {aligned_t0}\n")
        file.write(f"The minimum cost is: {minimum_cost}\n")
        file.write(f"Total time: {str(float('{:.4f}'.format(total_time)))} ms\n")
        file.write(f"Total memory: {str(float(total_memory))} KB\n\n")
