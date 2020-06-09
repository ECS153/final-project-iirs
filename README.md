# final-project-iirs
## File Structure
- Setup.py: Provides necessary info / modules to run the project
- Server.py: Runs the server backend
- Client.py: Runs the client side, creating one session for one user
- Iirs:
  - Message.py: Has message classes
  - Server:
    - connectionThread.py: Class for each connection, connected to the server, one per user
    - Deaddrop.py: The dead drop system
    - Main.py: Sets up the server to run the mix net and dead drop system together
    - Mix_net.py: Contains the mix net
  - Client:
    - Chat_session.py: IDK
    - Gui.py: Contains the gui
    - Main.py: IDK
    - Server_connection.py: IDK

## Concept Mapping
### Client
The client side software begins with the registration / login component. After a user completes this phase, they must select another user to communicate with. Then, a server connection is made, a chat session is created, and the GUI for the chat appears, at which point the client can now communicate with the desired user.
#### Login
Login and registration have a similar process, where a temporary server connection and chat session are made for the communications with the server. Both components also hash the user entered password using SHA512 and send a component of the hash to the server for storage / verification of a user. On registration, a public-private key pair is generated, the private key is encrypted, and both are sent to the server for storage. On login, this key pair is downloaded from the server, and the private key is decrypted to reconstruct the actual plaintext private key.
#### Encryption
For encryption between the client and the server, use use TLS, with the Python builtin `ssl` module. As implemented, the server randomly generates a certificate at start, and the client doesn't verify it. Of course, in actual deployment, the certificate would be checked, either with the normal certificate authority system, or by the application having it's own CA.

End-to-end encryption is implemented in the `PeerMessage` class. The low level cryptography primatives are provided by the `crytography` module from PyPI. The approach uses a hybrid encryption method, using ECDH to generate a shared AES key from the users keypairs. Using AES CBC mode with a random initialization vector, it should be impossible for for an attacker (including the server) to determine if two messages are identical or in any way similar. An ECDSA signature is included, within the encryption, so the message can be reliably verified to be from the sender.

This should be secure by any modern standard, except that it lacks forward secrecy, since the two clients always use the same key. This does mean no handshake is needed, though. Of course, it can be difficult to evaluate the security of a cryptosystem without sufficient background.

The `PeerMessage` has a fixed-size binary encoding, so it should expose no information about the contents of the message to the server. This is embedded in a `Message` class for sending to the server, which is encoded as json. If we had another week, that would also be updated to have a carefully designed fixed size binary encoding.

### Server
When the server is started the mix net and the dead drop systems are created. The server listens for new client connections on a particular port. For each new client that connects a new connectionThread is created. Messages will then be sent at a regular interval, mixed and sent to the dead drop system. The dead drop system then processes and returns messages. These messages are then unmixed and sent to the appropriate connectionThread.
#### Mix Net
The mix net is the first point of contact with the outside world. It is the mix net that listens for clients. The mix net is always listening for new messages from each of the clients and storing them to be processed at the start of the next round. Every 2 seconds a new round starts. With the start of a new round the queued messages have a layer of encryption decrypted. Then, the messages are mixed and sent to the dead drop class. After the dead drop class processes the messages, it will return outgoing messages. These outgoing messages are then unmixed and re-encrypted. The newly encrypted messages are then sent to there appropriate connectionThread.  

#### Dead Drop
Description
