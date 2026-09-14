from decimal import Decimal

import pytest

from PointOfSale.point_of_sale import LineItem, Product, Sale


def describe_product():
    def test_product_stores_its_information():
        product = Product("A100", "Apple", Decimal("0.75"), True)

        assert product.sku == "A100"
        assert product.name == "Apple"
        assert product.price == Decimal("0.75")
        assert product.taxable is True

    def test_product_sku_cannot_be_empty():
        with pytest.raises(ValueError):
            Product("", "Apple", Decimal("0.75"), True)

    def test_product_name_cannot_be_empty():
        with pytest.raises(ValueError):
            Product("A100", "", Decimal("0.75"), True)

    def test_product_price_cannot_be_negative():
        with pytest.raises(ValueError):
            Product("A100", "Apple", Decimal("-0.75"), True)

    def test_product_price_can_be_zero():
        product = Product("F100", "Free Sample", Decimal("0.00"), False)

        assert product.price == Decimal("0.00")

    def test_product_can_be_taxable_or_non_taxable():
        taxable_product = Product("C100", "Coffee Mug", Decimal("8.50"), True)
        non_taxable_product = Product("B100", "Bread", Decimal("3.25"), False)

        assert taxable_product.taxable is True
        assert non_taxable_product.taxable is False


def describe_line_item():
    def test_line_item_stores_a_product_and_quantity():
        product = Product("A100", "Apple", Decimal("0.75"), False)
        item = LineItem(product, 3)

        assert item.product is product
        assert item.quantity == 3

    def test_line_item_quantity_must_be_a_whole_number():
        product = Product("A100", "Apple", Decimal("0.75"), False)

        with pytest.raises(ValueError):
            LineItem(product, 1.5)

    def test_line_item_quantity_must_be_greater_than_zero():
        product = Product("A100", "Apple", Decimal("0.75"), False)

        with pytest.raises(ValueError):
            LineItem(product, 0)

    def test_get_subtotal_multiplies_price_by_quantity():
        product = Product("A100", "Apple", Decimal("0.75"), False)
        item = LineItem(product, 4)

        assert item.getSubtotal() == Decimal("3.00")


def describe_sale_items():
    def test_new_sale_starts_with_no_items():
        sale = Sale()

        assert sale.getItems() == []

    def test_add_item_adds_a_product_to_the_sale():
        sale = Sale()
        product = Product("A100", "Apple", Decimal("0.75"), False)

        sale.addItem(product)

        assert len(sale.getItems()) == 1
        assert sale.getItems()[0].product is product

    def test_add_item_uses_quantity_one_by_default():
        sale = Sale()
        product = Product("A100", "Apple", Decimal("0.75"), False)

        sale.addItem(product)

        assert sale.getItems()[0].quantity == 1

    def test_add_item_can_add_more_than_one_product():
        sale = Sale()
        product = Product("A100", "Apple", Decimal("0.75"), False)

        sale.addItem(product, 4)

        assert sale.getItems()[0].quantity == 4

    def test_adding_the_same_sku_increases_the_quantity():
        sale = Sale()
        apples = Product("A100", "Apple", Decimal("0.75"), False)

        sale.addItem(apples, 2)
        sale.addItem(apples, 3)

        assert len(sale.getItems()) == 1
        assert sale.getItems()[0].quantity == 5
