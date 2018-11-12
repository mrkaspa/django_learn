from rest_framework.response import Response
from rest_framework import status


def is_none(val):
    return val is None


def is_not_none(val):
    return val is not None


def gen_crud(model_cls, serializer_cls):
    def index(request):
        snippets = model_cls.objects.all()
        serializer = serializer_cls(snippets, many=True)
        return Response(serializer.data)

    def create(request):
        serializer = serializer_cls(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_by_id(pk, f):
        try:
            model = model_cls.objects.get(pk=pk)
            return f(model)
        except model_cls.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def show(request, pk):
        def do(model):
            serializer = serializer_cls(model)
            return Response(serializer.data)
        return get_by_id(pk, do)

    def update(request, pk):
        def do(model):
            serializer = serializer_cls(model, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return get_by_id(pk, do)

    def delete(request, pk):
        def do(model):
            model.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        return get_by_id(pk, do)

    return [
        ('GET', is_none, index),
        ('GET', is_not_none, show),
        ('POST', is_none, create),
        ('PUT', is_not_none, update),
        ('DELETE', is_not_none, delete),
    ]


def handle_crud(handlers, request, val=None):
    for (method, f, handler) in handlers:
        if method == request.method and f(val):
            if val is None:
                return handler(request)
            return handler(request, val)
    return Response(status=status.HTTP_404_NOT_FOUND)
