"""Test parse_cmd."""
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
    assert parse_cmd("-h")[0] is None
    assert "dummy" in parse_cmd("-h")[1]
    assert parse_cmd("-h")[2] in [""]

    # command = "a  b c"
    assert parse_cmd("a b c")[0].params == ["a", "b", "c"]

    command = "-e"  # expect stderr is not ""
    assert parse_cmd(command)[2] != ""
