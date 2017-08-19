# lambda-rainFallAPI

## Overview
現在の降水量を返します。  
データは10分毎に更新されます。  
データは30分前の観測データになります。  

## Request
Method : GET  
Endpoint : /production/rain-fall/japan/tokyo/arakawa  
Path Parameter :   
1. japan : 国名を指定 ex)japan, taiwan
2. tokyo : 都道府県を指定 ex)tokyo, taipei
3. arakawa : 河川名を指定 ex)arakawa, danshui

## Response

以下の Json を返します。
~~~
{
  "timestamp": "2017-08-12T12:50:00Z",
  "observation": "石川県金沢市",
  "rainFall": "0.0"
}
~~~

timestamp : 観測時点の日時(UTC)  
observation : 観測地点  
rainFall : 観測時点の降雨量[mm]  
