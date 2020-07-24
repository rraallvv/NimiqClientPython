__all__ = [
    "NimiqClient",
    "WrongFormatException",
    "BadMethodCallException",
    "ConsensusState",
    "AccountType",
    "LogLevel",
    "PeerAddressState",
    "PeerConnectionState",
    "PeerStateCommand",
    "PoolConnectionState"
]

import requests
from requests.auth import HTTPBasicAuth
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ConsensusState(str, Enum):
    """
    Consensus state returned by the server.
    """
    CONNECTING = "connecting" # Connecting.
    SYNCING = "syncing" # Syncing blocks.
    ESTABLISHED = "established" # Consensus established.

class AccountType(int, Enum):
    """
    Type of a Nimiq account.
    """
    BASIC = 0 # Normal Nimiq account.
    VESTING = 1 # Vesting contract.
    HTLC = 2 # Hashed Timelock Contract.

class LogLevel(str, Enum):
    """
    Used to set the log level in the JSONRPC server.
    """
    TRACE = "trace" # Trace level log.
    VERBOSE = "verbose" # Verbose level log.
    DEBUG = "debug" # Debugging level log.
    INFO = "info" # Info level log.
    WARN = "warn" # Warning level log.
    ERROR = "error" # Error level log.
    ASSERT = "assert" # Assertions level log.

class PeerAddressState(int, Enum):
    """
    Peer address state returned by the server.
    """
    NEW = 1 # New peer.
    ESTABLISHED = 2 # Established peer.
    TRIED = 3 # Already tried peer.
    FAILED = 4 # Peer failed.
    BANNED = 5 # Balled peer.

class PeerConnectionState(int, Enum):
    """
    Peer connection state returned by the server.
    """
    NEW = 1 # New connection.
    CONNECTING = 2 # Connecting.
    CONNECTED = 3 # Connected.
    NEGOTIATING = 4 # Negotiating connection.
    ESTABLISHED = 5 # Connection established.
    CLOSED = 6 # Connection closed.

class PeerStateCommand(str, Enum):
    """
    Commands to change the state of a peer.
    """
    CONNECT = "connect" # Connect.
    DISCONNECT = "disconnect" # Disconnect.
    BAN = "ban" # Ban.
    UNBAN = "unban" # Unban.

class PoolConnectionState(int, Enum):
    """
    Pool connection state information returned by the server.
    """
    CONNECTED = 0 # Connected.
    CONNECTING = 1 # Connecting.
    CLOSED = 2 # Closed.

class WrongFormatException(Exception):
    """ The client couldn't parse the JSON object. """
    pass

class BadMethodCallException(Exception):
    """ The server didn't recognize the method. """
    def __init__(self, message, code):
        super(BadMethodCallException, self).__init__("{} ({})".format(message, code))

class NimiqClient:
    """
    API client for the Nimiq JSON RPC server.
    """

    def __init__(self, scheme="http", user="", password="", host="127.0.0.1", port=8648, session=None):
        """
        Client initialization.
        :param scheme: Protocol squeme, "http" or "https".
        :param user: Authorized user.
        :param password: Password for the authorized user.
        :param host: Host IP address.
        :param port: Host port.
        :param session: Used to make all requests. If ommited the shared URLSession is used.
        """
        self.id = 0 # Number in the sequence for the of the next request.
        self.url = "{}://{}:{}".format(scheme, host, port) # URL of the JSONRPC server.
        self.auth = HTTPBasicAuth(user, password) # Base64 string containing authentication parameters.
        if session is None:
            session = requests.Session()
        self.session = session # requests Session instance used in requests sent to the JSONRPC server.

    def fetch(self, method, *args):
        """
        Used in all JSONRPC requests to fetch the data.
        :param method: JSONRPC method.
        :param params: Parameters used by the request.
        :retur: If succesfull, returns the model reperestation of the result, None otherwise.
        """

        # make JSON object to send to the server
        call_object = {
            "jsonrpc": "2.0",
            "method": method,
            "params": args,
            "id": self.id
        }

        logger.info("Request: {}".format(call_object))

        # make request
        try:
            resp_object = self.session.post(
                self.url,
                json = call_object,
                auth = self.auth
            ).json()

            logger.info("Response: {}".format(resp_object))

        # raise if there are any errors
        except Exception as error:
            raise WrongFormatException(error)

        error = resp_object.get("error")
        if error is not None:
            raise BadMethodCallException(error.get("message"), error.get("code"))

        # increase the JSONRPC client request id for the next request
        self.id += 1

        return resp_object.get("result")

    def accounts(self):
        """
        Returns a list of addresses owned by client.
        :return: Array of Accounts owned by the client.
        """
        return self.fetch("accounts", [])

    def blockNumber(self):
        """
        Returns the height of most recent block.
        :return: The current block height the client is on.
        """
        return self.fetch("blockNumber", [])

    def consensus(self):
        """
        Returns information on the current consensus state.
        :return: Consensus state. "established" is the value for a good state, other values indicate bad.
        """
        return self.fetch("consensus", [])

    def constant(self, constant, value = None):
        """
        Returns or overrides a constant value.
        When no parameter is given, it returns the value of the constant. When giving a value as parameter,
        it sets the constant to the given value. To reset the constant use resetConstant() instead.
        :param string: The class and name of the constant (format should be "Class.CONSTANT").
        :param value: The new value of the constant.
        :return: The value of the constant.
        """
        params = [constant]
        if value != None:
            params.append(value)
        return self.fetch("constant", params)

    def createAccount(self):
        """
        Creates a new account and stores its private key in the client store.
        :return: Information on the wallet that was created using the command.
        """
        return self.fetch("createAccount", [])

    def createRawTransaction(self, transaction):
        """
        Creates and signs a transaction without sending it. The transaction can then be send via sendRawTransaction() without accidentally replaying it.
        :param transaction: The transaction object.
        :return: Hex-encoded transaction.
        """
        return self.fetch("createRawTransaction", [transaction])

    def getAccount(self, address):
        """
        Returns details for the account of given address.
        :param address: Address to get account details.
        :return: Details about the account. Returns the default empty basic account for non-existing accounts.
        """
        return self.fetch("getAccount", [address])

    def getBalance(self, address):
        """
        Returns the balance of the account of given address.
        :param address: Address to check for balance.
        :return: The current balance at the specified address (in smalest unit).
        """
        return self.fetch("getBalance", [address])

    def getBlockByHash(self, hash, fullTransactions = False):
        """
        Returns information about a block by hash.
        :param hash: Hash of the block to gather information on.
        :param fullTransactions: If True it returns the full transaction objects, if False only the hashes of the transactions.
        :return: A block object or None when no block was found.
        """
        return self.fetch("getBlockByHash", [hash, fullTransactions])

    def getBlockByNumber(self, height, fullTransactions = False):
        """
        Returns information about a block by block number.
        :param height: The height of the block to gather information on.
        :param fullTransactions: If True it returns the full transaction objects, if False only the hashes of the transactions.
        :return: A block object or None when no block was found.
        """
        return self.fetch("getBlockByNumber", [height, fullTransactions])

    def getBlockTemplate(self, address = None, extraData = ""):
        """
        Returns a template to build the next block for mining. This will consider pool instructions when connected to a pool.
        If address and extraData are provided the values are overriden.
        :param address: The address to use as a miner for this block. This overrides the address provided during startup or from the pool.
        :param extraData: Hex-encoded value for the extra data field. This overrides the extra data provided during startup or from the pool.
        :return: A block template object.
        """
        params = []
        if address != None:
            params.append(address)
            params.append(extraData)
        return self.fetch("getBlockTemplate", params)

    def getBlockTransactionCountByHash(self, hash):
        """
        Returns the number of transactions in a block from a block matching the given block hash.
        :param hash: Hash of the block.
        :return: Number of transactions in the block found, or None, when no block was found.
        """
        return self.fetch("getBlockTransactionCountByHash", [hash])

    def getBlockTransactionCountByNumber(self, height):
        """
        Returns the number of transactions in a block matching the given block number.
        :param height: Height of the block.
        :return: Number of transactions in the block found, or None, when no block was found.
        """
        return self.fetch("getBlockTransactionCountByNumber", [height])

    def getTransactionByBlockHashAndIndex(self, hash, index):
        """
        Returns information about a transaction by block hash and transaction index position.
        :param hash: Hash of the block containing the transaction.
        :param index: Index of the transaction in the block.
        :return: A transaction object or None when no transaction was found.
        """
        return self.fetch("getTransactionByBlockHashAndIndex", [hash, index])

    def getTransactionByBlockNumberAndIndex(self, height, index):
        """
        Returns information about a transaction by block number and transaction index position.
        :param height: Height of the block containing the transaction.
        :param index: Index of the transaction in the block.
        :return: A transaction object or None when no transaction was found.
        """
        return self.fetch("getTransactionByBlockNumberAndIndex", [height, index])

    def getTransactionByHash(self, hash):
        """
        Returns the information about a transaction requested by transaction hash.
        :param hash: Hash of a transaction.
        :return: A transaction object or None when no transaction was found.
        """
        return self.fetch("getTransactionByHash", [hash])

    def getTransactionReceipt(self, hash):
        """
        Returns the receipt of a transaction by transaction hash.
        :param hash: Hash of a transaction.
        :return: A transaction receipt object, or None when no receipt was found.
        """
        return self.fetch("getTransactionReceipt", [hash])

    def getTransactionsByAddress(self, address, numberOfTransactions = 1000):
        """
        Returns the latest transactions successfully performed by or for an address.
        Note that this information might change when blocks are rewinded on the local state due to forks.
        :param address: Address of which transactions should be gathered.
        :param numberOfTransactions: Number of transactions that shall be returned.
        :return: Array of transactions linked to the requested address.
        """
        return self.fetch("getTransactionsByAddress", [address, numberOfTransactions])

    def getWork(self, address = None, extraData = ""):
        """
        Returns instructions to mine the next block. This will consider pool instructions when connected to a pool.
        :param address: The address to use as a miner for this block. This overrides the address provided during startup or from the pool.
        :param extraData: Hex-encoded value for the extra data field. This overrides the extra data provided during startup or from the pool.
        :return: Mining work instructions.
        """
        params = []
        if address != None:
            params.append(address)
            params.append(extraData)
        return self.fetch("getWork", params)

    def hashrate(self):
        """
        Returns the number of hashes per second that the node is mining with.
        :return: Number of hashes per second.
        """
        return self.fetch("hashrate", [])

    def log(self, tag, level):
        """
        Sets the log level of the node.
        :param tag: Tag: If "*" the log level is set globally, otherwise the log level is applied only on this tag.
        :param level: Minimum log level to display.
        :return: True if the log level was changed, False otherwise.
        """
        return self.fetch("log", [tag, level])

    def mempool(self):
        """
        Returns information on the current mempool situation. This will provide an overview of the number of transactions sorted into buckets based on their fee per byte (in smallest unit).
        :return: Mempool information.
        """
        result = self.fetch("mempool", [])
        transactionsPerBucket = {}
        for key, value in list(result.items()):
            if key.isdigit():
                transactionsPerBucket[int(key)] = value
                del result[key]
        result["transactionsPerBucket"] = transactionsPerBucket
        return result

    def mempoolContent(self, fullTransactions = False):
        """
        Returns transactions that are currently in the mempool.
        :param fullTransactions: If True includes full transactions, if False includes only transaction hashes.
        :return: Array of transactions (either represented by the transaction hash or a transaction object).
        """
        return self.fetch("mempoolContent", [fullTransactions])

    def minerAddress(self):
        """
        Returns the miner address.
        :return: The miner address configured on the node.
        """
        return self.fetch("minerAddress", [])

    def minerThreads(self, threads = None):
        """
        Returns or sets the number of CPU threads for the miner.
        When no parameter is given, it returns the current number of miner threads.
        When a value is given as parameter, it sets the number of miner threads to that value.
        :param threads: The number of threads to allocate for mining.
        :return: The number of threads allocated for mining.
        """
        params = []
        if threads != None:
            params.append(threads)
        return self.fetch("minerThreads", params)

    def minFeePerByte(self, fee = None):
        """
        Returns or sets the minimum fee per byte.
        When no parameter is given, it returns the current minimum fee per byte.
        When a value is given as parameter, it sets the minimum fee per byte to that value.
        :param fee: The new minimum fee per byte.
        :return: The new minimum fee per byte.
        """
        params = []
        if fee != None:
            params.append(fee)
        return self.fetch("minFeePerByte", params)

    def mining(self, state = None):
        """
        Returns true if client is actively mining new blocks.
        When no parameter is given, it returns the current state.
        When a value is given as parameter, it sets the current state to that value.
        :param state: The state to be set.
        :return: True if the client is mining, otherwise False.
        """
        params = []
        if state != None:
            params.append(state)
        return self.fetch("mining", params)

    def peerCount(self):
        """
        Returns number of peers currently connected to the client.
        :return: Number of connected peers.
        """
        return self.fetch("peerCount", [])

    def peerList(self):
        """
        Returns list of peers known to the client.
        :return: The list of peers.
        """
        return self.fetch("peerList", [])

    def peerState(self, address, command = None):
        """
        Returns the state of the peer.
        When no command is given, it returns peer state.
        When a value is given for command, it sets the peer state to that value.
        :param address: The address of the peer.
        :param command: The command to send.
        :return: The current state of the peer.
        """
        params = []
        params.append(address)
        if command != None:
            params.append(command)
        return self.fetch("peerState", params)

    def pool(self, address = None):
        """
        Returns or sets the mining pool.
        When no parameter is given, it returns the current mining pool.
        When a value is given as parameter, it sets the mining pool to that value.
        :param address: The mining pool connection string ("url:port") or boolean to enable/disable pool mining.
        :return: The mining pool connection string, or None if not enabled.
        """
        params = []
        if address != None:
            params.append(address)
        return self.fetch("pool", params)

    def poolConfirmedBalance(self):
        """
        Returns the confirmed mining pool balance.
        :return: The confirmed mining pool balance (in smallest unit).
        """
        return self.fetch("poolConfirmedBalance", [])

    def poolConnectionState(self):
        """
        Returns the connection state to mining pool.
        :return: The mining pool connection state.
        """
        return self.fetch("poolConnectionState", [])

    def sendRawTransaction(self, transaction):
        """
        Sends a signed message call transaction or a contract creation, if the data field contains code.
        :param transaction: The hex encoded signed transaction
        :return: The Hex-encoded transaction hash.
        """
        return self.fetch("sendRawTransaction", [transaction])

    def sendTransaction(self, transaction):
        """
        Creates new message call transaction or a contract creation, if the data field contains code.
        :param transaction: The hex encoded signed transaction
        :return: The Hex-encoded transaction hash.
        """
        return self.fetch("sendTransaction", [transaction])

    def submitBlock(self, block):
        """
        Submits a block to the node. When the block is valid, the node will forward it to other nodes in the network.
        :param block: Hex-encoded full block (including header, interlink and body). When submitting work from getWork, remember to include the suffix.
        :return: Always None.
        """
        return self.fetch("submitBlock", [block])

    def syncing(self):
        """
        Returns an object with data about the sync status or False.
        :return: An object with sync status data or False, when not syncing.
        """
        return self.fetch("syncing", [])

    def getRawTransactionInfo(self, transaction):
        """
        Deserializes hex-encoded transaction and returns a transaction object.
        :param transaction: The hex encoded signed transaction.
        :return: The transaction object.
        """
        return self.fetch("getRawTransactionInfo", [transaction])

    def resetConstant(self, constant):
        """
        Resets the constant to default value.
        :param constant: Name of the constant.
        :return: The new value of the constant.
        """
        return self.fetch("constant", [constant, "reset"])
