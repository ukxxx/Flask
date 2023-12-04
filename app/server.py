import flask
from errors import HttpError
from flask import jsonify, request, views
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from models import Advert, User, Session
from scheme import CreateAdvert, UpdateAdvert, CreateUser
from tools import validate

app = flask.Flask("app")
bcrypt = Bcrypt(app)


def hash_password(password: str):
    password = password.encode()
    return bcrypt.generate_password_hash(password).decode()


def check_password(password: str, hashed_password: str):
    password = password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.check_password_hash(hashed_password, password)


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response


@app.errorhandler(HttpError)
def error_handler(error):
    response = jsonify({"error": error.message})
    response.status_code = error.status_code
    return response


def get_advert(user_id: int):
    advert = request.session.get(Advert, user_id)
    if not advert:
        raise HttpError(404, "advert not found")
    return advert


def add_advert(advert: Advert):
    try:
        request.session.add(advert)
        request.session.commit()
    except IntegrityError as e:
        raise HttpError(409, "advert already exists") from e


class AdvertView(views.MethodView):
    @property
    def session(self) -> Session:
        return request.session

    def get(self, advert_id: int):
        advert = get_advert(advert_id)
        return jsonify(advert.dict)

    def post(self):
        advert_data = validate(CreateAdvert, request.json)
        advert = Advert(**advert_data)
        add_advert(advert)
        return jsonify({"id": advert.id})

    def patch(self, advert_id: int):
        advert = get_advert(advert_id)
        advert_data = validate(UpdateAdvert, request.json)
        print(advert_data)
        check_authority(get_user(advert_data["owner_id"]), advert)
        for key, value in advert_data.items():
            setattr(advert, key, value)
            add_advert(advert)
        return jsonify({"id": advert.id})

    def delete(self, advert_id: int):
        advert = get_advert(advert_id)
        advert_data = validate(UpdateAdvert, request.json)
        check_authority(get_user(advert_data["owner_id"]), advert)
        self.session.delete(advert)
        self.session.commit()
        return jsonify({"status": "advert deleted"})


def check_authority(user: User, advert: Advert):
    if user.id != advert.owner_id:
        raise HttpError(403, "user is not the owner")


def add_user(user: User):
    try:
        request.session.add(user)
        request.session.commit()
    except IntegrityError as e:
        # print(f"IntegrityError: {e}")
        raise HttpError(409, "user already exists") from e


def get_user(user_id: int):
    user = request.session.get(User, user_id)
    if not user:
        raise HttpError(404, "user not found")
    return user


class UserView(views.MethodView):
    @property
    def session(self) -> Session:
        return request.session

    def get(self, user_id: int):
        user = request.session.get(User, user_id)
        if not user:
            raise HttpError(404, "user not found")
        return jsonify(user.dict)

    def post(self):
        user_data = validate(CreateUser, request.json)
        user_data["password"] = hash_password(user_data["password"])
        user = User(**user_data)
        add_user(user)
        return jsonify({"id": user.id})

    def delete(self, user_id: int):
        user = request.session.get(User, user_id)
        if not user:
            raise HttpError(404, "user not found")
        self.session.delete(user)
        self.session.commit()
        return jsonify({"status": "user deleted"})


user_view = UserView.as_view("user_view")
advert_view = AdvertView.as_view("advert_view")

app.add_url_rule(
    "/advert/<int:advert_id>", view_func=advert_view, methods=["GET", "DELETE", "PATCH"]
)
app.add_url_rule("/advert", view_func=advert_view, methods=["POST"])
app.add_url_rule("/user/<int:user_id>", view_func=user_view, methods=["GET", "DELETE"])
app.add_url_rule("/user", view_func=user_view, methods=["POST"])

if __name__ == "__main__":
    app.run(port=8080, debug=True)
