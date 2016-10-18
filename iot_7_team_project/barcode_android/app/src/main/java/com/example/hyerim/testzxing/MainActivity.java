package com.example.hyerim.testzxing;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

//메인 액티비티
public class MainActivity extends AppCompatActivity implements View.OnClickListener {
    public String testStr = "data_is_null";

    private Button scanBtn, socketBtn; //바코드 스캔, 데이터 소켓 전송
    private TextView formatTxt, contentTxt,resultTxt;

    //소켓통신 관련 변수
    private Socket socket;
    BufferedReader socket_in;
    PrintWriter socket_out;
    String data;

    int count = 1;//데이터 송신 수, 번호

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //버튼, 텍스트뷰 선언
        scanBtn = (Button)findViewById(R.id.scan_button);
        formatTxt = (TextView)findViewById(R.id.scan_format);
        contentTxt = (TextView)findViewById(R.id.scan_content);
        resultTxt = (TextView)findViewById(R.id.tv_response);
        socketBtn = (Button)findViewById(R.id.socket_button);

        //클릭리스너 등록
        scanBtn.setOnClickListener(this);
        socketBtn.setOnClickListener(this);

        //소켓 통신 스레드 시작
        worker.start();
    }
    //클릭 이벤트
    public void onClick(View v){
        if(v.getId()==R.id.scan_button){ //바코드 스캔 버튼
            //IntentIntegrator 생성 후 스캔 하기 -> zxing 바코드 스캐너 어플 이용해 데이터 받아오기
            IntentIntegrator scanIntegrator = new IntentIntegrator(this);
            scanIntegrator.initiateScan();

        }else if(v.getId()==R.id.socket_button){ //데이터 전송 버튼
            Log.e("Network", " " + data);

            if(data != null) { //데이터 null이 아닐 때 소켓을 통한 바코드 데이터 전송
                socket_out.println(data); //데이터 전송

                resultTxt.append("\n" + count + ". " + data); //Textview에 바코드 데이터 전송 목록 띄우기
                count++;
            }else{ //데이터가 null일 경우 - 데이터 보내기 (" data is null ")
                Log.e("Network", testStr);
                socket_out.println(testStr);
            }
        }
    }

    //바코드 스캔 실행 결과
    public void onActivityResult(int requestCode, int resultCode, Intent intent) {
        IntentResult scanningResult = IntentIntegrator.parseActivityResult(requestCode, resultCode, intent);
        if (scanningResult != null) { //스캔 실행 결과가 null이 아닐 경우
            String scanFormat = scanningResult.getFormatName(); //바코드 형식
            String scanContent = scanningResult.getContents(); //바코드 내용

            formatTxt.setText("FORMAT: " + scanFormat); //바코드 형식 출력
            contentTxt.setText("CONTENT: " + scanContent); //바코드 내용 출력

            if(scanContent != null) //바코드 내용이 null이 아닐 경우 String data변수에 저장
                data = new String(scanContent);
        }else{ //스캔 실행 결과가 없을 경우 toast 메시지 출력
            Toast toast = Toast.makeText(getApplicationContext(),
                    "No scan data received!", Toast.LENGTH_SHORT);
            toast.show();
        }
    }

    //소켓 통신 스레드
    Thread worker = new Thread() {
        public void run() {
            try {
                socket = new Socket("192.168.150.109", 24680); //소켓 열기
                socket_out = new PrintWriter(socket.getOutputStream(), true);
                socket_in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            } catch (IOException e) {
                e.printStackTrace();
            }
            try {
                while (true) {
                    data = socket_in.readLine();
                }
            } catch (Exception e) {
            }
        }
    };

    //앱 종료시 소켓 닫기
    @Override
    protected void onDestroy() {
        super.onDestroy();
        try {
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
