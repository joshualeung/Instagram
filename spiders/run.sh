#!/bin/bash

rm *.json
rm *.jl
scrapy runspider ins.py -o result.jl
