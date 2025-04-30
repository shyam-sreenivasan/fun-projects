from io import BytesIO

def merge_pdfs(pdf_list, output_filename):
    from PyPDF2 import PdfMerger
    # Create a PdfMerger object
    merger = PdfMerger()

    # Loop over each uploaded PDF file
    for pdf_file in pdf_list:
        # Read file into memory as a byte stream (PDF is uploaded as bytes)
        pdf_bytes = pdf_file.read()
        pdf_stream = BytesIO(pdf_bytes)
        merger.append(pdf_stream)
        print(f"Added PDF from: {pdf_file.filename}")
    
    # Write the merged result to a file in the temp directory or location
    with open(output_filename, "wb") as output_file:
        merger.write(output_file)
    
    merger.close()
    print(f"\nMerged PDF saved as: {output_filename}")