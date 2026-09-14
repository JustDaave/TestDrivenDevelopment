from decimal import Decimal


class Product:
    def __init__(self, sku, name, price, taxable):
        if sku == "":
            raise ValueError("SKU cannot be empty")
        if name == "":
            raise ValueError("name cannot be empty")
        if price < Decimal("0.00"):
            raise ValueError("price cannot be negative")

        self.sku = sku
        self.name = name
        self.price = price
        self.taxable = taxable


class LineItem:
    def __init__(self, product, quantity):
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise ValueError("quantity must be a whole number")
        if quantity <= 0:
            raise ValueError("quantity must be greater than zero")

        self.product = product
        self.quantity = quantity

    def getSubtotal(self):
        return self.product.price * self.quantity


class Sale:
    def __init__(self):
        self.items = []
        self.discount_rate = Decimal("0.00")

    def addItem(self, product, quantity=1):
        new_item = LineItem(product, quantity)

        for item in self.items:
            if item.product.sku == product.sku:
                item.quantity += quantity
                return item

        self.items.append(new_item)
        return new_item

    def getItems(self):
        return self.items

    def removeItem(self, sku, quantity):
        for item in self.items:
            if item.product.sku == sku:
                if quantity > item.quantity:
                    raise ValueError("cannot remove more than the quantity in the sale")

                item.quantity -= quantity
                if item.quantity == 0:
                    self.items.remove(item)
                return

        raise ValueError("SKU is not in the sale")

    def getSubtotal(self):
        subtotal = Decimal("0.00")
        for item in self.items:
            subtotal += item.getSubtotal()
        return subtotal

    def getTaxableSubtotal(self):
        subtotal = Decimal("0.00")
        for item in self.items:
            if item.product.taxable:
                subtotal += item.getSubtotal()
        return subtotal

    def addPercentDiscount(self, discount_rate):
        self.discount_rate = discount_rate
