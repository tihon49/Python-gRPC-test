import os

from flask import Flask, render_template
import grpc

from recommendations_pb2 import BookCategory, RecommendationRequest, Data
from recommendations_pb2_grpc import RecommendationsStub

app = Flask(__name__)

recommendations_host = os.getenv("RECOMMENDATIONS_HOST", "localhost")
recommendations_channel = grpc.insecure_channel(f"{recommendations_host}:50051")
recommendations_client = RecommendationsStub(recommendations_channel)


@app.route("/")
def render_homepage():
    """домашняя страница"""
    recommendations_request = RecommendationRequest(user_id=1, category=BookCategory.SCIENCE_FICTION, max_results=3)
    recommendations_response = recommendations_client.Recommend(recommendations_request)
    return render_template("homepage.html", recommendations=recommendations_response.recommendations)


@app.route("/book/<int:book_id>")
def book_detail(book_id):
    book_request = Data(data=book_id)
    try:
        book_response = recommendations_client.BookDetail(book_request)
        return render_template('book.html', book_id=book_response.id, book_title=book_response.title)
    except Exception as error:
        print(error, flush=True)
    return render_template('book.html', book_id=book_id)
    # TODO: расширить модель book.
