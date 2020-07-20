"""
Server to send and accept metrics
"""
import asyncio

metrics_dict = {}


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode('utf-8'), metrics_dict)
        self.transport.write(resp.encode('utf-8'))

    def process_data(self, data_str, dictToStore):
        data_ok = self.check_request_str(data_str)
        if data_ok == 'put':
            result = self.parse_put(data_str, dictToStore)
        elif data_ok == 'get':
            result = self.parse_get(data_str, dictToStore)
        else:
            result = data_ok
        return result

    @staticmethod
    def is_integer(n):
        """
        Checks if a numerical string is integer
        :param n: a numerical string
        :return: True or False
        """
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()

    @staticmethod
    def is_float(n):
        try:
            float(n)
            return True
        except ValueError:
            return False

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
            if data_str[0] == 'put' and len(data_str) == 4 and \
                    self.is_float(data_str[2]) and \
                    self.is_integer(data_str[3]):
                is_ok = 'put'
            elif data_str[0] == 'get' and len(data_str) == 2:
                is_ok = 'get'
        return is_ok

    @staticmethod
    def parse_get(data_str, dictToStore):
        """
        Parses command get
        :param data_str: submitted command, including word get
        :param dictToStore: dictionary to store data
        :return: in case of * - all content of dictionary. Otherwise values
        for submitted key or ok\n\n
        """
        dictToStore_clean = ClientServerProtocol.remove_duplicate_timestamp(dictToStore)
        data_str = data_str.strip('\n+').split(" ")
        # remove put
        del data_str[0]
        # requested key
        req_key = data_str[0]
        if req_key in dictToStore_clean:
            result = 'ok\n'
            for value_for_key in dictToStore_clean[req_key]:
                result = result + req_key + ' ' + str(value_for_key[0]) + \
                         ' ' + str(value_for_key[1]) + '\n'
            result = result + '\n'
        elif req_key == '*':
            result = 'ok\n'
            for key, values in dictToStore_clean.items():
                for value_for_key in values:
                    result = result + key + ' ' + str(value_for_key[0]) + \
                             ' ' + str(value_for_key[1]) + '\n'
            result = result + '\n'
        else:
            result = 'ok\n\n'
        return result

    @staticmethod
    def parse_put(data_str, dictToStore):
        """
        Parses command put
        :param data_str: submitted command, including word put
        :param dictToStore: dictionary to store data
        :return: ok\n\n in case of success and error\n\n\n otherwise
        """
        data_str = data_str.strip('\n+').split(" ")
        # remove put
        del data_str[0]
        # new key
        new_key = data_str[0]
        if new_key in dictToStore:
            new_values = dictToStore[new_key]
            try:
                to_add = (float(data_str[1]), int(data_str[2]))
                # check that we are adding unique data
                if not to_add in new_values:
                    new_values.append(to_add)
                    dictToStore.update({new_key: new_values})
                server_status = "ok\n\n"
            except TypeError:
                server_status = "error\n\n\n"
        else:
            dictToStore[new_key] = [(float(data_str[1]), int(data_str[2]))]
            server_status = "ok\n\n"
        return server_status

    @staticmethod
    def remove_duplicate_timestamp(dictToStore):
        result = {}
        for key, values in dictToStore.items():
            # set to store unique timestamps
            seen = set()
            # deduplicate based on timestamps using list comprehension
            dedupl_values = [(measure, timestamp) for measure, timestamp in values[::-1]
                             if not (timestamp in seen or seen.add(timestamp))]
            # order according to timestamp
            dedupl_values = sorted(dedupl_values, key=lambda tup: tup[1])
            result[key] = dedupl_values

        return result


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

# run_server('127.0.0.1', 8181)
