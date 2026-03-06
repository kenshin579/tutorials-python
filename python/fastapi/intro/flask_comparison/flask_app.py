"""동일 API를 Flask로 구현한 비교용 코드."""

from flask import Flask, jsonify, request

app = Flask(__name__)

fake_db: dict[int, dict] = {
    1: {"id": 1, "username": "frank", "email": "frank@example.com", "full_name": "Frank Oh"},
    2: {"id": 2, "username": "alice", "email": "alice@example.com", "full_name": "Alice Kim"},
}
next_id = 3


# Flask: 타입 변환을 직접 처리하거나 <int:user_id> 사용
@app.get("/users")
def list_users():
    skip = request.args.get("skip", 0, type=int)
    limit = request.args.get("limit", 10, type=int)
    users = list(fake_db.values())
    return jsonify(users[skip : skip + limit])


@app.get("/users/<int:user_id>")
def get_user(user_id):
    if user_id not in fake_db:
        return jsonify({"detail": "사용자를 찾을 수 없습니다"}), 404
    return jsonify(fake_db[user_id])


# Flask: 요청 데이터를 수동으로 파싱하고 검증해야 함
@app.post("/users")
def create_user():
    global next_id
    data = request.get_json()
    if not data or "username" not in data or "email" not in data:
        return jsonify({"detail": "username과 email은 필수입니다"}), 422
    new_user = {
        "id": next_id,
        "username": data["username"],
        "email": data["email"],
        "full_name": data.get("full_name"),
    }
    fake_db[next_id] = new_user
    next_id += 1
    return jsonify(new_user), 201


@app.put("/users/<int:user_id>")
def update_user(user_id):
    if user_id not in fake_db:
        return jsonify({"detail": "사용자를 찾을 수 없습니다"}), 404
    data = request.get_json()
    stored = fake_db[user_id]
    if "username" in data:
        stored["username"] = data["username"]
    if "email" in data:
        stored["email"] = data["email"]
    if "full_name" in data:
        stored["full_name"] = data["full_name"]
    return jsonify(stored)


@app.delete("/users/<int:user_id>")
def delete_user(user_id):
    if user_id not in fake_db:
        return jsonify({"detail": "사용자를 찾을 수 없습니다"}), 404
    del fake_db[user_id]
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
