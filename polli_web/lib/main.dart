import 'package:flutter/material.dart';
import 'builder/mainPageBuilder.dart';

void main() {
  runApp(Polli());
}

class Polli extends StatefulWidget {
  @override
  _PolliState createState() => _PolliState();
}

class _PolliState extends State<Polli> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        body: MainPageBuilder(),
      ),
    );
  }
}
