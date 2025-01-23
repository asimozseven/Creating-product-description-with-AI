import csv
import google.generativeai as genai
import os
import sys
import html

def generate_product_description(product_name):
    """Generate SEO-friendly product description using Google Gemini"""
    try:
        # Configure Gemini API (replace with your actual API key)
        genai.configure(api_key='AIzaSyATg1uLwEgx_uCaTuVRpY5LS-aQ2JGM7FY')

        # Initialize the model
        model = genai.GenerativeModel('gemini-pro')
        
        # Prompt for generating description
        prompt = f"{product_name} için max 300 kelimelik SEO uyumlu profesyonel bir ürün açıklaması yaz."
        
        # Generate description
        response = model.generate_content(prompt)
        
        # Escape HTML special characters
        html_description = html.escape(response.text.strip())
        
        # Wrap in HTML paragraph tags
        return f"<p>{html_description}</p>"
    
    except Exception as e:
        error_msg = html.escape(str(e))
        return f"<p>Açıklama oluşturulamadı: {error_msg}</p>"

def process_csv(input_file, output_file):
    """Process CSV file and add generated HTML-formatted descriptions"""
    try:
        # Read input CSV
        with open(input_file, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            
            # Prepare output CSV with additional column
            fieldnames = reader.fieldnames + ['Ürün Açıklaması']
            
            with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                
                # Process each row
                for row in reader:
                    product_name = row['Ürün İsmi']
                    description = generate_product_description(product_name)
                    
                    # Add HTML-formatted description to row
                    row['Ürün Açıklaması'] = description
                    writer.writerow(row)
        
        print(f"İşlem tamamlandı. Çıktı: {output_file}")
    
    except FileNotFoundError:
        print(f"Dosya bulunamadı: {input_file}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Example usage
if __name__ == "__main__":
    # Check if correct number of arguments
    if len(sys.argv) != 3:
        print("Kullanım: python script.py input.csv output.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    process_csv(input_file, output_file)
