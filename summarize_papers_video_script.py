# Define the folder containing the PDF files
folder = './pdfs/'

def summarize_papers(folder):
    for filename in os.listdir(folder):
        pdf_summary_text = ""
        if filename.endswith('.pdf'):
            # Open the PDF file
            pdf_file = open(os.path.join(folder, filename), 'rb')

            # Read the PDF file using PyPDF2
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Loop through all the pages in the PDF file
            for page_num in range(len(pdf_reader.pages)):
                # Extract the text from the page
                page_text = pdf_reader.pages[page_num].extract_text().lower()
                
                response = openai.ChatCompletion.create(
                                model="gpt-3.5-turbo",
                                messages=[
                                    {"role": "system", "content": "You are a helpful research assistant."},
                                    {"role": "user", "content": f"Summarize this: {page_text}"},
                                        ],
                                            )

                page_summary = response["choices"][0]["message"]["content"]
                
                pdf_summary_text+=page_summary + "\n"
                new_filename = filename.replace(os.path.splitext(filename)[1], "_summary.txt")
                with open(new_filename, "w+") as file:
                    file.write(pdf_summary_text)
            
            pdf_file.close()
            