import numpy as np
import pandas


class CartAnalyser:
    
    def __init__(self, path):
        self.data = pandas.read_csv(path, header=None)
        
    def recomendations_for_product(self, product, quantity=-1):
        """ Building recomendations for the product
        :product: string
        
        """
        baskets = self._divide_carts(self.data)
        items = self._extract_items(baskets)
        products, percentage = self._count_items(baskets, items, min_percent=0.4)
        baskets_with_products = self._search_items(baskets, product)
        recomendations, percentage = self._count_items(pork, items, min_percent=0.1)
        
        return recomendations
        
    def _divide_carts(self):
        """ Divides given products into carts
        :rtype: list
        """
        
        baskets = []
        for id in data[1].unique():
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
                
        if quantity == -1:
            return recomendations
        else:
            return recomendations[0:quantity-1]
        
    def _search_items(self, baskets, product):
        """ Creates a list of baskets that include the exact product
        :baskets: list
        :product: string
        """
        
        carts = []
        for cart in basket:
            for item in cart:
                if item == product:
                    del cart[cart.index(product)]
                    carts.append(cart)
                    
        return carts
