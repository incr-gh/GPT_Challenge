CHECK_FILE= r"D:\Projects\AMIC AI Challenge\AI_CHALLENGE_sample\results\one_shot.txt"
with open(CHECK_FILE, 'r') as f:
    ls= f.readlines()
i=1
print(len(ls))
seen=set()
for j in range(len(ls)):
    if int(ls[j].split()[0]) in seen:
        print(f"Seen at {ls[j].split()[0]}")
    seen.add(int(ls[j].split()[0]))
    if i!= int(ls[j].split()[0]):
        print(f'Discreprancy at id{i}')
        i=int(ls[j].split()[0])
    i+=1


