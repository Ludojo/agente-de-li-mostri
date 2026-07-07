# -*- coding: utf-8 -*-
"""Dove sono le mie carte? Stato della box CardTrader Zero e ordini recenti.

Uso:
  python scripts/ct_box.py           (box CT Zero: arrivate all'hub vs in viaggio)
  python scripts/ct_box.py orders    (ultimi ordini con stato e tracking)
"""
import sys

from ct_api import ct_get


def box():
    items = ct_get("/ct0_box_items")
    arrived = [i for i in items if i.get("arrived_at") and not i.get("cancelled_at")]
    transit = [i for i in items if not i.get("arrived_at") and not i.get("cancelled_at")]

    print(f"Box CardTrader Zero: {len(items)} oggetti")
    print(f"\n== In viaggio verso l'hub ({len(transit)}) ==")
    for i in sorted(transit, key=lambda x: x.get("estimated_arrived_at") or ""):
        eta = (i.get("estimated_arrived_at") or "?")[:10]
        print(f"  {i['name']:<35} | atteso {eta} | {i['seller']['username']}")
    tot_t = sum(i["buyer_price"]["cents"] for i in transit) / 100
    print(f"  Valore: {tot_t:.2f} EUR")

    print(f"\n== Arrivate all'hub, pronte per la spedizione finale ({len(arrived)}) ==")
    for i in sorted(arrived, key=lambda x: x["arrived_at"]):
        print(f"  {i['name']:<35} | arrivata {i['arrived_at'][:10]}")
    tot_a = sum(i["buyer_price"]["cents"] for i in arrived) / 100
    print(f"  Valore: {tot_a:.2f} EUR")


def orders():
    data = ct_get("/orders", sort="date.desc")
    print(f"Ordini totali: {len(data)} (ultimi 10)")
    for o in data[:10]:
        ship = o.get("order_shipping_method") or {}
        track = ship.get("tracking_code") or "-"
        print(f"  #{o['id']} | {o.get('paid_at','?')[:10]} | stato: {o['state']:<10} | "
              f"{o['size']} carte | {o.get('buyer_total',{}).get('cents',0)/100:.2f} EUR | tracking: {track}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "orders":
        orders()
    else:
        box()
