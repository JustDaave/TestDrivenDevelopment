# Point of Sale System

## High Level Requirements

The point of sale system is for a small store.

It keeps track of products that a customer is buying.

Each product has a SKU, name, price, and whether it is taxable.

The system can add and remove products from a sale.

It calculates the subtotal, discounts, tax, and final total.

This project only tests the program logic. It will not test user input, menus, or printed receipts.

## Specifications

Creating a product stores its SKU, name, price, and taxable status.

A product SKU cannot be empty.

A product name cannot be empty.

A product price cannot be negative.

A product price can be zero.

A product can be taxable or non-taxable.

Creating a line item connects a product with a quantity.

A line item quantity must be a whole number.

A line item quantity must be greater than zero.

`getSubtotal()` on a line item returns the product price times its quantity.

Creating a sale starts with no items.

`addItem()` adds a product to the sale.

`addItem()` uses a quantity of one when no quantity is given.

Adding a quantity greater than one adds that many products.

Adding the same SKU again increases the quantity of the existing line item.

Adding a different SKU creates a different line item.

An item with a quantity of zero cannot be added.

An item with a negative quantity cannot be added.

`removeItem()` removes the requested quantity from the sale.

Removing some of an item's quantity leaves the rest in the sale.

Removing all of an item's quantity removes its line item.

Removing an SKU that is not in the sale throws an error.

Removing more than the available quantity throws an error.

If removing an item throws an error, the sale does not change.

`getItems()` returns the items currently in the sale.

`getSubtotal()` returns the total price before discounts and tax.

The subtotal of an empty sale is $0.00.

`getTaxableSubtotal()` includes only taxable products.

The taxable subtotal is $0.00 when all products are non-taxable.

A percent discount can be added to a sale.

A percent discount must be between 0% and 100%.

A 0% discount does not change the sale total.

A 100% discount reduces the subtotal to $0.00.

Discounts are calculated before tax.

The discount cannot be greater than the subtotal.

`getDiscountTotal()` returns the amount saved.

`getTax()` returns the tax on the discounted taxable subtotal.

A sale with no taxable products has $0.00 tax.

The tax rate cannot be negative.

The tax rate cannot be greater than 100%.

`getTotal()` returns the subtotal minus discounts plus tax.

The total of an empty sale is $0.00.

The total can never be negative.

All money calculations are rounded to two decimal places.

Half of a cent is rounded up.

Invalid values throw a `ValueError`.

## Point of Sale State Data

Product SKU: string

Product name: string

Product price: decimal number

Taxable: True or False

Quantity: positive whole number

Items: list of line items

Tax rate: decimal number from 0 to 1

Discount rate: decimal number from 0 to 1

Subtotal: decimal number

Discount total: decimal number

Tax: decimal number

Total: decimal number

## Point of Sale Operations

Create a product

Create a sale

Add an item

Remove an item

Get the items

Calculate the subtotal

Calculate the taxable subtotal

Apply a percent discount

Calculate tax

Calculate the final total

## Testing Requirement

The final test suite will have at least 30 different unit tests. Each specification above can be tested by calling a class method and checking its return value, state, or error. Tests will not check keyboard input or printed output.

## Parking Lot

Print a receipt

Accept cash or card payments

Calculate change

Add buy-one-get-one-free sales

Keep track of inventory

Save products to a file or database

Add a barcode scanner
