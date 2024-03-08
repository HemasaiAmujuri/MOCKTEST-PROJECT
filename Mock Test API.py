from pymongo import MongoClient
from fastapi import FastAPI
from urllib.parse import quote_plus

app = FastAPI()

username = quote_plus("hemasaiamujuri3")
password = quote_plus("hemasai@123")

# Update connection string with encoded username and password
connection_string = f"mongodb+srv://{username}:{password}@questions.e2ai2cz.mongodb.net/"

# Connect to MongoDB
client = MongoClient(connection_string)

db = client['MockTestDatabase']

# Define endpoint to fetch questions based on branch and number of questions
@app.get('/questions')
def get_questions(body: dict):
    branch = str(body['branch'])
    num_questions = int(body['num_questions'])

    # Define the percentages for each category
    percentages = {
        branch: 50,
        "APTITUDE": 18,
        "REASONING": 16,
        "VERBAL": 16
    }

    # Calculate the number of questions for each category based on the percentages
    num_questions_per_category = {category: int(num_questions * (percentage / 100)) for category, percentage in percentages.items()}

    # Fetch questions from MongoDB based on the calculated number of questions for each category
    formatted_questions = {}
    for category, num_questions in num_questions_per_category.items():
        questions = list(db[category].aggregate([{'$sample': {'size': num_questions}}]))
        formatted_questions[category] = [{'id': str(q['_id']), 'question': q['question'], 'options': q['options']} for q in questions]
        
    return {'questions': formatted_questions,}

    

@app.get('/')
def home():
    return {"message": "hello world"}

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost")
