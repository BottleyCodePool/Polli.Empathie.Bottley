import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:dio/dio.dart';

class ResultsViewBuilder extends StatefulWidget {
  @override
  _ResultsViewBuilderState createState() => _ResultsViewBuilderState();
}

class _ResultsViewBuilderState extends State<ResultsViewBuilder> {
  List results = [];

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Color(0xFF1A1A1A),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          Padding(
            padding: EdgeInsets.only(top: 24),
            child: Container(
              height: 80,
              width: 800,
              decoration: BoxDecoration(
                color: Color(0xFF121212),
                borderRadius: BorderRadius.all(Radius.circular(50)),
              ),
              child: TextField(
                style: GoogleFonts.lexendDeca(
                    color: Color(0xFFFFFFFF), fontSize: 30),
                cursorColor: Colors.white,
                textAlign: TextAlign.start,
                decoration: InputDecoration(
                    hintStyle: GoogleFonts.lexendDeca(
                        color: Colors.grey[600], fontSize: 30),
                    contentPadding:
                        EdgeInsets.only(left: 30, top: 20, right: 30),
                    border: InputBorder.none,
                    hintText: "Search for YouTube-Polls"),
                onSubmitted: (value) {
                  setState(() {
                    Future<String> searchFunction(String query,
                        {String channelId = null,
                        int resultsLimit = null,
                        int totalVotesFactor = null}) async {
                      final dio = Dio();
                      //
                      Map queryParameters = new Map();
                      queryParameters["key"] =
                          "gbdHLPPmHd99FPtS69drSjaFbxhMBhZtyFpkXLHNjNqQs7zssvbpUCRxGUC7XyLx";
                      queryParameters["query"] = query;
                      if (channelId != null) {
                        queryParameters["channelId"] = channelId;
                      }
                      if (resultsLimit != null) {
                        queryParameters["resultsLimit"] = resultsLimit;
                      }
                      if (totalVotesFactor != null) {
                        queryParameters["totalVotesFactor"] = totalVotesFactor;
                      }
                      //
                      final url = "http://0.0.0.0:8000";
                      queryParameters =
                          new Map<String, dynamic>.from(queryParameters);
                      final onGetResponse =
                          await dio.get(url, queryParameters: queryParameters);
                      this.setState(() {
                        results = onGetResponse.data["results"]["hits"]["hits"];
                      });
                    }

                    searchFunction(value);
                  });
                },
              ),
            ),
          ),
          SizedBox(height: 25),
          Expanded(
            child: Container(
              child: GridView.builder(
                itemCount: results.length,
                gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 3),
                itemBuilder: (BuildContext context, int index) {
                  List<Widget> bars =
                      _barChartBuilder(results[index]["_source"]);
                  return Padding(
                    padding: EdgeInsets.all(10),
                    child: Container(
                      decoration: BoxDecoration(
                        color: Color(0xFF121212),
                        border: Border.all(
                          width: 4,
                          color: Color(0xFF000000),
                        ),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withOpacity(0.8),
                            blurRadius: 15,
                            offset: Offset(4, 4),
                          ),
                        ],
                        borderRadius: BorderRadius.all(
                          Radius.circular(20),
                        ),
                      ),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: <Widget>[
                          Align(
                            alignment: Alignment.topLeft,
                            child: Padding(
                              padding:
                                  EdgeInsets.only(top: 40, left: 24, right: 24),
                              child: Text(
                                results[index]["_source"]["question"],
                                style: GoogleFonts.lexendDeca(
                                  textStyle: TextStyle(
                                      color: Colors.white, fontSize: 33),
                                ),
                              ),
                            ),
                          ),
                          Column(
                            children: bars,
                          ),
                          Align(
                            alignment: Alignment.bottomLeft,
                            child: Padding(
                              padding: EdgeInsets.only(
                                  bottom: 40, left: 24, right: 24),
                              child: Text(
                                results[index]["_source"]["totalVotes"]
                                        .toString() +
                                    " Votes • " +
                                    results[index]["_source"]["likes"]
                                        .toString() +
                                    " Likes" +
                                    "   -   " +
                                    results[index]["_source"]["date"]
                                        .replaceAll("-", "."),
                                style: GoogleFonts.lexendDeca(
                                  textStyle: TextStyle(
                                      color: Colors.white, fontSize: 20),
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),
          )
        ],
      ),
    );
  }
}

_barChartBuilder(chartData) {
  List<Widget> bars = [];
  List answers =
      List<String>.from(chartData["pollAnswersText"].values.toList());
  List percents =
      List<double>.from(chartData["pollAnswersVotesInPercent"].values.toList());

  for (var index = 0; index < answers.length; index++) {
    String answer = answers[index];
    double percent = (percents[index] * 100).round();
    bars.add(
      Align(
        alignment: Alignment.centerLeft,
        child: Padding(
          padding: EdgeInsets.only(left: 24),
          child: Stack(
            alignment: Alignment.centerLeft,
            children: <Widget>[
              Text(percent.toString() + "%",
                  style: GoogleFonts.lexendDeca(
                      textStyle: TextStyle(color: Colors.white, fontSize: 20))),
              Padding(
                padding: EdgeInsets.only(left: 50),
                child: Container(
                  height: 50,
                  width: percent * 5,
                  decoration: BoxDecoration(
                    color: Colors.purple[900],
                    borderRadius: BorderRadius.all(
                      Radius.circular(5),
                    ),
                  ),
                ),
              ),
              Padding(
                padding: EdgeInsets.only(left: 50),
                child: Container(
                  height: 50,
                  width: 500,
                  decoration: BoxDecoration(
                    border: Border.all(width: 1, color: Colors.white),
                    borderRadius: BorderRadius.all(
                      Radius.circular(5),
                    ),
                  ),
                  child: Align(
                    alignment: Alignment.centerLeft,
                    child: Padding(
                      padding: EdgeInsets.only(left: 15),
                      child: Text(answer,
                          style: GoogleFonts.lexendDeca(
                              textStyle: TextStyle(
                                  color: Colors.white, fontSize: 20))),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
    bars.add(SizedBox(height: 15));
  }
  return bars;
}
