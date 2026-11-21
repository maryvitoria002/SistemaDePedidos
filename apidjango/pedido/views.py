from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Pedido
from .serializers import PedidoSerializer
from .services import PedidoService

service = PedidoService()

# listar pedidos
@api_view(['GET'])
def pedido_list(request):
    serializer = PedidoSerializer(service.listar(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# obter pedido por ID
@api_view(['GET'])
def get_by_id(request, id):
    try:
        pedido = service.buscar(id)
    except Pedido.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(PedidoSerializer(pedido).data, status=status.HTTP_200_OK)

# criar pedido
@api_view(['POST'])
def create_pedido(request):
    serializer = PedidoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    dados = dict(serializer.validated_data)
    itens = dados.pop('itens', None)
    try:
        pedido = service.criar(
            cliente=dados['cliente'],
            status=dados.get('status'),
            produto=dados.get('produto'),
            quantidade=dados.get('quantidade'),
            itens=itens,
        )
    except ValueError as error:
        return Response(
            {'error': str(error)},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(PedidoSerializer(pedido).data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_pedido(request, id):
    try:
        pedido = service.buscar(id)
    except Pedido.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not request.data:
        return Response(
            {'error': 'Nenhum dado fornecido para atualização.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    serializer = PedidoSerializer(pedido, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    try:
        pedido = service.atualizar(pedido, **serializer.validated_data)
    except ValueError as error:
        return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(PedidoSerializer(pedido).data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_pedido(request, id):
    try:
        pedido = service.buscar(id)
    except Pedido.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        service.excluir(pedido)
    except ValueError as error:
        return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def pagar_pedido(request, id):
    try:
        pedido = service.buscar(id)
    except Pedido.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    forma_pagamento = request.data.get('forma_pagamento')
    if not forma_pagamento:
        return Response(
            {'forma_pagamento': 'Este campo é obrigatório.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        pedido = service.pagar(pedido, forma_pagamento)
    except ValueError as error:
        return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(PedidoSerializer(pedido).data, status=status.HTTP_200_OK)

@api_view(['POST'])
def cancelar_pedido(request, id):
    try:
        pedido = service.buscar(id)
    except Pedido.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        pedido = service.cancelar(pedido)
    except ValueError as error:
        return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(PedidoSerializer(pedido).data, status=status.HTTP_200_OK)
