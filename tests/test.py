from nimiqclient import *
import unittest
from fixtures import Fixtures
from session_stub import SessionStub

class TestStringMethods(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        cls.client = NimiqClient(scheme = "http", user = "", password = "", host = "127.0.0.1", port = 8648, session = SessionStub())

    @classmethod
    def tearDownClass(cls):
        pass

    def test_peerCount(self):
        SessionStub.testData = Fixtures.peerCount()

        result = self.client.peerCount()

        self.assertEqual("peerCount", SessionStub.latestRequestMethod)

        self.assertEqual(6, result)

    def test_syncingStateWhenSyncing(self):
        SessionStub.testData = Fixtures.syncing()

        result = self.client.syncing()

        self.assertEqual("syncing", SessionStub.latestRequestMethod)

        self.assertIsNot(type(result), bool)
        self.assertEqual(578430, result.get("startingBlock"))
        self.assertEqual(586493, result.get("currentBlock"))
        self.assertEqual(586493, result.get("highestBlock"))

    def test_syncingStateWhenNotSyncing(self):
        SessionStub.testData = Fixtures.syncingNotSyncing()

        result = self.client.syncing()

        self.assertEqual("syncing", SessionStub.latestRequestMethod)

        self.assertIs(type(result), bool)
        self.assertEqual(False, result)

    def test_consensusState(self):
        SessionStub.testData = Fixtures.consensusSyncing()

        result = self.client.consensus()

        self.assertEqual("consensus", SessionStub.latestRequestMethod)

        self.assertEqual(ConsensusState.SYNCING, result)

    def test_peerListWithPeers(self):
        SessionStub.testData = Fixtures.peerList()

        result = self.client.peerList()

        self.assertEqual("peerList", SessionStub.latestRequestMethod)

        self.assertEqual(len(result), 2)
        self.assertIsNotNone(result[0])
        self.assertEqual("b99034c552e9c0fd34eb95c1cdf17f5e", result[0].get("id"))
        self.assertEqual("wss://seed1.nimiq-testnet.com:8080/b99034c552e9c0fd34eb95c1cdf17f5e", result[0].get("address"))
        self.assertEqual(PeerAddressState.ESTABLISHED, result[0].get("addressState"))
        self.assertEqual(PeerConnectionState.ESTABLISHED, result[0].get("connectionState"))

        self.assertIsNotNone(result[1])
        self.assertEqual("e37dca72802c972d45b37735e9595cf0", result[1].get("id"))
        self.assertEqual("wss://seed4.nimiq-testnet.com:8080/e37dca72802c972d45b37735e9595cf0", result[1].get("address"))
        self.assertEqual(PeerAddressState.FAILED, result[1].get("addressState"))
        self.assertEqual(None, result[1].get("connectionState"))

    def test_peerListWhenEmpty(self):
        SessionStub.testData = Fixtures.peerListEmpty()

        result = self.client.peerList()

        self.assertEqual("peerList", SessionStub.latestRequestMethod)

        self.assertEqual(len(result), 0)

    def test_peerNormal(self):
        SessionStub.testData = Fixtures.peerStateNormal()

        result = self.client.peerState("wss://seed1.nimiq-testnet.com:8080/b99034c552e9c0fd34eb95c1cdf17f5e")

        self.assertEqual("peerState", SessionStub.latestRequestMethod)
        self.assertEqual("wss://seed1.nimiq-testnet.com:8080/b99034c552e9c0fd34eb95c1cdf17f5e", SessionStub.latestRequestParams[0])

        self.assertIsNotNone(result)
        self.assertEqual("b99034c552e9c0fd34eb95c1cdf17f5e", result.get("id"))
        self.assertEqual("wss://seed1.nimiq-testnet.com:8080/b99034c552e9c0fd34eb95c1cdf17f5e", result.get("address"))
        self.assertEqual(PeerAddressState.ESTABLISHED, result.get("addressState"))
        self.assertEqual(PeerConnectionState.ESTABLISHED, result.get("connectionState"))

    def test_peerFailed(self):
        SessionStub.testData = Fixtures.peerStateFailed()

        result = self.client.peerState("wss://seed4.nimiq-testnet.com:8080/e37dca72802c972d45b37735e9595cf0")

        self.assertEqual("peerState", SessionStub.latestRequestMethod)
        self.assertEqual("wss://seed4.nimiq-testnet.com:8080/e37dca72802c972d45b37735e9595cf0", SessionStub.latestRequestParams[0])

        self.assertIsNotNone(result)
        self.assertEqual("e37dca72802c972d45b37735e9595cf0", result.get("id"))
        self.assertEqual("wss://seed4.nimiq-testnet.com:8080/e37dca72802c972d45b37735e9595cf0", result.get("address"))
        self.assertEqual(PeerAddressState.FAILED, result.get("addressState"))
        self.assertEqual(None, result.get("connectionState"))

    def test_peerError(self):
        SessionStub.testData = Fixtures.peerStateError()

        self.assertRaises(BadMethodCallException, self.client.peerState, "unknown")

    def test_setPeerNormal(self):
        SessionStub.testData = Fixtures.peerStateNormal()

        result = self.client.peerState("wss://seed1.nimiq-testnet.com:8080/b99034c552e9c0fd34eb95c1cdf17f5e", PeerStateCommand.CONNECT)

        self.assertEqual("peerState", SessionStub.latestRequestMethod)
        self.assertEqual("wss://seed1.nimiq-testnet.com:8080/b99034c552e9c0fd34eb95c1cdf17f5e", SessionStub.latestRequestParams[0])
        self.assertEqual("connect", SessionStub.latestRequestParams[1])

        self.assertIsNotNone(result)
        self.assertEqual("b99034c552e9c0fd34eb95c1cdf17f5e", result.get("id"))
        self.assertEqual("wss://seed1.nimiq-testnet.com:8080/b99034c552e9c0fd34eb95c1cdf17f5e", result.get("address"))
        self.assertEqual(PeerAddressState.ESTABLISHED, result.get("addressState"))
        self.assertEqual(PeerConnectionState.ESTABLISHED, result.get("connectionState"))

    def test_sendRawTransaction(self):
        SessionStub.testData = Fixtures.sendTransaction()

        result = self.client.sendRawTransaction("00c3c0d1af80b84c3b3de4e3d79d5c8cc950e044098c969953d68bf9cee68d7b53305dbaac7514a06dae935e40d599caf1bd8a243c00000000000000010000000000000001000dc2e201b5a1755aec80aa4227d5afc6b0de0fcfede8541f31b3c07b9a85449ea9926c1c958628d85a2b481556034ab3d67ff7de28772520813c84aaaf8108f6297c580c")

        self.assertEqual("sendRawTransaction", SessionStub.latestRequestMethod)
        self.assertEqual("00c3c0d1af80b84c3b3de4e3d79d5c8cc950e044098c969953d68bf9cee68d7b53305dbaac7514a06dae935e40d599caf1bd8a243c00000000000000010000000000000001000dc2e201b5a1755aec80aa4227d5afc6b0de0fcfede8541f31b3c07b9a85449ea9926c1c958628d85a2b481556034ab3d67ff7de28772520813c84aaaf8108f6297c580c", SessionStub.latestRequestParams[0])

        self.assertEqual("81cf3f07b6b0646bb16833d57cda801ad5957e264b64705edeef6191fea0ad63", result)

    def test_createRawTransaction(self):
        SessionStub.testData = Fixtures.createRawTransactionBasic()

        transaction = {
            "from": "NQ39 NY67 X0F0 UTQE 0YER 4JEU B67L UPP8 G0FM",
            "fromType": AccountType.BASIC,
            "to": "NQ16 61ET MB3M 2JG6 TBLK BR0D B6EA X6XQ L91U",
            "toType": AccountType.BASIC,
            "value": 100000,
            "fee": 1,
            "data": None
        }

        result = self.client.createRawTransaction(transaction)

        self.assertEqual("createRawTransaction", SessionStub.latestRequestMethod)

        param = SessionStub.latestRequestParams[0]
        self.assertEqual(param, {
            "from": "NQ39 NY67 X0F0 UTQE 0YER 4JEU B67L UPP8 G0FM",
            "fromType": 0,
            "to": "NQ16 61ET MB3M 2JG6 TBLK BR0D B6EA X6XQ L91U",
            "toType": 0,
            "value": 100000,
            "fee": 1,
            "data": None
        })

        self.assertEqual("00c3c0d1af80b84c3b3de4e3d79d5c8cc950e044098c969953d68bf9cee68d7b53305dbaac7514a06dae935e40d599caf1bd8a243c00000000000186a00000000000000001000af84c01239b16cee089836c2af5c7b1dbb22cdc0b4864349f7f3805909aa8cf24e4c1ff0461832e86f3624778a867d5f2ba318f92918ada7ae28d70d40c4ef1d6413802", result)

    def test_sendTransaction(self):
        SessionStub.testData = Fixtures.sendTransaction()

        transaction = {
            "from": "NQ39 NY67 X0F0 UTQE 0YER 4JEU B67L UPP8 G0FM",
            "fromType": AccountType.BASIC,
            "to": "NQ16 61ET MB3M 2JG6 TBLK BR0D B6EA X6XQ L91U",
            "toType": AccountType.BASIC,
            "value": 1,
            "fee": 1,
            "data": None
        }

        result = self.client.sendTransaction(transaction)

        self.assertEqual("sendTransaction", SessionStub.latestRequestMethod)

        param = SessionStub.latestRequestParams[0]
        self.assertEqual(param, {
            "from": "NQ39 NY67 X0F0 UTQE 0YER 4JEU B67L UPP8 G0FM",
            "fromType": 0,
            "to": "NQ16 61ET MB3M 2JG6 TBLK BR0D B6EA X6XQ L91U",
            "toType": 0,
            "value": 1,
            "fee": 1,
            "data": None
        })

        self.assertEqual("81cf3f07b6b0646bb16833d57cda801ad5957e264b64705edeef6191fea0ad63", result)

    def test_getRawTransactionInfo(self):
        SessionStub.testData = Fixtures.getRawTransactionInfoBasic()

        result = self.client.getRawTransactionInfo("00c3c0d1af80b84c3b3de4e3d79d5c8cc950e044098c969953d68bf9cee68d7b53305dbaac7514a06dae935e40d599caf1bd8a243c00000000000186a00000000000000001000af84c01239b16cee089836c2af5c7b1dbb22cdc0b4864349f7f3805909aa8cf24e4c1ff0461832e86f3624778a867d5f2ba318f92918ada7ae28d70d40c4ef1d6413802")

        self.assertEqual("getRawTransactionInfo", SessionStub.latestRequestMethod)
        self.assertEqual("00c3c0d1af80b84c3b3de4e3d79d5c8cc950e044098c969953d68bf9cee68d7b53305dbaac7514a06dae935e40d599caf1bd8a243c00000000000186a00000000000000001000af84c01239b16cee089836c2af5c7b1dbb22cdc0b4864349f7f3805909aa8cf24e4c1ff0461832e86f3624778a867d5f2ba318f92918ada7ae28d70d40c4ef1d6413802", SessionStub.latestRequestParams[0])

        self.assertIsNotNone(result)
        self.assertEqual("7784f2f6eaa076fa5cf0e4d06311ad204b2f485de622231785451181e8129091", result.get("hash"))
        self.assertEqual("b7cc7f01e0e6f0e07dd9249dc598f4e5ee8801f5", result.get("from"))
        self.assertEqual("NQ39 NY67 X0F0 UTQE 0YER 4JEU B67L UPP8 G0FM", result.get("fromAddress"))
        self.assertEqual("305dbaac7514a06dae935e40d599caf1bd8a243c", result.get("to"))
        self.assertEqual("NQ16 61ET MB3M 2JG6 TBLK BR0D B6EA X6XQ L91U", result.get("toAddress"))
        self.assertEqual(100000, result.get("value"))
        self.assertEqual(1, result.get("fee"))

    def test_getTransactionByBlockHashAndIndex(self):
        SessionStub.testData = Fixtures.getTransactionFull()

        result = self.client.getTransactionByBlockHashAndIndex("bc3945d22c9f6441409a6e539728534a4fc97859bda87333071fad9dad942786", 0)

        self.assertEqual("getTransactionByBlockHashAndIndex", SessionStub.latestRequestMethod)
        self.assertEqual("bc3945d22c9f6441409a6e539728534a4fc97859bda87333071fad9dad942786", SessionStub.latestRequestParams[0])
        self.assertEqual(0, SessionStub.latestRequestParams[1])

        self.assertIsNotNone(result)
        self.assertEqual("78957b87ab5546e11e9540ce5a37ebbf93a0ebd73c0ce05f137288f30ee9f430", result.get("hash"))
        self.assertEqual("bc3945d22c9f6441409a6e539728534a4fc97859bda87333071fad9dad942786", result.get("blockHash"))
        self.assertEqual(0, result.get("transactionIndex"))
        self.assertEqual("355b4fe2304a9c818b9f0c3c1aaaf4ad4f6a0279", result.get("from"))
        self.assertEqual("NQ16 6MDL YQHG 9AE8 32UY 1GX1 MAPL MM7N L0KR", result.get("fromAddress"))
        self.assertEqual("4f61c06feeb7971af6997125fe40d629c01af92f", result.get("to"))
        self.assertEqual("NQ05 9VGU 0TYE NXBH MVLR E4JY UG6N 5701 MX9F", result.get("toAddress"))
        self.assertEqual(2636710000, result.get("value"))
        self.assertEqual(0, result.get("fee"))

    def test_getTransactionByBlockHashAndIndexWhenNotFound(self):
        SessionStub.testData = Fixtures.getTransactionNotFound()

        result = self.client.getTransactionByBlockHashAndIndex("bc3945d22c9f6441409a6e539728534a4fc97859bda87333071fad9dad942786", 5)

        self.assertEqual("getTransactionByBlockHashAndIndex", SessionStub.latestRequestMethod)
        self.assertEqual("bc3945d22c9f6441409a6e539728534a4fc97859bda87333071fad9dad942786", SessionStub.latestRequestParams[0])
        self.assertEqual(5, SessionStub.latestRequestParams[1])

        self.assertIsNone(result)

    def test_getTransactionByBlockNumberAndIndex(self):
        SessionStub.testData = Fixtures.getTransactionFull()

        result = self.client.getTransactionByBlockNumberAndIndex(11608, 0)

        self.assertEqual("getTransactionByBlockNumberAndIndex", SessionStub.latestRequestMethod)
        self.assertEqual(11608, SessionStub.latestRequestParams[0])
        self.assertEqual(0, SessionStub.latestRequestParams[1])

        self.assertIsNotNone(result)
        self.assertEqual("78957b87ab5546e11e9540ce5a37ebbf93a0ebd73c0ce05f137288f30ee9f430", result.get("hash"))
        self.assertEqual(11608, result.get("blockNumber"))
        self.assertEqual(0, result.get("transactionIndex"))
        self.assertEqual("355b4fe2304a9c818b9f0c3c1aaaf4ad4f6a0279", result.get("from"))
        self.assertEqual("NQ16 6MDL YQHG 9AE8 32UY 1GX1 MAPL MM7N L0KR", result.get("fromAddress"))
        self.assertEqual("4f61c06feeb7971af6997125fe40d629c01af92f", result.get("to"))
        self.assertEqual("NQ05 9VGU 0TYE NXBH MVLR E4JY UG6N 5701 MX9F", result.get("toAddress"))
        self.assertEqual(2636710000, result.get("value"))
        self.assertEqual(0, result.get("fee"))

    def test_getTransactionByBlockNumberAndIndexWhenNotFound(self):
        SessionStub.testData = Fixtures.getTransactionNotFound()

        result = self.client.getTransactionByBlockNumberAndIndex(11608, 0)

        self.assertEqual("getTransactionByBlockNumberAndIndex", SessionStub.latestRequestMethod)
        self.assertEqual(11608, SessionStub.latestRequestParams[0])
        self.assertEqual(0, SessionStub.latestRequestParams[1])

        self.assertIsNone(result)

    def test_getTransactionByHash(self):
        SessionStub.testData = Fixtures.getTransactionFull()

        result = self.client.getTransactionByHash("78957b87ab5546e11e9540ce5a37ebbf93a0ebd73c0ce05f137288f30ee9f430")

        self.assertEqual("getTransactionByHash", SessionStub.latestRequestMethod)
        self.assertEqual("78957b87ab5546e11e9540ce5a37ebbf93a0ebd73c0ce05f137288f30ee9f430", SessionStub.latestRequestParams[0])

        self.assertIsNotNone(result)
        self.assertEqual("78957b87ab5546e11e9540ce5a37ebbf93a0ebd73c0ce05f137288f30ee9f430", result.get("hash"))
        self.assertEqual(11608, result.get("blockNumber"))
        self.assertEqual("355b4fe2304a9c818b9f0c3c1aaaf4ad4f6a0279", result.get("from"))
        self.assertEqual("NQ16 6MDL YQHG 9AE8 32UY 1GX1 MAPL MM7N L0KR", result.get("fromAddress"))
        self.assertEqual("4f61c06feeb7971af6997125fe40d629c01af92f", result.get("to"))
        self.assertEqual("NQ05 9VGU 0TYE NXBH MVLR E4JY UG6N 5701 MX9F", result.get("toAddress"))
        self.assertEqual(2636710000, result.get("value"))
        self.assertEqual(0, result.get("fee"))

    def test_getTransactionByHashWhenNotFound(self):
        SessionStub.testData = Fixtures.getTransactionNotFound()

        result = self.client.getTransactionByHash("78957b87ab5546e11e9540ce5a37ebbf93a0ebd73c0ce05f137288f30ee9f430")

        self.assertEqual("getTransactionByHash", SessionStub.latestRequestMethod)
        self.assertEqual("78957b87ab5546e11e9540ce5a37ebbf93a0ebd73c0ce05f137288f30ee9f430", SessionStub.latestRequestParams[0])

        self.assertIsNone(result)

    def test_getTransactionByHashForContractCreation(self):
        SessionStub.testData = Fixtures.getTransactionContractCreation()

        result = self.client.getTransactionByHash("539f6172b19f63be376ab7e962c368bb5f611deff6b159152c4cdf509f7daad2")

        self.assertEqual("getTransactionByHash", SessionStub.latestRequestMethod)
        self.assertEqual("539f6172b19f63be376ab7e962c368bb5f611deff6b159152c4cdf509f7daad2", SessionStub.latestRequestParams[0])

        self.assertIsNotNone(result)
        self.assertEqual("539f6172b19f63be376ab7e962c368bb5f611deff6b159152c4cdf509f7daad2", result.get("hash"))
        self.assertEqual("96fef80f517f0b2704476dee48da147049b591e8f034e5bf93f1f6935fd51b85", result.get("blockHash"))
        self.assertEqual(1102500, result.get("blockNumber"))
        self.assertEqual(1590148157, result.get("timestamp"))
        self.assertEqual(7115, result.get("confirmations"))
        self.assertEqual("d62d519b3478c63bdd729cf2ccb863178060c64a", result.get("from"))
        self.assertEqual("NQ53 SQNM 36RL F333 PPBJ KKRC RE33 2X06 1HJA", result.get("fromAddress"))
        self.assertEqual("a22eaf17848130c9b370e42ff7d345680df245e1", result.get("to"))
        self.assertEqual("NQ87 L8PA X5U4 G4QC KCTG UGPY FLS5 D06Y 4HF1", result.get("toAddress"))
        self.assertEqual(5000000000, result.get("value"))
        self.assertEqual(0, result.get("fee"))
        self.assertEqual("d62d519b3478c63bdd729cf2ccb863178060c64af5ad55071730d3b9f05989481eefbda7324a44f8030c63b9444960db429081543939166f05116cebc37bd6975ac9f9e3bb43a5ab0b010010d2de", result.get("data"))
        self.assertEqual(1, result.get("flags"))

    def test_getTransactionReceipt(self):
        SessionStub.testData = Fixtures.getTransactionReceiptFound()

        result = self.client.getTransactionReceipt("fd8e46ae55c5b8cd7cb086cf8d6c81f941a516d6148021d55f912fb2ca75cc8e")

        self.assertEqual("getTransactionReceipt", SessionStub.latestRequestMethod)
        self.assertEqual("fd8e46ae55c5b8cd7cb086cf8d6c81f941a516d6148021d55f912fb2ca75cc8e", SessionStub.latestRequestParams[0])

        self.assertIsNotNone(result)
        self.assertEqual("fd8e46ae55c5b8cd7cb086cf8d6c81f941a516d6148021d55f912fb2ca75cc8e", result.get("transactionHash"))
        self.assertEqual(-1, result.get("transactionIndex"))
        self.assertEqual(11608, result.get("blockNumber"))
        self.assertEqual("bc3945d22c9f6441409a6e539728534a4fc97859bda87333071fad9dad942786", result.get("blockHash"))
        self.assertEqual(1523412456, result.get("timestamp"))
        self.assertEqual(718846, result.get("confirmations"))

    def test_getTransactionReceiptWhenNotFound(self):
        SessionStub.testData = Fixtures.getTransactionReceiptNotFound()

        result = self.client.getTransactionReceipt("unknown")

        self.assertEqual("getTransactionReceipt", SessionStub.latestRequestMethod)
        self.assertEqual("unknown", SessionStub.latestRequestParams[0])

        self.assertIsNone(result)

    def test_getTransactionsByAddress(self):
        SessionStub.testData = Fixtures.getTransactionsFound()

        result = self.client.getTransactionsByAddress("NQ05 9VGU 0TYE NXBH MVLR E4JY UG6N 5701 MX9F")

        self.assertEqual("getTransactionsByAddress", SessionStub.latestRequestMethod)
        self.assertEqual("NQ05 9VGU 0TYE NXBH MVLR E4JY UG6N 5701 MX9F", SessionStub.latestRequestParams[0])

        self.assertEqual(3, len(result))
        self.assertIsNotNone(result[0])
        self.assertEqual("a514abb3ee4d3fbedf8a91156fb9ec4fdaf32f0d3d3da3c1dbc5fd1ee48db43e", result[0].get("hash"))
        self.assertIsNotNone(result[1])
        self.assertEqual("c8c0f586b11c7f39873c3de08610d63e8bec1ceaeba5e8a3bb13c709b2935f73", result[1].get("hash"))
        self.assertIsNotNone(result[2])
        self.assertEqual("fd8e46ae55c5b8cd7cb086cf8d6c81f941a516d6148021d55f912fb2ca75cc8e", result[2].get("hash"))

    def test_getTransactionsByAddressWhenNoFound(self):
        SessionStub.testData = Fixtures.getTransactionsNotFound()

        result = self.client.getTransactionsByAddress("NQ10 9VGU 0TYE NXBH MVLR E4JY UG6N 5701 MX9F")

        self.assertEqual("getTransactionsByAddress", SessionStub.latestRequestMethod)
        self.assertEqual("NQ10 9VGU 0TYE NXBH MVLR E4JY UG6N 5701 MX9F", SessionStub.latestRequestParams[0])

        self.assertEqual(0, len(result))

    def test__mempoolContentHashesOnly(self):
        SessionStub.testData = Fixtures.mempoolContentHashesOnly()

        result = self.client.mempoolContent()

        self.assertEqual("mempoolContent", SessionStub.latestRequestMethod)
        self.assertEqual(False, SessionStub.latestRequestParams[0])

        self.assertEqual(3, len(result))
        self.assertIsNotNone(result[0])
        self.assertEqual("5bb722c2afe25c18ba33d453b3ac2c90ac278c595cc92f6188c8b699e8fb006a", result[0])
        self.assertIsNotNone(result[1])
        self.assertEqual("f59a30e0a7e3348ef569225db1f4c29026aeac4350f8c6e751f669eddce0c718", result[1])
        self.assertIsNotNone(result[2])
        self.assertEqual("9cd9c1d0ffcaebfcfe86bc2ae73b4e82a488de99c8e3faef92b05432bb94519c", result[2])

    def test_mempoolContentFullTransactions(self):
        SessionStub.testData = Fixtures.mempoolContentFullTransactions()

        result = self.client.mempoolContent(True)

        self.assertEqual("mempoolContent", SessionStub.latestRequestMethod)
        self.assertEqual(True, SessionStub.latestRequestParams[0])

        self.assertEqual(3, len(result))
        self.assertIsNotNone(result[0])
        self.assertEqual("5bb722c2afe25c18ba33d453b3ac2c90ac278c595cc92f6188c8b699e8fb006a", result[0].get("hash"))
        self.assertIsNotNone(result[1])
        self.assertEqual("f59a30e0a7e3348ef569225db1f4c29026aeac4350f8c6e751f669eddce0c718", result[1].get("hash"))
        self.assertIsNotNone(result[2])
        self.assertEqual("9cd9c1d0ffcaebfcfe86bc2ae73b4e82a488de99c8e3faef92b05432bb94519c", result[2].get("hash"))

    def test_mempoolWhenFull(self):
        SessionStub.testData = Fixtures.mempool()

        result = self.client.mempool()

        self.assertEqual("mempool", SessionStub.latestRequestMethod)

        self.assertIsNotNone(result)
        self.assertEqual(3, result.get("total"))
        self.assertEqual([1], result.get("buckets"))
        self.assertEqual(3, result.get("transactionsPerBucket")[1])

    def test_mempoolWhenEmpty(self):
        SessionStub.testData = Fixtures.mempoolEmpty()

        result = self.client.mempool()

        self.assertEqual("mempool", SessionStub.latestRequestMethod)

        self.assertIsNotNone(result)
        self.assertEqual(0, result.get("total"))
        self.assertEqual([], result.get("buckets"))
        self.assertEqual(0, len(result.get("transactionsPerBucket")))

    def test_minFeePerByte(self):
        SessionStub.testData = Fixtures.minFeePerByte()

        result = self.client.minFeePerByte()

        self.assertEqual("minFeePerByte", SessionStub.latestRequestMethod)

        self.assertEqual(0, result)

    def test_setMinFeePerByte(self):
        SessionStub.testData = Fixtures.minFeePerByte()

        result = self.client.minFeePerByte(0)

        self.assertEqual("minFeePerByte", SessionStub.latestRequestMethod)
        self.assertEqual(0, SessionStub.latestRequestParams[0])

        self.assertEqual(0, result)

    def test_mining(self):
        SessionStub.testData = Fixtures.miningState()

        result = self.client.mining()

        self.assertEqual("mining", SessionStub.latestRequestMethod)

        self.assertEqual(False, result)

    def test_setMining(self):
        SessionStub.testData = Fixtures.miningState()

        result = self.client.mining(False)

        self.assertEqual("mining", SessionStub.latestRequestMethod)
        self.assertEqual(False, SessionStub.latestRequestParams[0])

        self.assertEqual(False, result)

    def test_hashrate(self):
        SessionStub.testData = Fixtures.hashrate()

        result = self.client.hashrate()

        self.assertEqual("hashrate", SessionStub.latestRequestMethod)

        self.assertEqual(52982.2731, result)

    def test_minerThreads(self):
        SessionStub.testData = Fixtures.minerThreads()

        result = self.client.minerThreads()

        self.assertEqual("minerThreads", SessionStub.latestRequestMethod)

        self.assertEqual(2, result)

    def test_setMinerThreads(self):
        SessionStub.testData = Fixtures.minerThreads()

        result = self.client.minerThreads(2)

        self.assertEqual("minerThreads", SessionStub.latestRequestMethod)
        self.assertEqual(2, SessionStub.latestRequestParams[0])

        self.assertEqual(2, result)

    def test_minerAddress(self):
        SessionStub.testData = Fixtures.minerAddress()

        result = self.client.minerAddress()

        self.assertEqual("minerAddress", SessionStub.latestRequestMethod)

        self.assertEqual("NQ39 NY67 X0F0 UTQE 0YER 4JEU B67L UPP8 G0FM", result)

    def test_pool(self):
        SessionStub.testData = Fixtures.poolSushipool()

        result = self.client.pool()

        self.assertEqual("pool", SessionStub.latestRequestMethod)

        self.assertEqual("us.sushipool.com:443", result)

    def test_setPool(self):
        SessionStub.testData = Fixtures.poolSushipool()

        result = self.client.pool("us.sushipool.com:443")

        self.assertEqual("pool", SessionStub.latestRequestMethod)
        self.assertEqual("us.sushipool.com:443", SessionStub.latestRequestParams[0])

        self.assertEqual("us.sushipool.com:443", result)

    def test_getPoolWhenNoPool(self):
        SessionStub.testData = Fixtures.poolNoPool()

        result = self.client.pool()

        self.assertEqual("pool", SessionStub.latestRequestMethod)

        self.assertEqual(None, result)

    def test_poolConnectionState(self):
        SessionStub.testData = Fixtures.poolConnectionState()

        result = self.client.poolConnectionState()

        self.assertEqual("poolConnectionState", SessionStub.latestRequestMethod)

        self.assertEqual(PoolConnectionState.CLOSED, result)

    def test_poolConfirmedBalance(self):
        SessionStub.testData = Fixtures.poolConfirmedBalance()

        result = self.client.poolConfirmedBalance()

        self.assertEqual("poolConfirmedBalance", SessionStub.latestRequestMethod)

        self.assertEqual(12000, result)

    def test_getWork(self):
        SessionStub.testData = Fixtures.getWork()

        result = self.client.getWork()

        self.assertEqual("getWork", SessionStub.latestRequestMethod)

        self.assertEqual("00015a7d47ddf5152a7d06a14ea291831c3fc7af20b88240c5ae839683021bcee3e279877b3de0da8ce8878bf225f6782a2663eff9a03478c15ba839fde9f1dc3dd9e5f0cd4dbc96a30130de130eb52d8160e9197e2ccf435d8d24a09b518a5e05da87a8658ed8c02531f66a7d31757b08c88d283654ed477e5e2fec21a7ca8449241e00d620000dc2fa5e763bda00000000", result.get("data"))
        self.assertEqual("11fad9806b8b4167517c162fa113c09606b44d24f8020804a0f756db085546ff585adfdedad9085d36527a8485b497728446c35b9b6c3db263c07dd0a1f487b1639aa37ff60ba3cf6ed8ab5146fee50a23ebd84ea37dca8c49b31e57d05c9e6c57f09a3b282b71ec2be66c1bc8268b5326bb222b11a0d0a4acd2a93c9e8a8713fe4383e9d5df3b1bf008c535281086b2bcc20e494393aea1475a5c3f13673de2cf7314d201b7cc7f01e0e6f0e07dd9249dc598f4e5ee8801f50000000000", result.get("suffix"))
        self.assertEqual(503371296, result.get("target"))
        self.assertEqual("nimiq-argon2", result.get("algorithm"))

    def test_getWorkWithOverride(self):
        SessionStub.testData = Fixtures.getWork()

        result = self.client.getWork("NQ46 NTNU QX94 MVD0 BBT0 GXAR QUHK VGNF 39ET", "")

        self.assertEqual("getWork", SessionStub.latestRequestMethod)
        self.assertEqual("NQ46 NTNU QX94 MVD0 BBT0 GXAR QUHK VGNF 39ET", SessionStub.latestRequestParams[0])
        self.assertEqual("", SessionStub.latestRequestParams[1])

        self.assertEqual("00015a7d47ddf5152a7d06a14ea291831c3fc7af20b88240c5ae839683021bcee3e279877b3de0da8ce8878bf225f6782a2663eff9a03478c15ba839fde9f1dc3dd9e5f0cd4dbc96a30130de130eb52d8160e9197e2ccf435d8d24a09b518a5e05da87a8658ed8c02531f66a7d31757b08c88d283654ed477e5e2fec21a7ca8449241e00d620000dc2fa5e763bda00000000", result.get("data"))
        self.assertEqual("11fad9806b8b4167517c162fa113c09606b44d24f8020804a0f756db085546ff585adfdedad9085d36527a8485b497728446c35b9b6c3db263c07dd0a1f487b1639aa37ff60ba3cf6ed8ab5146fee50a23ebd84ea37dca8c49b31e57d05c9e6c57f09a3b282b71ec2be66c1bc8268b5326bb222b11a0d0a4acd2a93c9e8a8713fe4383e9d5df3b1bf008c535281086b2bcc20e494393aea1475a5c3f13673de2cf7314d201b7cc7f01e0e6f0e07dd9249dc598f4e5ee8801f50000000000", result.get("suffix"))
        self.assertEqual(503371296, result.get("target"))
        self.assertEqual("nimiq-argon2", result.get("algorithm"))

    def test_getBlockTemplate(self):
        SessionStub.testData = Fixtures.getWorkBlockTemplate()

        result = self.client.getBlockTemplate()

        self.assertEqual("getBlockTemplate", SessionStub.latestRequestMethod)

        self.assertEqual(901883, result.get("header").get("height"))
        self.assertEqual(503371226, result.get("target"))
        self.assertEqual("17e250f1977ae85bdbe09468efef83587885419ee1074ddae54d3fb5a96e1f54", result.get("body").get("hash"))

    def test_getBlockTemplateWithOverride(self):
        SessionStub.testData = Fixtures.getWorkBlockTemplate()

        result = self.client.getBlockTemplate("NQ46 NTNU QX94 MVD0 BBT0 GXAR QUHK VGNF 39ET", "")

        self.assertEqual("getBlockTemplate", SessionStub.latestRequestMethod)
        self.assertEqual("NQ46 NTNU QX94 MVD0 BBT0 GXAR QUHK VGNF 39ET", SessionStub.latestRequestParams[0])
        self.assertEqual("", SessionStub.latestRequestParams[1])

        self.assertEqual(901883, result.get("header").get("height"))
        self.assertEqual(503371226, result.get("target"))
        self.assertEqual("17e250f1977ae85bdbe09468efef83587885419ee1074ddae54d3fb5a96e1f54", result.get("body").get("hash"))

    def test_submitBlock(self):
        SessionStub.testData = Fixtures.submitBlock()

        blockHex = "000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f6ba2bbf7e1478a209057000471d73fbdc28df0b717747d929cfde829c4120f62e02da3d162e20fa982029dbde9cc20f6b431ab05df1764f34af4c62a4f2b33f1f010000000000015ac3185f000134990001000000000000000000000000000000000000000007546573744e657400000000"

        self.client.submitBlock(blockHex)

        self.assertEqual("submitBlock", SessionStub.latestRequestMethod)
        self.assertEqual(blockHex, SessionStub.latestRequestParams[0])

    def test_accounts(self):
        SessionStub.testData = Fixtures.accounts()

        result = self.client.accounts()

        self.assertEqual(SessionStub.latestRequestMethod, "accounts")

        self.assertEqual(3, len(result))

        self.assertIsNotNone(result[0])
        account = result[0]
        self.assertEqual("f925107376081be421f52d64bec775cc1fc20829", account.get("id"))
        self.assertEqual("NQ33 Y4JH 0UTN 10DX 88FM 5MJB VHTM RGFU 4219", account.get("address"))
        self.assertEqual(0, account.get("balance"))
        self.assertEqual(AccountType.BASIC, account.get("type"))

        self.assertIsNotNone(result[1])
        vesting = result[1]
        self.assertEqual("ebcbf0de7dae6a42d1c12967db9b2287bf2f7f0f", vesting.get("id"))
        self.assertEqual("NQ09 VF5Y 1PKV MRM4 5LE1 55KV P6R2 GXYJ XYQF", vesting.get("address"))
        self.assertEqual(52500000000000, vesting.get("balance"))
        self.assertEqual(AccountType.VESTING, vesting.get("type"))
        self.assertEqual("fd34ab7265a0e48c454ccbf4c9c61dfdf68f9a22", vesting.get("owner"))
        self.assertEqual("NQ62 YLSA NUK5 L3J8 QHAC RFSC KHGV YPT8 Y6H2", vesting.get("ownerAddress"))
        self.assertEqual(1, vesting.get("vestingStart"))
        self.assertEqual(259200, vesting.get("vestingStepBlocks"))
        self.assertEqual(2625000000000, vesting.get("vestingStepAmount"))
        self.assertEqual(52500000000000, vesting.get("vestingTotalAmount"))

        self.assertIsNotNone(result[2])
        htlc = result[2]
        self.assertEqual("4974636bd6d34d52b7d4a2ee4425dc2be72a2b4e", htlc.get("id"))
        self.assertEqual("NQ46 NTNU QX94 MVD0 BBT0 GXAR QUHK VGNF 39ET", htlc.get("address"))
        self.assertEqual(1000000000, htlc.get("balance"))
        self.assertEqual(AccountType.HTLC, htlc.get("type"))
        self.assertEqual("d62d519b3478c63bdd729cf2ccb863178060c64a", htlc.get("sender"))
        self.assertEqual("NQ53 SQNM 36RL F333 PPBJ KKRC RE33 2X06 1HJA", htlc.get("senderAddress"))
        self.assertEqual("f5ad55071730d3b9f05989481eefbda7324a44f8", htlc.get("recipient"))
        self.assertEqual("NQ41 XNNM A1QP 639T KU2R H541 VTVV LUR4 LH7Q", htlc.get("recipientAddress"))
        self.assertEqual("df331b3c8f8a889703092ea05503779058b7f44e71bc57176378adde424ce922", htlc.get("hashRoot"))
        self.assertEqual(1, htlc.get("hashAlgorithm"))
        self.assertEqual(1, htlc.get("hashCount"))
        self.assertEqual(1105605, htlc.get("timeout"))
        self.assertEqual(1000000000, htlc.get("totalAmount"))

    def test_createAccount(self):
        SessionStub.testData = Fixtures.createAccount()

        result = self.client.createAccount()

        self.assertEqual("createAccount", SessionStub.latestRequestMethod)

        self.assertIsNotNone(result)
        self.assertEqual("b6edcc7924af5a05af6087959c7233ec2cf1a5db", result.get("id"))
        self.assertEqual("NQ46 NTNU QX94 MVD0 BBT0 GXAR QUHK VGNF 39ET", result.get("address"))
        self.assertEqual("4f6d35cc47b77bf696b6cce72217e52edff972855bd17396b004a8453b020747", result.get("publicKey"))

    def test_getBalance(self):
        SessionStub.testData = Fixtures.getBalance()

        result = self.client.getBalance("NQ46 NTNU QX94 MVD0 BBT0 GXAR QUHK VGNF 39ET")

        self.assertEqual("getBalance", SessionStub.latestRequestMethod)
        self.assertEqual("NQ46 NTNU QX94 MVD0 BBT0 GXAR QUHK VGNF 39ET", SessionStub.latestRequestParams[0])

        self.assertEqual(1200000, result)

    def test_getAccount(self):
        SessionStub.testData = Fixtures.getAccountBasic()

        result = self.client.getAccount("NQ46 NTNU QX94 MVD0 BBT0 GXAR QUHK VGNF 39ET")

        self.assertEqual("getAccount", SessionStub.latestRequestMethod)
        self.assertEqual("NQ46 NTNU QX94 MVD0 BBT0 GXAR QUHK VGNF 39ET", SessionStub.latestRequestParams[0])

        self.assertEqual("b6edcc7924af5a05af6087959c7233ec2cf1a5db", result.get("id"))
        self.assertEqual("NQ46 NTNU QX94 MVD0 BBT0 GXAR QUHK VGNF 39ET", result.get("address"))
        self.assertEqual(1200000, result.get("balance"))
        self.assertEqual(AccountType.BASIC, result.get("type"))

    def test_getAccountForVestingContract(self):
        SessionStub.testData = Fixtures.getAccountVesting()

        result = self.client.getAccount("NQ09 VF5Y 1PKV MRM4 5LE1 55KV P6R2 GXYJ XYQF")

        self.assertEqual("getAccount", SessionStub.latestRequestMethod)
        self.assertEqual("NQ09 VF5Y 1PKV MRM4 5LE1 55KV P6R2 GXYJ XYQF", SessionStub.latestRequestParams[0])

        self.assertEqual("ebcbf0de7dae6a42d1c12967db9b2287bf2f7f0f", result.get("id"))
        self.assertEqual("NQ09 VF5Y 1PKV MRM4 5LE1 55KV P6R2 GXYJ XYQF", result.get("address"))
        self.assertEqual(52500000000000, result.get("balance"))
        self.assertEqual(AccountType.VESTING, result.get("type"))
        self.assertEqual("fd34ab7265a0e48c454ccbf4c9c61dfdf68f9a22", result.get("owner"))
        self.assertEqual("NQ62 YLSA NUK5 L3J8 QHAC RFSC KHGV YPT8 Y6H2", result.get("ownerAddress"))
        self.assertEqual(1, result.get("vestingStart"))
        self.assertEqual(259200, result.get("vestingStepBlocks"))
        self.assertEqual(2625000000000, result.get("vestingStepAmount"))
        self.assertEqual(52500000000000, result.get("vestingTotalAmount"))

    def test_getAccountForHashedTimeLockedContract(self):
        SessionStub.testData = Fixtures.getAccountVestingHtlc()

        result = self.client.getAccount("NQ46 NTNU QX94 MVD0 BBT0 GXAR QUHK VGNF 39ET")

        self.assertEqual("getAccount", SessionStub.latestRequestMethod)
        self.assertEqual("NQ46 NTNU QX94 MVD0 BBT0 GXAR QUHK VGNF 39ET", SessionStub.latestRequestParams[0])

        self.assertEqual("4974636bd6d34d52b7d4a2ee4425dc2be72a2b4e", result.get("id"))
        self.assertEqual("NQ46 NTNU QX94 MVD0 BBT0 GXAR QUHK VGNF 39ET", result.get("address"))
        self.assertEqual(1000000000, result.get("balance"))
        self.assertEqual(AccountType.HTLC, result.get("type"))
        self.assertEqual("d62d519b3478c63bdd729cf2ccb863178060c64a", result.get("sender"))
        self.assertEqual("NQ53 SQNM 36RL F333 PPBJ KKRC RE33 2X06 1HJA", result.get("senderAddress"))
        self.assertEqual("f5ad55071730d3b9f05989481eefbda7324a44f8", result.get("recipient"))
        self.assertEqual("NQ41 XNNM A1QP 639T KU2R H541 VTVV LUR4 LH7Q", result.get("recipientAddress"))
        self.assertEqual("df331b3c8f8a889703092ea05503779058b7f44e71bc57176378adde424ce922", result.get("hashRoot"))
        self.assertEqual(1, result.get("hashAlgorithm"))
        self.assertEqual(1, result.get("hashCount"))
        self.assertEqual(1105605, result.get("timeout"))
        self.assertEqual(1000000000, result.get("totalAmount"))

    def test_blockNumber(self):
        SessionStub.testData = Fixtures.blockNumber()

        result = self.client.blockNumber()

        self.assertEqual("blockNumber", SessionStub.latestRequestMethod)

        self.assertEqual(748883, result)

    def test_getBlockTransactionCountByHash(self):
        SessionStub.testData = Fixtures.blockTransactionCountFound()

        result = self.client.getBlockTransactionCountByHash("bc3945d22c9f6441409a6e539728534a4fc97859bda87333071fad9dad942786")

        self.assertEqual("getBlockTransactionCountByHash", SessionStub.latestRequestMethod)
        self.assertEqual("bc3945d22c9f6441409a6e539728534a4fc97859bda87333071fad9dad942786", SessionStub.latestRequestParams[0])

        self.assertEqual(2, result)

    def test_getBlockTransactionCountByHashWhenNotFound(self):
        SessionStub.testData = Fixtures.blockTransactionCountNotFound()

        result = self.client.getBlockTransactionCountByHash("bc3945d22c9f6441409a6e539728534a4fc97859bda87333071fad9dad942786")

        self.assertEqual("getBlockTransactionCountByHash", SessionStub.latestRequestMethod)
        self.assertEqual("bc3945d22c9f6441409a6e539728534a4fc97859bda87333071fad9dad942786", SessionStub.latestRequestParams[0])

        self.assertEqual(None, result)

    def test_getBlockTransactionCountByNumber(self):
        SessionStub.testData = Fixtures.blockTransactionCountFound()

        result = self.client.getBlockTransactionCountByNumber(11608)

        self.assertEqual("getBlockTransactionCountByNumber", SessionStub.latestRequestMethod)
        self.assertEqual(11608, SessionStub.latestRequestParams[0])

        self.assertEqual(2, result)

    def test_getBlockTransactionCountByNumberWhenNotFound(self):
        SessionStub.testData = Fixtures.blockTransactionCountNotFound()

        result = self.client.getBlockTransactionCountByNumber(11608)

        self.assertEqual("getBlockTransactionCountByNumber", SessionStub.latestRequestMethod)
        self.assertEqual(11608, SessionStub.latestRequestParams[0])

        self.assertEqual(None, result)

    def test_getBlockByHash(self):
        SessionStub.testData = Fixtures.getBlockFound()

        result = self.client.getBlockByHash("bc3945d22c9f6441409a6e539728534a4fc97859bda87333071fad9dad942786")

        self.assertEqual("getBlockByHash", SessionStub.latestRequestMethod)
        self.assertEqual("bc3945d22c9f6441409a6e539728534a4fc97859bda87333071fad9dad942786", SessionStub.latestRequestParams[0])
        self.assertEqual(False, SessionStub.latestRequestParams[1])

        self.assertIsNotNone(result)
        self.assertEqual(11608, result.get("number"))
        self.assertEqual("bc3945d22c9f6441409a6e539728534a4fc97859bda87333071fad9dad942786", result.get("hash"))
        self.assertEqual(739224, result.get("confirmations"))
        self.assertEqual([
            "78957b87ab5546e11e9540ce5a37ebbf93a0ebd73c0ce05f137288f30ee9f430",
            "fd8e46ae55c5b8cd7cb086cf8d6c81f941a516d6148021d55f912fb2ca75cc8e",
        ], result.get("transactions"))

    def test_getBlockByHashWithTransactions(self):
        SessionStub.testData = Fixtures.getBlockWithTransactions()

        result = self.client.getBlockByHash("bc3945d22c9f6441409a6e539728534a4fc97859bda87333071fad9dad942786", True)

        self.assertEqual("getBlockByHash", SessionStub.latestRequestMethod)
        self.assertEqual("bc3945d22c9f6441409a6e539728534a4fc97859bda87333071fad9dad942786", SessionStub.latestRequestParams[0])
        self.assertEqual(True, SessionStub.latestRequestParams[1])

        self.assertIsNotNone(result)
        self.assertEqual(11608, result.get("number"))
        self.assertEqual("bc3945d22c9f6441409a6e539728534a4fc97859bda87333071fad9dad942786", result.get("hash"))
        self.assertEqual(739501, result.get("confirmations"))

        self.assertEqual(2, len(result.get("transactions")))
        self.assertIs(type(result.get("transactions")[0]), dict)
        self.assertIs(type(result.get("transactions")[1]), dict)

    def test_getBlockByHashNotFound(self):
        SessionStub.testData = Fixtures.getBlockNotFound()

        result = self.client.getBlockByHash("bc3945d22c9f6441409a6e539728534a4fc97859bda87333071fad9dad942786")

        self.assertEqual("getBlockByHash", SessionStub.latestRequestMethod)
        self.assertEqual("bc3945d22c9f6441409a6e539728534a4fc97859bda87333071fad9dad942786", SessionStub.latestRequestParams[0])
        self.assertEqual(False, SessionStub.latestRequestParams[1])

        self.assertIsNone(result)

    def test_getBlockByNumber(self):
        SessionStub.testData = Fixtures.getBlockFound()

        result = self.client.getBlockByNumber(11608)

        self.assertEqual("getBlockByNumber", SessionStub.latestRequestMethod)
        self.assertEqual(11608, SessionStub.latestRequestParams[0])
        self.assertEqual(False, SessionStub.latestRequestParams[1])

        self.assertIsNotNone(result)
        self.assertEqual(11608, result.get("number"))
        self.assertEqual("bc3945d22c9f6441409a6e539728534a4fc97859bda87333071fad9dad942786", result.get("hash"))
        self.assertEqual(739224, result.get("confirmations"))
        self.assertEqual([
            "78957b87ab5546e11e9540ce5a37ebbf93a0ebd73c0ce05f137288f30ee9f430",
            "fd8e46ae55c5b8cd7cb086cf8d6c81f941a516d6148021d55f912fb2ca75cc8e",
        ], result.get("transactions"))

    def test_getBlockByNumberWithTransactions(self):
        SessionStub.testData = Fixtures.getBlockWithTransactions()

        result = self.client.getBlockByNumber(11608, True)

        self.assertEqual("getBlockByNumber", SessionStub.latestRequestMethod)
        self.assertEqual(11608, SessionStub.latestRequestParams[0])
        self.assertEqual(True, SessionStub.latestRequestParams[1])

        self.assertIsNotNone(result)
        self.assertEqual(11608, result.get("number"))
        self.assertEqual("bc3945d22c9f6441409a6e539728534a4fc97859bda87333071fad9dad942786", result.get("hash"))
        self.assertEqual(739501, result.get("confirmations"))

        self.assertEqual(2, len(result.get("transactions")))
        self.assertIs(type(result.get("transactions")[0]), dict)
        self.assertIs(type(result.get("transactions")[1]), dict)

    def test_getBlockByNumberNotFound(self):
        SessionStub.testData = Fixtures.getBlockNotFound()

        result = self.client.getBlockByNumber(11608)

        self.assertEqual("getBlockByNumber", SessionStub.latestRequestMethod)
        self.assertEqual(11608, SessionStub.latestRequestParams[0])
        self.assertEqual(False, SessionStub.latestRequestParams[1])

        self.assertIsNone(result)

    def test_constant(self):
        SessionStub.testData = Fixtures.constant()

        result = self.client.constant("BaseConsensus.MAX_ATTEMPTS_TO_FETCH")

        self.assertEqual("constant", SessionStub.latestRequestMethod)
        self.assertEqual("BaseConsensus.MAX_ATTEMPTS_TO_FETCH", SessionStub.latestRequestParams[0])

        self.assertEqual(5, result)

    def test_setConstant(self):
        SessionStub.testData = Fixtures.constant()

        result = self.client.constant("BaseConsensus.MAX_ATTEMPTS_TO_FETCH", 10)

        self.assertEqual("constant", SessionStub.latestRequestMethod)
        self.assertEqual("BaseConsensus.MAX_ATTEMPTS_TO_FETCH", SessionStub.latestRequestParams[0])
        self.assertEqual(10, SessionStub.latestRequestParams[1])

        self.assertEqual(5, result)

    def test_resetConstant(self):
        SessionStub.testData = Fixtures.constant()

        result = self.client.resetConstant("BaseConsensus.MAX_ATTEMPTS_TO_FETCH")

        self.assertEqual("constant", SessionStub.latestRequestMethod)
        self.assertEqual("BaseConsensus.MAX_ATTEMPTS_TO_FETCH", SessionStub.latestRequestParams[0])
        self.assertEqual("reset", SessionStub.latestRequestParams[1])

        self.assertEqual(5, result)

    def test_log(self):
        SessionStub.testData = Fixtures.log()

        result = self.client.log("*", LogLevel.VERBOSE)

        self.assertEqual("log", SessionStub.latestRequestMethod)
        self.assertEqual("*", SessionStub.latestRequestParams[0])
        self.assertEqual("verbose", SessionStub.latestRequestParams[1])

        self.assertEqual(True, result)

if __name__ == '__main__':
    unittest.main()
