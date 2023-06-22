# Feature Collector
Feature collector allows you to collect data (features) using any monitoring approach and then store the obtained data 
in any storage. The overall principle is based on asynchronous data acquisition, when data is stored in a queue and 
this queue is asynchronously flushed to the selected storage. These two asynchronous functions can be timed arbitrarily 
using configuration parameters.

**Monitoring approaches:** SLMPClient, Mitsubishi monitor

**Data storage:** InfluxDB