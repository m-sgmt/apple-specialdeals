# -*- coding: utf-8 -*-

import sys
import os

sys.path.append("/Users/sgmt/GitHub/apple-specialdeals/apple")
os.environ['DJANGO_SETTINGS_MODULE'] = 'apple.settings'

from specialdeals.models import Product
from specialdeals.models import ModelLine
from specialdeals.models import Offer

from pyquery import PyQuery as pq
import re
import datetime

offer_price = {}

def get_Monitor(spec):
    r_inch = re.compile("^([1-9.]+)")
    try:
        result_inch = r_inch.search(spec)
        return result_inch.group(1)
    except:
        None

def get_CPU(spec):
    r_CPU = re.compile("([0-9.]+GHz(\w+Intel i[0-9]| \w+ Intel Xeon E[0-9]))")
    try:
        result_CPU = r_CPU.search(spec)
        return result_CPU.group(1)
    except:
        None

def get_ModelYear(spec):
    r_ModelYear = re.compile("([0-9]+年[0-9]+月)")
    try:
        result_ModelYear = r_ModelYear.search(spec)
        return result_ModelYear.group(1)
    except:
        None

def get_RAM(spec):
    r_RAM = re.compile("\s([0-9]*GB)(のメモリ|メモリ| [0-9]+MHz DDR\w+ \w+RAM|（[0-9]GB x [0-9]）)")
    try:
        result_RAM = r_RAM.search(spec)
        return result_RAM.group(1)
    except:
        None

def get_Disk(spec):
    r_Disk = re.compile("\s([0-9]*(GB|TB)\S*(ATA|フラッシュストレージ| PCIeベースフラッシュストレージ))")
    try:
        result_Disk = r_Disk.search(spec)
        return result_Disk.group(1)
    except:
        None

def get_GPU(spec):
    r_GPU = re.compile("\s(Intel\s.*)$")
    try:
        result_GPU = r_GPU.search(spec)
        return result_GPU.group(1)
    except:
        None

def get_ProductID(url):
    r_ProductID = re.compile("http://store.apple.com/jp/product/(\w+)/\w+")
    try:
        result_ProductID = r_ProductID.search(url)
        return result_ProductID.group(1)
    except:
        None


def newProduct(model,productID,model_year,size,cpu,ram,disk,other,url):
    product = Product()
    product.model_line = model
    product.product_id = productID
    product.model_year = model_year
    product.size       = size
    product.cpu        = cpu
    product.ram        = ram
    product.disk       = disk
    product.other      = other
    product.url        = url
    product.save()

    return product

def newOffer(product,price):
    offer = Offer()
    offer.product = product
    offer.price = price
    offer.save()

def checkSoldOffer():
    for offer in Offer.objects.filter(sold=False):
        if not offer.product.product_id in offer_price:
            offer.sold = True
            offer.end = datetime.datetime.now()
            offer.save()

def getOffer(pd):
    for offer in Offer.objects.filter(sold=False):
        if offer.product.product_id == pd.product_id:
            return offer
    return None

def parseProductPage(url, model):
    url  = "http://store.apple.com" + url
    query = pq(url)

    pd = Product()

    for spec in query.find("meta"):
        if pq(spec).attr("name") == "description":
            try:
                pd = Product.objects.get(product_id=get_ProductID(url))
            except:
                pd = newProduct( model,
                            get_ProductID(url),
                            get_ModelYear(((pq(spec).attr("content")))),
                            get_Monitor(((pq(spec).attr("content")))),
                            get_CPU(((pq(spec).attr("content")))),
                            get_RAM(((pq(spec).attr("content")))),
                            get_Disk(((pq(spec).attr("content")))),
                            get_GPU(((pq(spec).attr("content")))),
                            url,
                          )

    for price in query.find("p.current_price"):
        offer = getOffer(pd)
        if offer == None:
            offer = newOffer(pd,pq(price).text())

        offer_price[pd.product_id] = pq(price).text()


def parseTopSite(url,model):
    query = pq(url)

    for product in query.find("a.button"):
        if pq(product).has_class("button") and pq(product).has_class("secondary"):
            parseProductPage(pq(product).attr('href'),model)


for model in ModelLine.objects.all():
    parseTopSite(model.url, model)

checkSoldOffer()
