# Milestones
## IIRS Group  
Irvin Leshchinsky, Ian Scott, Rohit Dhamankar, Spencer Grossarth

# Milestone 1 (5/12/2020)

## Update Video:  
https://drive.google.com/file/d/1YWEhSMiVv7tZsqzAGcj60thygVtAs7gp/view?usp=sharing

## Meeting Notes:  
- Shared progress and ideas, went over github and current code.  
- Discussed different ways we can implement handshake, client/server, and various connection methods.  
- Figured out our 4 key features to implement design docs for: Client handshake system, Mixing Net, Deadrop, and the Server Database.   
- Set a goal of recording our milestone videos and filling information.  
- Set a future goal of researching into how sockets work, client/server connections, and handshakes within python.  
- Set a follow-up meeting on Wednesday to delegate further work, and have team members start on a design doc or two.  

## Team Progress:
### Irvin:  
- Last week I researched secure messaging, read the Vuvuzela paper, and wrote part of the proposal.  
- This week I am looking into how python sockets work, how to connect to two computers over the internet, and how to have a secure handshake between two users; once our work is further delegated after research, I will be working on either client or server side depending on what we decide.  
- My team and I were stuck on trying to figure out how to create an abstract layout of the server side, hence our goal to look into how networking works.  

### Ian:  
- I wrote some initial boilerplate code, and looked into encryption in Python. The `ssl` standard library module is too high level for our use. It seems the module `cryptography` on PyPI is preferred for offering cryptography algorithms.
- I think I'll try to look into use the `cryptography` module for end-to-end encryption. Perhaps using RSA, AES, and Diffie-Hellman key exchange.
- It's difficult to figure out exactly how to create some initial class definitions and divide the program so we can work on things separately.

### Rohit:  
- Last week I did some preliminary research on end to end encryption and read some papers / articles (Vuvuzela), wrote section of proposal.  
- This week i’m researching socket programming in python, secure handshake, and other server client procedures in hopes of getting a better idea of the work we need to do. After we delegate tasks, I will start programming some feature / component TBD.  
- We had some trouble outlining the necessary components of our app and getting a good handle on what steps to take going forward.  

### Spencer:  
- Last week I worked on the initial proposal. And in preparation for that spent time researching how end to end encrypted chat apps worked. After we decided on an app similar to Vuvuzela, I spent time reading that paper and got a deeper understanding of how it works.  
- I created a simple client and hooked it up to the gui. I also connected the client to the server, so when you type in a message it sent back to the client.
- We are still figuring out exactly how we want to implement our app. After we do a bit of research we should be able to resolve this issue.

# Milestone 2 (5/19/2020)  

## Update Video  
[Link Goes Here]  

## Meeting Notes  
### Discussion items
- How to have two clients talk to one another?
- Do clients know each others key beforehand or will there be a look up table?
- Does a lookup table lead to security issues?
- How to split up the work 4 different ways.

### Design documents:
- Mix net
- Dead drop system/server
- Client
- Connection between client and server 


### Breaking it up into 4 parts:
- Client side - sending out messages each round that are fixed sizes (SSL to server)
- Server side - handling the drop box and how it handled 
- mixing net -  mixes the messages
- connecting between servers - handling all of the security with how to connect from a client to a server 

### Goals for this week:
- Allow a couple of users to talk to each other, in a non secure way
- Try and get rounds to work this week
- Get initial implementation of a mixing net, connected to the back end



## Team Progress  

### Irvin:  
- Last week I learned about how python sockets work, how to implement handshakes, etc.; I also coded up a basic server that can accept a message from a client.
- This week I am researching into threading, encrpytion, deadrops, and re-writing the entire server to accept multiple connections at the same time, allowing users to have a full fledged conversation.  
- Not really stuck on anything.
- Relevant Commits:  
59f0271c602a0a478c2c468713065a10cc8181c4  (this week's progress)
cde3d59ed89094ae718dc1e838052dce4b1c8653  
3556f77358c24a219f87018c4fb513223baa4572 (last week)  
76a86432eaec130185ac0b9818f9436c9576f7fa  

### Ian:  
- I implemented a basic GUI using `tkinter` (f263e7e07de0ec6a4c1d6ebecf04e3bee6610d67), reorganized the code to match python best practices (6669979ead0058bdac60b8ac1b6deb712b79df8d), and added a serializable message class for use in both the client and server (ff0438c5c32333614eb0d4fef16851b76e4cb993).
- Next week I intend to take a look at the `cryptography` library from PyPI, and try to use the primitives there to implement an end-to-end encryption scheme to prevent the server from reading messages, and also verify sender identity.
- Receiving messages asynchronously without blocking the UI has proven a bit awkward, but I think I've figured it out.

### Rohit:  
- Last week I researched socket programming with python, key generation and encryption, and coded some threading functionality for the server.
- This week I worked on client side code, specifically simple registration, login, and connecting to another user.
- Wasn't really stuck on anything, still need to push code that integrates with server code and adds encryption.
- Relevant Commits:  
a2d3e6fa6e916937e591fe857b8b1c14ffb678f0 (this week's progress)  
2a1457a33aa7ac9c93bf849667ad6867e61380af  
b0ee4c18a64ab0b4a8e53dbd2b8559e13c437c36 (last week)  

### Spencer:  
- Last week I learned more about client server encryptions. I also created a very simple front end and connected that to the back end so we could send a message to the server and the server would send it right back. 

- This week I researched mixing networks and I started to implement a basic one that fits the scope of the project.

- I'm still trying to understand how the actual mixing is done in the mixing network. Specifically, if there are particular algorithms that need to be used to do this or if it can be fairly simple as long as it is random and reversible. 

(this week)

(last week)
https://github.com/ECS153/final-project-iirs/commit/31b5e7b276089ad2c13d6406183870f5aff2319f
https://github.com/ECS153/final-project-iirs/commit/24295f9f1d6e2fbef1f28a23ed906dbf91658831
