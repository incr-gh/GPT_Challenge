CONVERT_FILE1=r"D:\Projects\AMIC AI Challenge\AI_CHALLENGE_sample\results\one_shot.txt"
CONVERT_FILE2=r"D:\Projects\AMIC AI Challenge\AI_CHALLENGE_sample\results\one_shot_fix.txt"
TO= r"D:\Projects\AMIC AI Challenge\AI_CHALLENGE_sample\results\results.txt"

di= dict()
with open(CONVERT_FILE1, 'r') as f:
    ls=list(map(lambda x: x.split(), f.readlines()))
with open(CONVERT_FILE2,'r') as f:
    ls1=list(map(lambda x: x.split(), f.readlines()))

for i in ls:
    di[int(i[0])]= f"{i[1]}\t{i[2]}"
for i in ls1:
    di[int(i[0])]= f"{i[1]}\t{i[2]}"
res=''
for k in sorted(di.keys()):
    res += di[k] +'\n'

with open(TO,'w') as f:
    f.write(res)
