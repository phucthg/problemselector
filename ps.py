#codeforces script
#this script choose problem that is solved by some account but not some other account
#formally given two set of account SOLVED and UNSOLVED, a problem P is chosen if and only if P was solved by at least one account in SOLVED and P was not solved by any account in UNSOLVED
#input format:
#list of account in SOLVED
#list of account in UNSOLVED
#rating low, rating high
#list of tag that should be included
#list of tag that should be excluded
#(a problem is included if it has at least one tag that should be included and no tag that should be excluded
#tags in the same line should be separated using a comma without any extra space)
#number of output: 0 for all problems
import time
import json
from lxml import html
import requests
import random
def get_solved(account):
  ok=False
  temp=0
  while not ok:
    try:
        print(account)
        temp=json.loads(requests.get("https://codeforces.com/api/user.status?handle="+account, timeout=10).text)
        if(temp['status']=='OK'):
            ok=True
    except:
        print("error!")
  submissions=temp["result"]
  res=[]
  for s in submissions:
    if (s["verdict"]=="OK") and ("rating" in s["problem"]):
       if not s["problem"] in res:
        res.append(s["problem"])
  return res
def get_solved_list(accounts):
  res=[]
  for a in accounts:
    temp=get_solved(a)
    for p in temp:
       if not p in res:
        res.append(p)
  return res
def have_common_element(a, b):
  for x in a:
    if(x=="everything"):
      return True
  for x in b:
    if(x=="everything"):
      return True
  for x in a:
    if x in b:
      return True
  return False
def print_pretty(p):
  print(str(p["contestId"])+p["index"]+" "+str(p["rating"])+" tags: "+str(p["tags"]))
def print_clickable_contest(p):
  print("https://codeforces.com/contest/"+str(p["contestId"])+"/problem/"+p["index"])
def print_clickable_problemset(p):
  print("https://codeforces.com/problemset/problem/"+str(p["contestId"])+"/"+p["index"])

SOLVED=input().split()
UNSOLVED=input().split()
solved=get_solved_list(SOLVED)
unsolved=get_solved_list(UNSOLVED)
rating_limits=input().split()
rating_low=int(rating_limits[0])
rating_high=int(rating_limits[1])
res=[]
included=input().split(',')
excluded=input().split(',')
for p in solved:
  if not p in unsolved:
    rating=int(p["rating"])
    if (rating>=rating_low) and (rating<=rating_high):
      if have_common_element(p["tags"], included) and (not have_common_element(p["tags"], excluded)):
        res.append(p)
print(len(res))
random.shuffle(res)
size=int(input())
if size==0:
  size=len(res)
res=res[0:size];
for p in res:
  print_pretty(p)
extra=int(input())
if(extra==1):
  for p in res:
    print_clickable_contest(p);
elif(extra==2):
  for p in res:
    print_clickable_problemset(p);
    
