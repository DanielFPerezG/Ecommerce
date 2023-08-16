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

    def productCartWithStock(cart, products):
        productCart = json.loads(cart.products)
        productCartWithStock = []

        for item in productCart:
            productId = item['id']
            productName = item['name']
            price = item['price']
            image_url = item['image_url']
            productTotal = item['total']
            quantity = item['quantity']
            product = products.get(pk=productId)
            stock = product.stock
            itemWithStock = {
                'id': productId,
                'name': productName,
                'price': price,
                'image_url': image_url,
                'total': productTotal,
                'quantity': quantity,
                'stock': stock,
            }
            productCartWithStock.append(itemWithStock)

        return productCartWithStock

    def productCartWithStockCheckout(cart, products):
        productCart = json.loads(cart.products)
        productCartWithStock = []

        for item in productCart:
            productId = item['id']
            productName = item['name']
            price = item['price']
            image_url = item['image_url']
            productTotal = item['total']
            quantity = item['quantity']
            product = products.get(pk=productId)
            stock = product.stock

            if int(quantity) > int(stock):
                productTotal = int(price)*int(stock)
                quantity = stock
            itemWithStock = {
                'id': productId,
                'name': productName,
                'price': price,
                'image_url': image_url,
                'total': productTotal,
                'quantity': quantity,
                'stock': stock,
            }
            productCartWithStock.append(itemWithStock)

        return productCartWithStock

    def subtotalCart(cart, page):
        subTotal = 0

        if page == 'cart':
            productCarts = json.loads(cart.products)

            for productJson in productCarts:
                subTotal += productJson['total']

            return subTotal

        else:
            for item in cart:
                subTotal += item['total']

            return subTotal
