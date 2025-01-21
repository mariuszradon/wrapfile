from wrapfile import TextFileReader, TextFileWriter, FileWrapper
from wrapfile.error import WrapFileValueError
import tempfile
import os
import pathlib
import gzip

DATA="ndht5433\nC44nhcx 44dmnhn4\n\nkjnh43uyx 4%54x"

def test_file_writer_and_reader():
    """Test TextFileWriter and TextFileReader
    """
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tf:
        tf.write(DATA)
    tfpath = tf.name

    # writer, arg is path
    with TextFileWriter(tfpath) as w:
        w.write(DATA)
        assert w.getvalue() is None
    assert w.closed
    with open(tfpath, 'r') as f:
        assert f.read() == DATA

    # writer, arg is file
    with open(tfpath, 'w') as f:
        with TextFileWriter(f) as w:
            w.write(DATA)
            assert w.getvalue() is None
        assert not w.closed
        assert not f.closed
        assert w.actual_file == f
    assert w.closed
    assert f.closed

    # reader, arg is path
    with TextFileReader(tfpath) as r:
        assert not hasattr(r, "getvalue")
        t = r.read()
    assert r.closed
    assert t == DATA

    # reader, arg is file
    with open(tfpath, 'r') as f:
        with TextFileReader(f) as r:
            assert not hasattr(r, "getvalue")
            t = r.read()
        assert not r.closed
        assert not f.closed
    assert r.closed
    assert f.closed
    assert t == DATA

    os.remove(tfpath)

def test_file_writer_and_reader_gz():
    """Test writer and reader for gzip-compressed files
    """
    tempdir = pathlib.Path(tempfile.mkdtemp())
    tfpath = tempdir / 'test.txt.gz'

    # writer, arg is path
    with TextFileWriter(tfpath) as w:
        w.write(DATA)
        assert w.getvalue() is None
    assert w.closed
    with gzip.open(tfpath, 'rt') as f:
        assert f.read() == DATA

    # writer, arg is file
    with gzip.open(tfpath, 'wt') as f:
        with TextFileWriter(f) as w:
            w.write(DATA)
            assert w.getvalue() is None
        assert not w.closed
        assert not f.closed
        assert w.actual_file == f
    assert w.closed
    assert f.closed

    # reader, arg is path
    with TextFileReader(tfpath) as r:
        assert not hasattr(r, "getvalue")
        t = r.read()
    assert r.closed
    assert t == DATA

    # reader, arg is file
    with gzip.open(tfpath, 'rt') as f:
        with TextFileReader(f) as r:
            assert not hasattr(r, "getvalue")
            t = r.read()
        assert not r.closed
        assert not f.closed
    assert r.closed
    assert f.closed
    assert t == DATA

    tfpath.unlink()
    tempdir.rmdir()


def test_strbuf():
    """Test string buffer functionality
    """
    with TextFileWriter(None) as w:
        w.write(DATA)
        assert w.getvalue() == DATA

def test_attributes():
    """Test if wrapper has all attributes of the original file
    """
    with tempfile.TemporaryFile() as f:
        with FileWrapper(f, 'r') as buf:
            for name in dir(f):
                assert hasattr(buf, name)


def test_inmemory_mode():
    """Test if in-memory buffer can be created with a specified mode
    """
    def ok(mode):
        try:
            with FileWrapper(None, mode) as f:
                return True
        except WrapFileValueError:
            return False
    assert ok('w')
    assert ok('wt')
    assert ok('wb')
    assert not ok('r')
    assert not ok('rt')
    assert not ok('rb')
