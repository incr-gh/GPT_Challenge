import requests
import openai
import argparse
import time
import re
import base64
import os
from json import dumps
from dataset import get_data
from itertools import chain

with open(r"D:\Projects\AMIC AI Challenge\AI_CHALLENGE_sample\openai_api_key.txt", "r") as f:
    KEY = f.readline()

CLIENT = openai.OpenAI(api_key=KEY)
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {KEY}"
}

CONST_PROMPT = "Choose the correct option to the following question. Let\'s think step by step:"
DIAGRAMS_PATH = r"D:\Projects\AMIC AI Challenge\diagrams"


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def send_request(prompt, ref_image=None, image_paths=[], temperature=0.2):
    base64_images = []

    if len(image_paths) != 0:
        base64_images = list(map(encode_image, image_paths))

    content = [
        {
            "type": "text",
            "text": prompt
        }]

    if ref_image:
        content[0]['text'] += ' Use the following image as a guide.'
        content += [{"type": "image_url",
                     "image-url": {
                         "url": f"data:image/jpeg;base64,{encode_image(ref_image)}",
                         'detail': 'low'
                     }}]
    content += chain(*[[
        {
            "type": "text",
            "text": f"Image No. {i+1}"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_images[i]}",
                'detail': 'low'
            }
        }] for i in range(len(base64_images))])

    payload = {
        "model": "gpt-3.5-turbo-1106" if len(base64_images) == 0 else "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "max_tokens": 1500,
        "temperature": temperature
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=HEADERS, json=payload, timeout=10).json()
    # print(content)
    return response


def get_ans_MCQ(text):
    # print(text)
    try:
        ans = re.findall('([abcdeABCDE])(?=( *\)))', text)[-1][0]
    except:
        ans = 'FAILED'
    return ans

def get_ans_WR(text):
    try:
        ans=re.findall('Answer:.*?([+-]?[0-9,]+\.?[0-9]*\/?[0-9]*)',text)[-1]
    except: 
        try:
            ans= re.findall('([+-]?[0-9,]+\.?[0-9]*\/?[0-9]*)', text)[-1]
        except:
            ans="FAILED"
    return ans




def get_images(text):
    # print(re.findall('([a-z]+).png', text))
    # print(re.sub('([a-z]+.png)', 'IMAGE', text))
    return (re.findall('([a-z0-9]+).png', text), re.sub('([a-z0-9]+.png)', 'IMAGE', text))


def get_one_shot(category):
    if category == 'general':
        return '''when a positive integer x is divided by another positive integer y , the remainder is 6 . if x / y = 6.12 , what is the value of y ? 
Options: a ) 96 , b ) 75 , c ) 50 , d ) 25 , e ) 12
Because x divided by y has a remainder of 6, (x-6)/y=6 and x/y=6.12. x-6=6y and x=6.12y. so 6.12y-6=6y. 0.12y-6=0. y=6/0.12. y=50. So c) 50.'''

    elif category == 'gain':
        return '''a watch was sold at a loss of 16 % . if it was sold for rs . 140 more , there would have been a gain of 4 % . what is the cost price ?
Options: a ) 700 , b ) 882 , c ) 799 , d ) 778 , e ) 901
p is the price of the watch. The selling price is 0.84p. 0.84p + 140 = 1.04p. 0.2p =140. p= 140/0.5. p=700. So a) 700.'''

    elif category == 'physics':
        return '''in a kilometer race , a beats b by 54 meters or 12 seconds . what time does a take to complete the race ?
Options: a ) 212 , b ) 190 , c ) 277 , d ) 181 , e )
122 time taken by b to run 1000 meters = ( 1000 * 12 ) / 54 = 222 sec . time taken by a = 224 - 12 = 212 sec . answer : a)'''

    elif category == 'geometry':
        return '''the area of sector of a circle whose radius is 18 metro and whose angle at the center is 42 \u00b0 is ?
Options: a ) 52.6 , b ) 52.9 , c ) 52.8 , d ) 118.8 , e ) 52.2
42 / 360 * 22 / 7 * 18 * 18 = 118.8 m 2 answer : d)'''

    elif category == 'other':
        return '''three numbers are in the ratio of 2 : 3 : 4 and their l . c . m . is 180 . what is their h . c . f . ?
Options: a ) 15 , b ) 20 , c ) 40 , d ) 60 , e ) 70
let the numbers be 2 x , 3 x , and 4 x . lcm of 2 x , 3 x and 4 x is 12 x . 12 x = 180 x = 15 hcf of 2 x , 3 x and 4 x = x = 15 the answer is a) .'''

    elif category == 'probability':
        return '''a bag contains 6 black and 3 white balls . one ball is drawn at random . what is the probability that the ball drawn is white ?
Options: a ) 3 / 4 , b ) 1 / 3 , c ) 1 / 7 , d ) 1 / 8 , e ) 4 / 3
let number of balls = ( 6 + 3 ) = 9 . number of white balls = 3 . p ( drawing a white ball ) = 3 / 9 = 1 / 3 . option b) .'''

    elif category == 'closed':
        return '''If the sum of the consecutive integers from \\(-15\\) to x, inclusive, is 51, what is the value of x ?
Options: a)15 , b)16 , c)18 , d)53 , e)66
The sum -15 + -14 + ... + 14 + 15 =0. So 16 + ... + x = 51. x= 51-16-17= 18. So x=18. The answer is c)'''
    elif category == 'WR':
        return '''Write the final line of the answer in the format "Answer: 50" or "Answer: 100" after thinking step by step.'''
    else:
        return '''the area of sector of a circle whose radius is 18 metro and whose angle at the center is 42 \u00b0 is ?
Options: a ) 52.6 , b ) 52.9 , c ) 52.8 , d ) 118.8 , e ) 52.2
42 / 360 * 22 / 7 * 18 * 18 = 118.8. So the answer is d)'''


CURRENT = 0
#frac {x} {y}
def frac_removal(text):
    ls= re.findall(r'frac *\{ *(.+?) *\} *\{ *(.+?) *\}', text)
    #print(ls)
    for x, y in ls:
        text= re.sub(r'frac *\{ *(.+?) *\} *\{ *(.+?) *\}', f'{re.escape(x)}/{re.escape(y)}', text, count=1)
    text=re.sub(r'\\','',text)
    return text
def main(questions):
    global CURRENT
    results = []

    for problem in questions[CURRENT:]:
        print(f"CURRENT: {CURRENT}")
        question = frac_removal(problem["Problem"])
        response = {}
        # print(get_one_shot(problem['category']))
        if problem['options']!='':
            prompt = CONST_PROMPT + '\n' + \
            get_one_shot(problem['category']) + '\n' + CONST_PROMPT + '\n'
        else:
            prompt= CONST_PROMPT + '\n' + \
            get_one_shot('WR') + '\n' +CONST_PROMPT +'\n'
        image_links, new_options = get_images(problem['options'])
        image_links = list(map(lambda x: os.path.join(
            DIAGRAMS_PATH, x+'.png'), image_links))
        diagram = None
        if problem['diagramRef'] != '':
            diagram = os.path.join(DIAGRAMS_PATH, problem['diagramRef'])

        
        prompt += question + '\n'
        if problem['options']!='':
            for i in range(len(image_links)):
                new_options = new_options.replace('IMAGE', f'Image No. {i+1}', 1)
            prompt += f'Options: {new_options}'
        else:
            pass
        MAX_RETRIES=3
        failed=True
        while MAX_RETRIES>0 and failed:
            try:
                print(f'Requesting \n"{question}"')
                t1 = time.time()
                response = send_request(prompt, diagram, image_links, temperature=0.2+0.1*(3-MAX_RETRIES))
                print(response['choices'][0]['message']['content'])
                if problem['options']!='':
                    ans = get_ans_MCQ(response['choices'][0]['message']['content'])
                else:
                    ans= get_ans_WR(response['choices'][0]['message']['content'])
                print(ans)
                with open(r"D:\Projects\AMIC AI Challenge\AI_CHALLENGE_sample\results\one_shot.txt", 'a') as f:
                    f.write(f'{problem["id"]} {ans} {time.time()-t1}\n') 
                failed=False
            except:
                MAX_RETRIES-=1
            time.sleep(0.5)
            # except Exception as e:
            #    print(e)
            #    continue
        if failed:
            with open(r"D:\Projects\AMIC AI Challenge\AI_CHALLENGE_sample\results\one_shot.txt", 'a') as f:
                    f.write(f'{problem["id"]} FAILED {time.time()-t1}\n') 
        # send_request(prompt, diagram, image_links)
        # if len(image_links) != 0:
        #    print(prompt)
        #    print(image_links)
        #    print()
        #    print()
        CURRENT += 1


questions = get_data(
    r'D:\Projects\AMIC AI Challenge\public_data_round_1_wtest\test\all_test_round1.json')
main(questions)
