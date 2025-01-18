from rest_framework import serializers
from .models import Node

class NodeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Node
        fields = "__all__"

    def get_children(self, obj):
        # Recursively serialize child nodes
        children = obj.children.all()
        return NodeSerializer(children, many=True).data
    
    # Ensuring a node cannot be its own parent
    def validate_parent(self, value):
        if self.instance and value == self.instance:
            raise serializers.ValidationError("A node cannot be its own parent.")

        if self.instance and value:
            if self.is_descendant(value):
                raise serializers.ValidationError("Cannot set the parent of this node to one of its descendants.")
        return value

    # Ensures there is only one root node in the tree
    def validate(self, data):        
        # If data's parent is None, count existing nodes with parent as None. If found, meaning root node already exists
        if data.get('parent') is None:
            root_nodes = Node.objects.filter(parent__isnull=True)
            if self.instance:  # If updating an existing node
                root_nodes = root_nodes.exclude(id=self.instance.id)
            if root_nodes.exists():
                raise serializers.ValidationError("Only one root node allowed. Please select parent person.")
        return data
    
    # Checks whether a potential parent is a descendant of the current node
    def is_descendant(self, potential_parent):
        current_node = self.instance
        while potential_parent:
            if potential_parent == current_node:
                return True
            potential_parent = potential_parent.parent
        return False
