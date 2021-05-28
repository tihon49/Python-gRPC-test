from concurrent import futures
import random

import grpc

from recommendations_pb2 import (
    BookCategory,
    BookRecommendation,
    RecommendationResponse,
)

import recommendations_pb2_grpc

from fakeBD import books_by_category


class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):
    """класс, реализующий функции микросервиса"""

    def Recommend(self, request, context):
        if request.category not in books_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

        books_for_category = books_by_category[request.category]
        num_results = min(request.max_results, len(books_for_category))
        books_to_recommend = random.sample(books_for_category, num_results)

        return RecommendationResponse(recommendations=books_to_recommend)

    def BookDetail(self, request, context):
        for category_id in books_by_category:
            for b in books_by_category[category_id]:
                if b.id == request.data:
                    book = b
                    break
        return BookRecommendation(id=book.id, title=book.title)
        # TODO: проверку/валидацию данных для return


def serve():
    """запускает сетевой сервер и использует класс микросервиса для обработки запросов"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(RecommendationService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
