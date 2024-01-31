import 'dart:math';

import 'package:raylib/raylib.dart';

double mapValue(
    double value, double inMin, double inMax, double outMin, double outMax) {
  return (value - inMin) * (outMax - outMin) / (inMax - inMin) + outMin;
}

class WindowState {
  final wid = 1200;
  final hgt = 800;
  Vector2 mousePos = Vector2(-1, -1);
  bool leftClickDown = false;
  bool leftClickPressed = false;
  Vector2 lastDpiScale = Vector2(1, 1);
  Vector2 dpiScale = Vector2(1, 1);
  double maxDpiScale = 1;
  List<LinePlot> linePlots = [];

  void update() {
    mousePos = getMousePosition();
    leftClickDown = isMouseButtonDown(MouseButton.left);
    leftClickPressed = isMouseButtonPressed(MouseButton.left);
    dpiScale = getWindowScaleDPI();
    if (dpiScale != lastDpiScale) {
      lastDpiScale = dpiScale;
      maxDpiScale = max(dpiScale.x, dpiScale.y);
      setWindowMinSize((wid * dpiScale.x).toInt(), (hgt * dpiScale.y).toInt());
    }
  }

  void drawAllLinePlots() {
    for (LinePlot plot in linePlots) {
      plot.draw(this);
    }
  }
}

class LinePlot {
  final Rectangle rect;
  Rectangle? scaledRect;
  final Color backColor;
  final Color foreColor;
  List<double> data = [];

  LinePlot(this.rect, this.backColor, this.foreColor) {
    scaledRect = rect;
  }

  void sendValue(double value) {
    var numPoints = data.length;
    if (numPoints > 0 && scaledRect != null) {
      while (numPoints > scaledRect!.width) {
        data.removeAt(0);
        numPoints = data.length;
      }
    }
    data.add(value);
  }

  void draw(WindowState ws) {
    scaledRect = Rectangle(
      rect.x * ws.dpiScale.x,
      rect.y * ws.dpiScale.y,
      rect.width * ws.dpiScale.x,
      rect.height * ws.dpiScale.y,
    );

    drawRectangleRec(scaledRect!, backColor);

    var numPoints = data.length;
    if (numPoints != 0) {
      var maxY = data.reduce(max) + 1;
      var minY = data.reduce(min) - 1;

      List<Vector2> vectors = [];
      for (var i = 0; i < numPoints; i++) {
        var scaledData = data[i];
        if (maxY != minY) {
          scaledData = mapValue(
            scaledData,
            minY,
            maxY,
            scaledRect!.y,
            scaledRect!.y + scaledRect!.height,
          );
        }
        vectors.add(Vector2(scaledRect!.x + i, scaledData));
      }

      drawLineStrip(vectors, foreColor);
    }
  }
}
