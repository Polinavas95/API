from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.generics import get_object_or_404


class ArticleView(APIView):
    """Method of viewing all articles.

    """
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(
            {
                'articles': serializer.data
            }
        )

    def post(self, request):
        article = request.data.get('article')
        serializer = ArticleSerializer(data=article)
        if serializer.is_valid(raise_exception=True):
            article_saved = serializer.save()
        return Response(
            {
                'success': f'Новая запись {article_saved.title} успешно добавлена!'
            }
        )

    def put(self, request, pk):
        saved_article = get_object_or_404(Article.objects.all(), pk=pk)
        data = request.data.get('article')
        serializer = ArticleSerializer(instance=saved_article, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            article_saved = serializer.save()
        return Response(
            {
            'success': f'Запись {article_saved.title} успешно изменена'
            }
        )

    def delete(self, request, pk):
        article = get_object_or_404(Article.objects.all(), pk=pk)
        article.delete()
        return Response(
            {
            'message': f'Запись с id {pk} успешно удалена'},
            status=204
        )
