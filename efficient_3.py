import time
import sys
import psutil

delta=30
alpha_table={
        ("A", "C"): 110, ("A", "G"): 48, ("A", "T"): 94, ("A", "A"): 0,
        ("C", "A"): 110, ("G", "A"): 48, ("T", "A"): 94,
        ("C", "G"): 118, ("C", "T"): 48, ("C", "C"): 0,
        ("G", "C"): 118, ("T", "C"): 48,
        ("G", "T"): 110, ("G", "G"): 0,
        ("T", "G"): 110, ("T", "T"): 0,
}

def string_generator(steps,original_string):
    result=original_string
    for index in steps:
        result=result[:index+1]+result+result[index+1:]
    return result


def basic_alignment(s0, t0, delta, alpha_table):
        m = len(s0)
        n = len(t0)

        OPT = [[0] * (n + 1) for i in range(m + 1)]

        for i in range(1, m + 1):
            OPT[i][0] = i * delta
        for j in range(0, n + 1):
            OPT[0][j] = j * delta

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                OPT[i][j] = min(OPT[i - 1][j - 1] + alpha_table[(s0[i - 1] , t0[j - 1])],OPT[i][j - 1] + delta, OPT[i - 1][j] + delta)

        i, j = m, n

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

        # print(new_s0)
        # print(new_t0)
        new_s0.reverse()
        new_t0.reverse()

        return ''.join(new_s0), ''.join(new_t0), OPT[m][n]

def helper_div_conquer(X, Y,delta,alpha_table):
    prev = []
    for i in range(len(Y) + 1):
        prev.append(i*delta)

    for x in X:
        current = [prev[0] + delta]
        for j in range(1, len(Y) + 1):
            current.append(min(
                current[j - 1] + delta,  # Insertion
                prev[j] + delta,  # Deletion
                prev[j - 1] + alpha_table[(x, Y[j - 1])]  # Match/Mismatch
            ))
        prev = current
    return prev
#def helper_div_conquer(X, Y,delta,alpha_table):
    #m=len(X)
    #n=len(Y)
    #prev = []

    #for i in range(m + 1):
        #prev.append([0] * (n + 1))
    #for j in range(n + 1):
        #prev[0][j] = j * delta

    #for i in range(1,m+1):
        #prev[i][0] = prev[i-1][0] + delta
        #for j in range(1, n + 1):
            #prev[i][j] = min(prev[i - 1][j - 1] + alpha_table[(X[i - 1] ,Y[j - 1])],prev[i][j - 1] + delta,prev[i - 1][j] + delta)
        #prev[i - 1] = []
    #return prev[m]


def div_and_conquer_sol(s0, t0,delta,alpha_table):
        m = len(s0)
        n = len(t0)
        if m < 2 or n < 2:
            return basic_alignment(s0, t0,delta,alpha_table)
        else:
            mid=m//2
            left_cost = helper_div_conquer(s0[:mid], t0, delta, alpha_table)
            right_cost = helper_div_conquer(s0[mid:][::-1], t0[::-1],delta, alpha_table)


            min_cost = float('inf')
            split_point = 0
            for i in range(len(left_cost)):
                cost = left_cost[i] + right_cost[len(t0) - i]
                if cost < min_cost:
                    min_cost = cost
                    split_point = i

            left_part = div_and_conquer_sol(s0[:mid], t0[:split_point],delta,alpha_table)
            right_part = div_and_conquer_sol(s0[mid:], t0[split_point:],delta,alpha_table)

        return [left_part[i] + right_part[i] for i in range(3)]



if len(sys.argv) !=3:
    print("Error: Please provide the correct files")
    sys.exit(1)

input_file=sys.argv[1]
output_file=sys.argv[2]

with open(input_file,'r') as file:
    input_data = file.readlines()

s0=input_data[0].strip()
#print(s0)
s0_steps=[]
i=1
while i< len(input_data) and input_data[i].strip().isdigit():
    s0_steps.append(int(input_data[i].strip()))
    i += 1
#print(s0_steps)

t0=input_data[i].strip()
t0_steps=list(map(int, (line.strip() for line in input_data[i+1:] if line.strip().isdigit())))
#print(t0)
#print(t0_steps)

generated_s0 = string_generator(s0_steps, s0)
generated_t0 = string_generator(t0_steps, t0)
#print(generated_s0)
#print(generated_t0)
# Run the memory efficient recursive alignment

start_time=time.time()
aligned_s0, aligned_t0, minimum_cost = div_and_conquer_sol(generated_s0, generated_t0,delta,alpha_table)
end_time=time.time()
process = psutil.Process()
memory_info = process.memory_info()
total_memory=int(memory_info.rss / 1024)
final_time=(end_time-start_time)*1000
# Write output to file
with open(output_file, 'w') as file:
    file.write(f"The minimum cost is: {minimum_cost}\n")
    file.write(f"After aligning s0: {aligned_s0}\n")
    file.write(f"After aligning t0: {aligned_t0}\n")
    file.write(f"The total time is: {final_time}\n")
    file.write(f"The total memory is: {total_memory}\n")


