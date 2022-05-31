
from tkinter.dnd import DndHandler
import discord
import random
import os

# import the names from dnd_commands.py
from dnd_commands import *


intents = discord.Intents.all()
intents.members = True


class Dbot(discord.Client):

    # The on_ready method
    async def on_ready(self):

        print('Logged in as')
        print(self.user)

    # The on_message method

    async def on_message(self, message):

        # If the message comes from 669108141354385418 (A channel) delete the message
        if message.channel.id == 669108141354385418:
            await message.delete()

        message_content = message.content.lower()
        message_parts = message_content.split(" ")

        # If the message starts with !roll
        if message_parts[0] == "!roll":
            await roll(message, message_parts)

        if message_parts[0] == "!pp":
            # Look for a file called "pp.txt" in the Pointless_Points folder in the same directory as this file
            with open("Pointless_Points/pp.txt", "r") as pp_file:
                pp_points = pp_file.read()
                await message.channel.send(pp_points)

        if message_parts[0] == "!settlement_name":
            await self.settlement_roll(message, message_parts)

        if "f to c" in message_content or "c to f" in message_content:
            await convert_temp(message, message_parts)


async def convert_temp(message, message_parts):
    if message_parts[1] == "f":
        celsius = (int(message_parts[0]) - 32) * 5/9
        await message.channel.send("Celsius: " + str(celsius))
    elif message_parts[1] == "c":
        fahrenheit = int(message_parts[0]) * 9/5 + 32
        await message.channel.send("Fahrenheit: " + str(fahrenheit))

        async def settlement_roll(self, message, message_parts):
            settlement_number = None
            if len(message_parts) > 1:
                # is the next word in the message a number?
                try:
                    settlement_number = int(message_parts[1])
                except:
                    pass

            if settlement_number is not None:
                # Get a amount of settlement names from the settlement_name_table list equal to the number
                settlement_names = random.sample(
                    settlement_name_table, settlement_number)
                # Join the settlement names together with a space in between
                settlement_names_string = " ".join(settlement_names)
                # Send the settlement names to the channel
                await message.channel.send(settlement_names_string)
            else:
                # Get a random settlement name from the settlement_name_table list
                settlement_name = random.choice(settlement_name_table)
                # Send the settlement name to the channel
                await message.channel.send(settlement_name)
        pass


async def roll(message, message_parts):
    roll_command = message_parts[1].split("d")
    # If there is a plus or minus after the dice
    addition = []
    if roll_command[1].find("+") != -1:
        addition = roll_command[1].split("+")
        roll_command[1] = addition[0]

    dice_count = int(roll_command[0])
    dice_type = int(roll_command[1])
    dice_rolls = []
    dice_total = 0
    for i in range(dice_count):
        dice_rolls.append(random.randint(1, dice_type))

        # If there was a addition
    if len(addition) > 1:
        await message.channel.send(str(dice_rolls) + " + " + addition[1] + " Total: " + str(sum(dice_rolls) + int(addition[1])))
    else:  # Send what every single dice rolled than send the usm
        await message.channel.send(str(dice_rolls) + " Total: " + str(sum(dice_rolls)))

# The main method


def main():
    # Print the text in tokon.txt
    token = open('Token.txt', 'r').read()

    # Create a new instance of Dbot
    dbot = Dbot(intents=intents)

    dbot.run(token)


if __name__ == '__main__':
    main()
