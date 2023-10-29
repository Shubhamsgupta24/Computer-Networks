import socket
from socket import *

#RDT 2.0 - It has checksum to detect bit errors along with ACK and NACK

def checksum_generator(message):
    