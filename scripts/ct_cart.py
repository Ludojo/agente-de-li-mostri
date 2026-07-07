# -*- coding: utf-8 -*-
"""Gestione carrello CardTrader. L'ACQUISTO NON E' IMPLEMENTATO, di proposito.

Uso:
  python scripts/ct_cart.py show
  python scripts/ct_cart.py add <product_id> [quantita'] [--direct]
  python scripts/ct_cart.py remove <product_id> [quantita']
"""
import sys

from ct_api import ct_get, ct_post


def show():
    d = ct_get("/cart")
    total = d.get("total", {}).get("cents", 0) / 100
    print(f"Carrello (id {d.get('id')}) — totale {total:.2f} EUR")
    for sc in d.get("subcarts", []):
        zero = "CT Zero" if sc.get("via_cardtrader_zero") else "diretto"
        print(f"  Venditore: {sc['seller']['username']} [{zero}]")
        for it in sc["cart_items"]:
            print(f"    - {it['product']['name_en']} x{it['quantity']} = "
                  f"{it['price_cents']/100:.2f} EUR (product_id {it['product']['id']})")
    if not d.get("subcarts"):
        print("  (vuoto)")
    print("\nRicorda: l'acquisto si conferma sul sito cardtrader.com, non da qui.")


def add(product_id, qty=1, via_zero=True):
    d = ct_post("/cart/add", {"product_id": int(product_id), "quantity": int(qty),
                              "via_cardtrader_zero": via_zero})
    print(f"Aggiunto. Totale carrello: {d['total']['cents']/100:.2f} EUR")


def remove(product_id, qty=1):
    d = ct_post("/cart/remove", {"product_id": int(product_id), "quantity": int(qty)})
    print(f"Rimosso. Totale carrello: {d['total']['cents']/100:.2f} EUR")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "show":
        show()
    elif cmd == "add":
        qty = next((a for a in sys.argv[3:] if a.isdigit()), 1)
        add(sys.argv[2], qty, via_zero="--direct" not in sys.argv)
    elif cmd == "remove":
        qty = next((a for a in sys.argv[3:] if a.isdigit()), 1)
        remove(sys.argv[2], qty)
    else:
        sys.exit(f"Comando sconosciuto: {cmd}\n{__doc__}")


if __name__ == "__main__":
    main()
