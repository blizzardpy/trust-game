from bots import *


class Tournament:
    def __init__(self, players, number_of_rounds=10, top_players_to_reproduce=5, new_game=True):
        self.players = players
        self.number_of_rounds = number_of_rounds
        self.top_players_to_reproduce = top_players_to_reproduce
        self.new_game = new_game

        if self.new_game:
            self.scores = {player: 0 for player in self.players}
        self.payout = {
            ("C", "C"): (2, 2),
            ("C", "N"): (-1, 3),
            ("N", "C"): (3, -1),
            ("N", "N"): (0, 0)
        }

    def run_tournament(self):
        print("Starting tournament...")
        # print("Scores:", scores)
        for player1_index, player1 in enumerate(self.players):
            for player2_index in range(player1_index + 1, len(self.players)):
                player2 = self.players[player2_index]
                for _ in range(self.number_of_rounds):
                    move1 = player1.move()
                    move2 = player2.move()
                    payoff = self.payout[(move1, move2)]
                    self.scores[player1] += payoff[0]
                    self.scores[player2] += payoff[1]
        self.players.sort(key=lambda x: self.scores[x], reverse=True)
        top_players = self.players[:self.top_players_to_reproduce]
        print("Tournament finished!")
        print("Final standings:")
        for player in top_players:
            print(
                f"{player.__class__.__name__} - Score: {self.scores[player]}")

        self.new_game = False


def create_players():
    players = [
        AlwaysCooperate(), AlwaysCooperate(), AlwaysCooperate(),
        AlwaysBetray(), AlwaysBetray(), AlwaysBetray(),
        Copycat(), Copycat(), Copycat(),
        Copykitten(), Copykitten(), Copykitten(),
        Simpleton(), Simpleton(), Simpleton(),
        Random(), Random(), Random(), Random(),
        Grudger(), Grudger(), Grudger(),
        Detective(), Detective(), Detective(),
    ]
    return players


def main():
    new_game = True
    # Define tournament parameters
    number_of_rounds = 10
    number_of_top_players_to_reproduce = 5

    while True:
        if new_game:
            # Create initial set of players
            players = create_players()
            for player in players:
                print(f"{player.__class__.__name__}")

            print("__________________________________________________")

            # Create tournament instance and run the tournament
            tournament = Tournament(
                players, number_of_rounds, number_of_top_players_to_reproduce)
            tournament.run_tournament()
            new_game = False

        else:
            for player in new_players:
                print(f"{player.__class__.__name__}")

            print("__________________________________________________")
            tournament.run_tournament()

        # Get top 20 players from the previous tournament
        top_players_previous = tournament.players[:int(len(
            tournament.players)) - number_of_top_players_to_reproduce]

        # Get the top 5 players to reproduce
        top_players_to_reproduce = tournament.players[:number_of_top_players_to_reproduce]

        # Reset scores of top 5 players to reproduce
        for player in top_players_to_reproduce:
            tournament.scores[player] = 0

        # Add top 5 players to the new tournament with reset scores
        new_players = top_players_previous + top_players_to_reproduce

        prompt = input("Do you want to run another tournament? (y/n): ")
        if prompt.lower() != "y":
            break


if __name__ == "__main__":
    main()
