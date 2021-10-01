import 'package:dio/dio.dart';

searchFunction(String query,
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
  queryParameters = new Map<String, dynamic>.from(queryParameters);
  final onGetResponse = await dio.get(url, queryParameters: queryParameters);
  return onGetResponse;
}

// Create search function
// Make background widget Component
// Create test listbuilder with "Text()" for response
// Make Charts Component
