import random


class SolitaireClass:
    def __init__(self, deck):
        self.joker_one = 53
        self.joker_two = 54
        self.deck = deck

    def prep_message(self, message):
        prepped = ""
        message = message.upper()
        for i in message:
            if i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                prepped += i

        return prepped

    def text_to_numbers(self, text):
        number_list = []
        for i in text:
            index = 0

            for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                index += 1
                if x == i:
                    number_list.append(index)
        return number_list

    def numbers_to_text(self, numbers):
        text = ""
        alpha_numbers = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
                         "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        for i in numbers:
            text += alpha_numbers[i - 1]
        return text

    def first_joker_down_one(self):
        joker_index = self.deck.index(self.joker_one)
        if joker_index != len(self.deck) - 1:
            swap_index = (joker_index + 1) % len(self.deck)
            self.deck[joker_index], self.deck[swap_index] = self.deck[swap_index], self.deck[joker_index]
        else:
            temp_deck = [i for i in range(len(self.deck))]
            temp_deck[0] = self.deck[0]
            temp_deck[1] = self.deck[joker_index]
            for i in range(2, len(self.deck)):
                temp_deck[i] = self.deck[i - 1]
            self.deck = temp_deck
        return self.deck

    def second_joker_down_two(self):
        joker_index = self.deck.index(self.joker_two)
        if joker_index != (len(self.deck) - 1) and joker_index != (len(self.deck) - 2):
            temp = self.deck[joker_index]
            self.deck[joker_index] = self.deck[joker_index + 1]
            self.deck[joker_index + 1] = self.deck[joker_index + 2]
            self.deck[joker_index + 2] = temp
        elif joker_index == (len(self.deck) - 2):
            temp_deck = [i for i in range(len(self.deck))]
            temp_deck[0] = self.deck[0]
            temp_deck[1] = self.deck[joker_index]
            temp_deck[len(self.deck) - 1] = self.deck[len(self.deck) - 1]
            for i in range(2, len(self.deck) - 1):
                temp_deck[i] = self.deck[i - 1]
            self.deck = temp_deck
        elif joker_index == (len(self.deck) - 1):
            temp_deck = [i for i in range(len(self.deck))]
            temp_deck[0] = self.deck[0]
            temp_deck[1] = self.deck[1]
            temp_deck[2] = self.deck[joker_index]
            for i in range(3, len(self.deck)):
                temp_deck[i] = self.deck[i - 1]
            self.deck = temp_deck
        return self.deck

    def three_way_cut(self):
        flag = False
        for i in self.deck:
            if i == self.joker_one or i == self.joker_two:
                if flag == False:
                    first_joker_index = self.deck.index(i)
                    flag = True
                else:
                    second_joker_index = self.deck.index(i)
        top_slice = self.deck[:first_joker_index:1]
        bottom_slice = self.deck[second_joker_index + 1::1]
        middle_slice = self.deck[first_joker_index:second_joker_index + 1:1]

        temp_deck = []
        for i in bottom_slice:
            temp_deck.append(i)
        for i in middle_slice:
            temp_deck.append(i)
        for i in top_slice:
            temp_deck.append(i)
        return temp_deck

    def top_to_bottom_cut(self):
        if self.deck[len(self.deck) - 1] == len(self.deck):
            value = len(self.deck) - 1
        else:
            value = self.deck[len(self.deck) - 1]
        top_slice = self.deck[:value:1]
        temp_deck = self.deck[value:len(self.deck) - 1:1]
        for i in top_slice:
            temp_deck.append(i)
        temp_deck.append(value)
        return temp_deck

    def get_key(self):
        top_card = self.deck[0]
        value = self.deck[top_card - 1]
        return value

    def generate_keystream(self, message_numbers):
        keystream = []
        for i in range(0, message_numbers):
            self.deck = self.first_joker_down_one()
            self.deck = self.second_joker_down_two()
            self.deck = self.three_way_cut()
            self.deck = self.top_to_bottom_cut()
            keystream.append(self.get_key())
        return keystream

    def encrypt_message(self, message, keystream):
        encrypted_message = []
        for i in range(len(message)):
            encrypted_message.append((message[i] + keystream[i]) % 26)
        return encrypted_message

    def decrypt_message(self, message, keystream):
        decrypted_message = []
        for i in range(len(message)):
            number = message[i] - keystream[i]
            number_two = abs(((number // 26) * 26) - number)
            decrypted_message.append(number_two)
        return decrypted_message
