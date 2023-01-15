HotFix at 24 December 2022:

1. Add parameter "product_Code" in NBO and NBO Response Log.

```python
product_code = from_str(obj.get("productCode"))
```

2. Create class for gathering and output statistic to Console.

```python
classConsoleStats:
	def__init__(self)->None:
		self.consumerCounter =0
		self.clientLogCounter =0
		self.nboLogCounter =0
		self.nboResponseLogCounter =0
		self.noneLogCounter=0
		self.errorCounter =0
		self.othersCounter =0
		self.usersCounter =0
```

3. Implement Stats class into Kafka Connector.

```python
globals.stats.setUsersCounter(len(users))
if log isnot None:
	globals.stats.raiseConsumerCounter
```

4. Create third thread for showing statistics in console by given time delay.

```python
th3 = threading.Thread(target=console)  
th3.daemon =True  
th3.start()
```

5. Create additional parameter in config file to manage delay for output statistics into console.

```ini
# частота обновления данных в консоли
frequency=60
```
