# Mini Ultimatum Game

# Candidate ID BSI_103

This is a mini ultimatum game implemented using the oTree framework. In this game, three players are involved, and they make decisions related to sending and receiving money. Player 3 has the choice to punish or not punish the decisions made by Player 1.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your system.
- oTree framework installed. You can install it using pip:

`pip install otree`

# Installation
To install this project, follow these steps:

Clone the repository to your local machine:

`git clone <repository-url>`

## Navigate to the project directory:

`cd mini_ultimatum`

### Create a virtual environment (optional but recommended):

`python -m venv venv`

Activate the virtual environment:

`source venv/bin/activate`

Install the project dependencies:
`pip install -r requirements.txt`

Follow these steps to run the project:


Start the oTree development server:

`otree devserver`

Open a web browser and go to http://127.0.0.1:8000/ to access the oTree admin interface.

Create a session and start the game from the admin interface.

# Game Rules

Player 1 starts with an initial endowment of Ksh 200.
Player 1 sends an amount to Player 2.
Player 3 (the Punisher) observes the transaction and decides whether to punish Player 1's decision.
Player 3's choice affects the payouts for all players.

# Customization
You can customize the game by modifying the oTree project files. Refer to the oTree documentation for more information on how to customize your oTree apps and games.