from Logger import Logger
import pytest


def test_create_Logger():
    Logger(print_logs=True)
    with pytest.raises(Exception):
        Logger(666)


def test__format_Logger():
    l = Logger()
    s = l._format(666, ["test.com", "t3st.com"], "pytest")
    ss = l._format(160, ["test.com", "t3st.com"], "pytest")
    sss = l._format(42, ["test.com", "t3st.com"], "pytest")
    assert s == "[HIGH] - test.com,t3st.com - pytest"
    assert ss == "[MEDIUM] - test.com,t3st.com - pytest"
    assert sss == "[LOW] - test.com,t3st.com - pytest"
