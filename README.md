# final-project-iirs
## File Structure
- Setup.py: IDK
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
Description
#### Login
Descripton
#### Encryption
Description

### Server
When the server is started the mix net and the dead drop systems are created. The server listens for new client connections on a particular port. For each new client that connects a new connectionThread is created. Messages will then be sent at a regular interval, mixed and sent to the dead drop system. The dead drop system then processes and returns messages. These messages are then unmixed and sent to the appropriate connectionThread. 
#### Mix Net
The mix net is the first point of contact with the outside world. It is the mix net that listens for clients. The mix net is always listening for new messages from each of the clients and storing them to be processed at the start of the next round. Every 2 seconds a new round starts. With the start of a new round the queued messages have a layer of encryption decrypted. Then, the messages are mixed and sent to the dead drop class. After the dead drop class processes the messages, it will return outgoing messages. These outgoing messages are then unmixed and re-encrypted. The newly encrypted messages are then sent to there appropriate connectionThread.  

#### Dead Drop
Description
