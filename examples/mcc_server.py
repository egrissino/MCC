import asyncio
import websockets
from mcc.keygen import KeyGenerator
from mcc.encryption import Encryption
from mcc.keyexchange import KeyExchange

# Generate server key pair
server_key = KeyGenerator.generate_keypair()

async def handler(websocket, path):
    # Perform key exchange with client
    client_public_key = await websocket.recv()
    shared_secret = KeyExchange.compute_shared_secret(server_key['constant_sum'], server_key['public_key'])

    # Send server's public key to the client
    await websocket.send(server_key.public_key)

    # Securely communicate using shared secret
    while True:
        encrypted_message = await websocket.recv()
        message = Encryption.decrypt(encrypted_message, shared_secret)
        print(f"Received: {message}")
        
        response = f"Server response to: {message}"
        encrypted_response = Encryption.encrypt(response, shared_secret)
        await websocket.send(encrypted_response)

start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
