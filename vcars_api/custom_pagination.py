from rest_framework.pagination import LimitOffsetPagination


class PicListPaginatorWithMaxLimit(LimitOffsetPagination):
    max_limit = 6

