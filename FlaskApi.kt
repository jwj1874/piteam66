package com.example.test1

import retrofit2.Call
import retrofit2.http.GET

interface FlaskApi {
    @GET("/get-sensor-data")
    fun getSensorData(): Call<SensorData>  // 센서 데이터를 가져옴

    @GET("/0/1")  // LED 켜기 요청
    fun turnOnLED_0(): Call<Void>

    @GET("/0/0")  // LED 끄기 요청
    fun turnOffLED_0(): Call<Void>

    @GET("/1/1")
    fun turnOnLED_1(): Call<Void>

    @GET("/1/0")
    fun turnOffLED_1(): Call<Void>

    @GET("/2/1")
    fun turnOnLED_2(): Call<Void>

    @GET("/2/0")
    fun turnOffLED_2(): Call<Void>
}