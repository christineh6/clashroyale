import requests # type: ignore
import tkinter as tk
from tkinter import messagebox, scrolledtext

#fetch battle history from Clash Royale API
def fetch_battle_history(api_key, player_tag):
    headers = {"Authorization": f"Bearer {api_key}"}
    url = f"https://api.clashroyale.com/v1/players/%23{player_tag}/battlelog"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        battles = response.json()
        return battles
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"Other error occurred: {err}"

# Function to display the battle history
def display_battle_history():
    api_key = api_key_entry.get()
    player_tag = player_tag_entry.get()

    if not api_key or not player_tag:
        messagebox.showwarning("Input Error", "Please enter both API key and player tag.")
        return

    battle_history = fetch_battle_history(api_key, player_tag)

    if isinstance(battle_history, list):
        # Clear the previous results
        battle_textbox.delete(1.0, tk.END)

        for battle in battle_history:
            result = "Victory" if battle['team'][0]['crowns'] > battle['opponent'][0]['crowns'] else "Defeat"
            team_deck = ", ".join([card['name'] for card in battle['team'][0]['cards']])
            opponent_deck = ", ".join([card['name'] for card in battle['opponent'][0]['cards']])
            battle_textbox.insert(tk.END, f"Result: {result}\n")
            battle_textbox.insert(tk.END, f"Your Deck: {team_deck}\n")
            battle_textbox.insert(tk.END, f"Opponent Deck: {opponent_deck}\n")
            battle_textbox.insert(tk.END, "-" * 40 + "\n")
    else:
        messagebox.showerror("Error", battle_history)

# Create the main application window
root = tk.Tk()
root.title("Clash Royale Battle History")

# Create the API key label and entry
api_key_label = tk.Label(root, text="API Key:")
api_key_label.grid(row=0, column=0, padx=10, pady=10)
api_key_entry = tk.Entry(root, width=50, show="*")
api_key_entry.grid(row=0, column=1, padx=10, pady=10)

# Create the player tag label and entry
player_tag_label = tk.Label(root, text="Player Tag (without #):")
player_tag_label.grid(row=1, column=0, padx=10, pady=10)
player_tag_entry = tk.Entry(root, width=50)
player_tag_entry.grid(row=1, column=1, padx=10, pady=10)

# Create the button to fetch battle history
fetch_button = tk.Button(root, text="Fetch Battle History", command=display_battle_history)
fetch_button.grid(row=2, column=0, columnspan=2, pady=10)

# Create a scrollable textbox to display battle history
battle_textbox = scrolledtext.ScrolledText(root, width=80, height=20)
battle_textbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Start the application loop
root.mainloop()