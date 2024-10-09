package com.example.test1

data class SensorData(
    val temperature: Float,
    val humidity: Float,
    val distance: Float,
    val ledStates: List<Int>,
    val auto_flag: Int
)