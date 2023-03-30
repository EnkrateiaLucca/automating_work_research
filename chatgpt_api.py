import os
import openai
import argparse

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", type=str, default=None,
                        help="Ask chatgpt a question")
    parser.add_argument("-c", type=str, default=None,
                        help="Talk to chatgpt about anything")
    parser.add_argument("-system", type=str, default=None,
                        help="Ask chatgpt to act as a given description")
    args = parser.parse_args()

    openai.api_key = os.environ["OPENAI_API_KEY"]

    if args.q!=None:
        prompt_question = args.q
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a helpful coding and learning assistant."},
                {"role": "user", "content": prompt_question},
            ]
        )
        print(response["choices"][0]["message"]["content"])
    
    if args.c!=None:
        prompt_question = ""
        if args.system!=None:
            system_profile = args.system
        else:
            system_profile = "You are a helpful coding and learning assistant."
        
        while prompt_question!="exit":
            prompt_question = input("Hi! What you want to know? (type exit to leave): ")
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": system_profile},
                    {"role": "user", "content": prompt_question},
                ]
            )
            print(response["choices"][0]["message"]["content"])