import os
import subprocess
import argparse

def convert_pdf_to_text(pdf_path, output_file):
    # Get the total number of pages in the PDF
    result = subprocess.run(['pdfinfo', pdf_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error getting PDF info: {result.stderr}")
        return
    
    # Extract the number of pages
    for line in result.stdout.splitlines():
        if line.startswith("Pages:"):
            total_pages = int(line.split(":")[1].strip())
            break
    else:
        print("Could not determine the number of pages.")
        return

    # Convert each page to text and append to the output file
    with open(output_file, 'w') as outfile:
        for page_num in range(1, total_pages + 1):
            result = subprocess.run(['pdftotext', '-f', str(page_num), '-l', str(page_num), pdf_path, '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                print(f"Error converting page {page_num}: {result.stderr}")
                continue
            
            outfile.write(result.stdout)
            outfile.write("\n----------\n")
            print(f"Converted page {page_num}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF to text with page separators.")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("output_file", help="Path to the output text file")
    args = parser.parse_args()

    convert_pdf_to_text(args.pdf_path, args.output_file)