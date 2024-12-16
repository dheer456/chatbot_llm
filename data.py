from pymongo import MongoClient
from datetime import datetime

def get_company_info(input_text: str) -> str:
    """Get information about a company from MongoDB database"""
    try:
        # MongoDB connection
        client = MongoClient('mongodb://username:password@your-host:27017/your-database')
        db = client['company_database']
        collection = db['company_info']

        # Clean and format input
        company_name = input_text.strip().lower()

        # Query the database
        query = {
            'company_name': company_name,
            'status': 'active'  # Assuming we only want active companies
        }

        # Find company information
        company_data = collection.find_one(query)

        if company_data:
            # Format the response
            response = f"""
Company: {company_data.get('company_name', '').title()}
Industry: {company_data.get('industry', 'N/A')}
Description: {company_data.get('description', 'No description available')}
Founded: {company_data.get('founded_year', 'N/A')}
Services: {', '.join(company_data.get('services', []))}
            """
            return response.strip()
        else:
            return "Company information not found in our database."

    except Exception as e:
        print(f"Database error: {str(e)}")
        return "Sorry, there was an error accessing the company information."
    
    finally:
        client.close()
