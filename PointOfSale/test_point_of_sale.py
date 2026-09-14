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

    def test_adding_a_different_sku_creates_a_different_line_item():
        sale = Sale()
        apples = Product("A100", "Apple", Decimal("0.75"), False)
        bread = Product("B100", "Bread", Decimal("3.25"), False)

        sale.addItem(apples)
        sale.addItem(bread)

        assert len(sale.getItems()) == 2
        assert sale.getItems()[0].product.sku != sale.getItems()[1].product.sku

    def test_item_with_zero_quantity_cannot_be_added():
        sale = Sale()
        product = Product("A100", "Apple", Decimal("0.75"), False)

        with pytest.raises(ValueError):
            sale.addItem(product, 0)

    def test_item_with_negative_quantity_cannot_be_added():
        sale = Sale()
        product = Product("A100", "Apple", Decimal("0.75"), False)

        with pytest.raises(ValueError):
            sale.addItem(product, -2)


def describe_removing_sale_items():
    def test_remove_item_removes_the_requested_quantity():
        sale = Sale()
        product = Product("A100", "Apple", Decimal("0.75"), False)
        sale.addItem(product, 5)

        sale.removeItem("A100", 2)

        assert sale.getItems()[0].quantity == 3

    def test_removing_some_items_leaves_the_rest_in_the_sale():
        sale = Sale()
        product = Product("A100", "Apple", Decimal("0.75"), False)
        sale.addItem(product, 4)

        sale.removeItem("A100", 1)

        assert len(sale.getItems()) == 1
        assert sale.getItems()[0].quantity == 3

    def test_removing_all_of_an_item_removes_its_line_item():
        sale = Sale()
        product = Product("A100", "Apple", Decimal("0.75"), False)
        sale.addItem(product, 2)

        sale.removeItem("A100", 2)

        assert sale.getItems() == []

    def test_removing_an_unknown_sku_raises_an_error():
        sale = Sale()

        with pytest.raises(ValueError):
            sale.removeItem("NOT-HERE", 1)

    def test_removing_more_than_available_raises_an_error():
        sale = Sale()
        product = Product("A100", "Apple", Decimal("0.75"), False)
        sale.addItem(product, 2)

        with pytest.raises(ValueError):
            sale.removeItem("A100", 3)

    def test_sale_does_not_change_when_removing_raises_an_error():
        sale = Sale()
        product = Product("A100", "Apple", Decimal("0.75"), False)
        sale.addItem(product, 2)

        with pytest.raises(ValueError):
            sale.removeItem("A100", 3)

        assert len(sale.getItems()) == 1
        assert sale.getItems()[0].quantity == 2


def describe_sale_totals():
    def test_get_items_returns_the_items_in_the_sale():
        sale = Sale()
        apples = Product("A100", "Apple", Decimal("0.75"), False)
        bread = Product("B100", "Bread", Decimal("3.25"), False)
        sale.addItem(apples)
        sale.addItem(bread)

        items = sale.getItems()

        assert len(items) == 2
        assert [item.product for item in items] == [apples, bread]

    def test_get_subtotal_returns_total_before_discount_and_tax():
        sale = Sale()
        apples = Product("A100", "Apple", Decimal("0.75"), False)
        mug = Product("C100", "Coffee Mug", Decimal("8.50"), True)
        sale.addItem(apples, 2)
        sale.addItem(mug)

        assert sale.getSubtotal() == Decimal("10.00")

    def test_empty_sale_has_zero_subtotal():
        sale = Sale()

        assert sale.getSubtotal() == Decimal("0.00")

    def test_taxable_subtotal_only_includes_taxable_products():
        sale = Sale()
        bread = Product("B100", "Bread", Decimal("3.25"), False)
        mug = Product("C100", "Coffee Mug", Decimal("8.50"), True)
        sale.addItem(bread)
        sale.addItem(mug, 2)

        assert sale.getTaxableSubtotal() == Decimal("17.00")

    def test_taxable_subtotal_is_zero_when_all_products_are_non_taxable():
        sale = Sale()
        apples = Product("A100", "Apple", Decimal("0.75"), False)
        bread = Product("B100", "Bread", Decimal("3.25"), False)
        sale.addItem(apples)
        sale.addItem(bread)

        assert sale.getTaxableSubtotal() == Decimal("0.00")


def describe_sale_discounts():
    def test_percent_discount_can_be_added_to_a_sale():
        sale = Sale()

        sale.addPercentDiscount(Decimal("0.20"))

        assert sale.discount_rate == Decimal("0.20")
