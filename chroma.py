#!/usr/bin/python
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import colorsys
import random
import logging

from openrazer.client import DeviceManager
from openrazer.client import constants as razer_constants
device_manager = DeviceManager()


logging.basicConfig( filename="chroma-daemon.log",
                     filemode='w',
                     level=logging.DEBUG,
                     format= '%(asctime)s - %(levelname)s - %(message)s',
                   )

def main():
    logging.info("Found {} Razer devices".format(len(device_manager.devices)))
    device_manager.sync_effects = False
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    with SimpleXMLRPCServer(("localhost", 16767),
                            requestHandler=RequestHandler,
                            allow_none=True,
                            logRequests=False) as server:
        server.register_introspection_functions()

        server.register_function(random_keys)
        server.register_function(wave)

        server.serve_forever()



def random_color():
    rgb = colorsys.hsv_to_rgb(random.uniform(0, 1), random.uniform(0.5, 1), 1)
    return tuple(map(lambda x: int(256 * x), rgb))


def random_keys():
    for device in device_manager.devices:
        rows, cols = device.fx.advanced.rows, device.fx.advanced.cols

        for row in range(rows):
            for col in range(cols):
                device.fx.advanced.matrix[row, col] = random_color()

        device.fx.advanced.draw()


def wave():
    for device in device_manager.devices:
        device.fx.wave(razer_constants.WAVE_RIGHT)


try:
    main()
except:
    logging.exception("Couldn't run chroma daemon!")
