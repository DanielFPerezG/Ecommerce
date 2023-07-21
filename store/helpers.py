import json

class ProductCart:

    def numberProducts(cart):
        productCarts = json.loads(cart.products)
        numberProductsCart = 0
        for productJson in productCarts:
            numberProductsCart += 1

        return numberProductsCart

    def newProductCart(cart, newProduct):
        newProductCarts = []
        productCarts = json.loads(cart.products)
        for productJson in productCarts:
            if int(productJson["id"]) == int(newProduct.id):
                newProductCarts.append(productJson)

        return newProductCarts

    def subtotalCart(cart):
        subTotal= 0
        productCarts = json.loads(cart.products)

        for productJson in productCarts:
            subTotal += productJson['total']

        return subTotal