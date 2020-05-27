from rest_framework.serializers import ModelSerializer, RelatedField
from .models import Link, TitleAkas, TitleBasics, TitleRating, NameBasics, TitlePrincipals


class TitleAkasSerializer(ModelSerializer):
    class Meta:
        model = TitleAkas
        fields = [
            'region',
            'language'
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
        model = TitleRating
        fields = [
            'averagerating',
            'numofvotes',
            ]

class TitleSerializer(ModelSerializer):
    akas = TitleAkasSerializer(read_only=True)
    rating = RatingSerializer(read_only=True)
    writers = NameBasicsSerializer(many=True, read_only=True)
    directors = NameBasicsSerializer(many=True, read_only=True)
    class Meta:
        model = TitleBasics
        fields = [
            'writers',
            'directors',
            'rating',
            'akas',
            'primarytitle',
            'originaltitle',
            'titletype',
            'isadult',
            'startyear',
            'endyear',
            'runtimeminutes',
            'genres',
            'imagelink',
        ]
        read_only_fields = fields
