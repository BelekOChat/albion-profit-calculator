import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import requests
import unicodedata
from Item_Mapping import ITEMS
from Item_Mapping import RESSOURCES_PAR_ENCHANTEMENT

def get_market_data(item, city):

    url = f"https://europe.albion-online-data.com/api/v2/stats/prices/{item}.json?locations={city}&qualities=1"

    reponse = requests.get(url)
    donnees = reponse.json()

    if not donnees:
        return None

    city_data = donnees[0]["city"]
    sell_price = donnees[0]["sell_price_min"]


    return city_data, sell_price

def windows():
    
    root = tb.Window(
        title="Albion Profit Calculator",
        themename="darkly",
        size=(1000, 800),
        resizable=(True, True)
    )
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    title = tb.Label(
        root,
        text="Recherche de Prix Albion",
        font=("Arial", 24, "bold")
    )
    title.grid(
        row=0,
        column=0,
        pady=(30, 20)
    )

    main_frame = tb.Frame(
        root,
        padding=25
    )
    main_frame.grid(
        row=1,
        column=0,
        sticky="nsew"
    )
    main_frame.columnconfigure(1, weight=1)

    search_frame = tb.Labelframe(
        main_frame,
        text="Parametre de recherche",
    )
    search_frame.grid(
        row=0,
        column=0
    )
    search_frame.columnconfigure(1, weight=1)

    city_label = tb.Label(
        search_frame,
        text="Ville :",
        font=("Arial", 11)
    )
    city_label.grid(
        row=0,
        column=0,
        sticky="w",
        padx=(0, 15),
        pady=10
    )

    city_combobox = tb.Combobox(
        search_frame,
        values=[
            "Bridgewatch",
            "Caerleon",
            "Fort Sterling",
            "Lymhurst",
            "Martlock",
            "Thetford"
        ],
        state="readonly"
    )
    city_combobox.grid(
        row=0,
        column=1,
        sticky="ew",
        padx=10,
        pady=10
    )
    city_combobox.set("Lymhurst")

    tier_label = tb.Label(
         search_frame,
         text="Tier :",
         font=("Arial", 11)
    )
    tier_label.grid(
         row=1,
         column=0,
         sticky="w",
         padx=(0, 15),
         pady=10
    )

    tier_combobox = tb.Combobox(
         search_frame,
        values=[
             "T4",
             "T5",
             "T6",
             "T7",
             "T8"
        ],
        state="readonly"
    )
    tier_combobox.grid(
         row=1,
         column=1
    )
    tier_combobox.set("T4")

    enchantement_label = tb.Label(
         search_frame,
         text="Enchantement vers :",
         font=("Arial", 11)
    )
    enchantement_label.grid(
         row=2,
         column=0,
         sticky="w",
         padx=(0, 15),
         pady=10
    )

    enchantement_combobox = tb.Combobox(
         search_frame,
         values=[
              ".1",
              ".2",
              ".3"
         ],
         state="readonly"
    )
    enchantement_combobox.grid(
         row=2,
         column=1
    )
    enchantement_combobox.set(".1")

    entry_label = tb.Label(
         search_frame,
         text="Saisir l'identifiant de l'objet",
         font=("Arial", 11)
    )
    entry_label.grid(
         row=5,
         column=0,
         sticky="w",
         padx=(0, 15),
         pady=10
    )

    all_item_names = list(ITEMS.keys())

    item_search_variable = tk.StringVar()

    item_entry = tb.Entry(
         search_frame,
         textvariable=item_search_variable,
         font=("Arial", 11)
    )
    item_entry.grid(
        row=5,
        column=1,
        sticky="w",
        padx=(0, 15),
        pady=10
    )

    results_listbox = tk.Listbox(
        search_frame,
        height=10,
        font=("Arial", 11),
        bg="#303030",
        fg="white",
        selectbackground="#375a7f",
        selectforeground="white",
        borderwidth=0,
        highlightthickness=1,
        highlightbackground="#555555",
    )
    results_listbox.grid(
        row=6,
        column=0,
        columnspan=2,
        sticky="nsew",
        padx=10,
        pady=(0, 10)
    )

    result_label = tb.Label(
        root,
        text="Aucun prix trouvé",
        font=("Arial", 12)
    )
    result_label.grid(
         row=6,
         column=0,
         padx=(0, 15),
         pady=10
    )

    def rechercher():
        tier_level = tier_combobox.get()
        api_tier = tier_level + "_"
        nom_objet = item_entry.get()
        
        if nom_objet not in ITEMS:
            result_label.config(
                text="Sélectionne un objet valide dans la liste."
            )
            return
        
        item = api_tier + ITEMS[nom_objet]
        city = city_combobox.get()
        select_enchantement = enchantement_combobox.get()
        niveaux = select_enchantement.split(".")[1]
        api_enchantement = "@" + niveaux
        rune_text = rune_number_entry.get().strip()

        if not rune_text.isdigit():
            result_label.config(text="Saisis un nombre de runes valide.")
            return
        
        rune_quantity = int(rune_text)


        ressources = RESSOURCES_PAR_ENCHANTEMENT[select_enchantement]
        resource_total_cost = 0

        for ressource in ressources:
            ressource_id = f"{tier_level}_{ressource}"
            resultat_ressource = get_market_data(ressource_id, city)
            if resultat_ressource is None or resultat_ressource[1] == 0:
                result_label.config(
                    text=f"Prix indisponible pour {ressource_id}."
                )
                return

            _, prix_unitaire = resultat_ressource

            resource_total_cost += prix_unitaire * rune_quantity

        resultat = get_market_data(item, city)

        if resultat is None:
                result_label.config(text="Objet introuvable.")
                return

        ville, prix = resultat

        if prix == 0:
            result_label.config(
                 text="Prix indisponible"
            )
        else:
            add_enchant = item + api_enchantement
            prix_enchant = get_market_data(add_enchant, city)

            if prix_enchant is None or prix_enchant[1] == 0:
                result_label.config(text="Prix de l'objet enchanté indisponible.")
                return
            
            total_cost, market_fee, net_profit, roi = calculate_profit(
                prix,
                prix_enchant[1],
                resource_total_cost,
                6.5
            )

            total_cost_variable.set(f"{total_cost:,} Silver")
            
            item_cost_variable.set(f"{prix:,} Silver")

            resources_cost_variable.set(f"{resource_total_cost:,} Silver")

            enchanted_item_varaible.set(f"{prix_enchant[1]:,} Silver")

            market_fee_variable.set(f"{market_fee:,} Silver")

            roi_variable.set(f"{roi}%")

            result_label.config(
                text=f"Profit net : {net_profit:,} Silver"
            )                 

    search_button = tb.Button(
        root,
        text="Rechercher",
        command=rechercher
    )
    search_button.grid(
         row=7,
         column=0,
         pady=(30, 20)
    )

    rune_number_label = tb.Label(
         search_frame,
         text="Quantité de ressources par niveau",
         font=("Arial", 11)
    )
    rune_number_label.grid(
         row=4,
         column=0,
         sticky="w",
         padx=(0, 15),
         pady=10
    )

    rune_number_entry = tb.Entry(search_frame)
    rune_number_entry.grid(
         row=4,
         column=1,
    )

    recap_frame = tb.Labelframe(
        main_frame,
        text="Cout total et profit",
    )
    recap_frame.grid(
        row=0,
        column=1
    )
    recap_frame.columnconfigure(1, weight=1)

    flat_price_label = tb.Label(
        recap_frame,
        text="Côut de l'item :",
        font=("Arial", 11)
    )
    flat_price_label.grid(
        row=0,
        column=0,
        sticky="w",
        padx=(0, 10),
        pady=8
    )

    resources_cost_label = tb.Label(
        recap_frame,
        text="Côut total des resources :",
        font=("Arial", 11)
    )
    resources_cost_label.grid(
        row=1,
        column=0,
        sticky="w",
        padx=(0, 10),
        pady=8
    )

    total_cost_label = tb.Label(
        recap_frame,
        text="Côut total de l'item + resources :",
        font=("Arial", 11)
    )
    total_cost_label.grid(
        row=2,
        column=0,
        sticky="w",
        padx=(0, 10),
        pady=8
    )

    enchanted_item_label = tb.Label(
        recap_frame,
        text="Prix de l'item enchantée :",
        font=("Arial", 11)
    )
    enchanted_item_label.grid(
        row=3,
        column=0,
        sticky="w",
        padx=(0, 10),
        pady=8
    )

    market_fee_label = tb.Label(
        recap_frame,
        text="Frais du marchée :",
        font=("Arial", 11)
    )
    market_fee_label.grid(
        row=4,
        column=0,
        sticky="w",
        padx=(0, 10),
        pady=8
    )

    roi_label = tb.Label(
        recap_frame,
        text="Retour sur investissement :",
        font=("Arial", 11)
    )
    roi_label.grid(
        row=5,
        column=0,
        sticky="w",
        padx=(0, 10),
        pady=8
    )

    total_cost_variable = tb.StringVar(value="-")

    total_cost_value_label = tb.Label(
        recap_frame,
        textvariable=total_cost_variable,
        font=("Arial", 11)
    )
    total_cost_value_label.grid(
        row=2,
        column=1,
        sticky="w",
        padx=(0, 15),
        pady=5
    )

    item_cost_variable = tb.StringVar(value="-")

    item_cost_label = tb.Label(
        recap_frame,
        textvariable=item_cost_variable,
        font=("Arial", 11)
    )
    item_cost_label.grid(
        row=0,
        column=1,
        sticky="w",
        padx=(0, 10),
        pady=5
    )

    resources_cost_variable = tb.StringVar(value="-")

    resources_cost_label = tb.Label(
        recap_frame,
        textvariable=resources_cost_variable,
        font=("Arial", 11)
    )
    resources_cost_label.grid(
        row=1,
        column=1,
        sticky="w",
        padx=(0, 10),
        pady=5
    )

    enchanted_item_varaible = tb.StringVar(value="-")

    enchanted_item_label = tb.Label(
        recap_frame,
        textvariable=enchanted_item_varaible,
        font=("Arial", 11)
    )
    enchanted_item_label.grid(
        row=3,
        column=1,
        sticky="w",
        padx=(0, 10),
        pady=5
    )

    market_fee_variable = tb.StringVar(value="-")

    market_fee_label = tb.Label(
        recap_frame,
        textvariable=market_fee_variable,
        font=("Arial", 11)
    )
    market_fee_label.grid(
        row=4,
        column=1,
        sticky="w",
        padx=(0, 10),
        pady=5
    )

    roi_variable = tb.StringVar(value="-")

    roi_label = tb.Label(
        recap_frame,
        textvariable=roi_variable,
        font=("Arial", 11)
    )
    roi_label.grid(
        row=5,
        column=1,
        sticky="w",
        padx=(0, 10),
        pady=5
    )

    def filter_item(*args):

        search = normalize_text(item_entry.get().strip())

        if search == "":
            filtred_item = all_item_names
        else:
            filtred_item = [
                name 
                for name in all_item_names
                if search in normalize_text(name)
            ]
        results_listbox.delete(0, tk.END)

        for name in filtred_item:
            results_listbox.insert(tk.END, name)

    def select_item(event=None):
        selection = results_listbox.curselection()

        if not selection:
            return

        selected_name = results_listbox.get(selection[0])
        item_search_variable.set(selected_name)

    item_search_variable.trace_add("write", filter_item)

    results_listbox.bind("<<ListboxSelect>>", select_item)

    filter_item()
    root.mainloop()

def normalize_text(text):
    normalized = unicodedata.normalize("NFD", text.casefold())

    return "".join(
        character
        for character in normalized
        if not unicodedata.combining(character)
    )

def calculate_profit(flat_price, enchanted_price, resources_cost, fee_rate):

    total_cost = flat_price + resources_cost

    market_fees = enchanted_price * fee_rate / 100

    net_revenue = enchanted_price - market_fees

    net_profit = net_revenue - total_cost

    roi = net_profit / total_cost * 100

    return (
        round(total_cost),
        round(market_fees),
        round(net_profit),
        round(roi, 2)
    )

windows()