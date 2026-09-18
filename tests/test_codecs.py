from neurocodec.codecs.registry import get_codec
def test_json_round_trip():
    r={"temperature":28.4,"location":"PH","status":"OK"}; c=get_codec("json"); assert c.decode(c.encode(r))==r
def test_pipe_round_trip():
    r={"temperature":28.4,"location":"PH","timestamp":1758211200}; c=get_codec("pipe"); assert c.decode(c.encode(r))==r
def test_csv_round_trip():
    r={"temperature":28.4,"location":"PH","timestamp":1758211200}; c=get_codec("csv"); assert c.decode(c.encode(r))==r
