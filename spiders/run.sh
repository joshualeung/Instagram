#!/bin/bash

rm *.json
scrapy runspider ins.py -o result.jl
