from discogs_cli.ext.utils import TextUtils


class TestTextUtils:
    def setup_method(self):
        self.utils = TextUtils()

    def test_get_tokens(self):
        text = "ogs artist 123"
        tokens = self.utils.get_tokens(text)
        assert tokens == ["ogs", "artist", "123"]

    def test_get_tokens_quoted(self):
        text = 'ogs search "massive attack"'
        tokens = self.utils.get_tokens(text)
        assert tokens == ["ogs", "search", "massive attack"]

    def test_last_token(self):
        text = "ogs artist"
        assert self.utils._last_token(text) == "artist"

    def test_safe_split_valid(self):
        text = "hello world"
        assert self.utils._safe_split(text) == ["hello", "world"]

    def test_safe_split_invalid_quote(self):
        # shlex raises ValueError on unclosed quotes
        text = 'hello "world'
        # The updated code catches ValueError and returns the original text
        assert self.utils._safe_split(text) == text
