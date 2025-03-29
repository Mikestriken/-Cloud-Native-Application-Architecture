import json
import google.generativeai as genai

if __name__ == "__main__":
    with open('api_key.json', 'r') as file:
        api_json_data = json.load(file)
        
    API_KEY = api_json_data.get("key")
    
    genai.configure(api_key=API_KEY)
    data = {
        "products": [
        {"name": "Laptop", "price": 1200, "quantity": 10},
        {"name": "Mouse", "price": 25, "quantity": 50},
        {"name": "Keyboard", "price": 75, "quantity": 20}
        ]
    }
    
    prompt = f"""
    You are a helpful assistant analyzing inventory data for a small
    electronics store.
    1. For each product, compute the **total value in stock** (price ×
    quantity).
    2. Include a **short human-friendly explanation** for each product's
    value.
    3. Provide a **grand total** value of all products combined.
    4. Return a JSON object with:
    - "product_summaries": a list of dictionaries, each containing:
    - "name"
    - "total_value"
    - "explanation"
    - "total_value": the combined value of all products.
    Here is the data:
    {json.dumps(data, indent=2)}
    """
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    print(response.text)