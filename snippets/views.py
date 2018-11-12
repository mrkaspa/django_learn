from rest_framework.decorators import api_view
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from snippets.crud import gen_crud, handle_crud


snippet_crud = gen_crud(Snippet, SnippetSerializer)


@api_view(['GET', 'POST'])
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    return handle_crud(snippet_crud, request)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    return handle_crud(snippet_crud, request, pk)
