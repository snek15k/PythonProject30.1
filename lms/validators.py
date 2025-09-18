from urllib.parse import urlparse

from rest_framework import serializers


class YouTubeOnlyValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        value = attrs.get(self.field)
        if not value:
            return

        parsed_url = urlparse(value)
        domain = parsed_url.netloc.lower()
        allowed_domains = ['youtube.com', 'www.youtube.com', 'youtu.be', 'www.youtu.be']

        if domain not in allowed_domains:
            raise serializers.ValidationError(
                {self.field: "Допустимы только ссылки на youtube.com или youtu.be"}
            )
