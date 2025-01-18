from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Node
from .serializers import NodeSerializer

# Create your views here.
class NodeListView(APIView):
    # Fetches the root node, its children array is dynamically computed by the serializer
    def get(self, request):
        try:
            node = Node.objects.get(parent=None)
            nodes = Node.objects.all().values("id", "name")
            serializer = NodeSerializer(node)
        except Node.DoesNotExist:
            return Response({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"orgTree":serializer.data, "parents": list(nodes)})

    # Creates a new node in the DB
    def post(self, request):
        parent_id = request.data.get('parent')
        if parent_id:
            try:
                parent_node = Node.objects.get(pk=parent_id)
            except Node.DoesNotExist:
                return Response({"error": "Parent node not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            parent_node = None  # Root node if no parent is specified

        serializer = NodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(parent=parent_node)
            return Response(serializer.data, status=status.HTTP_201_CREATED)                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NodeDetailView(APIView):
    # Gets the details of an individual node
    def get(self, request, pk):
        try:
            node = Node.objects.get(pk=pk)
            serializer = NodeSerializer(node)
            return Response(serializer.data)
        except Node.DoesNotExist:
            return Response({"error": "Node not found"}, status=status.HTTP_404_NOT_FOUND)

    # Updating existing node details with incoming requset data
    def put(self, request, pk):
        try:
            node = Node.objects.get(pk=pk)
            serializer = NodeSerializer(node, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Node.DoesNotExist:
            return Response({"error": "Node not found"}, status=status.HTTP_404_NOT_FOUND)

    # Deletes an existing node
    def delete(self, request, pk):
        try:
            node = Node.objects.get(pk=pk)
            if node.children.exists():
                return Response(
                    {"error": "Cannot delete a parent node with children."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            node.delete()
            return Response({"message": "Node deleted successfully"}, status=status.HTTP_200_OK)
        except Node.DoesNotExist:
            return Response({"error": "Node not found"}, status=status.HTTP_404_NOT_FOUND)
