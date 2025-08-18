import os
from bs4 import BeautifulSoup
from weasyprint import HTML, CSS

def generate_resume_pdf(html_file_path="index.html", output_filename="blake-rayvid-cv.pdf"):
    """
    Reads an HTML file, extracts the resume content and its styles,
    and generates a picture-perfect PDF with correct page breaks and margins.

    Args:
        html_file_path (str): The path to the HTML file containing the resume.
        output_filename (str): The desired name for the output PDF file.
    """
    if not os.path.exists(html_file_path):
        print(f"Error: HTML file not found at '{html_file_path}'")
        return

    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the essential components: the resume content and its styles
        resume_div = soup.find(id='resume-content')
        style_tag = soup.find('style')

        if not resume_div:
            print("Error: Could not find the element with id 'resume-content'.")
            return
        if not style_tag:
            print("Error: Could not find the <style> tag in the HTML.")
            return

        # --- CSS Configuration ---
        # 1. Define the PDF page layout. This is the most reliable way to set margins.
        #    This CSS will be applied to the page itself.
        page_layout_css = """
        @page {
            size: letter;
            margin: 0.02in;
        }
        """

        # 2. Get the original CSS from the HTML. We will use this exactly as written.
        #    Your @media print rules will be automatically applied by WeasyPrint.
        original_css = style_tag.string

        # --- HTML Preparation ---
        # We create a minimal HTML document containing ONLY the resume content.
        # WeasyPrint will render this content within the page margins we defined above.
        html_to_render = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"></head>
        <body>
            {resume_div.prettify()}
        </body>
        </html>
        """

        # --- PDF Generation ---
        # Get the base URL to help WeasyPrint find relative resources (like your custom font)
        base_url = os.path.dirname(os.path.abspath(html_file_path))

        # Create WeasyPrint objects
        html_obj = HTML(string=html_to_render, base_url=base_url)
        
        # Create separate CSS objects. This keeps layout and content styles clean.
        css_layout_obj = CSS(string=page_layout_css)
        css_content_obj = CSS(string=original_css)
        
        # Render the PDF, applying both stylesheets.
        # The page layout CSS sets up the page, and the original content CSS
        # styles the text, tables, etc., inside it.
        # Your @media print rule will set #resume-content width to 'auto',
        # which makes it fit perfectly between the page margins we defined.
        html_obj.write_pdf(
            output_filename,
            stylesheets=[css_layout_obj, css_content_obj]
        )

        print(f"Successfully generated '{output_filename}'")

    except Exception as e:
        print(f"An error occurred during PDF generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Ensure 'index.html' and any resources like 'src/bka.ttf'
    # are in the correct location relative to this script.
    generate_resume_pdf("index.html")