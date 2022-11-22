#!/bin/python3

import json
import random
import smtplib, ssl
from getpass import getpass

# Open json with names
try:
    file = open("names.json", "r")
except FileNotFoundError:
    print("[ERROR] Names file not found!")
    exit(1)
except Exception as err:
    print(err)
    exit(1)
else:
    names_and_emails = json.load(file)
    file.close()

# Open json with email settings
try:
    file = open("settings.json", "r")
except FileNotFoundError:
    print("[ERROR] Settings file not found!")
    exit(1)
except Exception as err:
    print(err)
    exit(1)
else:
    settings = json.load(file)
    file.close()

# Get all the names
names = list(names_and_emails.keys())
print("Got {} names!\n".format(len(names)))
for i in range(len(names)):
    print("{}: {} -> {}".format(i+1, names[i], names_and_emails[names[i]]))
print()

# Create a new list with all names and start drawing
names_aux = names.copy()
result = {}
for person in names:
    rand_num = random.randint(0, len(names_aux) - 1)
    # Check if a person got his own name
    if person == names_aux[rand_num]:
        continue
    else:
        result[person] = names_aux[rand_num]
        names_aux.pop(rand_num)

# Save the result
with open("result.json", "w") as file:
    json.dump(result, file)

# Check if port exists, otherwise set to default port
try:
    port = settings["port"]
except:
    port = 465 # default port for Gmail's SMTP 
# Check if smtp domain exists, otherwise set to Gmail
try:
    smtp_link = settings["smtp_link"]
except:
    smtp_link = "smtp.gmail.com"
try:
    sender = settings["sender"]
except:
    print("[ERROR] No sender provided. Please, check your settings.")
    exit(1)

password = getpass("Type your email password: ")

print("\nSMTP settings:")
print("port = {}".format(port))
print("smtp_link = {}".format(smtp_link))
print("sender = {}".format(sender))

context = ssl.create_default_context()

message = """\
        Subject: Natal Familia De Franco 2022!

        Ola!

        Sejam bem vindos a mais um natal da familia De Franco!

        E como sempre, claro, nao podia faltar nosso amigo secreto =)

        Neste ano, voce {sender} tirou o(a) {receiver}!

        Esperamos por voce la! Feliz Natal!

        
        Por favor, este e um email automatico enviado por um computador usando o email do autor deste codigo. Favor nao responder.

        Obs: Este software foi escrito por Hiago De Franco, o source code pode ser verificado aqui: https://github.com/hiagofranco/secret-santa-python. O codigo eh open source."""

print("\nOpening connection...")
# Open connection
try:
    with smtplib.SMTP_SSL(smtp_link, port, context=context) as server:
        server.login(settings["sender"], password)
        # Send email
        for person in result:
            print("Sending email to {}: {}...".format(person, names_and_emails[person]))
            server.sendmail(
                settings["sender"],
                names_and_emails[person],
                message.format(sender=person, receiver=result[person])
            )

except Exception as err:
    print("[ERROR] {}".format(err))

else:
    print("Finished successfully!")
