from plug.key import ED25519SigningKey
from plug.hash import sha256
from plug.proof import SingleKeyProof
from balance_tutorial.transform import FreeMoney
from plug.transaction import Transaction
from plug.constant import TransactionEvent
from plug.message import Event
from plug.registry import Registry
import aiohttp
import json
import asyncio
from balance_tutorial.user import User

async def main():
    registry = Registry().with_default()
    registry.register(Event)
    registry.register(FreeMoney)

    user_data = json.load(open("user_data.json", "r"))

    if user_data["key"] is "":
        print("----- NO KEY IN FILE ------")
        user_data["key"] = ED25519SigningKey.to_string(ED25519SigningKey.new())
        user_data["nonce"] = -1

    alice = User(ED25519SigningKey.from_string(user_data["key"]))

    print(user_data)
    user_data["nonce"] += 1
    with open("user_data.json", "w") as write_file:
        json.dump(user_data, write_file)

    transform = FreeMoney(
        receiver=alice.address,
        amount=1000,
    )

    challenge = transform.hash(sha256)
    proof = SingleKeyProof(alice.address, user_data["nonce"], challenge, 'balance_tutorial')
    proof.sign(alice.signing_key)
    transaction = Transaction(transform, {proof.address: proof})

    event = Event(
        event=TransactionEvent.ADD,
        payload=transaction
    )

    payload = registry.pack(event)

    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:8181/_api/v1/transaction", json=payload) as response:
            data = await response.json()

    # print(data)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
