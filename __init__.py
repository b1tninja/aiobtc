import asyncio
import enum
import hashlib
import socket
import struct


class Magic(enum.Enum):
    main = 0xD9B4BEF9
    testnet = 0xDAB5BFFA
    testnet3 = 0x0709110B
    namecoin = 0xFEB4BEF9


def sha256(value):
    return hashlib.sha256(value).digest()


def sha256_dup(value):
    return sha256(sha256(value))


class MerkleTree(list):
    def calculate_root(self):
        root = hashlib.sha256()
        for i, v in enumerate(self):
            root.update(sha256_dup(v))

        if not i % 2:
            root.update(sha256_dup(v))

        return root.digest()


class VarInt(int):
    """
    Variable Integer encoder/decoder
    """

    # < 0xFD	1	uint8_t
    # <= 0xFFFF	3	0xFD followed by the length as uint16_t
    # <= 0xFFFF FFFF	5	0xFE followed by the length as uint32_t
    # -	9	0xFF followed by the length as uint64_t

    def __bytes__(self):
        if self < 0xFD:
            assert self >= 0
            return struct.pack('<B', self)
        elif self < 0xFFFF:
            return b'\xFD' + struct.pack('<H', self)
        elif self < 0xFFFFFFFF:
            return b'\xFE' + struct.pack('<L', self)
        else:
            assert self <= 0xFFFFFFFFFFFFFFFF
            return b'\xFF' + struct.pack('<Q', self)

    @classmethod
    def from_bytes(cls, value: bytes):
        if value[0] < 0xFD:
            n, = struct.unpack('<B', value)
        elif value[0] == 0xFD:
            n, = struct.unpack_from('<H', value, 1)
        elif value[0] == 0xFE:
            n, = struct.unpack_from('<L', value, 1)
        else:  # elif value[0] == 0xFF:
            n, = struct.unpack_from('<Q', value, 1)

        return cls(n)


class Message:
    pass


class Node:
    SEEDS = ['seed.bitcoin.sipa.be',
             'dnsseed.bluematt.me',
             'dnsseed.bitcoin.dashjr.org',
             'seed.bitcoinstats.com',
             'seed.bitcoin.jonasschnelli.ch',
             'seed.btc.petertodd.org']

    async def resolve_seeds(self, seeds=SEEDS):
        loop = asyncio.get_event_loop()
        return await asyncio.gather(*[loop.getaddrinfo(seed, 8333, proto=socket.IPPROTO_TCP) for seed in seeds])


class BlockHeader(struct.Struct):
    pass
    # magic = 0xD9B4BEF9
    # block_size 4 bytes
    # header
    #   version
    #   hash_prev_block - 32 bytes
    #   hash_merkle_root - 32 bytes
    #   time
    #   bits
    #   nonce
