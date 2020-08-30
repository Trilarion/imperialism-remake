from imperialism_remake.base import network as base_network


class ServerNetworkClient(base_network.NetworkClient):
    """
    Server network client.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # important properties
        self.subscribed_to_chat = False
        self.name = ''
