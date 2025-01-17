from wrapfile import wrapfile
import tempfile
import os

def test_wrapfile():
    # create some tempfile and write in some data
    DATA="ndht5433\nC44nhcx 44dmnhn4\n\nkjnh43uyx 4%54x"
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tf:
        tf.write(DATA)
        tf_name = tf.name

    # open this file by providing its name
    with wrapfile(tf_name, 'r') as buf1:
        test1 = buf1.read()

    # open this file by providing file object
    with open(tf_name, 'r') as f:
        with wrapfile(f, 'r') as buf2:
            test2 = buf2.read()

    tf.close()
    os.remove(tf_name)
    
    assert test1 == test2
    assert test1 == DATA
    assert buf1.closed
    assert buf2.closed


    
