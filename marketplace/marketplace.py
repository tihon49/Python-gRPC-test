import os

from flask import Flask, render_template
import grpc

from recommendations_pb2 import BookCategory, RecommendationRequest
from recommendations_pb2_grpc import RecommendationsStub

app = Flask(__name__)

recommendations_host = os.getenv("RECOMMENDATIONS_HOST", "localhost")
# recommendations_channel = grpc.insecure_channel("localhost:50051")
recommendations_channel = grpc.insecure_channel(f"{recommendations_host}:50051")
recommendations_client = RecommendationsStub(recommendations_channel)


@app.route("/")
def render_homepage():
    """домашняя страница"""
    recommendations_request = RecommendationRequest(user_id=1, category=BookCategory.MYSTERY, max_results=3)
    recommendations_response = recommendations_client.Recommend(recommendations_request)
    return render_template("homepage.html", recommendations=recommendations_response.recommendations)


@app.route("/book/<int:book_id>")
def book_detail(book_id):
    return render_template('book.html', book_id=book_id)
# TODO: сделать функцию запроса в .proto для детального отображения
# TODO: расширить модель book.
