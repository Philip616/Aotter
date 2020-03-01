# 配置環境

* **作業系統** : Ubuntu 18.0.4
* **Python** : 3.7.3
* **Mongodb**: 3.6
* **Scrapy** 1.8.0


# 安裝方法

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
# 執行爬蟲
## 執行方法一
   
   直接在外部執行container指令

* 默認配置執行

  默認爬取的板塊為`Beauty`，默認日期為當日
   ```
   sudo docker run --network='host' philip616/ptt
   ```
* 可修改的參數
   
   日期格式為 "mm/dd"，目前只能針對當年度的月份去調整爬蟲區間。
   ```
   sudo docker run --network='host' -e ip='localhost' -e board='Guitar' -e start_date='03/01' -e end_date='03/01' philip616/ptt
   ```
   
## 執行方法二

    容器內部執行
    
    1. 先進入容器內的bash
       ```
       sudo docker run -it philip616/ptt bash
       ```
    2. 安裝Mongodb
       ```
       sudo apt-get install mongodb
       ```
    3. 執行默認爬蟲指令
       ```
       scrapy crawl ptt
       ```
    *  修改執行參數
       ```
       scrapy crawl -a ip='localhost' -a board='Guitar' -a start_date='03/01' -a end_date='03/01' ptt
       ```
 
 
# 規格需求
- [x] 每筆 row data 必須確保是 unique 

  運用Mongodb內的replace_one方法避免重複輸入。
- [ ] 須考慮機器如因不可預期狀況停機，後續如何追朔未擷取之資料

  若在容器內執行，可以運用Scrapy的job執行方法，在中斷的時候恢復執行。
- [ ] 須考慮爬蟲會被部署在多台機器架構下的狀況
- [ ] 須考量如何監控爬蟲狀態及相關異常通知

  部分輸入異常會提示、找不到指定區間會提示。
- [x] 須考量如何才能概括⼤部份的分類看板
- [x] 須考量如何避免因過度快速擷取⾴⾯⽽造成的網路資安問題

  每次下載間隔1秒，每次請求間隔2秒


