import 'package:flutter/material.dart';

import '../types/index.dart';

class ButtonsBlock extends StatelessWidget {
  final IValueSetter onBtnPressed;
  final List<String> buttons = [
    '7',
    '8',
    '9',
    '/',
    '4',
    '5',
    '6',
    '*',
    '1',
    '2',
    '3',
    '-',
    '0',
    'C',
    '=',
    '+'
  ];

  ButtonsBlock({Key? key, required this.onBtnPressed}) : super(key: key);

  List<Widget> renderButtonsBlockChildren() {
    return buttons.map((btn) {
      Operation op;
      String payload = btn;

      switch (btn) {
        case '/':
          op = Operation.divide;
          break;
        case '*':
          op = Operation.multiply;
          break;
        case '-':
          op = Operation.subtract;
          break;
        case '+':
          op = Operation.add;
          break;
        case 'C':
          op = Operation.clear;
          break;
        case '=':
          op = Operation.equal;
          break;
        default:
          op = Operation.settingNumber;
      }

      return Container(
        decoration: BoxDecoration(
            border: Border.all(color: Colors.blue),
            borderRadius: const BorderRadius.all(Radius.circular(5.0))),
        child: TextButton(
          key: Key(btn),
          onPressed: () => onBtnPressed(ControlButtonContent(op, payload)),
          child: Text(
            btn,
            style: const TextStyle(fontSize: 18),
          ),
        ),
      );
    }).toList();
  }

  @override
  Widget build(BuildContext context) {
    return GridView.count(
      padding: const EdgeInsets.all(5),
      crossAxisCount: 4,
      mainAxisSpacing: 10,
      crossAxisSpacing: 10,
      children: renderButtonsBlockChildren(),
    );
  }
}
