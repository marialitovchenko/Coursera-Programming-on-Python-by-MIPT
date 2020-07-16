"""
Server to send and accept metrics
"""
import asyncio

metrics_dict = ()


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = ClientServerProtocol.process_data(data.decode(), metrics_dict)
        self.transport.write(resp.encode())

    @property
    def is_integer(self, n):
        """
        Checks if a numerical string contains integer
        :param n: a numerica string
        :return: True or False
        """
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()

    @property
    def check_request_str(self, data_str):
        """
        Checks if request is in right format
        :param data_str: string, representing request
        :return: put or get in case of valid request, error otherwise
        """
        # will contain True if data string is ok and false otherwise
        is_ok = 'error\nwrong command\n\n'
        # check that string ends with \n
        if data_str.endswith('\n'):
            data_str = data_str.split(" ")
            if data_str[0] == 'put' and len(data_str) == 4 and ClientServerProtocol.is_integer(data_str[3]):
                is_ok = 'put'
            elif data_str[0] == 'get' and len(data_str) == 2:
                is_ok = 'get'
        return is_ok

    @property
    def parse_put(self, data_str, metric_dict):
        data_str = data_str.split(" ")
        # remove put
        del data_str[0]
        new_key = data_str[0]
        if new_key in metric_dict:
            new_values = metric_dict[new_key]
            try:
                new_values.append((int(data_str[2]), float(data_str[1])))
                new_values = sorted(new_values, key=lambda tup: tup[0])
                metric_dict.update({new_key: new_values})
            except TypeError:
                pass
        else:
            metric_dict[new_key] = [(int(data_str[2]), float(data_str[1]))]
        return metric_dict

    def process_data(data_str):
        data_ok = ClientServerProtocol.check_request_str(data_str)
        if data_ok == 'put':
            result = ClientServerProtocol.parse_put(data_str, metrics_dict)
        elif data_ok == 'get':
            pass
        else:
            result = data_ok
        return result


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(ClientServerProtocol, host, port, loop=loop)
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
