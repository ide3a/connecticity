import zmq


class ZMessaging():

    def __init__(self, frontend: str = "tcp://127.0.0.1:5566"):
        ctx = zmq.Context()

        client = ctx.socket(zmq.DEALER)
        warning = ctx.socket(zmq.DEALER)
        warning_report = ctx.socket(zmq.DEALER)
        client.setsockopt(zmq.IDENTITY, b"req.interaction")
        warning.setsockopt(zmq.IDENTITY, b"service.warning")
        warning_report.setsockopt(zmq.IDENTITY, b"service.warning_report")

        client.connect(frontend)
        warning.connect(frontend)
        warning_report.connect(frontend)
        poller = zmq.Poller()
        poller_warning = zmq.Poller()

        self.client = client
        self.warning = warning
        self.warning_report = warning_report

        poller.register(self.client, zmq.POLLIN)
        poller_warning.register(self.warning, zmq.POLLIN)
        poller_warning.register(self.warning_report)

        self.poller = poller
        self.poller_warning = poller_warning

    def receive_data(self, timeout: int = 100):
        self.client.send(b"req.interaction", zmq.SNDMORE)
        self.client.send(b"", 0)
        sockets = dict(self.poller.poll(timeout))
        if self.client in sockets:
            msg = self.client.recv_multipart()
            return msg
        else:
            return None

    def send_warning(self, road_id: str, timeout: int = 100):
        self.warning.send_string("service.warning", zmq.SNDMORE)
        self.warning.send_string(road_id, 0)
        self.warning_report.send(b"service.warning_report", zmq.SNDMORE)
        self.warning_report.send(b"", 0)
        sockets = dict(self.poller_warning.poll(timeout))
        if self.warning_report in sockets:
            ret = self.warning_report.recv_multipart()
            return ret
        else:
            return None
