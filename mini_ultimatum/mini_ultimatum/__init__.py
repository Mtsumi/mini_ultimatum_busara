from otree.api import *


doc = """
A Mini Ultimatum Game with 3 players. 
Player 1 endows Ksh 200, sends an amount to Player 2. 
Player 3, the Punisher, observes and decides to punish or not. 
Payouts depend on Player 3's choice. An exit survey follows.
"""


class C(BaseConstants):
    PLAYERS_PER_GROUP = 3
    # PLAYER_1_ROLE = 'Player 1'
    # PLAYER_2_ROLE = 'Player 2'
    # PLAYER_3_ROLE = 'Player 3'
    NUM_ROUNDS = 1
    NAME_IN_URL = 'mini_ultimatum'
    INITIAL_ENDOWMENT = cu(200)  # Player 1's initial endowment

# Tried to have individual roles for each player but it didn't work


# class Subsession(BaseSubsession):
#     def creating_session(self):
#         for group in self.get_groups():
#             players = group.get_players()
#             players[0].role = C.PLAYER_1_ROLE
#             players[1].role = C.PLAYER_2_ROLE
#             players[2].role = C.PLAYER_3_ROLE


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # Total amount sent by Player 1 to Player 2
    amount_sent = models.CurrencyField()

    # Decision made by The Punisher - True for "Not Punish," False for "Punish"
    punish_decision = models.BooleanField(
        label="Choose your decision:",
        widget=widgets.RadioSelectHorizontal,
    )

    # Amount received by Player 2
    amount_received = models.CurrencyField()


class Player(BasePlayer):
    # Amount to send to Player 2 (Player 1)
    amount_to_send = models.CurrencyField(
        min=0, max=C.INITIAL_ENDOWMENT,
        label="Please choose the amount to send to Player 2:"
    )

    punish_decision = models.BooleanField()

    # Player 1's payout
    payout_player1 = models.CurrencyField()

    # Player 2's payout
    payout_player2 = models.CurrencyField()


def calculate_payoffs(group: Group):
    players = group.get_players()

    amount_sent = players[0].amount_to_send

# It was quite challenging to get the code to work with individual roles for each player,
# partiularly assigning the value from the player to the "punish_decision" variable.
# Couldn't figure out because of limited time
    # for player in players:
    #     if player.punish_decision:
    #         # Player chose to "Punish"
    #         player.payout_player1 = 0
    #         player.payout_player2 = 0
    #     else:
    #         # Player chose to "Not Punish"
    #         player.payout_player1 = C.INITIAL_ENDOWMENT - amount_sent
    #         player.payout_player2 = amount_sent

    punish_decision = group.punish_decision

    for player in players:
        if punish_decision:
            # Player 3 chose to "Punish"
            player.payout_player1 = 0
            player.payout_player2 = 0
        else:
            # Player 3 chose to "Not Punish"
            player.payout_player1 = C.INITIAL_ENDOWMENT - amount_sent
            player.payout_player2 = amount_sent

# PAGES


class Introduction(Page):
    pass

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Player1Send(Page):
    form_model = 'player'
    form_fields = ['amount_to_send']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.group.amount_sent = player.amount_to_send


class Player3Decision(Page):
    form_model = 'player'
    form_fields = ['punish_decision']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.group.punish_decision = player[1].punish_decision

    @staticmethod
    def vars_for_template(player: Player):
        amount_sent = player.amount_to_send
        # player.group.punish_decision = player.punish_decision

        # Calculate the payoffs for this player's group
        calculate_payoffs(player.group)

        return {
            'amount_sent': amount_sent,
            'punish_decision': player.group.punish_decision,
            'player1_payout': player.payout_player1,
            'player2_payout': player.payout_player2,
        }


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        amount_sent = player.amount_to_send
        punish_decision = player.punish_decision
        payout_player1 = player.payout_player1
        payout_player2 = player.payout_player2
        return {
            'amount_sent': amount_sent,
            'punish_decision': punish_decision,
            'player1_payout': payout_player1,
            'player2_payout': payout_player2,
        }


class ExitSurvey(Page):
    form_model = 'player'
    form_fields = ['capital_city', 'math_question', 'population_question']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        correct_math_answer = 14 + 15  # Calculate the correct answer for Question 2
        return {
            'correct_math_answer': correct_math_answer,
        }

    @staticmethod
    def error_message(player: Player, values):
        errors = {}

        # Validate the answer for Question 2
        if values['math_question'] != player.vars['correct_math_answer']:
            errors['math_question'] = 'Incorrect answer. Please enter the correct sum of 14 and 15.'

        return errors


page_sequence = [Introduction, Player1Send,
                 Player3Decision, Results, ExitSurvey]
