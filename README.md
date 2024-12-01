# PyProducer
Python CLI for generating and producing kafka events


# How to use

Call the pyproducer.py with the python interpreter. (`-h` for a list of available arguments ;) )

## To define the events

Create a python package (default is `models.py` but target can be changed) with your classes that represent the Events and extend EventBase.
In this class, create a class, decorate it with the `@event` decorator and add a `payload` field to it with a value object of that extends the Datatype class.
```
class Example(ObjectDatatype):
    def __init__(self):
        self.field = NumericDatatype()
        self.field2 = UUIDDatatype()
        self.field3 = ConstDatatype("HELLO!")
        self.field4 = ConstDatatype(3)
        self.field5 = StringDatatype()
        self.field7 = CustomDatatype(lambda: 0)
        self.field9 = ObjectDatatype()
        self.field10 = NullDatatype()
        self.field11 = DatetimeDatatype()

@event
class ExampleEvent:
    payload = Example()
```

The topic destination can be set on the event by adding a second field to the class called topic or by passing the ´-t´ flag on the CLI.

## Available Datatypes

### NumericDatatype

Generates a random number.
Args:
- min (default 0)
- max (default 1000000000)
- step (default 1)

### StringDatatype

Generates a random string.
Args:
- regex (default [A-Za-z]{5}[0-9]{3})

### UUIDDatatype

Generates a random UUID

Note: 
Only version 1 and 4 are supported. Other versions should be implemented with CustomDatatype.
When python adds native support for v7, it will be added.

### DatetimeDatatype

Generates a random Datetime inside a range
Args:
- start (default 1970/1/1 00:00:00)
- end (default 2114/12/31 00:00:00)
- format (default %Y-%m-%d %H:%M:%S)

### ObjectDatatype

Builder for custom objects.
Individual fields defined as object atributes.

### ConstDatatype

Always returns the same value
Args:
- value

### NullDatatype

Always returns null

### CustomDatatype

Accepts a callable as argument to always run on payload generation

## Creating your own 

You can access and extend the Datatype class.
All you need to do is implement a method called apply that takes no arguments except self.

## Sequencing Events
To sequence events, add a field called `dependencies` to the dependent class. This field is an array of strings with the name of the classes representing the dependency event.
Afterwards, in the dependent object, you can use one of the sequencing datatypes to reference the previous event. 

Example:

```
class Example(ObjectDatatype):
    def __init__(self):
        self.field = NumericDatatype()
        self.field2 = UUIDDatatype()
        self.field3 = ConstDatatype("HELLO!")

class Example2(ObjectDatatype):
    def __init__(self):
        self.field = NumericDatatype()
        self.field2 = PrevDatatype("field2")
        self.field3 = ConstDatatype("HELLO2!")

@event
class ExampleEvent:
    payload = Example()
    topic = "some_topic100"

@event
class ExampleEvent2:
    payload = Example2()
    topic = "some_topic100"
    dependencies = ['ExampleEvent']
```
Currently, only the `PrevDatatype` is supported which simple reuses the field value of a previous event of the depedency. But more will be added soon!

#### Note
Whenvever a dependency event is used by a dependent, it is removed from the previous events list, so it will only be used once.
