class GetDetailSerializerMixin:
    """Mixin for accessing detailed serializer if the action is retrieve"""

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == "retrieve" and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        if self.action == "update" and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()
