# final-project-iirs (Secure Chat Client)  
**Note:** For final project video and slides, view the bottom of milestones.md.
## File Structure
- Setup.py: Provides necessary info / modules to run the project
- Server.py: Runs the server backend
- Client.py: Runs the client side, creating one session for one user
- Iirs:
  - Message.py: Has message classes
  - Server:  
    - connectionThread.py: Class for each connection, connected to the server, one per user
    - Deaddrop.py: The dead drop system. Contains the manager, deaddrop container, etc. Handles all storage/retrieval.
    - Main.py: Sets up the server to run the mix net and dead drop system together
    - Mix_net.py: Contains the mix net
  - Client:  
    - \_\_init\_\_.py: Contains necessary functions for login, registration, user validation. Also holds DeadDropSync class.
    - Gui.py: Contains the gui
    - Main.py: Main function, which creates a connection, invokes the login method and starts the GUI
    - Server_connection.py: Provides `ServerConnection`, which creates a socket to the server, and spawns threads to send and  recieve
    - Chat_session.py: `ChatSession` wraps `ServerConnection`, with the information about the user who the chat session is with. The caller then can deal with simple plain text message, unencrypted.

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

#### Dead Drop Sync  
Dead Drop syncing is defined within `client/__init__.py`, in the `DeadDropSync` class. Once a client starts a chat session, the syncing system will start directing connection requests to dead drop 0 (our universal connection dead drop). Each request is populated with the desired first dead drop to use for the coversation, encrypted within `PeerMessage` in the `deaddrop` field, and with the start time of the conversation (with the format `$TIME$[time stamp goes here]`). Once the second client connects, it will start doing the same thing. The moment a client recieves its first message from the other client, it will quickly compare its own start time with the other client's start time. The client with the earliest start time will be designated the `generator` and will call `generate()` after recieving a message from the destination client. The other client will be designated the `listener` and will call `listener_update()` after recieving a message from the destination client.  
`generate()` puts the previous "future" dead drop, into the `currentDD` var and generates a new dead drop number in `nextDD`.  
`listener_update()` obtains the "future" dead drop from the recieved message, and applies it to its own `currentDD` variable.  
Thus, every round, both the listener and generator have a synced agreement as to which dead drop to use next, and always switch around, ensuring anonymity within the network.  

### Server
When the server is started the mix net and the dead drop systems are created. The server listens for new client connections on a particular port. For each new client that connects a new connectionThread is created. Messages will then be sent at a regular interval, mixed and sent to the dead drop system. The dead drop system then processes and returns messages. These messages are then unmixed and sent to the appropriate connectionThread.
#### Mix Net
The mix net is the first point of contact with the outside world. It is the mix net that listens for clients. The mix net is always listening for new messages from each of the clients and storing them to be processed at the start of the next round. Every 2 seconds a new round starts. With the start of a new round the queued messages have a layer of encryption decrypted. Then, the messages are mixed and sent to the dead drop class. After the dead drop class processes the messages, it will return outgoing messages. These outgoing messages are then unmixed and re-encrypted. The newly encrypted messages are then sent to there appropriate connectionThread.  

#### Dead Drop
The dead drop system is initialized upon server creation. The main class, within `deaddrop.py`, is the `DeadDropManager` class. It will create all the specifified deaddrops, handle all transfering of data using private methods `__get()` and `__store()`, and will make sure to clear all data from each deaddrop after every round. The `DeadDrop` class is what actually holds and manages the data given to it. Data is stored using a python list internally. The `DeaddropMessage` class is what wraps the standard `Message` class for the purposes of garbage collection. An optional `GarbageCollector(Thread)` is implemented to allow the clearing of dead drops using time instead of rounds.  
A typical flow with the dead drop system is that the mixnet will call `handle_messages()` from the manager, which is a `List[Message]`, and the dead drop system will store each message in a specific dead drop, populate same index positions with their respective dead drop contents, and then send it back to the mixnet.
## Install Instructions  
The program can be installed with `python3 setup.py install` and run `iirs-server` and `iirs-client`.

Alternately, it can be run without installation. First install the dependencies, with a command like `pip3 install --user cryptography apscheduler`. Then it can be run as `./server.py` and `./client.py`.

## Usage Instructions 
For the server side, all you need to do is run it on your local machine. Nothing else needs to be done.  
For the client side, to hold an active conversation you need to have two active client processes runnining, logged in, and connected.

### Login/Registration  
Once the client is running, type `r` to register or `l` to login an already registered user. 
Note: The server stores client registration info in RAM so once server is stopped, all users have to re-register. 
Once selected and option, enter a username and password and wait for the next server prompt. (This will take a few seconds).

### Starting Chat Session  
The server will ask what user you want to talk to. Once you enter the username of the user, the client session will start shortly.  
Note: The user has to be actually registered (i.e. progressed to a point where the server atleast asked them who to talk to)

### The Chat Session  
When the chat window opens, you will initially be blocked from sending messages. This is because a dead drop sync needs to occur between both clients. Once the sync is complete, a message from the other client will appear saying `Connection established successfully`. After that, you can send messages as much as you want to the other client.  
Note: If the other client is not actively seeking to talk to you, you will be blocked from sending them messages until they start a conversation with you.

