# lambda-waterLevelAPI

## Overview
現在の降水量を返します。  
データは10分毎に更新されます。  
データは20分前の観測データになります。  

## Request
Method : GET  
Endpoint : /production/rain-fall  
Parameter : ComingSoon  

## Response

以下の Json を返します。
~~~
{
  "timestamp": "2017-08-12-12-50"
  "observation": "石川県金沢市"
  "rainFall": "0.0"
}
~~~

timestamp : 観測時点の日時  
observation : 観測地点  
rainFall : 観測時点の降雨量  
