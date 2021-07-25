"""Test url2txt."""
from koyeb_nb2.url2txt import url2txt


def test_url2txt():
    """test url2txt www.python.org."""
    url = "www.python.org"
    res = url2txt(url)
    assert len(res) > 100


def test_url2txt_nourl():
    """test url2txt show_url=False, www.python.org."""
    url = "www.python.org"
    res = url2txt(url, show_url=False)
    assert len(res) > 100
