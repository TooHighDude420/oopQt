# Blackjack dealer training program 
   This is my take on a Dealer traing program for Blackjack, made with Python using PyQt6

# Why i choose PyQt6
1. I have already used it once before for a private project
2. It feels more modern then Tkinter
3. It's styling feels close to css and it's possible to use reusable ui classes
4. Its a wrapper for a popular C++ lib and because of that it has 35 extensions i can used

# how i manged viassabilety of preperties
Python has a build in system that aplies name mangeling when i name a property __prop_name
when i try and acces that property from outside that class i get a ValueException because __prop_name becomes _ClassName__prop_name internally
<br> the example can be copied into example.py and run succesfully showing my explenation
<br>example:

```python

class TestClass():
   def __init__(self):
      self.__test_prop = "test"

class TestUse():
   def __init__(self):
      self.test_class = TestClass()

   def use(self):
    # this gives AttributeError
      print(self.test_class.__test_prop)
    # this wont but is bad practise here only to give example
      print(self.test_class._TestClass__test_prop)

test = TestUse()
test.use()

```

# Official description from their site:
    Qt is set of cross-platform C++ libraries that implement high-level APIs for accessing many aspects of modern desktop and mobile systems. These include location and positioning services, multimedia, NFC and Bluetooth connectivity, a Chromium based web browser, as well as traditional UI development.

    PyQt6 is a comprehensive set of Python bindings for Qt v6. It is implemented as more than 35 extension modules and enables Python to be used as an alternative application development language to C++ on all supported platforms including iOS and Android.