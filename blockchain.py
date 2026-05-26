from web3 import Web3

web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

contract_address = "0x89c10789878Ae19881CD973B60d262d00a90112b"

ABI = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_student",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_authority",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_certificatename",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_hash",
				"type": "string"
			}
		],
		"name": "addCertificate",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "certificates",
		"outputs": [
			{
				"internalType": "string",
				"name": "student",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "authority",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "certificatename",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "hash",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

contract = web3.eth.contract(
    address=contract_address,
    abi=ABI
)
tx_hash = contract.functions.addCertificate(
    "Piyush",
    "LNCT",
    "BlockchainCertificate",
    "abc123"
).transact({
    "from": web3.eth.accounts[0]
})

def AddCertificateToBlockchain(
    student,
    authority,
    certificatename,
    filehash
):
    tx_hash = contract.functions.addCertificate(
        student,
        authority,
        certificatename,
        filehash
    ).transact({
        "from": web3.eth.accounts[0]
    })

    return tx_hash.hex()