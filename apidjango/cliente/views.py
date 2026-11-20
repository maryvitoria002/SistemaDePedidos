from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Cliente
from .serializers import ClienteSerializer
from .services import ClienteService
from pedido.serializers import PedidoSerializer

service = ClienteService()

# listar clientes
@api_view(['GET'])
def cliente_list(request):
    clientes = service.listar()
    serializer = ClienteSerializer(clientes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def cliente_pedidos(request, id):
    try:
        pedidos = service.buscar_pedidos(id)
    except Cliente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PedidoSerializer(pedidos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# obter cliente por ID
@api_view(['GET'])
def get_by_id(request, id):
    try:
        cliente = service.buscar(id)
    except Cliente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(ClienteSerializer(cliente).data, status=status.HTTP_200_OK)

# criar cliente
@api_view(['POST'])
def create_cliente(request):
    serializer = ClienteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    cliente = service.criar(**serializer.validated_data)
    return Response(ClienteSerializer(cliente).data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_cliente(request, id):
    try:
        cliente = service.buscar(id)
    except Cliente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not request.data:
        return Response(
            {'error': 'Nenhum dado fornecido para atualização.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    serializer = ClienteSerializer(cliente, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    cliente = service.atualizar(cliente, **serializer.validated_data)
    return Response(ClienteSerializer(cliente).data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_cliente(request, id):
    try:
        cliente = service.buscar(id)
    except Cliente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    service.excluir(cliente)
    return Response(status=status.HTTP_204_NO_CONTENT)