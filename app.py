# app.py
import gspread
import openai
import flask
from flask import Flask, request, jsonify
from model import db, RequestData, RequestData2
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # Use SQLite database, change this to your preferred database
db.init_app(app)
app.secret_key = '2e080bda326637fc0ef1e42efc87887c1026ebbd2e315958408e64f8981a05'

openai.api_key = "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"

@app.route('/', methods=['POST'])
def mainpath():
    # Get the JSON data from the Dialogflow request
    data = request.get_json()
    # Extract the 'intent' from the request data
    intent = data['queryResult']['intent']['displayName']
    if intent == "Beiginning":
        return flask.redirect('/dialog', code=307)
    elif intent == "alternative":
        return flask.redirect('/alternative', code=307)
    # elif intent == "open_ai_response":
    #     return flask.redirect('/open_ai_response', code=307)
    # elif intent == "open_ai_response2 ":
    #     return flask.redirect('/open_ai_response', code=307)
    else:
        return jsonify({"fulfillmentText": "Invalid intent. Please try again."})

@app.route('/dialog', methods=['POST'])
def mainpaths():
    data = request.get_json()

    topography = data['queryResult']['parameters'].get('topography')
    vegetation = data['queryResult']['parameters'].get('vegetation')
    gfeatures = data['queryResult']['parameters'].get('gfeatures')
    climate = data['queryResult']['parameters'].get('climate')
    wildlife = data['queryResult']['parameters'].get('wildlife')
    building = data['queryResult']['parameters'].get('building')
    scent = data['queryResult']['parameters'].get('scent')
    bodies = data['queryResult']['parameters'].get('bodies')
    terrain = data['queryResult']['parameters'].get('terrain')

    row_count = RequestData2.query.count()
    random_id = random.randint(1, row_count)
    random_row = RequestData2.query.filter_by(id=random_id).first()
    target1 = random_row.target1
    target2 = random_row.target2
    print(target1,target2)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.5,
        max_tokens=70,
        top_p=1.0,
        frequency_penalty=0.8,
        presence_penalty=0.0,
        messages=[
            {
                "role": "system",
                "content": f"You are a remote viewing assistant. Give which location {target1} and {target2} based on the given parameters: topography - {topography}, vegetation - {vegetation}, climate - {climate}, wildlife - {wildlife}. Choose the location that best fits the provided criteria. When saying the answer, say it like this: The location1 (%percentage) and location2 (%percentage)."

            },
            {
                "role": "user",
                "content": f"Topography: {topography}, Climate: {climate}, Vegetation: {vegetation}, Wildlife: {wildlife}"
            }
        ]
    )
    responses = response['choices'][0]['message']['content']


    if topography is not None and terrain is not None :
        # Find the existing row in the database
        request_data = RequestData(topography=topography, responses=responses, vegetation=vegetation, gfeatures=gfeatures, wildlife=wildlife, climate=climate, building=building, scent=scent, bodies=bodies, terrain=terrain )
        db.session.add(request_data)
        db.session.commit()

        return flask.redirect('/alternative', code=307)
    return jsonify({"fulfillmentText": "Please provide attendees and date first."})



@app.route('/alternative', methods=['POST'])
def mainpathss():
    data = RequestData.query.order_by(RequestData.id.desc()).first()
    assistant_response = data.responses
    gc = gspread.service_account(filename="credentials.json")

    sheet = gc.open("Remote_bot")

    worksheet = sheet.worksheet("Sheet1")

    data_to_append = [data.topography, data.vegetation, data.gfeatures, data.climate, data.wildlife, data.building,
                      data.scent, data.bodies, data.terrain, assistant_response]
    worksheet.append_row(data_to_append)
    print("data_updated")

    return jsonify({"fulfillmentText": assistant_response})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='localhost', port=8080)
