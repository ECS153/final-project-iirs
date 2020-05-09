Project Proposal
================

What problem are you solving?
-----------------------------
The problem that we are trying to solve is one of privacy. Specifically we are trying to solve the issue of privacy within text based communication mediums. In today’s chat apps there is end to end encryption that ensures privacy of the actual content of the message but there is nothing done about the metadata surrounding the conversation that can be used to easily determine the sender/receiver and even the rough content of the message through context clues. Our goal within this project is to build a secure chat application that will also secure metadata in such a way that observing the sender or receiver will be useless to an attacker.

Why is it important?
--------------------
Hiding metadata is essential in our increasingly computerized world. Our online personas have become an important part of our life. By hiding metadata this will allow individuals to communicate more freely without worrying about what an attacker might gleam from their conversations. The ability to communicate online privately is key to keeping the internet safe and open.

What do you plan to build?
--------------------------
We plan on building an end-to-end encrypted messaging app similar to Vuvuzela. We will design a dead drop system while using an existing mixing net implementation to maintain privacy standards. We will use SQLite as our database management system, flask for the web framework, and HTTP as the communication protocol. Our main focus is on the actual communication system, so the application front-end will be a stretch goal since it is not relevant to the performance of the system.

What are your expected results?
-------------------------------
We expect to have a cross-platform command line application that is usable for end-to-end chat, using a mixing net. A serious fully-featured chat application should probably have a more user friendly interface, but that is not our focus. The exact set of features and protections will be dependent on how long it takes to get the core functionality working.

