#! /usr/bin/env python
#coding=utf-8
import urllib2
import json


class readjson():
    def read(self,obj,key):
        collect = list()
        for k in obj:
            v = obj[k]

            if isinstance(v,str) or isinstance(v,unicode):
                if key== ' ':
                    collect.append({k:v})
                else:
                    collect.append({str(key)+"."+k:v})
            elif isinstance(v,int):
                if key== ' ':
                    collect.append({k:v})
                else:
                    collect.append({str(key)+"."+k:v})
            elif isinstance(v,bool):
                if key== ' ':
                    collect.append({k:v})
                else:
                    collect.append({str(key)+"."+k:v})
            elif isinstance(v,dict):
                collect.extend(self.read(v,k))
            elif isinstance(v,list):
                collect.extend(self.readList(v,key))
        return collect

    def readList(self,obj,key):
        collect = list()
        for index,item in enumerate(obj):
            for k in item:
                v = item[k]
                if isinstance(v,str) or isinstance(v,unicode):
                    collect.append({key+"["+str(index)+"]"+"."+k:v})
                elif isinstance(v,int):
                    collect.append({key+"["+str(index)+"]"+"."+k:v})
                elif isinstance(v,bool):
                    collect.append({key+"["+str(index)+"]"+"."+k:v})
                elif isinstance(v,dict):
                    collect.extend(self.read(v,key+"["+str(index)+"]"))
                elif isinstance(v,list):
                    collect.extend(self.readList(v,key+"["+str(index)+"]"))
        return collect


ojt={"a":"q","b":{"3":{"e":"09"},"4":"tr"},"iu":[{"ye":"fg","er":"67"},{"rt":"if"}]}
red = readjson()
print red.read(ojt,' ')