from typing import TypedDict


type Rubles = int
type PIN = str

class Card(TypedDict):
    pin: PIN
    balance: Rubles

type CardNumber = str
type Cards = dict[CardNumber, Card]