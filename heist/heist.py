#  Bankheist.py was created by Redjumpman for Redbot
#  This will create a system.JSON file and a data folder
#  This will modify values your bank.json from economy.py
import os
import asyncio
import random
from discord.ext import commands
from .utils.dataIO import fileIO
from random import randint
from .utils import checks
from __main__ import send_cmd_help
try:   # Check if Tabulate is installed
    from tabulate import tabulate
    tabulateAvailable = True
except:
    tabulateAvailable = False


class Heist:
    """Bankheist system inspired by Deepbot, a Twitch bot. Integrates with Economy"""

    def __init__(self, bot):
        self.bot = bot
        self.system = fileIO("data/bankheist/system.json", "load")
        self.good = [["{} had the car gassed up and ready to go +25 points.", 25],
                     ["{} cut the power to the bank +50 points.", 50],
                     ["{} erased the video footage +50 points", 50],
                     ["{} hacked the security system and put it on a loop feed +75 points", 75],
                     ["{} stopped the teller from triggering the silent alarm +50 points", 50],
                     ["{} knocked out the local security +50 points", 50],
                     ["{} stopped a local from being a hero +50 points", 50],
                     ["{} got the police negotiator to deliver everyone pizza +25 points", 25],
                     ["{} brought masks of former presidents to hide our identity +25 points", 25],
                     ["{} found an escape route +25 points", 25],
                     ["{} brought extra ammunition for the crew +25 points", 25],
                     ["{} cut through that safe like butter +25 points", 25],
                     ["{} kept the hostages under control +25 points", 25],
                     ["{} counter sniped a sniper +100 points", 100],
                     ["{} distracted the guard +25 points", 25],
                     ["{} brought a Go-Bag for the team +25 points", 25],
                     ["{} found a secret stash in the deposit box room +50 points", 25],
                     ["{} found a box of jewelry on a civilian, +25 points", 25]]
        self.bad = ["A shoot out with local authorities began and {} was hit." + "\n" +
                    "```{} dropped out.```",
                    "The cops dusted for finger prints and arrested {}" + "\n" +
                    "```{} dropped out.```",
                    "{} thought they could double cross the crew and paid for it." + "\n" +
                    "```{} dropped out.```",
                    "{} blew a tire in the getaway car" + "\n" +
                    "```{} dropped out.```",
                    "{}'s gun jammed while trying to fight with local security and was shot" + "\n" +
                    "```{} dropped out.```",
                    "{} held off the police while the crew was making their getaway" + "\n" +
                    "```{} dropped out.```",
                    "A hostage situation went south, and {} was captured" + "\n" +
                    "```{} dropped out.```",
                    "{} showed up to the heist high as kite, and was subsequently apprehended." + "\n" +
                    "```{} dropped out.```",
                    "{}'s bag of money contained exploding blue ink and was later caught" + "\n" +
                    "```{} dropped out.```",
                    "{} was sniped by a swat sniper" + "\n" +
                    "```{} dropped out.```",
                    "The crew decided to shaft {}" + "\n" +
                    "```{} dropped out.```",
                    "{} was hit by friendly fire" + "\n" +
                    "```{} dropped out.```",
                    "Security system's redundancies caused {} to be caught" + "\n" +
                    "```{} dropped out.```",
                    "{} accidentally revealed their identity." + "\n" +
                    "```{} dropped out.```",
                    "The swat team released sleeping gas, {} is sleeping like a baby" + "\n" +
                    "```{} dropped out.```",
                    "'FLASH BANG OUT!', was the last thing {} heard" + "\n" +
                    "```{} dropped out.```",
                    "'GRENADE OUT!', {} is now sleeping with the fishes" + "\n" +
                    "```{} dropped out.```",
                    "{} tripped a laser wire and was caught" + "\n" +
                    "```{} dropped out.```",
                    "Before the crew could intervene a security guard tazed {} and is now incapacitated." + "\n" +
                    "```{} dropped out.```",
                    "Swat came through the vents, and neutralized {}." + "\n" +
                    "```{} dropped out.```"]

    async def ready_up(self):
        flag = True
        while flag:
            fileIO("data/bankheist/system.json", "save", self.system)
            await asyncio.sleep(1)
            self.system["Banks"]["The Local Bank"]["Vault"] += 22
            self.system["Banks"]["First National Bank"]["Vault"] += 31
            self.system["Banks"]["PNC Bank"]["Vault"] += 48
            self.system["Banks"]["Bank of America"]["Vault"] += 53
            self.system["Banks"]["Fort Knox"]["Vault"] += 60
            fileIO("data/bankheist/system.json", "save", self.system)
            frequency = self.system["Config"]["Vault Frequency"]
            await asyncio.sleep(frequency)  # task runs every 60 seconds

    @commands.group(pass_context=True, no_pm=True)
    async def heist(self, ctx):
        """General heist related commands"""

        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @heist.command(name="play", pass_context=True)
    async def _play_heist(self, ctx, bet: int):
        """This begin's a heist"""
        user = ctx.message.author
        server = ctx.message.server
        if bet >= 50:
            if self.account_check(user):
                if self.enough_points(user.id, bet, server):
                    if self.cooldown:  # time between heists
                        if self.heist_started:  # Checks if a heist is currently happening
                            if self.heist_plan():  # checks if a heist is being planned or not
                                self.system["Config"]["Min Bet"] = bet
                                self.heist_ptoggle()
                                self.heist_stoggle()
                                self.crew_add(user.id, user.name, bet)
                                self.subtract_bet(user.id, bet, server)
                                wait = self.system["Config"]["Wait Time"]
                                time = int(wait / 2)
                                half_time = int(time / 2)
                                split_time = int(half_time / 2)
                                await self.bot.say("A heist as been started by " + user.name +
                                                   "\n" + str(wait) + " seconds until the heist begins")
                                await asyncio.sleep(time)
                                await self.bot.say(str(time) + " seconds until the heist begins")
                                await asyncio.sleep(half_time)
                                await self.bot.say(str(half_time) + " seconds until the heist begins")
                                await asyncio.sleep(split_time)
                                await self.bot.say("Hurry up! " + str(split_time) + " seconds until the heist begins")
                                await asyncio.sleep(split_time)
                                await self.bot.say("Lock and load. The heist is starting")
                                self.system["Config"]["Bankheist Running"] = "Yes"
                                fileIO("data/bankheist/system.json", "save", self.system)
                                bank = self.check_banks()
                                await self.bot.say("The crew has decided to hit " + bank)
                                j = self.game_outcomes()
                                j_temp = j[:]
                                while j_temp is not None:
                                    result = random.choice(j_temp)
                                    j_temp.remove(result)
                                    await asyncio.sleep(10)
                                    await self.bot.say(result)
                                    if len(j_temp) == 0:
                                        self.system["Config"]["Bankheist Running"] = "No"
                                        fileIO("data/bankheist/system.json", "save", self.system)
                                        await asyncio.sleep(2)
                                        await self.bot.say("The Heist is over.")
                                        await asyncio.sleep(2)
                                        if self.system["Heist Winners"]:
                                            target = self.system["Config"]["Bank Target"]
                                            amount = self.system["Banks"][target]["Vault"] / self.system["Config"]["Players"]
                                            winners_names = [subdict["Name"] for subdict in self.system["Heist Winners"].values()]
                                            pullid = ', '.join(subdict["User ID"] for subdict in self.system["Heist Winners"].values())
                                            winners_bets = [subdict["Bet"] for subdict in self.system["Heist Winners"].values()]
                                            winners_bonuses = [subdict["Bonus"] for subdict in self.system["Heist Winners"].values()]
                                            winners = pullid.split()
                                            vtotal = self.system["Banks"][target]["Vault"]
                                            vault_remainder = vtotal - amount * len(winners)
                                            self.system["Banks"][target]["Vault"] -= int(round(vault_remainder))
                                            fileIO("data/bankheist/system.json", "save", self.system)
                                            multiplier = self.system["Banks"][bank]["Multiplier"]
                                            sm_raw = [int(round(x)) * multiplier for x in winners_bets]
                                            success_multiplier = [int(round(x)) for x in sm_raw]
                                            cs_raw = [amount] * int(round(self.system["Config"]["Players"]))
                                            credits_stolen = [int(round(x)) for x in cs_raw]
                                            total_winnings = [int(round(x)) + int(round(y)) + int(round(z)) for x, y, z in zip(success_multiplier, credits_stolen, winners_bonuses)]
                                            self.add_total(winners, total_winnings, server)
                                            z = list(zip(winners_names, winners_bets, success_multiplier, credits_stolen, winners_bonuses, total_winnings))
                                            t = tabulate(z, headers=["Players", "Bets", "Bet Payout", "Credits Stolen", "Bonuses", "Total Haul"])
                                            await self.bot.say("The total haul was split " +
                                                               "among the winners: ")
                                            await self.bot.say("```Python" + "\n" + t + "```")
                                            self.heistclear()
                                            self.winners_clear()
                                            break
                                        else:
                                            await self.bot.say("No one made it out safe.")
                                            self.heistclear()
                                            break
                                    else:
                                        continue
                            elif self.system["Config"]["Bankheist Running"] == "No":
                                if bet >= self.system["Config"]["Min Bet"]:
                                    if self.crew_check(user.id):  # join a heist that was started
                                        self.crew_add(user.id, user.name, bet)
                                        self.subtract_bet(user.id, bet, server)
                                        await self.bot.say(user.name + " has joined the crew")
                                    else:
                                        await self.bot.say("You are already in the crew")
                                else:
                                    minbet = self.system["Config"]["Min Bet"]
                                    await self.bot.say("Your bet must be equal to a greater" +
                                                       " than the starting bet of " + str(minbet))
                            elif self.system["Config"]["Bankheist Started"] == "Yes":
                                await self.bot.say("You can't join a heist in progress")
                            else:
                                await self.bot.say("If you are seeing this, I dun fucked up.")
                        else:
                            await self.bot.say("You can't join an ongoing heist")
                    else:
                        await self.bot.say("The cops are on high alert. Let's lay low for a while")
                else:
                    await self.bot.say("You don't have enough points to cover the minimum bet.")
            else:
                await self.bot.say("You need a bank account to place bets")
        else:
            await self.bot.say("Starting bet must at least be 50 points.")

    @heist.command(name="reset", pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _reset_heist(self, ctx):
        """Try using this only if shit is broken!"""
        self.heistclear()
        await self.bot.say("Bankheist has been reset.")

    @heist.command(name="banks", pass_context=True)
    async def _banks_heist(self, ctx):
        """Shows banks info"""
        column1 = []
        column2 = []
        column3 = []
        column4 = []
        column5 = []
        for key in self.system["Banks"].keys():
            column1.append(key)
        for subdict in self.system["Banks"].values():
            column2.append(subdict['Crew'])
        for subdict in self.system["Banks"].values():
            column3.append(subdict['Multiplier'])
        for subdict in self.system["Banks"].values():
            column4.append(subdict["Vault"])
        for subdict in self.system["Banks"].values():
            column5.append(subdict["Success"])
        sr = [str(x) + "%" for x in column5]
        m = list(zip(column1, column2, column3, column4, sr))
        t = tabulate(m, headers=["Bank", "Crew", "Bet Multiplier", "Vault", "Success Rate"])
        await self.bot.say("```Python" + "\n" + t + "```")

    @heist.command(name="info", pass_context=True)
    async def _info_heist(self, ctx):
        """Displays information about the game"""
        msg = "```\n"
        msg += "To begin a heist type !heist play. " + "\n"
        msg += "The initial bet will set the minimum bet required for other crew members." + "\n"
        msg += "A planning period will allow you to gather more crew." + "\n"
        msg += "Other players can join by typing !heist play" + "\n"
        msg += "Once the heist begins you can no longer add crew members." + "\n"
        msg += "The game will run through scenarios, resulting in some sucesses and failures for the crew." + "\n"
        msg += "Those who are successful will take a portion of the vaults credits, and their bet times a multiplier" + "\n"
        msg += "Bigger banks have bigger vaults, and higher bet multipliers, but you will need a larger crew." + "\n"
        msg += "Banks will gradually refill their vaults over time." + "\n"
        msg += "To check out the banks, type !heist banks" + "\n"
        msg += "To change heist settings, type !setheist (admins only)" + "```"
        await self.bot.say(msg)

    @commands.group(pass_context=True, no_pm=True)
    async def setheist(self, ctx):
        """Set different options in the heist config"""

        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @setheist.command(name="multiplier", pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _multiplier_setheist(self, ctx, multiplier: float, *, bankname):
        """Set the payout multiplier for a bank
        """
        if multiplier > 0:
            if len(bankname) > 0:
                if bankname in self.system["Banks"]:
                    self.system["Banks"][bankname]["Multiplier"] = multiplier
                    fileIO("data/bankheist/system.json", "save", self.system)
                    await self.bot.say("```" + bankname + "'s multiplier is now set to " +
                                       str(multiplier) + "```")
                else:
                    await self.bot.say("This bank name does not exist")
            else:
                await self.bot.say("You need to give a bank name")
        else:
            await self.bot.say("You need to specify a multiplier")

    @setheist.command(name="time", pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _time_setheist(self, ctx, seconds: int):
        """Set the wait time for a heist to start
        """
        if seconds > 0:
            self.system["Config"]["Wait Time"] = seconds
            fileIO("data/bankheist/system.json", "save", self.system)
            await self.bot.say("I have now set the wait time to " + str(seconds) + " seconds.")
        else:
            await self.bot.say("Time must be greater than 0.")

    @setheist.command(name="success", pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _success_setheist(self, ctx, rate: int, *, bankname):
        """Set the success rate for a bank. 1-100 %
        """
        if bankname in self.system["Banks"]:
            if rate > 0 and rate <= 100:
                self.system["Banks"][bankname]["Success"] = rate
                fileIO("data/bankheist/system.json", "save", self.system)
                await self.bot.say("I have now set the success rate for " + bankname + " to " + str(rate) + ".")
            else:
                await self.bot.say("Success rate must be greater than 0 or less than or equal to 100.")

    @setheist.command(name="vault", pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _vault_setheist(self, ctx, amount: int, *, bankname):
        """Set the amount of credits in a bank's vault.
        """
        if amount > 0:
            if bankname in self.system["Banks"]:
                self.system["Banks"][bankname]["Vault"] = amount
                fileIO("data/bankheist/system.json", "save", self.system)
                await self.bot.say("I have set " + bankname + "'s vault to " + str(amount) + " credits.")
            else:
                await self.bot.say("That bank does not exist. Use the !heistbanks command to see a list of names.")
        else:
            await self.bot.say("You need to enter an amount higher than 0.")

    @setheist.command(name="frequency", pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _frequency_setheist(self, ctx, seconds: int):
        """Sets how frequently banks regenerate credits. Default: 60 seconds.
        """
        if seconds > 0:
            self.system["Config"]["Vault Frequency"] = seconds
            fileIO("data/bankheist/system.json", "save", self.system)
            await self.bot.say("Vaults will now increase in credits every " + str(seconds) + " seconds.")
        else:
            await self.bot.say("You need to enter an amount higher than 0.")

    def account_check(self, uid):
        bank = self.bot.get_cog('Economy').bank
        if bank.account_exists(uid):
            return True
        else:
            return False

    def heistclear(self):
        self.winners_clear()
        del self.system["Players"]
        del self.system["Heist Winners"]
        self.system["Players"] = {}
        self.system["Config"]["Bankheist Running"] = "No"
        self.system["Config"]["Planning Heist"] = "No"
        self.system["Config"]["Bankheist Started"] = "No"
        self.system["Heist Winners"] = {}
        self.system["Config"]["Min Bet"] = 0
        self.system["Config"]["Players"] = 0
        self.system["Config"]["Bank Target"] = ""
        fileIO("data/bankheist/system.json", "save", self.system)

    def enough_points(self, uid, amount, server):
        bank = self.bot.get_cog('Economy').bank
        mobj = server.get_member(uid)
        if self.account_check(mobj):
            if bank.can_spend(mobj, amount):
                return True
            else:
                return False
        else:
            return False

    def check_banks(self):
        if self.system["Config"]["Players"] <= self.system["Banks"]["The Local Bank"]["Crew"]:
            self.system["Config"]["Bank Target"] = "The Local Bank"
            fileIO("data/bankheist/system.json", "save", self.system)
            return "The Local Bank"
        elif self.system["Config"]["Players"] <= self.system["Banks"]["First National Bank"]["Crew"]:
            self.system["Config"]["Bank Target"] = "First National Bank"
            fileIO("data/bankheist/system.json", "save", self.system)
            return "First National Bank"
        elif self.system["Config"]["Players"] <= self.system["Banks"]["PNC Bank"]["Crew"]:
            self.system["Config"]["Bank Target"] = "PNC Bank"
            fileIO("data/bankheist/system.json", "save", self.system)
            return "PNC Bank"
        elif self.system["Config"]["Players"] <= self.system["Banks"]["Bank of America"]["Crew"]:
            self.system["Config"]["Bank Target"] = "Bank of America"
            fileIO("data/bankheist/system.json", "save", self.system)
            return "Bank of America"
        elif self.system["Config"]["Players"] > self.system["Banks"]["Bank of America"]["Crew"]:
            self.system["Config"]["Bank Target"] = "Fort Knox"
            fileIO("data/bankheist/system.json", "save", self.system)
            return "Fort Knox"

    def winners(self):
        for subdict in self.system["Heist Winners"].values():
            return subdict['Name']

    def game_outcomes(self):
        players = []
        for subdict in self.system["Players"].values():
            players.append(subdict)
        temp_good_things = self.good[:]  # coping the lists
        temp_bad_things = self.bad[:]
        chance = self.heist_chance()
        results = []
        for player in players:
            if randint(0, 100) <= chance:
                key = player["Name"]
                good_thing = random.choice(temp_good_things)
                temp_good_things.remove(good_thing)
                results.append(good_thing[0].format(key))
                self.system["Heist Winners"][key] = {"Name": key,
                                                     "User ID": player["User ID"],
                                                     "Bet": player["Bet"],
                                                     "Bonus": good_thing[1]}
                fileIO("data/bankheist/system.json", "save", self.system)
            else:
                key = player["Name"]
                bad_thing = random.choice(temp_bad_things)
                temp_bad_things.remove(bad_thing)
                results.append(bad_thing.format(key, key))
        return results

    def heist_chance(self):
        if self.system["Config"]["Bank Target"] == "The Local Bank":
            return self.system["Banks"]["The Local Bank"]["Success"]
        elif self.system["Config"]["Bank Target"] == "First National Bank":
            return self.system["Banks"]["First National Bank"]["Success"]
        elif self.system["Config"]["Bank Target"] == "PNC Bank":
            return self.system["Banks"]["PNC Bank"]["Success"]
        elif self.system["Config"]["Bank Target"] == "Bank of America":
            return self.system["Banks"]["Bank of America"]["Success"]
        elif self.system["Config"]["Bank Target"] == "Fort Knox":
            return self.system["Banks"]["Fort Knox"]["Success"]

    def winners_clear(self):
        del self.system["Heist Winners"]
        self.system["Heist Winners"] = {}
        fileIO("data/bankheist/system.json", "save", self.system)

    def crew_add(self, uid, name, bet):
        self.system["Players"][uid] = {"Name": name,
                                       "Bet": int(bet),
                                       "User ID": uid}
        self.system["Config"]["Players"] = self.system["Config"]["Players"] + 1
        fileIO("data/bankheist/system.json", "save", self.system)

    def crew_check(self, uid):
        if uid not in self.system["Players"]:
            return True
        else:
            return False

    def add_total(self, winners, totals, server):
        bank = self.bot.get_cog('Economy').bank
        for winner in winners:
            for total in totals:
                userid = winner.replace(',', '')
                mobj = server.get_member(userid)
                bank.deposit_credits(mobj, total)

    def subtract_bet(self, userid, bet, server):
        bank = self.bot.get_cog('Economy').bank
        mobj = server.get_member(userid)
        if self.account_check(mobj):
            bank.withdraw_credits(mobj, bet)

    def player_counter(self, number):
        self.system["Players"] = self.system["Players"] + number
        fileIO("data/bankheist/system.json", "save", self.system)

    def heist_plan(self):
        if self.system["Config"]["Planning Heist"] == "No":
            return True
        else:
            return False

    def heist_started(self):
        if self.system["Config"]["Bankheist Started"] == "No":
            return True
        else:
            return False

    def heist_stoggle(self):
        if self.system["Config"]["Bankheist Started"] == "Yes":
            self.system["Config"]["Bankheist Started"] = "No"
            fileIO("data/bankheist/system.json", "save", self.system)
        elif self.system["Config"]["Bankheist Started"] == "No":
            self.system["Config"]["Bankheist Started"] = "Yes"
            fileIO("data/bankheist/system.json", "save", self.system)

    def heist_ptoggle(self):
        if self.system["Config"]["Planning Heist"] == "No":
            self.system["Config"]["Planning Heist"] = "Yes"
            fileIO("data/bankheist/system.json", "save", self.system)
        elif self.system["Config"]["Planning Heist"] == "Yes":
            self.system["Config"]["Planning Heist"] = "No"
            fileIO("data/bankheist/system.json", "save", self.system)

    def cooldown(self):
        if self.system["Cooldown"] == "No":
            return True
        else:
            return False


def check_folders():
    if not os.path.exists("data/bankheist"):
        print("Creating data/bankheist folder...")
        os.makedirs("data/bankheist")


def check_files():
    system = {"Players": {},
              "Config": {"Bankheist Started": "No", "Planning Heist": "No",
                         "Cooldown": "Off", "Bankheist Running": "No", "Players": 0,
                         "Min Bet": 0, "Wait Time": 120, "Bank Target": "",
                         "Vault Frequency": 120},
              "Heist Winners": {},
              "Banks": {"The Local Bank": {"Crew": 3, "Multiplier": 0.25, "Success": 46, "Vault": 2000},
                        "First National Bank": {"Crew": 5, "Multiplier": 0.31, "Success": 40, "Vault": 5000},
                        "PNC Bank": {"Crew": 8, "Multiplier": 0.35, "Success": 37, "Vault": 8000},
                        "Bank of America": {"Crew": 10, "Multiplier": 0.42, "Success": 32, "Vault": 12000},
                        "Fort Knox": {"Crew": 15, "Multiplier": 0.5, "Success": 28, "Vault": 20000},
                        },
              }

    f = "data/bankheist/system.json"
    if not fileIO(f, "check"):
        print("Creating default bankheist system.json...")
        fileIO(f, "save", system)
    else:  # consistency check
        current = fileIO(f, "load")
        if current.keys() != system.keys():
            for key in system.keys():
                if key not in current.keys():
                    current[key] = system[key]
                    print("Adding " + str(key) +
                          " field to bankheist system.json")
            fileIO(f, "save", current)
        elif current["Config"].keys() != system["Config"].keys():
            for key in system["Config"].keys():
                if key not in current["Config"].keys():
                    current["Config"][key] = system["Config"][key]
                    print("Adding " + str(key) +
                          " field to bankheist system.json")
            fileIO(f, "save", current)
        elif current["Banks"].keys() != system["Banks"].keys():
            for key in system["Banks"].keys():
                if key not in current["Banks"].keys():
                    current["Banks"][key] = system["Banks"][key]
                    print("Adding " + str(key) +
                          " field to bankheist system.json")
            fileIO(f, "save", current)
        elif current["Banks"].keys() != system["Banks"].keys():
            for key in system["Banks"].keys():
                if key not in current["Banks"].keys():
                    current["Banks"][key] = system["Banks"][key]
                    print("Adding " + str(key) +
                          " field to bankheist system.json")
            fileIO(f, "save", current)


def setup(bot):
    check_folders()
    check_files()
    n = Heist(bot)
    bot.add_listener(n.ready_up, "on_ready")
    bot.add_cog(n)
