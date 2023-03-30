import os
import PyPDF2
import re
import openai
import os

# Define the folder containing the PDF files
folder = './pdfs/'
# Check if there is a folder called pdfs and creates in case there isnt', does the same for "paper_extracts" and "snippet_summaries"
if not os.path.exists("./paper_extracts"):
    os.makedirs("./paper_extracts")
if not os.path.exists("./snippet_summaries"):
    os.makedirs("./snippet_summaries")

# Define the list of keywords to search for
keywords = input("Input keywords (separate them with ',')")

option = input("Use them together or individually? (t/i)")

search_name = keywords
print("Keywords chosen")
print(keywords.split(","))
keywords = keywords.split(",")


def create_and_pattern(keywords):
    # Escape special characters in keywords
    keywords = [re.escape(keyword) for keyword in keywords]
    # Join keywords with a positive lookahead and wildcard
    pattern = "(?=.*" + ")(?=.*".join(keywords) + ")"
    return pattern

# Loop through all the PDF files in the folder
i=0
for filename in os.listdir(folder):
    if filename.endswith('.pdf'):
        # Open the PDF file
        pdf_file = open(os.path.join(folder, filename), 'rb')

        # Read the PDF file using PyPDF2
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Loop through all the pages in the PDF file
        for page_num in range(len(pdf_reader.pages)):
            # Extract the text from the page
            page_text = pdf_reader.pages[page_num].extract_text().lower()

            # Split the text into paragraphs
            paragraphs = page_text.split('\n\n')

            # Loop through all the paragraphs
            for paragraph in paragraphs:
                # Check if any of the keywords appear in the paragraph
                if option=="t":
                    pattern = create_and_pattern(keywords)
                    if re.search(pattern, paragraph, re.IGNORECASE):
                        # If a keyword is found, print the matching paragraph
                        print(f'Found "{pattern}" in {filename}, page {page_num+1}, paragraph:')
                        with open(f"./paper_extracts/{pattern}_{i}.txt", "w+") as file:
                            file.write(paragraph)
                        i+=1
                else:
                    for keyword in keywords:
                        if re.search(keyword, paragraph, re.IGNORECASE):
                            # If a keyword is found, print the matching paragraph
                            print(f'Found "{keyword}" in {filename}, page {page_num+1}, paragraph:')
                            with open(f"./paper_extracts/{keyword}_{i}.txt", "w+") as file:
                                file.write(paragraph)
                            i+=1
                

# Variables
openai.api_key = os.environ["OPENAI_API_KEY"]
# Set the GPT-3 model
input_prompt= input("Input the prompt to apply to all the extracts")
model_engine = "text-davinci-003"
def summarize_file(transcription):
    # Summarize the transcription using GPT-3
    response = openai.Completion.create(
    model=model_engine,
    prompt=f"{input_prompt}" + transcription,
    temperature=0,
    max_tokens=256,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
    )
    
    return response["choices"][0]["text"]

folder = "./paper_extracts/"
for i,filename in enumerate(os.listdir(folder)):
    if filename.endswith('.txt'):
        # Open the extract .txt file
        paper_file = os.path.join(folder, filename)
        print(paper_file)
        with open(f"{paper_file}", "r") as f:
            transcription = f.read()
        # Print the summary
        try:
            summary = summarize_file(transcription)
        except:
            print("transcription too long")
        print(summary)
        print('*************************')
        with open(f"./snippet_summaries/summary_{search_name}{i}.txt", "a+") as file:
            file.write(summary)