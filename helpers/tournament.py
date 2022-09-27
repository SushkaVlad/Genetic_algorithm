import random


def tournament(tournament_participants, expected_winners_number):
    winners = []
    while len(winners) < expected_winners_number:
        index_list = list(range(0, len(tournament_participants)))
        player1_index, player2_index = random.sample(index_list, 2)
        player1, player2 = tournament_participants[player1_index], tournament_participants[player2_index]
        if player1.fitness > player2.fitness:
            winners.append(player1)
            tournament_participants.pop(player1_index)
        else:
            winners.append(player2)
            tournament_participants.pop(player2_index)
    return winners
