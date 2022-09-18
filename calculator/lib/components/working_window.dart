import 'package:flutter/material.dart';

class WorkingWindow extends StatelessWidget {
  final String currentExpression;
  final String? extraInfo;

  const WorkingWindow(
      {Key? key, required this.currentExpression, this.extraInfo})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(8),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(
            currentExpression,
            style: const TextStyle(fontSize: 24),
          ),
          Container(
            margin: const EdgeInsets.only(top: 20.0),
            child: Text(
              extraInfo ?? '',
              style: const TextStyle(fontSize: 28, color: Colors.red),
            ),
          )
        ],
      ),
    );
  }
}
