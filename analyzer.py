import pandas
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import sys

app = Flask(__name__)
api = Api(app)


class CartAnalyser:
    
    def __init__(self, path='dataset.csv'):
        self.data = pandas.read_csv(path, header=None)
        
    def recomendations_for_product(self, product, quantity=-1):
        """ Building recomendations for the product
        :product: string
        
        """

        baskets = self._divide_carts()
        items = self._extract_items(baskets)
        baskets_with_products = self._search_items(baskets, product)
        recomendations_, percentage = self._count_items(baskets_with_products, items, min_percent=0.4)

        recomendations = []

        for rec in recomendations_:
            recomendations.append(iter(rec).__next__())

        if quantity == -1:
            return list(recomendations)
        else:
            return list(recomendations)[0:quantity]

    def recomendation_for_cart(self, cart, quantity=-1):

        recomendation = {}

        for product in cart:
            rec_for_product = self.recomendations_for_product(product)

            for rec in rec_for_product:
                if rec not in recomendation.keys():
                    recomendation[rec] = 0
                recomendation[rec] += 1

            sum = 0
            for rec in recomendation.keys():
                sum += recomendation[rec]

            k = 100.0 / sum
            for rec in recomendation.keys():
                recomendation[rec] = recomendation[rec] * k

            if quantity == -1:
                return list(recomendation.keys())
            else:
                return list(recomendation.keys())[0:quantity]

    def _divide_carts(self):
        """ Divides given products into carts
        :rtype: list
        """
        
        baskets = []
        for id in self.data[1].unique():
            temp = []
            for c, v in enumerate(self.data[1]):
                if v == id:
                    temp.append(self.data[2][c])
            baskets.append(temp)
        return baskets
        
    def _extract_items(self, basket):
        """ Finds which products were in all the give baskets
        :basket: list
        :rtype: set
        """
        
        items = set()
        for cart in basket:
            for item in cart:
                items.add(frozenset([item]))
        return items
    
    def _count_items(self, basket, items, min_percent):
        """ Finds how often the exact product is bought
        :basket: list
        :items: set
        :min_percent: int
        :rtype: tuple(set, dict)
        """
        
        item_count = {}
        percentage = {}
        n = len(basket)
        products = set()
        
        for cart in basket:
            for item in items:
                if item.issubset(cart):
                    if item not in item_count:
                        item_count[item] = 0
                    item_count[item] += 1
        
        for item in item_count:
            if (item_count[item] / float(n)) >= min_percent:
                products.add(item)
                percentage[item] = item_count[item] / float(n)
                
        return products, percentage
        
    def _search_items(self, baskets, product):
        """ Creates a list of baskets that include the exact product
        :baskets: list
        :product: string
        """
        
        carts = []
        for cart in baskets:
            for item in cart:
                if item == product:
                    del cart[cart.index(product)]
                    carts.append(cart)
                    
        return carts


class Index(Resource):

    def post(self):
        json = request.json
        ca = CartAnalyser()

        if json['type'] == 'single':
            product = json['product']
            if json['quantity'] is not None:
                rec = ca.recomendations_for_product(product, json['quantity'])
            else:
                rec = ca.recomendations_for_product(product)
        elif json['type'] == 'cart':
            cart = ca.recomendation_for_cart(json['cart'])
            if json['quantity'] is not None:
                rec = ca.recomendation_for_cart(cart, json['quantity'])
            else:
                rec = ca.recomendation_for_cart(cart)

        responce = {'recomendations': rec}

        return jsonify(responce)


    def get(self):
        return jsonify({'message': 'API to built customers cart recomendations'})


api.add_resource(Index, '/')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
