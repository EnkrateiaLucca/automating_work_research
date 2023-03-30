import os
import PyPDF2
import re
import openai
import os
import argparse

def create_and_pattern(keywords):
    # Escape special characters in keywords
    keywords = [re.escape(keyword) for keyword in keywords]
    # Join keywords with a positive lookahead and wildcard
    pattern = "(?=.*" + ")(?=.*".join(keywords) + ")"
    return pattern


if __name__=="__main__":
    if not os.path.exists("./paper_summaries"):
        os.mkdir("./paper_summaries")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", type=str, default=None,
                        help="Prompt ChatGPT to do something with these pdfs")
    parser.add_argument("-path", type=str, default=None,
                        help="Folder with pdfs")
    args = parser.parse_args()
    
    openai.api_key = os.environ["OPENAI_API_KEY"]
    
    if args.s!=None:
        pdfs_action_prompt = args.s
        folder = args.path
        for filename in os.listdir(folder):
            if filename.endswith('.pdf'):
                summaries = []
                # Open the PDF file
                pdf_file = open(os.path.join(folder, filename), 'rb')

                # Read the PDF file using PyPDF2
                pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Loop through all the pages in the PDF file
            for page_num in range(len(pdf_reader.pages[:20])):
                # Extract the text from the page
                page_text = pdf_reader.pages[page_num].extract_text().lower()
                response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "system", "content": "You are a helpful research assistant."},
                        {"role": "user", "content": f"{pdfs_action_prompt}: {page_text}"},
                    ]
                )
                page_summary = response["choices"][0]["message"]["content"]
                print(page_summary)
                summaries.append(f"Summary for page {page_num}: {page_summary}")
                summaries.append("*******")
            
            summary = " ".join(summaries)
            with open(f"./paper_summaries/{filename}_summary.txt", "w+") as file:
                file.write(summary)
            
            print(f"Summary for: {filename}")   
            print(summary)
            print("*******************")
            
            
            
                
                
            
            
            
            
            
            

                



