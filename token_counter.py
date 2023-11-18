from dataset import get_data
problems= get_data(r'D:\Projects\AMIC AI Challenge\public_data_round_1_wtest\test\all_test_round1.json')
TOKENS_PROBLEM=0
TOKENS_TITLE=0
TOKENS_RATIONALE=0
TOKENS_DIAGRAMS=0
TOKENS_OPTIONS=0
TOKENS_ANSWER=0
def count(problem):
    global TOKENS_DIAGRAMS
    global TOKENS_PROBLEM
    global TOKENS_TITLE
    global TOKENS_RATIONALE
    global TOKENS_OPTIONS
    global TOKENS_ANSWER
    TOKENS_DIAGRAMS += (problem['diagramRef']!='')
    TOKENS_TITLE += len(problem['category'].split())
    TOKENS_PROBLEM += len(problem['Problem'].split())
    #TOKENS_RATIONALE += len(problem['Rationale'].split())
    #TOKENS_ANSWER += len(problem['correct'])
    TOKENS_OPTIONS += len(problem['options'].split())
for problem in problems:
    count(problem)
print(f'Problems: {TOKENS_PROBLEM}')
print(f'Rationale: {TOKENS_RATIONALE}')
print(f'Options: {TOKENS_OPTIONS}')
print(f'Title: {TOKENS_TITLE}')
print(f'Diagrams: {TOKENS_DIAGRAMS}')
print(f'Correct: {TOKENS_ANSWER}')
print(f'Tokens: {TOKENS_OPTIONS+ TOKENS_PROBLEM + TOKENS_RATIONALE + TOKENS_TITLE + TOKENS_ANSWER}')