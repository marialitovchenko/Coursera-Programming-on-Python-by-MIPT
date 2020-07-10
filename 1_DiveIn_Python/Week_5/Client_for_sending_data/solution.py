"""

"""
import time
import socket


class ClientError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.sock.connect((host, port))
        self.sock.settimeout(timeout)

    @staticmethod
    def check_server_name_and_metric(str_to_check):
        str_to_check = str_to_check.split('.')
        result = True
        if len(str_to_check) != 2:
            raise ClientError(str_to_check, 'Client error occurred')
        return result

    @staticmethod
    def is_integer(n):
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

    @staticmethod
    def which_is_timestamp(list_to_check):
        """
        Checks, which element of list is timestamp (int). Returns ordered list,
        where first element is value and second is timestamp
        :param list_to_check: list from 2 elements, which is needed to be
               checked
        :return: list, in which first element isn't int,
                 and second int(timestamp)
        """
        if '.' in list_to_check[0]:
            result = list_to_check[::-1]
        elif '.' in list_to_check[1]:
            result = list_to_check
        elif '.' not in list_to_check[0] and '.' not in list_to_check[1]:
            try:
                first = int(list_to_check[0])
                second = int(list_to_check[1])
                if first < second:
                    result = [second, first]
                elif second < first:
                    result = [first, second]
                else:
                    result = list_to_check
            except TypeError as ex:
                raise ClientError(list_to_check, 'Client error occurred')
        else:
            raise ClientError(list_to_check, 'Client error occurred')
        return result

    @staticmethod
    def add_metric_to_dict(new_entry, metric_dict):
        """
        Parses and adds server metrics to the existing dictionary

        :param new_entry:
        :param metric_dict:
        :return:
        """
        new_entry = new_entry.split(' ')
        if len(new_entry) == 3:  # should be only 3
            new_key = new_entry[0]  # this is server name, check its validity
            del new_entry[0]
            new_entry_rearranged = Client.which_is_timestamp(new_entry)
            if new_key in metric_dict:
                new_values = metric_dict[new_key]
                try:
                    new_values.append((int(new_entry_rearranged[0]),
                                       float(new_entry_rearranged[1])))
                    new_values = sorted(new_values, key=lambda tup: tup[0])
                    metric_dict.update({new_key: new_values})
                except TypeError:
                    raise ClientError(new_values, 'Client error occurred')
            else:
                metric_dict[new_key] = [(int(new_entry_rearranged[0]),
                                         float(new_entry_rearranged[1]))]
        else:
            raise ClientError(new_entry, 'Client error occurred')
        return metric_dict

    @staticmethod
    def decode_data(data_str):
        """
        Parses one entry (string) of server output.

        Returns dict with metrics if successful and ClientError otherwise.

        :param: data_str: string of data to parse
        :return: key - metrics values dictionary
        """
        data_str = data_str.decode("utf8")
        data_str = data_str.split("\n")

        # if length of the string is less than 3 or server returned error
        if data_str[0] != 'ok':
            raise ClientError(data_str, 'Client error occurred')
        else:
            # prep result
            result = {}
            # remove last two \n \n
            del data_str[-2:]

            # and if there are data
            if len(data_str) > 1:
                del data_str[0]  # remove ok
                # process every string and add it to the result dict
                for one_str in data_str:
                    result = Client.add_metric_to_dict(one_str, result)
            else:
                pass
        return result

    def get(self, metric_name):
        """
        Retrieves and parces metrics data from sever
        :param metric_name: name of the metric to be retrieved from the server
        :return: In case of success: dict with the retrieved metrics. Keys in
                 the dict are list of tuples will be transformed to int and
                 float respectively. List will be sorted by timestamp
                 (ascending).
                 In case of error: ClientError
        """
        # create a string to send - command to request data
        str_to_send = 'get ' + metric_name + '\n'
        # send request
        self.sock.sendall(str_to_send.encode('utf-8'))

        # receive data
        data = self.sock.recv(1024)
        result = self.decode_data(data)
        return result

    def put(self, metric_name, metric_value, timestamp=None):
        """
        Put (send) metrics to the server

        :param metric_name: name of the metric to send to the server
        :param metric_value: value of metric to send to the server
        :param timestamp: [optional], timestamp of the metric. If timestamp
                          isn't provided, function will put it automatically
        :return: nothing in case of success and ClientError otherwise
        """
        # compute timestamp, if needed
        if timestamp is None:
            timestamp = time.time()
        pass
        # create a string to send
        str_to_send = 'put ' + str(metric_name) + ' ' + str(metric_value) + \
                      ' ' + str(int(timestamp)) + '\n'
        # try sending
        try:
            self.sock.sendall(str_to_send.encode("utf8"))
            # receive data
            data = self.sock.recv(1024)
            if data.decode("utf8") != 'ok\n\n':
                raise ClientError(str_to_send, 'Client error occurred')
        except ClientError as ex:
            raise ClientError(str_to_send, 'Client error occurred')
