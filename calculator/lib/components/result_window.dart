import 'package:flutter/material.dart';

import '../types/index.dart';

class ResultWindow extends StatelessWidget {
  final List<MathExpressionResult> results;

  const ResultWindow({Key? key, required this.results}) : super(key: key);

  List<Widget> renderResults() {
    return results
        .map((resObj) => Container(
              margin: const EdgeInsets.only(bottom: 15.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    resObj.mathExpression,
                    style: const TextStyle(fontSize: 20),
                  ),
                  const Text('=', style: TextStyle(fontSize: 20)),
                  Text(
                    resObj.result,
                    style: const TextStyle(fontSize: 20),
                  ),
                ],
              ),
            ))
        .toList();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
        decoration: const BoxDecoration(
            border: Border(bottom: BorderSide(color: Colors.blue, width: 2.0))),
        child: ListView(
          padding: const EdgeInsets.all(8),
          children: renderResults(),
        ));
  }
}
