import 'package:flutter/material.dart';
import 'package:voice_reocrder/views/recorder_home_view.dart';
void upload(){
  var uri = Uri.parse(url);
  var request = new MultipartRequest("POST", uri);

  var multipartFile = await MultipartFile.fromPath("package", videoPath);
  request.files.add(multipartFile);

  StreamedResponse response = await request.send();
  response.stream.transform(utf8.decoder).listen((value) {
    print(value);
  });
}
void main() {
  runApp(MyApp());
  upload();
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Voice Recorder',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: RecorderHomeView(
        title: 'Flutter Voice',
      ),
    );
  }
}
