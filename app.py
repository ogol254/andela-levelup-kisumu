
from flask import Flask, jsonify, request
import datetime
import jwt
from functools import wraps



app = Flask(__name__)

app.config['SECRET_KEY'] = 'mcogol'

user1 =  'abraham'
pass1  =  'abraham'


def need_token(t):
    @wraps(t)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])

        except:
            return jsonify({'message' : 'Token is invalid'}), 403

        return t(*args, **kwargs)

    return decorated



@app.route('/', methods=['POST'])
def login():
    user2 = request.get_json()['user']
    pass2 = request.get_json()['pass']
    valid = 0

    if (user2 == ""):
      status = 000000
      valid = 1
      return jsonify({'message' : 'Username cannot be blank', 'status' : status})


    if (valid == 0):
            if (user1 == str(user2)):
                if (pass1 == pass2):
                    status = 200
                    token = jwt.encode({'user' : user1, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=15)}, app.config['SECRET_KEY'])
                    return jsonify({'message' : 'Login successful', 'status' : status, 'access-token' : token.decode('UTF-8')})
                else:
                    status = 401
                    return jsonify({'message' : 'Username and password do not match', 'status' : status})

            else:
                status = 501
                return jsonify({'message' : 'No such user', 'status' : status})


#to  get the list of friends

friends = [{'name' : 'steve'}, {'name' : 'Obrien'}, {'name' : 'Autine'}, {'name' : 'steven'}]


@app.route('/getfriends', methods=['GET'])
@need_token
def returnall():
    return jsonify({'friends':friends})


if __name__ == '__main__':
    app.run(debug=True, port=8080)
