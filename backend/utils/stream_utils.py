# utils/stream_utils.py
from flask import Response
import json

def sse_stream(generator):
    """
    Turn a Python generator that yields strings into a Server-Sent Events response.
    Each yielded chunk is sent as a JSON payload in data: {...}\n\n frames.
    """
    def event_stream():
        for chunk in generator:
            data = json.dumps({"chunk": chunk})
            yield f"data: {data}\n\n"
        # final event to signal done
        yield "event: done\ndata: {}\n\n"
    return Response(event_stream(), mimetype="text/event-stream")
