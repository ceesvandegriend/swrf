from swrf.check import logger, Check

def test_logger():
    assert logger


def test_init():
    chck = Check()
    assert chck
    assert chck.status == Check.WHITE


def test_clone():
    chck0 = Check()
    chck1 = chck0.clone()

    assert chck0.timestamp == chck1.timestamp
    assert chck0.type == chck1.type
    assert chck0.uuid == chck1.uuid
    assert chck0.name == chck1.name
    assert chck0.status == chck1.status
    assert chck0.duration == chck1.duration
    assert chck0.changed == chck1.changed
    assert chck0.period == chck1.period
    assert chck0.description == chck1.description


def test_encode():
    chck = Check()
    txt = chck.encode()
    lines = txt.splitlines()

    assert lines[0].startswith("timestamp: ")
    assert lines[1].startswith("type: ")
    assert lines[2].startswith("uuid: ")
    assert lines[3].startswith("name: ")
    assert lines[4].startswith("status: ")
    assert lines[5].startswith("duration: ")
    assert lines[6].startswith("changed: ")
    assert lines[7].startswith("period: ")


def test_decode():
    txt = """type: check
name: Dummy
status: 1

"""
    chck = Check.decode(txt)
    assert chck.type == "check"
    assert chck.name == "Dummy"
    assert chck.status == Check.GREEN
