"""Test parse_cmd."""
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, Namespace
from koyeb_nb2.parse_cmd import parse_cmd


def test_parse_cmd_dummy():
    """Test parse_cmd_dummy.

    parse_cmd returns Namespace, stdout, stderr

    a dummy parser is used when no parse is given:
    parser = ArgumentParser(
        prog="dummy",
        # exit_on_error=False,  # exit_on_error avail in 3.9
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("params", nargs="*")
    """
    # command = "-h"
    assert parse_cmd("-h")[0] == Namespace(params=[])
    assert parse_cmd("-h")[1] in [""]
    assert parse_cmd("-h")[2] in [""]

    # command = "a  b c"
    # assert parse_cmd("a b c")[0].params == ["a", "b", "c"]
    assert parse_cmd("a b c")[0].params == ["b", "c"]

    command = "-e"  # expect stderr is not ""
    # assert parse_cmd(command)[2] != ""


def test_parse_cmd_google_search():
    """Test parse_cmd_google_search."""
    parser = ArgumentParser(
        prog="scrape", formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("url", nargs="?", help="url of the desired page")
    parser.add_argument(
        "--bodywidth", type=int, default=5000, help="for displaying text"
    )
    parser.add_argument("--remove", action="store_true", help="removal of blank lines")
    parser.add_argument(
        "--show_url", action="store_true", help="show url in the begenning"
    )
    parser.add_argument(
        "--ignore_links", action="store_false", help="ignore links in text"
    )

    args, *_ = parse_cmd("/fetch \"http://google.com\"", parser)

    assert args.url == "http://google.com"
