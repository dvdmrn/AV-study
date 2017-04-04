# -*- coding: utf-8 -*-

import numpy as np
import sys

from enum import *

OrderedListErrors = enum('OBJECT_NOT_FOUND')

class OrderedListException(Exception):
    def __init__(self, code=0, message=""):
        self.args = (code, message)

class OrderedList():

    def __init__(self):

        self._new()

    def _new(self):
        
        self._list = np.array([])
        self._order = np.array([], dtype=int)

    def _append(self, item, order):

        self._list = np.append(self._list, item)
        self._order = np.append(self._order, order)
        
    def _move(self, order, down):
        
        if (down):
            if (order == int(self._order.max())): return
            value_to = order + 1
        else:
            if (order == int(self._order.min())): return
            value_to = order - 1

        index_from_swap = np.where(self._order == order)[0][0]
        index_to_swap = np.where(self._order == value_to)[0][0]
        
        value_to_swap = self._order[index_to_swap]
        self._order[index_to_swap] = self._order[index_from_swap]
        self._order[index_from_swap] = value_to_swap

    def _remove(self, objType, obj):

        if (isinstance(obj, objType)):
            try:
                index = np.where(self._list == obj)[0][0]
            except IndexError as e:
                raise OrderedListException(OrderedListErrors.OBJECT_NOT_FOUND)
        else:
            index = int(obj)

        order = self._order[index]
        
        self._list = np.delete(self._list, index)
        self._order = np.delete(self._order, index)
        
        indexes_to_adjust = np.where(self._order > order)[0]

        for index in indexes_to_adjust:
            self._order[index] = self._order[index] - 1

        return index

    def _remove_order(self, objType, order):
        
        try:
            index = np.where(self._order == order)[0][0]
        except IndexError as e:
            raise OrderedListException(OrderedListErrors.OBJECT_NOT_FOUND)
        
        return self._remove(objType, index)

    def _getNextOrder(self):
        
        order = 0
        if (self._order.size > 0): order = int(self._order.max()) + 1

        return order

    def _add(self, objType, obj):

        if (isinstance(obj, objType)):

            self._append(obj, self._getNextOrder())


    def moveUp(self, order):
        
        self._move(order, False)
        
    def moveDown(self, order):
        
        self._move(order, True)

    def getList(self):
        
        return self._list

    def getOrderedList(self):

        ordered = np.array([])
        
        if (self._list.size > 0):
            ordered = self._list[self._order.argsort()]

        return ordered

    def getOrder(self):
        
        return self._order

    def getItemFromOrder(self, order):

        try:
            index = np.where(self._order == order)[0][0]
        except IndexError as e:
            raise OrderedListException(OrderedListErrors.OBJECT_NOT_FOUND)

        return self._list[index]



class IndexedOrderedList(OrderedList):

    def __init__(self):

        OrderedList.__init__(self)

    def _new(self):

        OrderedList._new(self)
        self._id_list = np.array([], dtype=int)

    def _append(self, item, order, id):
        
        OrderedList._append(self, item, order)
        self._id_list = np.append(self._id_list, id)

    def _getNextId(self):

        id = 1
        if (self._id_list.size > 0): id = int(self._id_list.max()) + 1
        
        return id

    def _add(self, objType, obj):

        if (isinstance(obj, objType)):
            
            self._append(obj, self._getNextOrder(), self._getNextId())

    def _remove(self, objType, obj):

        index = OrderedList._remove(self, objType, obj)
        self._id_list = np.delete(self._id_list, index)

        return index

    def _remove_id(self, objType, id):

        try:
            index = np.where(self._id_list == id)[0][0]
        except IndexError as e:
            raise OrderedListException(OrderedListErrors.OBJECT_NOT_FOUND)
        
        return self._remove(objType, index)
    

    def getIdList(self):

        return self._id_list
