class MathExpressionResult {
  String mathExpression;
  String result;

  MathExpressionResult(this.mathExpression, this.result);
}

enum Operation {
  add,
  subtract,
  multiply,
  divide,
  clear,
  equal,
  settingNumber,
}

class ControlButtonContent {
  Operation op;
  String? payload;

  ControlButtonContent(this.op, this.payload);
}

typedef IValueSetter = void Function(ControlButtonContent value);
