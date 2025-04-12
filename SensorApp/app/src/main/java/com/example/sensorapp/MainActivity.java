//package com.example.sensorapp;
//
//import android.content.Context;
//import android.hardware.Sensor;
//import android.hardware.SensorEvent;
//import android.hardware.SensorEventListener;
//import android.hardware.SensorManager;
//import android.os.Bundle;
//import android.widget.TextView;
//import androidx.appcompat.app.AppCompatActivity;
//
//import java.io.OutputStream;
//import java.io.PrintWriter;
//import java.net.Socket;
//import java.util.Arrays;
//import java.util.LinkedList;
//
//public class MainActivity extends AppCompatActivity implements SensorEventListener {
//
//    private SensorManager sensorManager;
//    private Sensor accelerometer;
//    private Sensor gyroscope;
//
//    private TextView accTextView;
//    private TextView gyroTextView;
//
//    private LinkedList<float[]> accelBuffer = new LinkedList<>();
//    private LinkedList<float[]> gyroBuffer = new LinkedList<>();
//    private static final int MAX_BUFFER_SIZE = 70;
//    private static final long UPDATE_INTERVAL_MS = 200;
//
//    private long lastUpdateTime = 0;
//
//    @Override
//    protected void onCreate(Bundle savedInstanceState) {
//        super.onCreate(savedInstanceState);
//        setContentView(R.layout.activity_main);
//
//        accTextView = findViewById(R.id.accTextView);
//        gyroTextView = findViewById(R.id.gyroTextView);
//
//        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
//
//        if (sensorManager != null) {
//            accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
//            gyroscope = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
//        }
//    }
//
//    @Override
//    protected void onResume() {
//        super.onResume();
//        if (accelerometer != null)
//            sensorManager.registerListener(this, accelerometer, SensorManager.SENSOR_DELAY_GAME);
//        if (gyroscope != null)
//            sensorManager.registerListener(this, gyroscope, SensorManager.SENSOR_DELAY_GAME);
//    }
//
//    @Override
//    protected void onPause() {
//        super.onPause();
//        sensorManager.unregisterListener(this);
//    }
//
//    @Override
//    public void onSensorChanged(SensorEvent event) {
//        long currentTime = System.currentTimeMillis();
//        if ((currentTime - lastUpdateTime) < UPDATE_INTERVAL_MS) {
//            return;
//        }
//        lastUpdateTime = currentTime;
//
//        if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {
//            float[] values = event.values.clone();
//            accelBuffer.add(values);
//            if (accelBuffer.size() > MAX_BUFFER_SIZE) accelBuffer.removeFirst();
//
//            accTextView.setText(String.format("Accelerometer:\nX: %.2f\nY: %.2f\nZ: %.2f", values[0], values[1], values[2]));
//
//            if (isSpike(accelBuffer, values)) {
//                sendBufferedData();
//            }
//        } else if (event.sensor.getType() == Sensor.TYPE_GYROSCOPE) {
//            float[] values = event.values.clone();
//            gyroBuffer.add(values);
//            if (gyroBuffer.size() > MAX_BUFFER_SIZE) gyroBuffer.removeFirst();
//
//            gyroTextView.setText(String.format("Gyroscope:\nX: %.2f\nY: %.2f\nZ: %.2f", values[0], values[1], values[2]));
//        }
//    }
//
//    private boolean isSpike(LinkedList<float[]> buffer, float[] current) {
//        if (buffer.size() < 10) return false;
//
//        double sum = 0;
//        for (float[] v : buffer) {
//            sum += magnitude(v);
//        }
//        double avg = sum / buffer.size();
//        double currentMag = magnitude(current);
//
//        return Math.abs(currentMag - avg) > 9; // Adjust threshold as needed
//    }
//
//    private double magnitude(float[] v) {
//        return Math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
//    }
//
//    private void sendBufferedData() {
//        StringBuilder sb = new StringBuilder();
//        int size = Math.min(accelBuffer.size(), gyroBuffer.size());
//
//        for (int i = 0; i < size; i++) {
//            float[] acc = accelBuffer.get(i);
//            float[] gyro = gyroBuffer.get(i);
//            sb.append("acc: ").append(Arrays.toString(acc))
//                    .append(" | gyro: ").append(Arrays.toString(gyro))
//                    .append("\n");
//        }
//
//        sendToServer("padnav vo dupka, dvete gummi gi rusiv");
//    }
//
//    private void sendToServer(final String message) {
//        new Thread(() -> {
//            try {
//                Socket socket = new Socket("192.168.53.233", 9999); // Change IP as needed
//                OutputStream output = socket.getOutputStream();
//                PrintWriter writer = new PrintWriter(output, true);
//                writer.println(message);
//                socket.close();
//            } catch (Exception e) {
//                e.printStackTrace();
//            }
//        }).start();
//    }
//
//    @Override
//    public void onAccuracyChanged(Sensor sensor, int accuracy) {
//        // Not used
//    }
//}
//
//
//
//


package com.example.sensorapp;

import android.content.Context;
import android.content.res.AssetFileDescriptor;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Arrays;
import java.util.LinkedList;

public class MainActivity extends AppCompatActivity implements SensorEventListener {

    private SensorManager sensorManager;
    private Sensor accelerometer;
    private Sensor gyroscope;

    private TextView accTextView;
    private TextView gyroTextView;
    private Button alertButton;

    private LinkedList<float[]> accelBuffer = new LinkedList<>();
    private LinkedList<float[]> gyroBuffer = new LinkedList<>();
    private static final int MAX_BUFFER_SIZE = 70;
    private static final long UPDATE_INTERVAL_MS = 200;

    private long lastUpdateTime = 0;
    private boolean waitingForResponse = false;
    private Handler handler = new Handler();
    private MediaPlayer mediaPlayer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        accTextView = findViewById(R.id.accTextView);
        gyroTextView = findViewById(R.id.gyroTextView);
        alertButton = findViewById(R.id.alertButton);
        alertButton.setVisibility(View.GONE);

        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);

        if (sensorManager != null) {
            accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
            gyroscope = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
        }

        alertButton.setOnClickListener(v -> {
            stopSound();
            alertButton.setVisibility(View.GONE);
            waitingForResponse = false;
        });
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (accelerometer != null)
            sensorManager.registerListener(this, accelerometer, SensorManager.SENSOR_DELAY_GAME);
        if (gyroscope != null)
            sensorManager.registerListener(this, gyroscope, SensorManager.SENSOR_DELAY_GAME);
    }

    @Override
    protected void onPause() {
        super.onPause();
        sensorManager.unregisterListener(this);
        stopSound();
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        long currentTime = System.currentTimeMillis();
        if ((currentTime - lastUpdateTime) < UPDATE_INTERVAL_MS) {
            return;
        }
        lastUpdateTime = currentTime;

        if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {
            float[] values = event.values.clone();
            accelBuffer.add(values);
            if (accelBuffer.size() > MAX_BUFFER_SIZE) accelBuffer.removeFirst();

            accTextView.setText(String.format("Accelerometer:\nX: %.2f\nY: %.2f\nZ: %.2f", values[0], values[1], values[2]));

            if (isSpike(accelBuffer, values) && !waitingForResponse) {
                triggerAlert();
            }
        } else if (event.sensor.getType() == Sensor.TYPE_GYROSCOPE) {
            float[] values = event.values.clone();
            gyroBuffer.add(values);
            if (gyroBuffer.size() > MAX_BUFFER_SIZE) gyroBuffer.removeFirst();

            gyroTextView.setText(String.format("Gyroscope:\nX: %.2f\nY: %.2f\nZ: %.2f", values[0], values[1], values[2]));
        }
    }

    private boolean isSpike(LinkedList<float[]> buffer, float[] current) {
        if (buffer.size() < 10) return false;

        double sum = 0;
        for (float[] v : buffer) {
            sum += magnitude(v);
        }
        double avg = sum / buffer.size();
        double currentMag = magnitude(current);

        return Math.abs(currentMag - avg) > 9;
    }

    private double magnitude(float[] v) {
        return Math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
    }

    private void triggerAlert() {
        waitingForResponse = true;
        alertButton.setVisibility(View.VISIBLE);
        playSound();

        handler.postDelayed(() -> {
            if (waitingForResponse) {
                sendToServer("Alert!");
                alertButton.setVisibility(View.GONE);
                stopSound();
                waitingForResponse = false;
            }
        }, 10000); // 5 seconds
    }

    private void playSound() {
        try {
            AssetFileDescriptor afd = getAssets().openFd("audio-sound.mp3");
            mediaPlayer = new MediaPlayer();
            mediaPlayer.setDataSource(afd.getFileDescriptor(), afd.getStartOffset(), afd.getLength());
            mediaPlayer.setLooping(true);
            mediaPlayer.prepare();
            mediaPlayer.start();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void stopSound() {
        if (mediaPlayer != null && mediaPlayer.isPlaying()) {
            mediaPlayer.stop();
            mediaPlayer.release();
            mediaPlayer = null;
        }
    }

    private void sendToServer(final String message) {
        new Thread(() -> {
            try {
                Socket socket = new Socket("192.168.53.233", 9999); // Change as needed
                OutputStream output = socket.getOutputStream();
                PrintWriter writer = new PrintWriter(output, true);
                writer.println(message);
                socket.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }).start();
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
        // Not used
    }
}
