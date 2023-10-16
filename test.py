from flask import Flask, request, jsonify
from model import db, RequestData2  # Make sure to import the app and models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = '2e080bda326637fc0ef1e42efc87887c1026ebbd2e315958408e64f8981a05'

db.init_app(app)


@app.route('/', methods=['GET'])
def mainpath():

    target1 = 'Tower of Pisa'
    target2 = 'Nairobi Market Place'

# Create a new RequestData2 object and add it to the database session
    request_data = RequestData2(target1=target1, target2=target2)
    db.session.add(request_data)
    db.session.commit()
    return('okay')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='localhost', port=8080)
    # row_count = RequestData2.query.count()
    # random_id = random.randint(1, row_count)
    # random_row = RequestData2.query.filter_by(id=random_id).first()
    # target1 = random_row.target1
    # target2 = random_row.target2
    # data = RequestData.query.order_by(RequestData.id.desc()).first()
    #
    # topography = data.topography
    # prompt = f"Topography is {data.topography}, vegetation is {data.vegetation},scent is {data.scent},man-made building is {data.building},water-bodies is {data.bodies} climate is {data.climate}"

