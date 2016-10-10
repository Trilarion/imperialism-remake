************************
Economy
************************

The player needs income to pay for military, research, infrastructure and diplomatic actions. In this chapter it is
detailed how to gain money by selling/trading goods. International trade is a key element of the game.

* It increases the base of your income allowing larger investments in military and research.
* Increased trade improves international relations (also see :ref:`diplomacy`).
* Highly specialized economies are more productive.

Demand (consumption)
=============================

* The population is willing to pay for up to a certain amount of goods each turn. This is the demand.
* The demand of a single province can be normal (1.0x), poor (0.7x) or exceptional (1.5x).
* The base demand of a province is 1 unit of furniture and 1 unit of garment (maybe also paper and tools).
* The base demand may increase with a certain absolute value X (~0.01) per turn during the course of a scenario.
* A marketplace is the set of all provinces belonging to a single nation including colonies.
* For each marketplace the demand of all provinces belonging to this marketplace is summed up.
* People will buy and consume more than 100% of normal demand (up to 150%) if sufficient supply is present, but then the price will fall next
  turn. On the other hand if supply could not reach 100% of the demand, prices will increase. However, prices will increase
  so much that by keeping supply low and high alternately gives more profit than steadily supplying on an average basis.
* Base price of furniture and garment are ($300).
* Starvation: If the demand is not matched by the supply during the course of several turns (less than 70% fulfillment on
  average of the last 4 turns) then production of goods is severely reduced (30% penalty).

.. todo:: Provide formula for dependency price/demand/supply.

Trade
=============================

* Tradeable basic resources: fish&meat, grain&apple, wood, oil, ore, coal, cotton&wool
* Tradeable advanced products: timber, paper, furniture, cloth, garment, steel, weapon, can of food
* Each tradeable item can either be bought or sold.
* The amount to be bought or sold (target values) is specified during each turn.
* A minimal account balance is given, i.e. during trade the value of the current account should never fall below this limit. A buying
  transaction that would let the account fall under the limit is immediately canceled.
* Each marketplace has it's own prices.
* The prices are calculated by trade activity (demand and supply) during the last years.
* The prices are kept constant during one trade phase.
* Trade is performed simultaneously (all marketplaces one after another in a random order, for new each game turn
  there are multiple trade rounds with a random order).
* Trade capacity is important for sellers (sellers are responsible for delivery of the product). Selling transactions
  that would exceed the trade capacity are canceled. Players get an estimation how much trade capacity their sold products
  will approximately use.
* Subventions (15%, 30%, 50%) can additionally be placed on marketplaces, it means that the amount of product is
  adjusted, not the price. So as a buyer you get less units delivered than you paid for and as a seller you must
  deliver more units than you get paid for.
* Trade ends if nobody wants or can sell and buy anymore.
* During one trade round the marketplaces are executed in some random order. Typically there should be 5 – 10 trade rounds.
* On one marketplace, first all offers are collected, then these orders are ordered by best related nation to worst
  related nation, then all orders are partly fulfilled (not more than 2% or the demand per order)

.. todo:: Provide formula for price dependency on demand/supply of previous years. Subventions should work differently.
    You should get a higher market share directly but at the price of paying more.

Balance Sheet
=============================

* Income results from sold goods and some diplomatic treaties
* Expenses result from military upkeep, transportation network (railroad, merchant fleet) upkeep, buildings upkeep,
  construction costs, workforce salary, bought goods and from some diplomatic treaties