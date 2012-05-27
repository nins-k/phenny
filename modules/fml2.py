import urllib
import re
import cPickle
import os.path

def dict_sub(d, text): 
  """ Replace in 'text' non-overlapping occurences of REs whose patterns are keys
  in dictionary 'd' by corresponding values (which must be constant strings: may
  have named backreferences but not numeric ones). The keys must not contain
  anonymous matching-groups.
  Returns the new string.""" 

  # Create a regular expression  from the dictionary keys
  regex = re.compile("|".join("(%s)" % k for k in d))
  # Facilitate lookup from group number to value
  lookup = dict((i+1, v) for i, v in enumerate(d.itervalues()))

  # For each match, find which group matched and expand its value
  return regex.sub(lambda mo: mo.expand(lookup[mo.lastindex]), text)

def loadfml():
  datastring = urllib.urlopen("http://m.fmylife.com/random").read()
  # print datastring
  fmls = re.findall(r'<p class="text">[^<]+</p>',datastring)
  print fmls.__len__()
  nfml=[]
  cdict = {"FUCK":"F**K","Fuck":"F**k","fuck":"f**k",\
         "SLUT":"S**T","Slut":"S**t","slut":"s**t",\
         "CUNT":"C**T","Cunt":"C**t","cunt":"c**t",\
         "BITCH":"B**CH","Bitch":"B**ch","bitch":"b**ch",\
         "WHORE":"W**RE","Whore":"W**re","whore":"w**re",\
         "SHIT":"SH*T","Shit":"Sh*t","shit":"sh*t",\
         "DICK":"D**K","Dick":"D**k","dick":"di*k",\
         "MASTURBAT":"MA****BAT","Masturbat":"Ma****bat","masturbat":"ma****bat",\
         "&quot":"\""}
  for nyan in fmls:   
    nfml.append(dict_sub(cdict,nyan[16:-4]))
  return nfml    

def save(fmlo):
    f = open('fml.shana','w')
    cPickle.dump(fmlo,f)
    f.close()

def load():
    try:
        f = open('fml.shana','r')
        ret = cPickle.load(f)
        f.close()
    except IOError:
        ret = loadfml()
    return ret

def fml(phenny,input):
    fmllist = load()  
    phenny.say(fmllist.pop())
    phenny.say.("Taken from http://fmylife.com")
    #phenny.say(str(fmllist.__len__()))
    if fmllist.__len__()==0:
        #phenny.say(str(fmllist.__len__()))
        fmllist = loadfml()
    save(fmllist)
    
fml.commands=["fml"]
fml.priority="medium"

