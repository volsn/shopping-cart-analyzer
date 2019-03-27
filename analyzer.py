import pandas


class CartAnalyser:
    
    def __init__(self, path='dataset.csv'):
        self.data = pandas.read_csv(path, header=None)
        
    def recomendations_for_product(self, product, quantity=-1):
        """ Building recomendations for the product
        :product: string
        
        """
        baskets = self._divide_carts()
        items = self._extract_items(baskets)
        products, percentage = self._count_items(baskets, items, min_percent=0.4)
        baskets_with_products = self._search_items(baskets, product)
        recomendations, percentage = self._count_items(pork, items, min_percent=0.1)

        if quantity == -1:
            return recomendations
        else:
            return recomendations[0:quantity - 1]

    def recomendation_for_cart (self, cart):

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

            return recomendation

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
