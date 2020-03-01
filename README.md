## 配置環境

* **作業系統** : Ubuntu 18.0.4
* **Python** : 3.7.3
* **Mongodb**: 3.6
* **Scrapy** 1.8.0


## 安裝方法

1. 安裝Docker
   ```
   sudo apt-get install docker.io
   ```

2. 安裝Mongodb
   ```
   sudo apt-get install mongodb
   ```
3. 下載Docker Image
   ```
   sudo docker pull philip616/ptt
   ```
## 執行爬蟲

* 默認配置執行

  默認爬取的板塊為`Beauty`，默認日期為當日
   ```
   sudo docker run --network='host' philip616/ptt
   ```
 

