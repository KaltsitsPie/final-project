import numpy as np
import sys

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
    return result;

#use the bottom-up method to calculate the minimum total cost of alignment between two sequence
def cal_cost_basic_sequence_alignment(s0,t0,delta,alpha_table,OPT):
    s0_len=len(s0);
    t0_len=len(t0);

    #initialization
    #OPT=np.zeros((s0_len,t0_len))

    #basic cases
    for i in range(1, s0_len+1):
        OPT[i][0] = i*delta
    for j in range(1, t0_len+1):
        OPT[0][j] = j*delta

    #fill the dynamic table
    for i in range(1, s0_len+1):
        for j in range(1, t0_len+1):
            mismatch_penalty=OPT[i-1][j-1]+alpha_table[(s0[i-1],t0[j-1])]
            gap_match_s0=OPT[i-1][j]+delta
            gap_match_t0=OPT[i][j-1]+delta
            OPT[i][j]=min(mismatch_penalty,gap_match_s0,gap_match_t0)

    total_penalty=OPT[s0_len][t0_len]
    return total_penalty, OPT

#use top-down method to find the final result of two sequence after alignment
def show_result_alignment_sequence(OPT,s0,t0):
    i=len(s0)
    j=len(t0)

    new_s0=[]
    new_t0=[]

    while i>0 or j>0:
        if i>0 and OPT[i][j] == OPT[i-1][j] + delta:
            new_s0.append(s0[i-1])
            new_t0.append('_')
            i -= 1
        elif j>0 and OPT[i][j] == OPT[i][j-1] + delta:
            new_s0.append('_')
            new_t0.append(t0[j-1])
            j -= 1
        else:
            new_s0.append(s0[i-1])
            new_t0.append(t0[j-1])
            i -= 1
            j -= 1

    #print(new_s0)
    #print(new_t0)
    new_s0.reverse()
    new_t0.reverse()
    #print(new_s0)
    #print(new_t0)

    return new_s0, new_t0

if len(sys.argv) !=3:
    print("Error: Please provide the correct files")
    sys.exit(1)

input_file=sys.argv[1]
output_file=sys.argv[2]

with open(input_file,'r') as file:
    input_data = file.readlines()

s0=input_data[0].strip()
s0_steps=[]
i=1
while i< len(input_data) and input_data[i].strip().isdigit():
    s0_steps.append(int(input_data[i].strip()))
    i += 1

t0=input_data[i].strip()
t0_steps=list(map(int, (line.strip() for line in input_data[i+1:] if line.strip().isdigit())))


generated_s0=string_generator(s0_steps,s0)
generated_t0=string_generator(t0_steps,t0)
print(generated_s0)
print(generated_t0)

len1=len(generated_s0)
len2=len(generated_t0)
OPT=np.zeros((len1+1,len2+1))
minimum_cost,filled_OPT=cal_cost_basic_sequence_alignment(generated_s0,generated_t0,delta,alpha_table,OPT)
print(OPT)

aligned_s0, aligned_t0=show_result_alignment_sequence(filled_OPT,generated_s0,generated_t0)

with open(output_file,'w') as file:
    file.write(f"After aligning s0: {aligned_s0}\n")
    file.write(f"After aligning t0: {aligned_t0}\n")
    file.write(f"The minimum cost is: {minimum_cost}\n")










