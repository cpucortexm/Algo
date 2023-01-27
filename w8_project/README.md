## Algorand Encode bootcamp(Group 10)

### Authors

1. Yogesh Kulkarni (yogidk@gmail.com)

2. Venkat K (vnkorlipara@gmail.com)

## Project: Storage counter

Deployed at :

Counter deployed at:https://testnet.algoexplorer.io/application/156096526

### Details:

The project defines a global counter which can be incremented and decremented. It also has a global owner which variable which gives us info about the address that is performing the increment and decrement operations.

Handling of Overflow and Underflow:
Counter is implemented using an unsigned integer.
It is possible for the counter to have an overflow if we increment the unsigned integer with max value of 0xFFFFFFFFFFFFFFFF and an underflow if we decrement the unsigned integer with value of 0. This is handled by using a scratch pad variable which will be checked with an if condition for < 0xFFFFFFFFFFFFFFFF for increment and >0 for decrement.

## Output:

Using call_app helper function, the increment and decrement was done and below is the log.

Counter deployed at:https://testnet.algoexplorer.io/application/156096526

Waiting for confirmation...
Transaction W6YLXPQVMG5OU3GFMO7TXEHCIZVFDXXCWWAQTU3RXABQO2GP7GTA confirmed in round 27301579.
Created new app-id: 156096528

## before increment or decrement

Global state: {'counter': 0, 'owner': 'd3ZRv4j85UKzgfv9EWgdPd5gZEJIFR9hgn8I4DYf/pw='}
Call from account: O53FDP4I7TSUFM4B7P6RC2A5HXPGAZCCJAKR6YMCP4EOANQ772OIUQT3NM

## increment 1

Waiting for confirmation...
Transaction Q6X735KZ6VZQDXVZR352OOUHVYOOJQ7M5FYSH3IYQJBDHWNND54Q confirmed in round 27301581.
Local state: {}
Global state: {'counter': 1, 'owner': 'd3ZRv4j85UKzgfv9EWgdPd5gZEJIFR9hgn8I4DYf/pw='}

## increment 2

Call from account: O53FDP4I7TSUFM4B7P6RC2A5HXPGAZCCJAKR6YMCP4EOANQ772OIUQT3NM
Waiting for confirmation...
Transaction QYYAC36RUM6HN5RGBLRTI5J4PRR4PKKM6XZW7VTAO3HM3GUWKFMA confirmed in round 27301583.
Global state: {'counter': 2, 'owner': 'd3ZRv4j85UKzgfv9EWgdPd5gZEJIFR9hgn8I4DYf/pw='}

## decrement 1

Call from account: O53FDP4I7TSUFM4B7P6RC2A5HXPGAZCCJAKR6YMCP4EOANQ772OIUQT3NM
Waiting for confirmation...
Transaction 3TZ4BAKZSX2OVMPZWY24UN647WJ6Z2OQHQZRH6T6U7SZL3DV6D6Q confirmed in round 27301586.
Global state: {'counter': 1, 'owner': 'd3ZRv4j85UKzgfv9EWgdPd5gZEJIFR9hgn8I4DYf/pw='}
