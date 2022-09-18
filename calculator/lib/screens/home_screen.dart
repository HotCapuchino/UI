import 'package:calculator/components/buttons_block.dart';
import 'package:calculator/components/result_window.dart';
import 'package:dart_eval/dart_eval.dart';
import 'package:flutter/material.dart';

import '../components/working_window.dart';
import '../types/index.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<StatefulWidget> createState() => HomeScreenState();
}

class HomeScreenState extends State<HomeScreen> {
  String mathExpression = '';
  String? extraInfo = '';
  List<MathExpressionResult> mathExpressionResults = [];

  void onControlBtnPressed(ControlButtonContent content) {
    setState(() {
      switch (content.op) {
        case Operation.add:
        case Operation.subtract:
        case Operation.multiply:
        case Operation.divide:
          mathExpression += ' ${content.payload}';
          extraInfo = null;
          break;
        case Operation.clear:
          {
            mathExpression = '';
            extraInfo = null;
            break;
          }
        case Operation.equal:
          {
            var result = '';

            // Because there are problems with eval on strings that contains both int and float numbers
            var modifiedMathExpression =
                mathExpression.split(' ').map((symbol) {
              if (int.tryParse(symbol) != null) {
                return '$symbol.0';
              }
              return symbol;
            }).join('');

            try {
              result = eval(modifiedMathExpression).toString();

              mathExpressionResults
                  .add(MathExpressionResult(mathExpression, result));

              if (mathExpressionResults.length == 4) {
                mathExpressionResults = mathExpressionResults.sublist(1);
              }

              mathExpression = '';
              extraInfo = null;
            } catch (e) {
              // ignore: avoid_print
              print('Error occurred while eval ${e.toString()}');
              extraInfo = 'Error occurred while calculating math expression!';
            }
            break;
          }
        case Operation.settingNumber:
          {
            var number = content.payload;
            mathExpression += ' $number';
            extraInfo = null;
          }
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Calculator'),
      ),
      body: Center(
        child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
          Expanded(
              flex: 1, child: ResultWindow(results: mathExpressionResults)),
          Expanded(
              flex: 1,
              child: WorkingWindow(
                  currentExpression: mathExpression, extraInfo: extraInfo)),
          Expanded(
              flex: 3, child: ButtonsBlock(onBtnPressed: onControlBtnPressed))
        ]),
      ),
    );
  }
}
