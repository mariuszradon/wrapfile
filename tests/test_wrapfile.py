from wrapfile import TextFileReader, TextFileWriter, FileWrapper
import tempfile
import os

DATA="ndht5433\nC44nhcx 44dmnhn4\n\nkjnh43uyx 4%54x"

def test_file_writer_and_reader():
    """Test TextFileWriter and TextFileReader
    """
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tf:
        tf.write(DATA)
    tfpath = tf.name

    # writer, arg is path
    with TextFileWriter(tfpath) as w:
        assert not w.has_value
        w.write(DATA)
    assert w.closed
    with open(tfpath, 'r') as f:
        assert f.read() == DATA

    # writer, arg is file
    with open(tfpath, 'w') as f:
        with TextFileWriter(f) as w:
            assert not w.has_value
            w.write(DATA)
        assert not w.closed
        assert not f.closed
        assert w.actual_file == f
    assert w.closed
    assert f.closed

    # reader, arg is path
    with TextFileReader(tfpath) as r:
        assert not r.has_value
        t = r.read()
    assert r.closed
    assert t == DATA

    # reader, arg is file
    with open(tfpath, 'r') as f:
        with TextFileReader(f) as r:
            assert not r.has_value
            t = r.read()
        assert not r.closed
        assert not f.closed
    assert r.closed
    assert f.closed
    assert t == DATA

    os.remove(tfpath)

def test_strbuf():
    """Test string buffer functionality
    """
    with TextFileWriter() as w:
        w.write(DATA)
        assert w.has_value
        assert w.getvalue() == DATA

def test_attributes():
    """Test if wrapper has all attributes of the original file
    """
    with tempfile.TemporaryFile() as f:
        with FileWrapper(f, 'r') as buf:
            for name in dir(f):
                assert hasattr(buf, name)

