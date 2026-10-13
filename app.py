from flask import Flask, jsonify, request

from duckfine import DuckFine


app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/fine")
def fine():
    days_value = request.args.get("days")
    try:
        days = int(days_value)
    except (TypeError, ValueError):
        return jsonify(error="days must be a non-negative integer"), 400

    deluxe = request.args.get("deluxe") == "1"
    try:
        fee = DuckFine(member_id="api").charge(days, deluxe=deluxe)
    except ValueError as error:
        return jsonify(error=str(error)), 400

    return jsonify(fee=fee)


if __name__ == "__main__":
    app.run()