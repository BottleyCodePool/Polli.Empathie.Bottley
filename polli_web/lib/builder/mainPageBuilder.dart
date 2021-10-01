import 'package:flutter/material.dart';
import 'package:polli_web/builder/resultsViewBuilder.dart';
import 'package:polli_web/components/searchBarComponent.dart';
import 'package:google_fonts/google_fonts.dart';

class MainPageBuilder extends StatefulWidget {
  @override
  _MainPageBuilderState createState() => _MainPageBuilderState();
}

class _MainPageBuilderState extends State<MainPageBuilder> {
  @override
  Widget build(BuildContext context) {
    return ResultsViewBuilder();
  }
}
