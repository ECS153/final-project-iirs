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

