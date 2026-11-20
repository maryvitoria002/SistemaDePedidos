#vai chamar o service para fazer a regra de negocio, e o serializer para transformar o objeto em json


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Produto
from .serializers import ProdutoSerializer
from .services import ProdutoService

service = ProdutoService()

# listar produtos
@api_view(['GET'])
def produto_list(request):
    serializer = ProdutoSerializer(service.listar(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# obter produto por ID
@api_view(['GET'])
def get_by_id(request, id):
    try:
        produto = service.buscar(id)
    except Produto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(ProdutoSerializer(produto).data, status=status.HTTP_200_OK)

# criar produto
@api_view(['POST'])
def create_produto(request):
    serializer = ProdutoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    produto = service.criar(**serializer.validated_data)
    return Response(ProdutoSerializer(produto).data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_produto(request, id):
    try:
        produto = service.buscar(id)
    except Produto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not request.data:
        return Response(
            {'error': 'Nenhum dado fornecido para atualização.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    serializer = ProdutoSerializer(produto, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    produto = service.atualizar(produto, **serializer.validated_data)
    return Response(ProdutoSerializer(produto).data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_produto(request, id):
    try:
        produto = service.buscar(id)
    except Produto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    service.excluir(produto)
    return Response(status=status.HTTP_204_NO_CONTENT)



