## Introduction:
The Reliable Transport Protocol addresses the challenge of ensuring data transfer reliability over an unreliable network. This protocol offers a reliable channel for data transfer, handling issues such as packet loss, corruption, and out-of-order packets.

## Project Description:
The project aims to implement a transport protocol enhancing UDP's reliability through the Go-Back-N protocol. It involves creating specialized GBN sender and receiver scripts, each with distinct functionalities.

## Simulated Loss:
To simulate network conditions, random packet loss (5%-15%) is introduced by randomly dropping received packets at the receiver.

## How to use:
To get started, clone the repository and install any necessary dependencies. After ensuring all dependencies are installed, run the receiver file first, followed by the sender file. You can observe the packets being sent directly in the console.
