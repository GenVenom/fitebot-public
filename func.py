import psycopg2
import random
import discord
from discord.ext import commands , tasks
import os

DB_NAME= os.environ["DB_NAME"]
DB_USER=os.environ["DB_USER"]
DB_PASS= os.environ["DB_PASS"]
DB_HOST= os.environ["DB_HOST"]
DB_PORT= "5432"

activeChannels=[]

def itemNameSorter(items):
    items= items.lower()
    items= list(items)
    counter = len(items)
    for i in range (0,counter):
        if items[i]== " ":
            items[i]= "_"

    items = "".join(items)
    print (items)
    return items


def get_bal(passedid):
    conn=psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
    c=conn.cursor()
    c.execute(f"SELECT bal FROM userdata WHERE userid='{passedid}'")
    bal=c.fetchone()

    if bal is None:
        Balance = 0
    if bal is not None:
        balint = int (bal[0])
        Balance = balint
    return Balance


def balanceAdjuster(passedid,balance):
    conn=psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
    c=conn.cursor()
    c.execute (f"UPDATE userdata SET bal={balance} WHERE userid='{passedid}'")
    conn.commit()
    c.close()
    conn.close()


def entry_check_and_create(userid):
    
    conn=psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
    c=conn.cursor()
    c.execute(f"SELECT wprimary FROM userdata WHERE userid='{userid}'")
    result = c.fetchone()
    if result is None:
        c.execute(f"INSERT INTO userdata (userid,maxHP,bal,wins,losses,wprimary,wsecondary,potions) VALUES('{userid}',100,0,0,0,'wooden_sword','wooden_dagger','0')",)
        conn.commit()
    if result is not None:
        pass
    
    c.close()
    conn.close()

def enemyHit(enemy,challenger,damage,ChallengerHP,EnemyHP,Weapon,state):
    embed = discord.Embed(
        colour= discord.Colour.red(),
        title= f"{state.title()}!",
        description= f"{enemy.name} __{state.lower()}__ his shot on  {challenger.name} with his **{Weapon}** and dealt  **{damage}** damage!"
    )
    embed.add_field(name=f"{challenger.name}'s HP",value=ChallengerHP)
    embed.add_field(name=f"{enemy.name}'s HP",value=EnemyHP)
    return embed
      
def challengerHit(enemy,challenger,damage,ChallengerHP,EnemyHP,Weapon,state):
    embed = discord.Embed(
        colour= discord.Colour.red(),
        title= f"{state.title()}!",
        description= f"{challenger.name} __{state.lower()}__ his shot on {enemy.name} with his **{Weapon}** and dealt **{damage}** damage!"
    )
    embed.add_field(name=f"{challenger.name}'s HP",value=ChallengerHP)
    embed.add_field(name=f"{enemy.name}'s HP",value=EnemyHP)
    return embed         


def checkChannel(channel):
    if channel in activeChannels:
        rValue = "True"
    else:
        rValue = "False"
    
    return rValue


def get_primary(passedID):
    
    weaponDamages={
    'wooden_sword': random.randint(8,10),
    'ligt_sword': random.randint(9,12),
    'claymore': random.randint(13,16),
    'dual_sword': random.randint(14,17),
    'heavy_sword': random.randint(15,19),
    'bow': random.randint(18,23),
    'spear': random.randint(23,30)
    
    }
    weaponHitState= ['Hit','Missed']
    chance={
    'wooden_sword': 100,
    'ligt_sword': 95,
    'claymore':90,
    'dual_sword': 85,
    'heavy_sword': 73,
    'bow': 60,
    'spear': 50
    
    }
    conn=psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
    c=conn.cursor()
    c.execute(f"SELECT wprimary FROM userdata WHERE userid='{passedID}'")
    conn.commit
    result = c.fetchone()
    
    if result is None:
        didItHit= 'Hit'
        primaryWeapon = 'wooden_sword'
        damage= weaponDamages[primaryWeapon]
        

    if result is not None:
        c.execute (f"SELECT wprimary FROM userdata WHERE userid='{passedID}'")
        conn.commit()
        primaryWeapon= c.fetchone()
        
        chance=[chance[primaryWeapon[0]],100-chance[primaryWeapon[0]]]
        
        didItHit= random.choices(weaponHitState,chance)
        
        if didItHit[0] == "Hit":
            damage= weaponDamages[primaryWeapon[0]]
        else:
            damage= 0
        primaryWeapon= primaryWeapon[0]
   
    return damage,primaryWeapon,didItHit[0]

def get_secondary(passedID):
    weaponDamages={
        "wooden_dagger":random.randint(2,4),
        "dagger":random.randint(5,7),
        "khukuri" :random.randint(6,9),
        "throwing_knives":random.randint(9,14),
        "poison_dart":random.randint(12,16)
        }
    conn=psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
    c=conn.cursor()
    c.execute(f"SELECT wsecondary FROM userdata WHERE userid='{passedID}'")
    conn.commit
    result = c.fetchone()
    
    if result is None:
        secondaryWeapon = 'wooden_dagger'
        
        damage= weaponDamages[secondaryWeapon]
        
    if result is not None:
        c.execute (f"SELECT wsecondary FROM userdata WHERE userid='{passedID}'")
        conn.commit()
        secondaryWeapon= c.fetchone()

        damage= weaponDamages[secondaryWeapon[0]]
        secondaryWeapon=secondaryWeapon[0]
        state = "Hit"
    
    return damage,secondaryWeapon,state


def winnerStatUpdater (passedID):
    currentBalance  = get_bal(passedID)
    currentWins= get_wins(passedID)
    currentMaxHP = get_maxhp(passedID)
    conn=psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
    c=conn.cursor()
    c.execute (f"UPDATE userdata SET bal= {currentBalance + 50} WHERE userid='{passedID}'")
    c.execute(f"UPDATE userdata SET wins={currentWins+1} WHERE userid='{passedID}'")
    c.execute (f"UPDATE userdata SET maxhp={currentMaxHP + 2} WHERE userid = '{passedID}'")
    conn.commit()
    c.close()
    conn.close()

def lossStatUpdater (passedID):
    currentLosses= get_wins(passedID)
    currentMaxHP = get_maxhp(passedID)
    conn=psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
    c=conn.cursor()
    c.execute(f"UPDATE userdata SET losses={currentLosses+1} WHERE userid='{passedID}'")
    c.execute (f"UPDATE userdata SET maxhp={currentMaxHP-1} WHERE userid='{passedID}'")
    conn.commit()
    c.close()
    conn.close()

def get_wins(passedID):
    conn=psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
    c=conn.cursor()
    c.execute (f"SELECT wins FROM userdata WHERE userid='{passedID}'")
    conn.commit()
    result = c.fetchone()
    if result is None:
        wins = 0
    if result is not None:
        wins = int (result[0])
    c.close()
    conn.close()
    return wins

def get_loss (passedID):
    conn=psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
    c=conn.cursor()
    c.execute (f"SELECT losses FROM userdata WHERE userid='{passedID}'")
    conn.commit()
    result = c.fetchone()
    if result is None:
        losses = 0
    if result is not None:
        losses = int (result[0])
    c.close()
    conn.close()
    return losses

def get_maxhp(passedID):
    conn=psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
    c=conn.cursor()
    c.execute (f"SELECT maxhp FROM userdata WHERE userid='{passedID}'")
    conn.commit()
    maxhp=c.fetchone()
    maxhp= int(maxhp[0])
    return maxhp

def getLoadout(passedID):
    conn=psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
    c=conn.cursor()
    c.execute (f"SELECT wprimary FROM userdata WHERE userid='{passedID}'")
    result = c.fetchone()
    primary= result[0]

    c.execute (f"SELECT wsecondary FROM userdata WHERE userid='{passedID}'")
    result = c.fetchone()
    secondary= result[0]
    conn.commit()
    c.close()
    return primary,secondary

def itemNameFixer(items):
    items= list(items)
    counter = len(items)
    for i in  range (0,counter):
        if items[i]== "_":
            items[i]=" "
    items= "".join(items)
    items= items.title()
    return items
