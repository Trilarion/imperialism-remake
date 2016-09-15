************************
Economy
************************

The player needs income to pay for military, research, infrastructure and diplomatic actions. In this chapter it is detailed how to gain money by selling/trading goods. International trade is a key element of the game because
* increasing the base of your income allows larger investments in military and research
* increased trade improves international relations (see chapter Diplomacy)
* highly specialized economies are more productive

Demand (consumption)
=============================

* The population is willing to pay up to a certain amount of goods each turn. This is the demand.
* The demand of a single province can be normal (1.0x), poor (0.7x) or exceptional (1.5x).
* The base demand of a province is 1 unit of furniture and 1 unit of garment (maybe also paper and tools).
* The base demand may increase with a certain absolute value X (0.01) per turn.
* For each marketplace the demand of all provinces belonging to this marketplace is sumed up.
* People will accept up to 150% of their demand if sufficient supply is present, but then the price will fall next
  turn. On the other hand if supply could not fullfill 100% of the demand, prices will increase. However never so that
  by keeping supply low and high alternatingly gives more profit than steadily supplying on an average basis.
* Base price of furniture and garment are ($300).
* Starvation: If the demand is not fullfilled during the course of several turns (less than 70% fullfillment on
  average of the last 4 turns) then production of goods is severely reduced (30% penalty).

.. todo:: Provide formula for dependency price/demand/supply.

Trade
=============================

* Tradeable basic resources: fish&meat, grain&apple, wood, oil, ore, coal, cotton&wool
* Tradeable advanced products: timber, paper, furniture, cloth, garment, steel, weapon, can of food
* Each tradeable item can either be bought or sold.
* The amount to be bought or sold is specified during each turn.
* A minimal account balance is given, i.e. during trade the account should never fall below this limit. A buying
  transaction that would let the account fall under the limit is immediately canceled.
* Every nation including its colonies forms one marketplace.
* Each marketplace has it's own prices.
* The prices are calculated by trade activity (demand and supply) during the last years.
* The prices are kept constant  during one trade phase.
* Trade is performed simultaneously (all marketplaces one after another in a random order that is new each game turn
  but with multiple rounds between them).
* Trade capacity is important for sellers (sellers are responsible for delivery of the product). Selling transactions
  that would exceed the trade capacity are canceled.
* Subventions (15%, 30%, 50%) can additionally be placed on marketplaces, it means that the amount of product is
  adjusted, not the price. So as a buyer you get less units delivered that you paid for and as a seller you must
  deliver more units than you get paid for.
* Trade ends if nobody wants or can sell and buy anymore.
* During one trade round the marketplaces are executed in some random order. It doesn't really matter as long as
  there are several rounds (typically 5 – 10).
* On one marketplace, first all offers are collected, then these orders are ordered by best related nation to worst
  related nation, then all orders are partly fullfilled (not more than 2% or the demand per order)

.. todo:: Provide formula for price dependency on demand/supply of previous years.

Balance Sheet
=============================

* Income results from sold goods and some diplomatic treaties
* Exprenses result from military upkeep, transportation network (railroad, merchant fleet) upkeep, buildings upkeep,
  construction costs, workforce salary, bought goods and from some diplomatic treaties