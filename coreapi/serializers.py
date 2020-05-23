from rest_framework.serializers import ModelSerializer, RelatedField
from .models import Link, TitleAkas, TitleBasics, TitleRatings, NameBasics

class LinkSerializer(ModelSerializer):
    class Meta:
        model = Link
        fields = [
            'movieid',
            'imagelink',
        ]
        read_only_fields = fields

class TitleBasicsSerializer(ModelSerializer):
    class Meta:
        model = TitleBasics
        fields = [
            'runtimeminutes',
            ]

class NameBasicsSerializer(ModelSerializer):
    class Meta:
        model = NameBasics
        fields = [
            'nconst',
            'primaryname',
            ]

class RatingSerializer(ModelSerializer):
    class Meta:
        model = TitleRatings
        fields = [
            'averagerating',
            'numvotes',
            ]

class TitleSerializer(ModelSerializer):
    basics = TitleBasicsSerializer(read_only=True)
    rating = RatingSerializer(read_only=True)
    writers = NameBasicsSerializer(many=True, read_only=True)
    directors = NameBasicsSerializer(many=True, read_only=True)
    link = LinkSerializer(read_only=True)
    class Meta:
        model = TitleAkas
        fields = [
            'writers',
            'directors',
            'link',
            'rating',
            'basics',
            'titleid',
            'title',
        ]
        read_only_fields = fields

