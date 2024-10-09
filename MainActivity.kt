package com.example.test1

import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

public var auto: Int = 0
public var led1_states: Int = 0
public var led2_states: Int = 0
public var led3_states: Int = 0


class MainActivity : AppCompatActivity() {
    private lateinit var temperatureTextView: TextView
    private lateinit var humidityTextView: TextView
    private lateinit var distanceTextView: TextView
    private lateinit var modeTextView: TextView
    private lateinit var heaterStatusTextView: TextView
    private lateinit var acStatusTextView: TextView
    private lateinit var dehumidifierStatusTextView: TextView
    private lateinit var turnOnButton_0: Button
    private lateinit var turnOffButton_0: Button
    private lateinit var turnOnButton_1: Button
    private lateinit var turnOffButton_1: Button
    private lateinit var turnOnButton_2: Button
    private lateinit var turnOffButton_2: Button
    private lateinit var handler: Handler
    private val delay: Long = 1000




    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        //handler init
        handler = Handler(Looper.getMainLooper())



        // UI 요소 초기화
        temperatureTextView = findViewById(R.id.temperatureTextView)
        humidityTextView = findViewById(R.id.humidityTextView)
        distanceTextView = findViewById(R.id.distanceTextView)
        modeTextView = findViewById(R.id.modeTextView)
        heaterStatusTextView = findViewById(R.id.heaterStatusTextView)
        acStatusTextView = findViewById(R.id.acStatusTextView)
        dehumidifierStatusTextView = findViewById(R.id.dehumidifierStatusTextView)
        turnOnButton_0 = findViewById(R.id.turnOnButton_0)
        turnOffButton_0 = findViewById(R.id.turnOffButton_0)
        turnOnButton_1 = findViewById(R.id.turnOnButton_1)
        turnOffButton_1 = findViewById(R.id.turnOffButton_1)
        turnOnButton_2 = findViewById(R.id.turnOnButton_2)
        turnOffButton_2 = findViewById(R.id.turnOffButton_2)

        startRepeatingTask()

    }

    private val updateTask = object : Runnable {
        override fun run() {
            // 서버에 데이터를 요청하여 UI를 업데이트
            fetchDataFromServer()
            handler.postDelayed(this, delay) // 다시 1초 뒤에 실행
        }
    }

    private fun startRepeatingTask() {
        updateTask.run() // 바로 실행
    }

    private fun stopRepeatingTask() {
        handler.removeCallbacks(updateTask) // 반복 중지
    }

    private fun fetchDataFromServer() {
        val api = RetrofitClient.instance.create(FlaskApi::class.java)
        api.getSensorData().enqueue(object : Callback<SensorData> {
            override fun onResponse(call: Call<SensorData>, response: Response<SensorData>) {
                if (response.isSuccessful) {
                    val data = response.body()

                    if (data != null) {
                        temperatureTextView.text = "Temperature: ${data.temperature} C"
                        humidityTextView.text = "Humidity: ${data.humidity} %"
                        distanceTextView.text = "Distance: ${data.distance} cm"
                        auto = data.auto_flag
                        led1_states = data.ledStates[0]
                        led2_states = data.ledStates[1]
                        led3_states = data.ledStates[2]

                        if(led1_states == 1){
                            heaterStatusTextView.text = "heater: On"
                        }
                        else{
                            heaterStatusTextView.text = "heater: Off"
                        }
                        if(led2_states == 1){
                            acStatusTextView.text = "AC: On"
                        }
                        else{
                            acStatusTextView.text = "AC: Off"
                        }
                        if(led3_states == 1){
                            dehumidifierStatusTextView.text = "Dehumidifier: On"
                        }
                        else{
                            dehumidifierStatusTextView.text = "Dehumidifier: Off"
                        }

                        if(data.auto_flag == 1){
                            modeTextView.text = "Mode : AUTO"

                            turnOnButton_0.isEnabled = false  // turnOnButton_0 버튼을 비활성화
                            turnOnButton_0.alpha = 0.5f
                            turnOffButton_0.isEnabled = false  // turnOffButton_0 버튼을 비활성화
                            turnOffButton_0.alpha = 0.5f

                            turnOnButton_1.isEnabled = false  // turnOnButton_1 버튼을 비활성화
                            turnOnButton_1.alpha = 0.5f
                            turnOffButton_1.isEnabled = false  // turnOffButton_1 버튼을 비활성화
                            turnOffButton_1.alpha = 0.5f

                            turnOnButton_2.isEnabled = false  // turnOnButton_2 버튼을 비활성화
                            turnOnButton_2.alpha = 0.5f
                            turnOffButton_2.isEnabled = false  // turnOffButton_2 버튼을 비활성화
                            turnOffButton_2.alpha = 0.5f
                        }

                        else{
                            modeTextView.text = "Mode : MANUAL"

                            turnOnButton_0.isEnabled = true  // turnOnButton_0 버튼을 활성화
                            turnOnButton_0.alpha = 1.0f
                            turnOffButton_0.isEnabled = true  // turnOffButton_0 버튼을 활성화
                            turnOffButton_0.alpha = 1.0f

                            turnOnButton_1.isEnabled = true  // turnOnButton_1 버튼을 활성화
                            turnOnButton_1.alpha = 1.0f
                            turnOffButton_1.isEnabled = true  // turnOffButton_1 버튼을 활성화
                            turnOffButton_1.alpha = 1.0f

                            turnOnButton_2.isEnabled = true  // turnOnButton_2 버튼을 활성화
                            turnOnButton_2.alpha = 1.0f
                            turnOffButton_2.isEnabled = true  // turnOffButton_2 버튼을 활성화
                            turnOffButton_2.alpha = 1.0f
                        }
                    }
                } else {
                    //showToast("Failed to fetch sensor data")
                }
            }

            override fun onFailure(call: Call<SensorData>, t: Throwable) {
                //  showToast("Error: ${t.message}")
            }
        })
////////////////////////////////////////////////////////////////////////
        //LED1
///////////////////////////////////////////////////////////////////////
        turnOnButton_0.setOnClickListener {
                api.turnOnLED_0().enqueue(object : Callback<Void> {
                    override fun onResponse(call: Call<Void>, response: Response<Void>) {
                        if (response.isSuccessful) {
                            heaterStatusTextView.text = "heater: On"
                        } else {
                            // showToast("LED 켜기 실패")
                        }
                    }

                    override fun onFailure(call: Call<Void>, t: Throwable) {
                        // showToast("에러: ${t.message}")
                    }
                })
        }

        // LED 끄기 버튼
        turnOffButton_0.setOnClickListener {
            api.turnOffLED_0().enqueue(object : Callback<Void> {
                override fun onResponse(call: Call<Void>, response: Response<Void>) {
                    if (response.isSuccessful) {
                        heaterStatusTextView.text = "heater: Off"
                    } else {
                        // showToast("LED 끄기 실패")
                    }
                }
                override fun onFailure(call: Call<Void>, t: Throwable) {
                    // showToast("에러: ${t.message}")
                }
            })
        }

        turnOnButton_1.setOnClickListener {
            api.turnOnLED_1().enqueue(object : Callback<Void> {
                override fun onResponse(call: Call<Void>, response: Response<Void>) {
                    if (response.isSuccessful) {
                        acStatusTextView.text = "AC: On"
                    } else {
                        // showToast("LED 켜기 실패")
                    }
                }

                override fun onFailure(call: Call<Void>, t: Throwable) {
                    // showToast("에러: ${t.message}")
                }
            })
        }

        // LED 끄기 버튼
        turnOffButton_1.setOnClickListener {
            api.turnOffLED_1().enqueue(object : Callback<Void> {
                override fun onResponse(call: Call<Void>, response: Response<Void>) {
                    if (response.isSuccessful) {
                        acStatusTextView.text = "AC: Off"
                    } else {
                        // showToast("LED 끄기 실패")
                    }
                }
                override fun onFailure(call: Call<Void>, t: Throwable) {
                    // showToast("에러: ${t.message}")
                }
            })
        }

        turnOnButton_2.setOnClickListener {
            api.turnOnLED_2().enqueue(object : Callback<Void> {
                override fun onResponse(call: Call<Void>, response: Response<Void>) {
                    if (response.isSuccessful) {
                        dehumidifierStatusTextView.text = "Dehumidifier: On"
                    } else {
                        // showToast("LED 켜기 실패")
                    }
                }

                override fun onFailure(call: Call<Void>, t: Throwable) {
                    // showToast("에러: ${t.message}")
                }
            })
        }

        // LED 끄기 버튼
        turnOffButton_2.setOnClickListener {
            api.turnOffLED_2().enqueue(object : Callback<Void> {
                override fun onResponse(call: Call<Void>, response: Response<Void>) {
                    if (response.isSuccessful) {
                        dehumidifierStatusTextView.text = "Dehumidifier: Off"
                    } else {
                        // showToast("LED 끄기 실패")
                    }
                }
                override fun onFailure(call: Call<Void>, t: Throwable) {
                    // showToast("에러: ${t.message}")
                }
            })
        }
    }
    override fun onDestroy() {
        super.onDestroy()
        stopRepeatingTask() // 액티비티 종료 시 반복 중지
    }
}
